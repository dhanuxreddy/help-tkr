from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

DB = "campus.db"

# ---------------- DATABASE INIT ----------------
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
    # Image paths for blocks
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
    "a block": [
        "a block", "em diploma", "diploma",
        "ఎ బ్లాక్", "ఎబ్లాక్",
        "ए ब्लॉक"
    ],

    "pharmacy block": [
        "pharmacy",
        "ఫార్మసీ",
        "फार्मेसी"
    ],

    "em main block": [
        "em main", "main btech",
        "మెయిన్ బ్లాక్", "ఈఎం మెయిన్",
        "ईएम मेन"
    ],

    "em new block": [
        "em new", "em labs",
        "న్యూ బ్లాక్", "ఈఎం న్యూ",
        "ईएम न्यू"
    ],

    "r9 block": [
        "r9", "1st btech",
        "ఆర్9",
        "आर9"
    ],

    "boys hostel": [
        "boys hostel",
        "బాయ్స్ హాస్టల్",
        "बॉयज़ हॉस्टल"
    ],

    "girls hostel": [
        "girls hostel",
        "గర్ల్స్ హాస్టల్",
        "गर्ल्स हॉस्टल"
    ],

    "canteen": [
        "canteen",
        "కాంటీన్",
        "कैंटीन"
    ],

    "t block": [
        "t block",
        "టి బ్లాక్",
        "टी ब्लॉक"
    ],

    "rc main block": [
        "rc main",
        "ఆర్సీ మెయిన్",
        "आरसी मेन"
    ],

    "rc diploma block": [
        "rc diploma",
        "ఆర్సీ డిప్లొమా",
        "आरसी डिप्लोमा"
    ]
}




init_db()


# ---------------- MAIN PAGE ----------------
@app.route("/")
def mainpage():
    return render_template("mainhome.html")

# ---------------- CHAT PAGE ----------------
@app.route("/index")
def index():
    return render_template("index.html")
#-----------------mainhome2----------------
@app.route("/mainhome2")
def mainhome2():
    return render_template("mainhome2.html")
    # ---------------- LANGUAGE PAGES ----------------

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

    msg = user_msg.lower().replace("-", " ")
    msg = " ".join(msg.split())

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT name, en, te, hi FROM blocks")
    blocks = c.fetchall()
    conn.close()

    for b in blocks:
        block_name = b[0].lower().replace("-", " ")

        # get keywords for this block
        keywords = block_keywords.get(block_name, [block_name])

        for key in keywords:
            if key in msg:

                if lang == "te":
                    reply = b[2]
                elif lang == "hi":
                    reply = b[3]
                else:
                    reply = b[1]

                image = block_images.get(block_name, "")

                return jsonify({
                    "reply": reply,
                    "image": image
                })

    # default messages
    default_msgs = {
        "te": "దయచేసి బ్లాక్ పేరు అడగండి (ఉదా: A Block)",
        "hi": "कृपया ब्लॉक का नाम पूछें (जैसे A Block)",
        "en": "Please ask for a block name (example: A Block)"
    }

    return jsonify({
        "reply": default_msgs.get(lang, default_msgs["en"]),
        "image": ""
    })

# ---------------- INSERT DATA (RUN ONCE) ----------------
@app.route("/init-data")
def init_data():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # CREATE TABLE FIRST
    c.execute("""
    CREATE TABLE IF NOT EXISTS blocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        en TEXT,
        te TEXT,
        hi TEXT
    )
    """)

    # Clear old data
    c.execute("DELETE FROM blocks")

    # Insert data
    blocks = [
    ("A Block",
     "From A Gate, walk 3 meters straight. A Block will be on the left side.",
     "A గేట్ నుండి 3 మీటర్లు నేరుగా నడవండి. ఎడమ వైపున A బ్లాక్ ఉంటుంది.",
     "A गेट से 3 मीटर सीधे चलें। बाईं ओर A ब्लॉक मिलेगा।"),

    ("Pharmacy Block",
     "From A Gate, walk straight for 3 meters, then continue 20 meters. Pharmacy Block will be on the left side.",
     "A గేట్ నుండి 3 మీటర్లు నేరుగా వెళ్లి, తరువాత 20 మీటర్లు ముందుకు నడవండి. ఎడమ వైపున ఫార్మసీ బ్లాక్ ఉంటుంది.",
     "A गेट से 3 मीटर सीधे चलें, फिर 20 मीटर आगे जाएँ। बाईं ओर फार्मेसी ब्लॉक मिलेगा।"),

    ("EM Main Block",
     "From A Gate, walk 20 meters straight. EM Main Block will be on the left side.",
     "A గేట్ నుండి 20 మీటర్లు నేరుగా నడవండి. ఎడమ వైపున EM మెయిన్ బ్లాక్ ఉంటుంది.",
     "A गेट से 20 मीटर सीधे चलें। बाईं ओर EM मेन ब्लॉक मिलेगा।"),

    ("EM New Block",
     "From EM Main Block, go downstairs and walk straight. EM New Block is located behind the main building.",
     "EM మెయిన్ బ్లాక్ నుండి మెట్లు దిగి నేరుగా వెళ్లండి. వెనుక భాగంలో EM న్యూ బ్లాక్ ఉంటుంది.",
     "EM मेन ब्लॉक से नीचे उतरकर सीधे चलें। पीछे की ओर EM न्यू ब्लॉक स्थित है।"),

    ("R9 Block",
     "From Saraswathi Statue, walk towards Boys Hostel. R9 Block is beside the hostel.",
     "సరస్వతి విగ్రహం నుండి బాయ్స్ హాస్టల్ వైపు వెళ్లండి. హాస్టల్ పక్కన R9 బ్లాక్ ఉంటుంది.",
     "सरस्वती प्रतिमा से बॉयज़ हॉस्टल की ओर जाएँ। हॉस्टल के पास R9 ब्लॉक है।"),

    ("Boys Hostel",
     "From B Gate, walk straight for 3 meters. Boys Hostel will be on the right side.",
     "B గేట్ నుండి 3 మీటర్లు నేరుగా వెళ్లండి. కుడి వైపున బాయ్స్ హాస్టల్ ఉంటుంది.",
     "B गेट से 3 मीटर सीधे चलें। दाईं ओर बॉयज़ हॉस्टल मिलेगा।"),

    ("Girls Hostel",
     "From A Gate, walk 110 meters straight. After Saraswathi Statue, the Girls Hostel will be on the right side.",
     "A గేట్ నుండి 110 మీటర్లు నేరుగా వెళ్లండి. సరస్వతి విగ్రహాన్ని దాటి కుడి వైపున గర్ల్స్ హాస్టల్ ఉంటుంది.",
     "A गेट से 110 मीटर सीधे चलें। सरस्वती प्रतिमा पार करने के बाद दाईं ओर गर्ल्स हॉस्टल मिलेगा।"),

    ("Canteen",
     "From A Gate, walk towards Saraswathi Statue. The canteen is on the right side near the statue.",
     "A గేట్ నుండి సరస్వతి విగ్రహం వైపు వెళ్లండి. విగ్రహం దగ్గర కుడి వైపున కాంటీన్ ఉంటుంది.",
     "A गेट से सरस्वती प्रतिमा की ओर जाएँ। प्रतिमा के पास दाईं ओर कैंटीन है।"),

    ("T Block",
     "From A Gate, walk towards Saraswathi Statue. After the food court, T Block will be on the right side.",
     "A గేట్ నుండి సరస్వతి విగ్రహం వైపు వెళ్లండి. ఫుడ్ కోర్ట్ దాటి కుడి వైపున T బ్లాక్ ఉంటుంది.",
     "A गेट से सरस्वती प्रतिमा की ओर जाएँ। फूड कोर्ट के बाद दाईं ओर T ब्लॉक मिलेगा।"),

    ("RC Main Block",
     "From A Gate, walk 100 meters straight. RC Main Block will be on the left side.",
     "A గేట్ నుండి 100 మీటర్లు నేరుగా వెళ్లండి. ఎడమ వైపున RC మెయిన్ బ్లాక్ ఉంటుంది.",
     "A गेट से 100 मीटर सीधे चलें। बाईं ओर RC मेन ब्लॉक मिलेगा।"),

    ("RC Diploma Block",
     "From RC Main Block, cross the ground floor area and walk 20 meters. RC Diploma Block will be on the left side.",
     "RC మెయిన్ బ్లాక్ నుండి గ్రౌండ్ ఫ్లోర్ ప్రాంతం దాటి 20 మీటర్లు వెళ్లండి. ఎడమ వైపున RC డిప్లొమా బ్లాక్ ఉంటుంది.",
     "RC मेन ब्लॉक से ग्राउंड फ्लोर पार करके 20 मीटर आगे जाएँ। बाईं ओर RC डिप्लोमा ब्लॉक मिलेगा।")
]


    c.executemany(
        "INSERT INTO blocks (name, en, te, hi) VALUES (?, ?, ?, ?)",
        blocks
    )

    conn.commit()
    conn.close()

    return "Initial data inserted successfully"


    # ADD THIS
    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        dob TEXT
    )
    """)

    conn.commit()
    conn.close()
# ---------------- INSERT STUDENTS (RUN ONCE) ----------------
@app.route("/init-students")
def init_students():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    students = [
        ("23248-cs-070", "2001-01-01"),
        ("23248-cs-071", "2002-01-01"),
        ("23248-cs-072", "2003-01-01"),
        ("23248-cs-073", "2004-01-01"),
        ("23248-cs-074", "2005-01-01"),
        ("23248-cs-075", "2006-01-01"),
        ("23248-cs-076", "2007-01-01"),
        ("23248-cs-077", "2008-01-01"),
        ("23248-cs-078", "2000-01-01")
    ]

    c.executemany(
        "INSERT OR IGNORE INTO students (student_id, dob) VALUES (?, ?)",
        students
    )

    conn.commit()
    conn.close()
    return "Students added successfully"
    # ---------------- VERIFY STUDENT ----------------
@app.route("/verify-student", methods=["POST"])
def verify_student():
    data = request.json
    student_id = data.get("id")
    dob = data.get("dob")

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        "SELECT * FROM students WHERE student_id=? AND dob=?",
        (student_id, dob)
    )

    result = c.fetchone()
    conn.close()

    if result:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})
        # ---------------- STUDENT LOGIN PAGE ----------------
@app.route("/student")
def student():
    return render_template("studenthome.html")
@app.route("/studentindex")
def studentindex():
    return render_template("studentindex.html")


    

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
