from flask import Flask, render_template, flash, redirect, url_for, session, request, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from requests_oauthlib import OAuth2Session
from bs4 import BeautifulSoup
import ollama
import markdown
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from utils.pdf_reader import readPDF
from utils.comparison import comparePDF,compareTemplate
from utils.plagiarism_detector import extract_title,coreAPICall,download_pdf_from_url,extract_text_from_pdf_bytes,compute_similarity

load_dotenv()

# App configuration
app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = '25354b506e275410240b8376094ff9bd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure the upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'  
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB limit

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
db = SQLAlchemy(app)

# Define models first, before creating tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Form classes
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=10, max=25)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=30)])
    confirmPass = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField('Login')

# Create tables (only once, after models are defined)
with app.app_context():
    db.create_all()

# Load Google OAuth credentials from environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Google OAuth Setup
AUTHORISATION_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
AUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"
REDIRECT_URL = "http://localhost:5001/callback"
USER_INFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'

SCOPE = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

# OAuth Setup for Development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Routes
@app.route('/')
@app.route('/home')
def home():
    logged_in = session.get('logged_in', False)
    username = session.get('username', None)
    # Debug print to check session state
    print(f"Session state: logged_in={logged_in}, username={username}")
    

    response = ollama.generate(model="gemma3:1b", prompt="give one qoute about research given by a great person in 1-2 lines dont give author name or anything else, ONLY QUOTE",stream=False)['response']
    
    return render_template("index.html", logged_in=logged_in, username=username,thought=response,title="ResearchRankers",css_path='style-index')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data - using 'name' as sent by the form
        username = request.form.get('name')  # Note: 'name' not 'username'
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate field lengths manually since we're not using WTForms
        if len(username) < 10 or len(username) > 25:
            flash('Username must be between 10 and 25 characters.')
            return redirect(url_for('signup'))
            
        if len(password) < 8:
            flash('Password must be at least 8 characters.')
            return redirect(url_for('signup'))
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. Please log in instead.')
            return redirect(url_for('signup'))
        
        # Check if username exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken. Please try another.')
            return redirect(url_for('signup'))
        
        # Create new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        # Set session
        session['logged_in'] = True
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        
        flash('Account created successfully!')
        return redirect(url_for('home'))
    
    return render_template("signup.html", title="ResearchRankers-Sign Up", css_path='style-signup')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if not user or not user.check_password(password):
            flash('Invalid email or password. Please try again.')
            # Stay on login form rather than redirecting to signup
            return render_template("signup.html", title="ResearchRankers-Login", css_path='style-signup')
        
        # Set session variables
        session['logged_in'] = True
        session['user_id'] = user.id
        session['username'] = user.username
        
        flash('Logged in successfully!')
        return redirect(url_for('home'))
    
    # For GET requests, show the signup page (which contains the login form)
    return render_template("signup.html", title="ResearchRankers-Sign In", css_path='style-signup')

@app.route("/logout")
def logout():
    # Clear specific session variables
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

@app.route("/tools")
def tools():
    logged_in = session.get('logged_in', False)
    username = session.get('username', None)
    return render_template("tools.html",logged_in=logged_in, username=username,title="ResearchRankers-Tools",css_path='style-tools')
    
@app.route("/compare")
def compare():
    ai_result = session.get('ai_result_compare', None)
    logged_in = session.get('logged_in', False)
    username = session.get('username', None)
    return render_template("compare.html",logged_in=logged_in, username=username,title="ResearchRankers-Compare",css_path='style-compare',ai_result=ai_result)

#Uploading files for compare
@app.route("/compare-papers",methods=['POST'])
def compare_papers():
    if 'user_file' not in request.files or 'reference_file' not in request.files:
        return redirect(url_for('index'))
    
    user_file=request.files['user_file']
    reference_file=request.files['reference_file']

    if user_file.filename =='' or reference_file.filename=='':
        return redirect(url_for('index'))

    user_filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_file.filename))
    reference_filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(reference_file.filename))
    
    user_file.save(user_filepath)
    reference_file.save(reference_filepath)
    
    
    user_text=readPDF(user_filepath)
    reference_text=readPDF(reference_filepath)
    
    ai_result_compare=comparePDF(reference_text,user_text,"phi4")
    
    os.remove(user_filepath)
    os.remove(reference_filepath)
    
    session['ai_result_compare']= ai_result_compare
    
    return redirect(url_for('compare'))

@app.route("/templatechecker")
def templatechecker():
    logged_in = session.get('logged_in', False)
    username = session.get('username', None)
    ai_result = session.get('ai_result_template', None)
    return render_template("template-checker.html",logged_in=logged_in, username=username,title="ResearchRankers-Template_checking",css_path='style-template-checker',ai_result=ai_result)


#Uploading files for templatechecker
@app.route("/check-template",methods=['POST'])
def check_template():
    if 'user_file' not in request.files or 'template_file' not in request.files:
        return redirect(url_for('home'))
    
    user_file=request.files['user_file']
    template_file=request.files['template_file']

    if user_file.filename =='' or template_file.filename=='':
        return redirect(url_for('home'))
    user_filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_file.filename))
    template_filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(template_file.filename))
    
    user_file.save(user_filepath)
    template_file.save(template_filepath)
    
    user_text=readPDF(user_filepath)
    template_text=readPDF(template_filepath)
    
    ai_result_template=compareTemplate(template_text,user_text,"phi4")
    
    os.remove(user_filepath)
    os.remove(template_filepath)
    
    session['ai_result_template']= ai_result_template
    
    return redirect(url_for('templatechecker'))

@app.route("/grammercorrect")
def grammercorrect():
    logged_in = session.get('logged_in', False)
    username = session.get('username', None)
    return render_template("grammer-correct.html",logged_in=logged_in, username=username,title="ResearchRankers-Grammer_Correction",css_path='style-grammer-correction')

@app.route("/check-grammer")
def checkgrammer():
    if 'user_file_file' not in request.files:
        return render_template(url_for('home'))
    
    user_file=request.files['user_file']
    
    if user_file.filename == '':
        return render_template(url_for('home'))

    user_filepath=os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_file.filename))
    
    #Add processing logic here
        

    
@app.route('/plagarism')
def plagarism():
    logged_in = session.get('logged_in', False)
    username = session.get('username', None)
    plagarism_result =  session.get('plagarism_result',None)
    return render_template("plagarism.html",logged_in=logged_in, username=username,title="ResearchRankers-Plagarism",css_path='style-plagarism', plagarism_result=plagarism_result)
    

@app.route('/check-plagarism',methods=['POST'])
def check_plagarism():
    if 'user_file' not in request.files:
        return redirect(url_for('home'))

    user_file=request.files['user_file']

    if user_file.filename == '':
        return redirect(url_for('home'))  
    
    user_filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_file.filename))
    user_file.save(user_filepath)

    paper_titles=extract_title(user_filepath)
    urls=[]
    for title in paper_titles:
        urls+=coreAPICall(title)
    print(urls)
    downloaded_text=''
    for url in urls:
        pdf_bytes=download_pdf_from_url(url)
        downloaded_text+=extract_text_from_pdf_bytes(pdf_bytes)
    print(downloaded_text)
    #with open("debug_output.txt", "w", encoding="utf-8") as f:
    #   f.write(downloaded_text)
    # plag detction needs to be worked upon
    user_text=readPDF(user_filepath)
    plagarism_result=compute_similarity(user_text,downloaded_text)
    session['plagarism_result'] = round(float(plagarism_result) * 100, 2)
    os.remove(user_filepath)  
    return redirect(url_for('plagarism'))

@app.route("/google_login")
def google_login():
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URL, scope=SCOPE)
    auth_url, state = google.authorization_url(AUTHORISATION_BASE_URL, access_type="offline", prompt="select_account")
    session["oauth_state"] = state
    return redirect(auth_url)

@app.route("/callback")
def callback():
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URL, state=session["oauth_state"])
    token = google.fetch_token(AUTH_TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)
    session["oauth_token"] = token

    user_info = google.get(USER_INFO_URL).json()
    name = user_info["name"]
    email = user_info["email"]

    # Check if user already exists
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username=name, email=email, password="oauth")  # used dummy password for now, needs to be rectified in future
        db.session.add(user)
        db.session.commit()

    # Log the user in
    session['logged_in'] = True
    session['user_id'] = user.id
    session['username'] = user.username
    flash('Logged in with Google!')

    # NOTE: Should implement handling of accounts having same username

    return redirect("/")

if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)