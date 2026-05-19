from flask import Flask, render_template, request
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

pdf_text = ""
chat_history = []

@app.route("/", methods=["GET", "POST"])
def home():

    global pdf_text, chat_history
    answer = ""
    score = 0.0

    if request.method == "POST":

        # ---------------- PDF UPLOAD ----------------
        if "pdf" in request.files:

            file = request.files["pdf"]

            if file.filename != "":

                reader = PyPDF2.PdfReader(file)

                text = ""

                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + " "

                pdf_text = text.strip()
                chat_history = []

                answer = "PDF Uploaded Successfully ✅"
                score = 1.0

        # ---------------- QUESTION ----------------
        elif "question" in request.form:

            question = request.form["question"].lower()

            if pdf_text.strip() == "":
                answer = "Please upload a valid PDF first"
                score = 0.0

            else:

                # ---------------- CHUNKING ----------------
                words = pdf_text.split()
                chunks = []

                chunk_size = 150

                for i in range(0, len(words), chunk_size):
                    chunk = " ".join(words[i:i + chunk_size]).strip()
                    if len(chunk) > 30:
                        chunks.append(chunk)

                # ---------------- CHECK ----------------
                if len(chunks) == 0:
                    answer = "Not available in document (no content found)"
                    score = 0.0

                else:

                    # ---------------- TF-IDF ----------------
                    vectorizer = TfidfVectorizer().fit_transform([question] + chunks)
                    vectors = vectorizer.toarray()

                    question_vec = vectors[0]
                    chunk_vecs = vectors[1:]

                    similarities = cosine_similarity([question_vec], chunk_vecs)[0]

                    best_index = similarities.argmax()
                    best_score = float(similarities[best_index])

                    # ---------------- FINAL FILTER ----------------
                    if best_score > 0.2:
                        answer = chunks[best_index]
                        score = best_score
                    else:
                        answer = "Not available in document (low relevance detected)"
                        score = best_score

            # ---------------- CHAT HISTORY ----------------
            chat_history.append({
                "question": question,
                "answer": answer,
                "score": round(score, 2)
            })

    return render_template("index.html", chat=chat_history)


if __name__ == "__main__":
    app.run(debug=True)