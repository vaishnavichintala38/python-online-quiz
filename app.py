from flask import Flask, jsonify, render_template, request
import random

app = Flask(__name__)

QUESTIONS = [
    {
        "id": 1,
        "topic": "Python",
        "question": "Which keyword is used to define a function in Python?",
        "options": ["func", "def", "function", "define"],
        "answer": "def",
    },
    {
        "id": 2,
        "topic": "Python",
        "question": "Which data type in Python is immutable?",
        "options": ["list", "dict", "tuple", "set"],
        "answer": "tuple",
    },
    {
        "id": 3,
        "topic": "Python",
        "question": "What does len([10, 20, 30]) return?",
        "options": ["2", "3", "30", "Error"],
        "answer": "3",
    },
    {
        "id": 4,
        "topic": "Web",
        "question": "Which HTTP method is commonly used to send form/JSON data to a server?",
        "options": ["GET", "POST", "HEAD", "OPTIONS"],
        "answer": "POST",
    },
    {
        "id": 5,
        "topic": "Web",
        "question": "Which status code means Not Found?",
        "options": ["200", "201", "404", "500"],
        "answer": "404",
    },
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/questions")
def get_questions():
    topic = request.args.get("topic", "ALL")
    pool = QUESTIONS if topic == "ALL" else [q for q in QUESTIONS if q["topic"] == topic]
    quiz_list = []
    for q in pool:
        opts = q["options"][:]
        random.shuffle(opts)
        quiz_list.append({
            "id": q["id"],
            "topic": q["topic"],
            "question": q["question"],
            "options": opts,
        })
    return jsonify(quiz_list)


@app.route("/api/submit", methods=["POST"])
def submit_quiz():
    payload = request.get_json(silent=True) or {}
    answers = payload.get("answers", {})
    q_ids = payload.get("questionIds", [q["id"] for q in QUESTIONS])

    q_map = {q["id"]: q for q in QUESTIONS}
    score = 0
    details = []

    for qid in q_ids:
        q = q_map.get(qid)
        if not q:
            continue
        user_ans = answers.get(str(qid))
        is_correct = user_ans == q["answer"]
        if is_correct:
            score += 1
        details.append({
            "id": q["id"],
            "question": q["question"],
            "userAnswer": user_ans,
            "correctAnswer": q["answer"],
            "isCorrect": is_correct,
        })

    return jsonify({
        "score": score,
        "total": len(details),
        "details": details,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
