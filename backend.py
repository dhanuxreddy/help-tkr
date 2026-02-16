from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

DB = "campus.db"

# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Blocks table
    c.execute("""
    CREATE TABLE IF NOT EXISTS blocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        en TEXT,
        te TEXT,
        hi TEXT
    )
    """)

    # Students table
    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        dob TEXT
    )
    """)

    conn.commit()
    conn.close()


block_images = {
    "a block": "/static/ablockfin.JPEG",
    "pharmacy block": "/static/pharmacy.JPG",
    "em main block": "/static/mainblock.JPG",
    "em new block": "/static/EMNEWblock.JPEG",
    "r9 block": "/static/r9.JPEG",
    "boys hostel": "/static/boyshostel.JPEG",
    "girls hostel": "/static/gh.JPEG",
    "canteen": "/static/canteen.JPEG",
    "t block": "/static/tblock.JPEG",
    "rc main block": "/static/adminblock.PNG",
    "rc diploma block": "/static/rcdiploma.JPG"
}

block_keywords = {
    "a block": ["a block", "em diploma", "diploma", "ఎ బ్లాక్", "ए ब्लॉक"],
    "pharmacy block": ["pharmacy", "ఫార్మసీ", "फार्मेसी"],
    "em main block": ["em main", "main btech", "మెయిన్ బ్లాక్", "ईएम मेन"],
    "em new block": ["em new", "em labs", "న్యూ బ్లాక్", "ईएम न्यू"],
    "r9 block": ["r9", "1st btech", "ఆర్9", "आर9"],
    "boys hostel": ["boys hostel", "బాయ్స్ హాస్టల్", "बॉयज़ हॉस्टल"],
    "girls hostel": ["girls hostel", "గర్ల్స్ హాస్టల్", "गर्ल्स हॉस्टल"],
    "canteen": ["canteen", "కాంటీన్", "कैंटीन"],
    "t block": ["t block", "టి బ్లాక్", "टी ब्लॉक"],
    "rc main block": ["rc main", "ఆర్సీ మెయిన్", "आरसी मेन"],
    "rc diploma block": ["rc diploma", "ఆర్సీ డిప్లొమా", "आरसी डिप्लोमा"]
}

init_db()

# ---------------- MAIN PAGES ----------------
@app.route("/")
def mainpage():
    return render_template("mainhome.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/mainhome2")
def mainhome2():
    return render_template("mainhome2.html")

@app.route("/english")
def english():
    return render_template("index.html")

@app.route("/telugu")
def telugu():
    return render_template("telugu.html")

@app.route("/hindi")
def hindi():
    return render_template("hindi.html")

# ---------------- CHATBOT API ----------------
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    lang = data.get("lang", "en")

    msg = " ".join(user_msg.lower().replace("-", " ").split())

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT name, en, te, hi FROM blocks")
    blocks = c.fetchall()
    conn.close()

    for b in blocks:
        block_name = b[0].lower().replace("-", " ")
        keywords = block_keywords.get(block_name, [block_name])

        for key in keywords:
            if key in msg:
                reply = b[1] if lang == "en" else b[2] if lang == "te" else b[3]
                image = block_images.get(block_name, "")
                return jsonify({"reply": reply, "image": image})

    default_msgs = {
        "te": "దయచేసి బ్లాక్ పేరు అడగండి (ఉదా: A Block)",
        "hi": "कृपया ब्लॉक का नाम पूछें (जैसे A Block)",
        "en": "Please ask for a block name (example: A Block)"
    }

    return jsonify({"reply": default_msgs.get(lang, default_msgs["en"]), "image": ""})

# ---------------- STUDENT VERIFY ----------------
@app.route("/verify-student", methods=["POST"])
def verify_student():
    data = request.json
    student_id = data.get("id")
    dob = data.get("dob")

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE student_id=? AND dob=?", (student_id, dob))
    result = c.fetchone()
    conn.close()

    return jsonify({"status": "success" if result else "fail"})

@app.route("/student")
def student():
    return render_template("studenthome.html")

@app.route("/studentindex")
def studentindex():
    return render_template("studentindex.html")

# ---------------- RUN FOR RENDER ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
