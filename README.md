# 📄 PDF AI Chatbot (Document Q&A System)

## 🚀 Project Overview
This project is a Flask-based AI-powered PDF Question Answering system.

Users can upload a PDF document and ask questions based only on that document.
If the answer is not available in the document, the system returns:

**"Not available in document"**

---

## 🧠 How It Works

### 1. PDF Upload
- User uploads a PDF file
- Text is extracted using PyPDF2

### 2. Text Processing
- Extracted text is split into sentences
- Sentences are used as searchable data

### 3. Question Answering
- TF-IDF (Term Frequency - Inverse Document Frequency) is used
- Cosine similarity finds the most relevant sentence
- Best matching sentence is returned as answer

### 4. Hallucination Control
To ensure accuracy:
- Only document content is used
- Similarity threshold is applied
- If no strong match is found, system returns:
  "Not available in document"

---