from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bs4 import BeautifulSoup
import ollama
import markdown
# App configuration
app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = '25354b506e275410240b8376094ff9bd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

# Routes
@app.route('/')
@app.route('/home')
def home():
    logged_in = session.get('logged_in', False)
    username = session.get('username', None)
    # Debug print to check session state
    print(f"Session state: logged_in={logged_in}, username={username}")
    

    response = ollama.generate(model="tinyllama:1.1b", prompt="Return one light thought on research with author name.quotes should be off only 10 words.",stream=False)['response']
    
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
    return render_template("compare.html",title="ResearchRankers-Compare",css_path='style-compare')


if __name__ == "__main__":
    app.run(debug=True)
