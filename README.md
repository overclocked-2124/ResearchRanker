# 🔬 ResearchRankers

**AI-powered companion for student researchers—discover, write, compare, and validate your research with confidence.**

---

## 📚 About the Project

**ResearchRankers** is a full-stack Flask web application built to assist students through every stage of writing a research paper—especially those referencing IEEE papers. Whether you're forming an idea or polishing your final draft, ResearchRankers provides smart, intuitive tools to help you:

* 🔍 Discover relevant open-access IEEE papers
* 🤖 Clarify technical concepts using contextual AI
* ✍️ Get guided support on writing and structuring your paper
* 📊 Compare your paper with published works for feedback and benchmarking
* 🔒 Detect plagiarism using a curated open-access research corpus

---

## 🚀 Features

### 🔍 Smart Paper Discovery

Submit your research idea and instantly receive relevant IEEE/open-access papers using the CORE API.

### 🤖 Doubt Clarification via GenAI

Ask questions about your research topic and receive intelligent, contextual responses—powered by locally running LLMs via Ollama.

### ✍️ Research Writing Assistant

Receive guidance on writing your research paper, including structure suggestions for sections like abstract, literature review, methodology, and conclusion.

### 📊 Comparative Paper Analyzer

Upload your completed paper and:

* Compare its methodology, language, and findings against existing IEEE papers
* Get a similarity-based ranking and AI-generated feedback

### 🔒 Plagiarism Detection Engine

* Checks your uploaded work against **freely accessible IEEE/open-access research papers**
* Leverages title-based querying, PDF parsing, and similarity scoring
* Future-ready for semantic plagiarism detection using SBERT

---

## 🧠 How It Works (Plagiarism Detection Flow)

1. 📤 Upload your research paper (PDF)
2. 📌 Extract key titles from your work
3. 🌐 Fetch related papers via the CORE API
4. 📄 Extract and preprocess text from downloaded papers
5. 🧮 Compare user and reference content using NLP-based similarity
6. 📊 Return a detailed plagiarism score and match summary

---

## 🛠️ Tech Stack

| Tool / Library          | Purpose                            |
|-------------------------|------------------------------------|
| 🐍 Python 3.10+         | Backend language                   |
| 🌶️ Flask               | Web application framework          |
| 🧠 Ollama               | Local LLM for doubt clarification  |
| 🗃️ SQLAlchemy          | ORM + SQLite for user data         |
| 📄 pdfplumber / PyPDF2  | PDF text extraction                |
| 🔍 BeautifulSoup        | Scraping (fallback for open papers) |
| 🌐 CORE API             | Paper discovery (metadata + links) |
| 🛡️ WTForms             | User input validation              |
| ☁️ python-dotenv        | Secure env variable handling       |

---

## 📂 Project Structure

```
ResearchRankers/
├── app/
│   ├── app.py                     # Main Flask application
│   ├── .env                       # Environment variables
│   ├── requirements.txt          # Python dependencies
│   ├── instance/Users.db         # SQLite DB for user accounts
│   ├── static/                   # Static assets (CSS, JS, images, uploads)
│   ├── templates/                # HTML templates (Jinja2)
│   └── utils/                    # Core modules for AI and PDF processing
│       ├── pdf_reader.py         # PDF extraction logic
│       ├── comparison.py         # AI-based structure/method analysis
│       └── plagiarism_detector.py# CORE integration + similarity logic
├── tests/                        # Sample PDFs and basic test files
├── run.py                        # Entry point (alternative to app.py)
└── README.md                     # This documentation
```

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ResearchRankers.git
cd ResearchRankers/app
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```
CLIENT_ID=your_google_client_id
CLIENT_SECRET=your_google_client_secret
```

### 5. Run the Application

```bash
python app.py
```

Then open your browser at: [http://localhost:5001](http://localhost:5001)

---

## 🧪 Example Use Cases

* 💡 Type your research idea → get relevant IEEE papers to begin exploring
* 🤖 Ask AI for clarification on tough topics from existing research
* 📑 Upload your final paper → compare and benchmark it with published IEEE works
* 🕵️‍♀️ Run a plagiarism scan → ensure originality before submission

---

## 🌟 Support the Project

If you find this tool useful, please ⭐ the repository and share it with your peers in research communities. Contributions, suggestions, and feedback are always welcome!
