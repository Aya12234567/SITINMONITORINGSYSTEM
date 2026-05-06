from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import base64
from datetime import datetime
import os
import re  
import io
import csv

app = Flask(__name__)
app.secret_key = 'secretkey123'

FOUL_WORDS = {
    # ── ENGLISH ──
    "fuck", "f*ck", "f**k", "fu*k", "fuk", "fuq", "fvck", "phuck",
    "fucks", "fucking", "fucked", "fucker", "fuckers", "fuckhead",
    "fuckface", "fuckoff", "fuckup", "motherfucker", "motherfucking",
    "shit", "sh*t", "sh!t", "sht", "shyt", "shite", "shits", "shitting",
    "shithead", "shitheads", "shitface", "bullshit", "dipshit", "apeshit",
    "bitch", "b*tch", "b!tch", "btch", "biatch", "biotch", "bitches",
    "bitching", "bitchy", "sonofabitch", "son of a bitch",
    "ass", "a**", "a55", "arse", "asshole", "a**hole", "assh*le",
    "assholes", "jackass", "smartass", "dumbass", "badass", "fatass",
    "assface", "asswipe", "assclown", "asscunt",
    "bastard", "b*stard", "bastards", "bastad",
    "cunt", "c*nt", "c**t", "cunts", "cunting",
    "dick", "d*ck", "dck", "dicks", "dickhead", "dickface", "dickwad",
    "dickweed", "dicksucker", "d1ck",
    "pussy", "p*ssy", "pussies", "puss",
    "cock", "c*ck", "cocks", "cocksucker", "cockhead", "cockface",
    "c0ck", "cock",
    "whore", "wh*re", "whores", "whorebag", "whoring",
    "slut", "sl*t", "sluts", "slutty", "slvt",
    "retard", "r*tard", "retards", "retarded",
    "faggot", "f*ggot", "fag", "fags", "fagg",
    "nigger", "n*gger", "niger", "nigg", "nigga", "n1gga", "n1gger",
    "idiot", "idiots", "idiotic",
    "stupid", "stup1d", "stupido",
    "moron", "morons", "moronic",
    "imbecile", "imbeciles",
    "dumbass", "dumb", "dumbo",
    "loser", "l0ser", "losers",
    "scum", "scumbag", "scumball",
    "prick", "pr*ck", "pricks",
    "twat", "tw*t", "twats",
    "wanker", "w*nker", "wankers",
    "hell", "damn", "damned", "dammit", "d*mn",
    "crap", "craps", "crappy",
    "piss", "p*ss", "pissed", "pissing", "pissoff",
    "douchebag", "douche", "douchebags",
    "shithole", "shitbag",
    "turd", "turds",
    "bollocks", "b*llocks",
    "bugger", "buggered",
    "sodding", "sodder",
    "tosser", "tossers",
    "git", "twit",
    "slag", "slags",
    "minger", "mingers",
    "skank", "skanks", "skanky",
    "tramp", "tramps",
    "ho", "hoe", "hoes",
    "pimp", "pimps",
    "spastic", "spaz",
    "numbnuts", "knucklehead",
    "shitass", "asshat",
    "clusterfuck", "mindfuck",
    "godfuck", "goddam", "goddamn", "goddammit",
    "jesus christ", "holy shit", "holy crap",
    "son of a bitch", "sob",
    "wtf", "stfu", "gtfo", "kys",

    # ── BISAYA / CEBUANO ──
    "puta", "p*ta", "p.u.t.a", "puta_", "putang", "putangina",
    "putang ina", "putaing", "putahinamo", "puta ka",
    "yawa", "y*wa", "yawa ka", "yawaa", "yawa mo",
    "boang", "b*ang", "boanga", "boang ka", "boangon",
    "buang", "bu*ng", "buanga", "buang ka", "buangon",
    "bilat", "b*lat", "bilatmo", "bilat mo",
    "boto", "b*to", "botong", "boto mo",
    "unggoy", "ungoy", "unggoy ka",
    "bogo", "b*go", "bogoa", "bogo ka",
    "animal", "an1mal", "animal ka", "mananap",
    "gago", "g*go", "gagong", "gago ka", "gaga",
    "leche", "l*che", "letche", "letcheng",
    "punyeta", "p*nyeta", "punyetang", "punyeta ka",
    "tangina", "t*ngina", "tang ina", "tang ina mo", "tanginamo",
    "inutil", "in*til", "inutilmo",
    "peste", "p*ste", "pesteng",
    "kayat", "k*yat", "kayatmo", "kayat mo",
    "kineme", "kin*me", "kineme mo",
    "iyot", "iy*t", "iyot mo", "iyoton",
    "atay", "at*y", "atayka", "atay mo",
    "kupal", "k*pal", "kupalmo", "kupal ka",
    "pakyu", "pak*u", "pak u", "pak you", "pakyo",
    "ulol", "ul*l", "ulolmo", "ulol ka",
    "tarantado", "tar*ntado", "tarantadong",
    "demonyong", "demonyo", "dem0nyo",
    "hayop", "hay*p", "hayopka", "hayop ka",
    "sungit", "sung*t",
    "bugo", "bug*",
    "tanga", "t*nga", "tangamo", "tanga ka", "tangaa",
    "luko", "luk*", "luko ka",
    "buwa", "buw*", "buwa ka",
    "hinayupak", "hinayu*ak", "hinayupak ka",
    "olats", "ol*ts", "olats ka",
    "pakshet", "pak*het", "paksit",
    "amputa", "amp*ta", "amputang", "amputa ka",
    "hudas", "hud*s", "hudas ka",
    "bwisit", "bw*sit", "bwisitmo", "bwisit ka",
    "lintian", "lint*an", "lintianmo",
    "yawaa", "yawaon",
    "kadyot", "kad*ot", "kadyot mo",
    "pisot", "pis*t",
    "ngitngit", "ngitngit ka",
    "burikat", "bur*kat", "burikat ka",
    "hubog", "hub*g", "hubog ka",
    "buyag", "buy*g",
    "bastos", "bast*s", "bastos ka",
    "walay batasan", "walay ulaw",
    "hungog", "hung*g", "hungog ka",
    "balahiboong", "balahiboon",
    "mabuang", "maboang",
    "yawang", "yawang imo",
    "giatay", "gi atay", "gi-atay",
    "giiyot", "gi iyot", "gi-iyot",
    "gibilat", "gi bilat", "gi-bilat",
}
def contains_foul_language(text):
    original = text.lower()

    # Remove spaces around * to catch "f * ck"
    no_space_star = re.sub(r'\s*\*\s*', '*', original)

    # Version with * kept
    with_star = re.sub(r'[^a-z0-9\s\*]', '', no_space_star)

    # Version with everything stripped
    cleaned = re.sub(r'[^a-z0-9\s]', '', original)

    # Version with * removed entirely
    star_removed = no_space_star.replace('*', '')

    # Leet speak normalization
    leet = original
    leet = leet.replace('0', 'o').replace('1', 'i').replace('3', 'e')
    leet = leet.replace('4', 'a').replace('5', 's').replace('*', '')
    leet = re.sub(r'[^a-z\s]', '', leet)

    versions = [original, no_space_star, with_star, cleaned, star_removed, leet]

    for fw in FOUL_WORDS:
        fw_clean = re.sub(r'[^a-z\s]', '', fw.lower())
        fw_star  = fw.lower()

        for version in versions:
            if fw_star in version:
                return True
            if fw_clean in version:
                return True
            # Word-by-word check
            for word in version.split():
                if word == fw_star or word == fw_clean:
                    return True

    return False

# ── CONFIG ──
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# ── DATABASE PATH ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, 'database.db')

print("DB PATH:", DB_PATH)

# ── SESSION HELPER ──
CCS_COURSES = {'BSIT', 'BSCS'}

def get_sessions_for_course(course):
    return 30 if course in CCS_COURSES else 15


# ── DB CONNECTION ──
def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ── CREATE TABLES ──
def create_tables():
    conn = get_db_connection()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            idNumber    TEXT PRIMARY KEY,
            firstName   TEXT,
            lastName    TEXT,
            email       TEXT,
            courseLevel TEXT,
            course      TEXT,
            address     TEXT,
            password    TEXT,
            profilePic  TEXT,
            sessions    INTEGER DEFAULT 30
        )
    ''')

    for col, defn in [('profilePic', 'TEXT'), ('sessions', 'INTEGER DEFAULT 30')]:
        try:
            conn.execute(f'ALTER TABLE users ADD COLUMN {col} {defn}')
        except Exception:
            pass

    conn.execute("UPDATE users SET sessions = 30 WHERE sessions IS NULL")

    conn.execute('''
        CREATE TABLE IF NOT EXISTS sitin_active (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            idNumber    TEXT NOT NULL,
            studentName TEXT,
            purpose     TEXT,
            lab         TEXT,
            timeIn      TEXT,
            FOREIGN KEY (idNumber) REFERENCES users(idNumber)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS sitin_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            idNumber    TEXT,
            studentName TEXT,
            purpose     TEXT,
            lab         TEXT,
            timeIn      TEXT,
            timeOut     TEXT
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            content   TEXT NOT NULL,
            postedAt  TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            idNumber    TEXT NOT NULL,
            studentName TEXT,
            lab         TEXT,
            message     TEXT NOT NULL,
            submittedAt TEXT NOT NULL,
            sitin_log_id INTEGER,
            FOREIGN KEY (idNumber) REFERENCES users(idNumber)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            idNumber    TEXT NOT NULL,
            studentName TEXT,
            lab         TEXT NOT NULL,
            date        TEXT NOT NULL,
            timeSlot    TEXT NOT NULL,
            pcNumber    INTEGER NOT NULL,
            status      TEXT DEFAULT 'pending',
            createdAt   TEXT NOT NULL,
            FOREIGN KEY (idNumber) REFERENCES users(idNumber)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS pc_maintenance (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            lab      TEXT NOT NULL,
            pcNumber INTEGER NOT NULL,
            status   TEXT DEFAULT 'maintenance',
            reason   TEXT,
            UNIQUE(lab, pcNumber)
        )
    ''')

    # ── Migration: add status column for existing databases ──
    try:
        conn.execute("ALTER TABLE pc_maintenance ADD COLUMN status TEXT DEFAULT 'maintenance'")
    except Exception:
        pass
    conn.execute("UPDATE pc_maintenance SET status = 'maintenance' WHERE status IS NULL")

    # ── Lab availability (whole lab blocked) ──
    conn.execute('''
        CREATE TABLE IF NOT EXISTS lab_availability (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            lab       TEXT NOT NULL UNIQUE,
            available INTEGER DEFAULT 1,
            reason    TEXT,
            updatedAt TEXT
        )
    ''')

    # ── Notifications ──
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            idNumber   TEXT NOT NULL,
            title      TEXT NOT NULL,
            message    TEXT NOT NULL,
            isRead     INTEGER DEFAULT 0,
            createdAt  TEXT NOT NULL,
            type       TEXT DEFAULT 'info',
            FOREIGN KEY (idNumber) REFERENCES users(idNumber)
        )
    ''')
    # In create_tables(), add this to the feedback table creation:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            idNumber    TEXT NOT NULL,
            studentName TEXT,
            lab         TEXT,
            message     TEXT NOT NULL,
            submittedAt TEXT NOT NULL,
            sitin_log_id INTEGER,
            flagged     INTEGER DEFAULT 0,
            FOREIGN KEY (idNumber) REFERENCES users(idNumber)
        )
    ''')

# Migration for existing databases — add after the table creation:
    try:
        conn.execute("ALTER TABLE feedback ADD COLUMN flagged INTEGER DEFAULT 0")
    except Exception:
        pass
    
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sitin_evaluations (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            sitin_log_id    INTEGER NOT NULL,
            idNumber        TEXT NOT NULL,
            task_completed  INTEGER DEFAULT 0,
            pc_clean        INTEGER DEFAULT 0,
            evaluatedAt     TEXT NOT NULL,
            FOREIGN KEY (sitin_log_id) REFERENCES sitin_log(id),
            FOREIGN KEY (idNumber) REFERENCES users(idNumber)
        )
    ''')
 
    conn.execute('''
        CREATE TABLE IF NOT EXISTS student_points (
            idNumber        TEXT PRIMARY KEY,
            raw_points      INTEGER DEFAULT 0,
            bonus_points    INTEGER DEFAULT 0,
            total_sessions  INTEGER DEFAULT 0,
            total_minutes   INTEGER DEFAULT 0,
            FOREIGN KEY (idNumber) REFERENCES users(idNumber)
        )
    ''')
     
    conn.execute('''
        CREATE TABLE IF NOT EXISTS lab_software (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            lab     TEXT NOT NULL,
            name    TEXT NOT NULL,
            version TEXT,
            status  TEXT DEFAULT 'available'
        )
    ''')

        # ✅ I-ADD DIRI — before conn.commit()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS app_settings (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

create_tables()


# ════════════════════════════════════════
#  HELPER: Send notification to a student
# ════════════════════════════════════════
def send_notification(id_number, title, message, notif_type='info'):
    conn = get_db_connection()
    created_at = datetime.now().strftime('%Y-%m-%d %I:%M %p')
    conn.execute('''
        INSERT INTO notifications (idNumber, title, message, isRead, createdAt, type)
        VALUES (?, ?, ?, 0, ?, ?)
    ''', (id_number, title, message, created_at, notif_type))
    conn.commit()
    conn.close()


def send_notification_to_all(title, message, notif_type='info'):
    """Send a notification to every registered student."""
    conn = get_db_connection()
    students = conn.execute('SELECT idNumber FROM users').fetchall()
    created_at = datetime.now().strftime('%Y-%m-%d %I:%M %p')
    for s in students:
        conn.execute('''
            INSERT INTO notifications (idNumber, title, message, isRead, createdAt, type)
            VALUES (?, ?, ?, 0, ?, ?)
        ''', (s['idNumber'], title, message, created_at, notif_type))
    conn.commit()
    conn.close()


# ════════════════════════════════════════
#  STUDENT ROUTES
# ════════════════════════════════════════

@app.route('/')
def home():
    session.pop('login_error', None)
    return render_template('index.html')

@app.route('/admin/evaluate_sitin', methods=['POST'])
def admin_evaluate_sitin():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
 
    data           = request.get_json()
    sitin_id       = data.get('sitinId')
    task_completed = 1 if data.get('taskCompleted') else 0
    pc_clean       = 1 if data.get('pcClean') else 0
 
    conn   = get_db_connection()
    record = conn.execute('SELECT * FROM sitin_active WHERE id = ?', (sitin_id,)).fetchone()
    if not record:
        conn.close()
        return jsonify({'success': False, 'message': 'Sit-in record not found.'})
 
    id_number = record['idNumber']
    time_out  = datetime.now().strftime('%Y-%m-%d %I:%M %p')
 
    # ── 1. Move to sitin_log and deduct session ──
    conn.execute('''
        INSERT INTO sitin_log (idNumber, studentName, purpose, lab, timeIn, timeOut)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_number, record['studentName'], record['purpose'], record['lab'], record['timeIn'], time_out))
 
    new_log = conn.execute('SELECT last_insert_rowid() as lid').fetchone()['lid']
 
    conn.execute('UPDATE users SET sessions = MAX(0, sessions - 1) WHERE idNumber = ?', (id_number,))
    conn.execute('DELETE FROM sitin_active WHERE id = ?', (sitin_id,))
 
    # ── 2. Calculate session duration in minutes ──
    try:
        fmt     = '%Y-%m-%d %I:%M %p'
        t_in    = datetime.strptime(record['timeIn'],  fmt)
        t_out   = datetime.strptime(time_out,           fmt)
        minutes = max(0, int((t_out - t_in).total_seconds() / 60))
    except Exception:
        minutes = 0
 
    # ── 3. Save evaluation ──
    eval_at = datetime.now().strftime('%Y-%m-%d %I:%M %p')
    conn.execute('''
        INSERT INTO sitin_evaluations (sitin_log_id, idNumber, task_completed, pc_clean, evaluatedAt)
        VALUES (?, ?, ?, ?, ?)
    ''', (new_log, id_number, task_completed, pc_clean, eval_at))
 
    # ── 4. Update student_points ──
    # pc_clean gives 1 raw_point; every 3 raw_points = 1 bonus_point (for leaderboard)
    existing = conn.execute('SELECT * FROM student_points WHERE idNumber = ?', (id_number,)).fetchone()
    if existing:
        new_raw      = existing['raw_points']      + pc_clean
        new_sessions = existing['total_sessions']  + 1
        new_minutes  = existing['total_minutes']   + minutes
        # bonus_points = accumulated raw_points // 3
        new_bonus    = new_raw // 3
        conn.execute('''
            UPDATE student_points
            SET raw_points=?, bonus_points=?, total_sessions=?, total_minutes=?
            WHERE idNumber=?
        ''', (new_raw, new_bonus, new_sessions, new_minutes, id_number))
    else:
        new_raw   = pc_clean
        new_bonus = new_raw // 3
        conn.execute('''
            INSERT INTO student_points (idNumber, raw_points, bonus_points, total_sessions, total_minutes)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_number, new_raw, new_bonus, 1, minutes))
 
    conn.commit()
 
    updated = conn.execute('SELECT sessions FROM users WHERE idNumber = ?', (id_number,)).fetchone()
    conn.close()
 
    return jsonify({
        'success': True,
        'message': f'{record["studentName"]} logged out. Evaluation saved.',
        'remainingSessions': updated['sessions'],
        'pointsEarned': pc_clean
    })
 
 
@app.route('/api/leaderboard')
def api_leaderboard():
    """Public leaderboard — top 10 students by weighted score."""
    conn = get_db_connection()
 
    rows = conn.execute('''
        SELECT
            sp.idNumber,
            u.firstName,
            u.lastName,
            u.course,
            u.courseLevel,
            u.profilePic,
            sp.raw_points,
            sp.bonus_points,
            sp.total_sessions,
            sp.total_minutes
        FROM student_points sp
        JOIN users u ON sp.idNumber = u.idNumber
        ORDER BY sp.raw_points DESC, sp.total_sessions DESC
        LIMIT 10
    ''').fetchall()
    conn.close()
 
    result = []
    for r in rows:
        # Weighted score:
        # 50% from bonus_points (raw//3), 30% from hours, 20% from task_completed ratio
        # Normalised to a 100-pt display score per student
        bonus_score   = r['bonus_points'] * 50          # 1 bonus pt = 50 display pts
        hours_score   = (r['total_minutes'] / 60) * 30  # 1 hr = 30 display pts (capped naturally)
        session_score = r['total_sessions'] * 20         # 1 session = 20 pts
        display_score = round(bonus_score + hours_score + session_score, 1)
 
        result.append({
            'idNumber':      r['idNumber'],
            'name':          r['firstName'] + ' ' + r['lastName'],
            'course':        r['course'],
            'courseLevel':   r['courseLevel'],
            'profilePic':    r['profilePic'],
            'rawPoints':     r['raw_points'],
            'bonusPoints':   r['bonus_points'],
            'totalSessions': r['total_sessions'],
            'totalMinutes':  r['total_minutes'],
            'score':         display_score,
        })
 
    # Sort by final score descending
    result.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(result)

@app.route('/register', methods=['POST'])
def register():
    id_number = request.form.get('idNumber', '').strip()
    conn = get_db_connection()

    existing = conn.execute('SELECT * FROM users WHERE idNumber = ?', (id_number,)).fetchone()
    if existing:
        conn.close()
        return jsonify({'success': False, 'message': f'ID Number "{id_number}" is already registered.'})

    course   = request.form.get('course', '')
    sessions = get_sessions_for_course(course)

    conn.execute('''
        INSERT INTO users (idNumber, firstName, lastName, email, courseLevel, course, address, password, sessions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        id_number,
        request.form.get('firstName', ''),
        request.form.get('lastName', ''),
        request.form.get('email', ''),
        request.form.get('courseLevel', ''),
        course,
        request.form.get('address', ''),
        request.form.get('password', ''),
        sessions
    ))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Registration successful!'})
@app.route('/admin/flag_feedback', methods=['POST'])
def admin_flag_feedback():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data      = request.get_json()
    fb_id     = data.get('id')
    id_number = data.get('idNumber')
    message   = data.get('message', '')

    conn = get_db_connection()
    conn.execute('UPDATE feedback SET flagged = 1 WHERE id = ?', (fb_id,))
    conn.commit()
    conn.close()

    send_notification(
        id_number,
        '⚠️ Feedback Flagged',
        f'Your feedback "{message[:60]}{"..." if len(message) > 60 else ""}" was flagged by the admin for containing inappropriate language. Please keep your feedback respectful.',
        'warning'
    )

    return jsonify({'success': True, 'message': 'Feedback flagged and student notified.'})


@app.route('/admin/unflag_feedback', methods=['POST'])
def admin_unflag_feedback():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data  = request.get_json()
    fb_id = data.get('id')

    conn = get_db_connection()
    conn.execute('UPDATE feedback SET flagged = 0 WHERE id = ?', (fb_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Feedback unflagged.'})

@app.route('/login', methods=['POST'])
def login():
    id_number = request.form['idNumber']
    password  = request.form['password']

    if id_number == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))

    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE idNumber=? AND password=?', (id_number, password)
    ).fetchone()
    conn.close()

    if user:
        session['user'] = id_number
        return redirect(url_for('dashboard'))

    flash('Wrong ID or password')
    session['login_error'] = True
    return redirect(url_for('home'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    conn = get_db_connection()
    user          = conn.execute('SELECT * FROM users WHERE idNumber = ?', (session['user'],)).fetchone()
    announcements = conn.execute('SELECT * FROM announcements ORDER BY id DESC').fetchall()
    unread_count  = conn.execute(
        'SELECT COUNT(*) FROM notifications WHERE idNumber = ? AND isRead = 0',
        (session['user'],)
    ).fetchone()[0]
    conn.close()
    return render_template('dashboard.html', user=user, announcements=announcements, unread_count=unread_count)


# ── NOTIFICATIONS ──
@app.route('/student/notifications')
def student_notifications():
    if 'user' not in session:
        return jsonify([])
    id_number = session['user']
    conn = get_db_connection()
    notifs = conn.execute('''
        SELECT id, title, message, isRead, createdAt, type
        FROM notifications
        WHERE idNumber = ?
        ORDER BY id DESC
        LIMIT 50
    ''', (id_number,)).fetchall()
    conn.close()
    return jsonify([dict(n) for n in notifs])


@app.route('/student/notifications/mark_read', methods=['POST'])
def student_mark_notifications_read():
    if 'user' not in session:
        return jsonify({'success': False})
    id_number = session['user']
    data = request.get_json()
    notif_id = data.get('id')
    conn = get_db_connection()
    if notif_id:
        conn.execute('UPDATE notifications SET isRead = 1 WHERE id = ? AND idNumber = ?', (notif_id, id_number))
    else:
        conn.execute('UPDATE notifications SET isRead = 1 WHERE idNumber = ?', (id_number,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/student/notifications/unread_count')
def student_unread_count():
    if 'user' not in session:
        return jsonify({'count': 0})
    id_number = session['user']
    conn = get_db_connection()
    count = conn.execute(
        'SELECT COUNT(*) FROM notifications WHERE idNumber = ? AND isRead = 0',
        (id_number,)
    ).fetchone()[0]
    conn.close()
    return jsonify({'count': count})


@app.route('/student/history')
def student_history():
    if 'user' not in session:
        return jsonify([])

    id_number = session['user']
    conn = get_db_connection()
    records = conn.execute('''
        SELECT sl.id, sl.idNumber, sl.studentName, sl.purpose, sl.lab, sl.timeIn, sl.timeOut,
               CASE WHEN f.id IS NOT NULL THEN 1 ELSE 0 END as has_feedback
        FROM sitin_log sl
        LEFT JOIN feedback f ON f.sitin_log_id = sl.id
        WHERE sl.idNumber = ?
        ORDER BY sl.id DESC
    ''', (id_number,)).fetchall()
    conn.close()

    return jsonify([dict(r) for r in records])


@app.route('/student/submit_feedback', methods=['POST'])
def student_submit_feedback():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in.'})

    data         = request.get_json()
    sitin_log_id = data.get('sitin_log_id')
    message      = (data.get('message') or '').strip()
    lab          = data.get('lab', '')

    if not message:
        return jsonify({'success': False, 'message': 'Feedback message cannot be empty.'})

    # ── PROFANITY CHECK ──
    if contains_foul_language(message):
        return jsonify({'success': False, 'message': 'Your feedback contains inappropriate language. Please keep it respectful.'})

    id_number = session['user']
    conn = get_db_connection()

    user = conn.execute('SELECT firstName, lastName FROM users WHERE idNumber = ?', (id_number,)).fetchone()
    student_name = f"{user['firstName']} {user['lastName']}" if user else 'Unknown'

    existing = conn.execute('SELECT id FROM feedback WHERE sitin_log_id = ?', (sitin_log_id,)).fetchone()
    if existing:
        conn.close()
        return jsonify({'success': False, 'message': 'You already submitted feedback for this session.'})

    submitted_at = datetime.now().strftime('%Y-%m-%d %I:%M %p')
    conn.execute('''
        INSERT INTO feedback (idNumber, studentName, lab, message, submittedAt, sitin_log_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_number, student_name, lab, message, submitted_at, sitin_log_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Feedback submitted successfully!'})

@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in.'})

    id_number    = session['user']
    first_name   = request.form.get('firstName', '').strip()
    last_name    = request.form.get('lastName', '').strip()
    email        = request.form.get('email', '').strip()
    course_level = request.form.get('courseLevel', '').strip()
    course       = request.form.get('course', '').strip()
    address      = request.form.get('address', '').strip()
    new_password = request.form.get('password', '').strip()

    conn = get_db_connection()

    current = conn.execute('SELECT course FROM users WHERE idNumber = ?', (id_number,)).fetchone()
    if current and current['course'] != course:
        new_sessions = get_sessions_for_course(course)
        conn.execute('UPDATE users SET sessions = ? WHERE idNumber = ?', (new_sessions, id_number))

    profile_pic_data = None
    if 'profilePic' in request.files:
        file = request.files['profilePic']
        if file and file.filename:
            file_bytes = file.read()
            mime = file.content_type
            b64  = base64.b64encode(file_bytes).decode('utf-8')
            profile_pic_data = f'data:{mime};base64,{b64}'

    if profile_pic_data:
        if new_password:
            conn.execute('''UPDATE users SET firstName=?, lastName=?, email=?, courseLevel=?, course=?,
                address=?, password=?, profilePic=? WHERE idNumber=?''',
                (first_name, last_name, email, course_level, course, address, new_password, profile_pic_data, id_number))
        else:
            conn.execute('''UPDATE users SET firstName=?, lastName=?, email=?, courseLevel=?, course=?,
                address=?, profilePic=? WHERE idNumber=?''',
                (first_name, last_name, email, course_level, course, address, profile_pic_data, id_number))
    else:
        if new_password:
            conn.execute('''UPDATE users SET firstName=?, lastName=?, email=?, courseLevel=?, course=?,
                address=?, password=? WHERE idNumber=?''',
                (first_name, last_name, email, course_level, course, address, new_password, id_number))
        else:
            conn.execute('''UPDATE users SET firstName=?, lastName=?, email=?, courseLevel=?, course=?,
                address=? WHERE idNumber=?''',
                (first_name, last_name, email, course_level, course, address, id_number))

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Profile updated successfully!'})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# ════════════════════════════════════════
#  ADMIN ROUTES
# ════════════════════════════════════════

@app.route('/admin')
def admin_index():
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('home'))

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM users').fetchall()
    active   = conn.execute('''
        SELECT sa.*, u.sessions, u.profilePic
        FROM sitin_active sa
        JOIN users u ON sa.idNumber = u.idNumber
        ORDER BY sa.timeIn DESC
    ''').fetchall()
    total_log          = conn.execute('SELECT COUNT(*) FROM sitin_log').fetchone()[0]
    announcements      = conn.execute('SELECT * FROM announcements ORDER BY id DESC').fetchall()
    total_reservations = conn.execute(
        "SELECT COUNT(*) FROM reservations WHERE status != 'cancelled'"
    ).fetchone()[0]
    conn.close()

    stats = {
        'registered':   len(students),
        'current':      len(active),
        'total':        total_log,
        'reservations': total_reservations,
    }

    return render_template('admin_dashboard.html',
                           students=students,
                           active=active,
                           stats=stats,
                           announcements=announcements)


@app.route('/admin/stats_data')
def admin_stats_data():
    if not session.get('admin'):
        return jsonify({})

    conn = get_db_connection()

    purposes_log = conn.execute('''
        SELECT purpose, COUNT(*) as count FROM sitin_log GROUP BY purpose
    ''').fetchall()

    purposes_active = conn.execute('''
        SELECT purpose, COUNT(*) as count FROM sitin_active GROUP BY purpose
    ''').fetchall()

    labs_log = conn.execute('''
        SELECT lab, COUNT(*) as count FROM sitin_log GROUP BY lab ORDER BY count DESC
    ''').fetchall()

    labs_active = conn.execute('''
        SELECT lab, COUNT(*) as count FROM sitin_active GROUP BY lab ORDER BY count DESC
    ''').fetchall()

    conn.close()

    merged_purposes = {}
    for row in purposes_log:
        merged_purposes[row['purpose']] = merged_purposes.get(row['purpose'], 0) + row['count']
    for row in purposes_active:
        merged_purposes[row['purpose']] = merged_purposes.get(row['purpose'], 0) + row['count']

    sorted_purposes = sorted(merged_purposes.items(), key=lambda x: x[1], reverse=True)

    merged_labs = {}
    for row in labs_log:
        merged_labs[row['lab']] = merged_labs.get(row['lab'], 0) + row['count']
    for row in labs_active:
        merged_labs[row['lab']] = merged_labs.get(row['lab'], 0) + row['count']

    sorted_labs = sorted(merged_labs.items(), key=lambda x: x[1], reverse=True)

    return jsonify({
        'purpose_labels': [x[0] for x in sorted_purposes],
        'purpose_values': [x[1] for x in sorted_purposes],
        'lab_labels':     [x[0] for x in sorted_labs],
        'lab_values':     [x[1] for x in sorted_labs],
    })


@app.route('/admin/sitin_records')
def admin_sitin_records():
    if not session.get('admin'):
        return jsonify([])

    conn = get_db_connection()
    records = conn.execute('''
        SELECT id, idNumber, studentName, purpose, lab, timeIn, timeOut
        FROM sitin_log
        ORDER BY id DESC
    ''').fetchall()
    conn.close()

    return jsonify([dict(r) for r in records])


@app.route('/admin/feedback_reports')
def admin_feedback_reports():
    if not session.get('admin'):
        return jsonify([])

    conn = get_db_connection()
    records = conn.execute('''
        SELECT f.id, f.idNumber, f.studentName, f.lab, f.message, f.submittedAt, f.sitin_log_id, f.flagged
        FROM feedback f
        ORDER BY f.id DESC
    ''').fetchall()
    conn.close()

    return jsonify([dict(r) for r in records])

@app.route('/admin/add_student', methods=['POST'])
def admin_add_student():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data         = request.get_json()
    id_number    = data.get('idNumber', '').strip()
    first_name   = data.get('firstName', '').strip()
    last_name    = data.get('lastName', '').strip()
    email        = data.get('email', '').strip()
    course_level = data.get('courseLevel', '').strip()
    course       = data.get('course', '').strip()
    address      = data.get('address', '').strip()
    password     = data.get('password', '').strip()

    if not all([id_number, first_name, last_name, email, course_level, course, password]):
        return jsonify({'success': False, 'message': 'All fields are required.'})

    conn = get_db_connection()
    existing = conn.execute('SELECT idNumber FROM users WHERE idNumber = ?', (id_number,)).fetchone()
    if existing:
        conn.close()
        return jsonify({'success': False, 'message': f'ID Number "{id_number}" is already registered.'})

    sessions = get_sessions_for_course(course)
    conn.execute('''
        INSERT INTO users (idNumber, firstName, lastName, email, courseLevel, course, address, password, sessions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id_number, first_name, last_name, email, course_level, course, address, password, sessions))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': f'Student {first_name} {last_name} added successfully.'})


@app.route('/admin/reset_sessions', methods=['POST'])
def admin_reset_sessions():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data         = request.get_json()
    course_level = data.get('courseLevel', '').strip()
    course       = data.get('course', '').strip()

    conn = get_db_connection()

    # Build filter
    if course_level and course:
        students = conn.execute(
            'SELECT idNumber, course FROM users WHERE courseLevel=? AND course=?',
            (course_level, course)
        ).fetchall()
    elif course_level:
        students = conn.execute(
            'SELECT idNumber, course FROM users WHERE courseLevel=?',
            (course_level,)
        ).fetchall()
    else:
        students = conn.execute('SELECT idNumber, course FROM users').fetchall()

    affected_ids = [s['idNumber'] for s in students]

    # ✅ STEP 1: Delete sitin_log records
    if affected_ids:
        placeholders = ','.join(['?' for _ in affected_ids])
        conn.execute(
            f'DELETE FROM sitin_log WHERE idNumber IN ({placeholders})',
            affected_ids
        )
        # ✅ Also delete student_points para ma-reset ang summary
        conn.execute(
            f'DELETE FROM student_points WHERE idNumber IN ({placeholders})',
            affected_ids
        )

    # ✅ STEP 2: Reset sessions
    for s in students:
        new_sessions = get_sessions_for_course(s['course'])
        conn.execute(
            'UPDATE users SET sessions=? WHERE idNumber=?',
            (new_sessions, s['idNumber'])
        )

    conn.commit()
    conn.close()
    
      # ✅ Send notification to all affected students
    for id_number in affected_ids:
        send_notification(
            id_number,
            '🔄 Sessions Reset',
            f'Your sit-in sessions have been reset back to their default count '
            f'(30 for CCS students, 15 for others). Your sit-in history has also been cleared. '
            f'You may now start a fresh semester!',
            'info'
        )

    return jsonify({
        'success': True,
        'message': f'Sessions and sit-in logs reset for {len(affected_ids)} student(s).'
    })

@app.route('/admin/post_announcement', methods=['POST'])
def admin_post_announcement():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data    = request.get_json()
    content = data.get('content', '').strip()

    if not content:
        return jsonify({'success': False, 'message': 'Announcement cannot be empty.'})

    posted_at = datetime.now().strftime('%Y-%b-%d')

    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO announcements (content, postedAt) VALUES (?, ?)',
        (content, posted_at)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    send_notification_to_all(
        '📢 New Announcement',
        content[:120] + ('…' if len(content) > 120 else ''),
        'announcement'
    )

    return jsonify({
        'success': True,
        'message': 'Announcement posted!',
        'announcement': {'id': new_id, 'content': content, 'postedAt': posted_at}
    })


@app.route('/admin/delete_announcement', methods=['POST'])
def admin_delete_announcement():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data   = request.get_json()
    ann_id = data.get('id')

    conn = get_db_connection()
    conn.execute('DELETE FROM announcements WHERE id = ?', (ann_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Announcement deleted.'})


@app.route('/admin/search_student')
def admin_search_student():
    if not session.get('admin'):
        return jsonify([])

    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    conn = get_db_connection()
    results = conn.execute('''
        SELECT idNumber, firstName, lastName, course, courseLevel, email, sessions, profilePic
        FROM users
        WHERE idNumber LIKE ? OR firstName LIKE ? OR lastName LIKE ?
        LIMIT 10
    ''', (f'%{q}%', f'%{q}%', f'%{q}%')).fetchall()
    conn.close()

    return jsonify([dict(r) for r in results])


@app.route('/admin/sitin', methods=['POST'])
def admin_sitin():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data         = request.get_json()
    id_number    = data.get('idNumber', '').strip()
    student_name = data.get('studentName', '').strip()
    purpose      = data.get('purpose', '').strip()
    lab          = data.get('lab', '').strip()

    if not id_number or not purpose or not lab:
        return jsonify({'success': False, 'message': 'All fields are required.'})

    conn = get_db_connection()

    user = conn.execute('SELECT * FROM users WHERE idNumber = ?', (id_number,)).fetchone()
    if not user:
        conn.close()
        return jsonify({'success': False, 'message': 'Student not found.'})

    already = conn.execute('SELECT * FROM sitin_active WHERE idNumber = ?', (id_number,)).fetchone()
    if already:
        conn.close()
        return jsonify({'success': False, 'message': 'Student is already sitting in.'})

    if user['sessions'] <= 0:
        conn.close()
        return jsonify({'success': False, 'message': 'Student has no remaining sessions.'})

    time_in = datetime.now().strftime('%Y-%m-%d %I:%M %p')
    conn.execute('''
        INSERT INTO sitin_active (idNumber, studentName, purpose, lab, timeIn)
        VALUES (?, ?, ?, ?, ?)
    ''', (id_number, student_name, purpose, lab, time_in))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': f'{student_name} is now sitting in.'})


@app.route('/admin/sitin_logout', methods=['POST'])
def admin_sitin_logout():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data     = request.get_json()
    sitin_id = data.get('sitinId')

    conn   = get_db_connection()
    record = conn.execute('SELECT * FROM sitin_active WHERE id = ?', (sitin_id,)).fetchone()
    if not record:
        conn.close()
        return jsonify({'success': False, 'message': 'Sit-in record not found.'})

    id_number = record['idNumber']
    time_out  = datetime.now().strftime('%Y-%m-%d %I:%M %p')

    conn.execute('''
        INSERT INTO sitin_log (idNumber, studentName, purpose, lab, timeIn, timeOut)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_number, record['studentName'], record['purpose'], record['lab'], record['timeIn'], time_out))

    conn.execute('UPDATE users SET sessions = MAX(0, sessions - 1) WHERE idNumber = ?', (id_number,))
    conn.execute('DELETE FROM sitin_active WHERE id = ?', (sitin_id,))
    conn.commit()

    updated = conn.execute('SELECT sessions FROM users WHERE idNumber = ?', (id_number,)).fetchone()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Student logged out. 1 session deducted.',
        'remainingSessions': updated['sessions']
    })


@app.route('/admin/active_sitins')
def admin_active_sitins():
    if not session.get('admin'):
        return jsonify([])

    conn = get_db_connection()
    active = conn.execute('''
        SELECT sa.id, sa.idNumber, sa.studentName, sa.purpose, sa.lab, sa.timeIn,
               u.sessions, u.profilePic, u.course, u.courseLevel
        FROM sitin_active sa
        JOIN users u ON sa.idNumber = u.idNumber
        ORDER BY sa.timeIn DESC
    ''').fetchall()
    conn.close()

    return jsonify([dict(r) for r in active])


@app.route('/admin/edit_student', methods=['POST'])
def admin_edit_student():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data         = request.get_json()
    id_number    = data.get('idNumber', '').strip()
    first_name   = data.get('firstName', '').strip()
    last_name    = data.get('lastName', '').strip()
    email        = data.get('email', '').strip()
    course       = data.get('course', '').strip()
    course_level = data.get('courseLevel', '').strip()

    if not id_number:
        return jsonify({'success': False, 'message': 'ID Number is required.'})

    conn = get_db_connection()

    current = conn.execute('SELECT course FROM users WHERE idNumber = ?', (id_number,)).fetchone()
    if current and current['course'] != course:
        new_sessions = get_sessions_for_course(course)
        conn.execute('UPDATE users SET sessions = ? WHERE idNumber = ?', (new_sessions, id_number))

    conn.execute('''
        UPDATE users SET firstName=?, lastName=?, email=?, course=?, courseLevel=?
        WHERE idNumber=?
    ''', (first_name, last_name, email, course, course_level, id_number))
    conn.commit()

    updated = conn.execute('SELECT sessions FROM users WHERE idNumber = ?', (id_number,)).fetchone()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Student updated successfully.',
        'newSessions': updated['sessions']
    })


@app.route('/admin/delete_student', methods=['POST'])
def admin_delete_student():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data      = request.get_json()
    id_number = data.get('idNumber', '').strip()

    if not id_number:
        return jsonify({'success': False, 'message': 'ID Number is required.'})

    conn = get_db_connection()
    conn.execute('DELETE FROM sitin_active WHERE idNumber = ?', (id_number,))
    conn.execute('DELETE FROM users WHERE idNumber = ?', (id_number,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Student deleted successfully.'})


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('home'))


# ════════════════════════════════════════
#  STUDENT RESERVATION ROUTES
# ════════════════════════════════════════

@app.route('/student/available_labs')
def student_available_labs():
    if 'user' not in session:
        return jsonify([])

    ALL_LABS  = ['524', '526', '528', '530', '544', '542']
    TOTAL_PCS = 40
    ALL_SLOTS = [
        '07:00 AM - 09:00 AM', '09:00 AM - 11:00 AM', '11:00 AM - 01:00 PM',
        '01:00 PM - 03:00 PM', '03:00 PM - 05:00 PM', '05:00 PM - 07:00 PM',
    ]

    date      = request.args.get('date', '').strip()
    id_number = session['user']

    if not date:
        return jsonify([])

    conn = get_db_connection()

    blocked_rows = conn.execute(
        "SELECT lab FROM lab_availability WHERE available = 0"
    ).fetchall()
    blocked_labs = {row['lab'] for row in blocked_rows}

    # All non-available statuses (in_use, not_working, maintenance) block a PC
    maint_rows = conn.execute(
        'SELECT lab, COUNT(*) as cnt FROM pc_maintenance GROUP BY lab'
    ).fetchall()
    maint_map = {row['lab']: row['cnt'] for row in maint_rows}

    available_labs = []

    for lab in ALL_LABS:
        if lab in blocked_labs:
            continue

        maint_count = maint_map.get(lab, 0)
        usable_pcs  = TOTAL_PCS - maint_count

        if usable_pcs <= 0:
            continue

        has_available_slot = False
        for slot in ALL_SLOTS:
            reserved_count = conn.execute("""
                SELECT COUNT(*) FROM reservations
                WHERE lab=? AND date=? AND timeSlot=? AND status != 'cancelled' AND idNumber != ?
            """, (lab, date, slot, id_number)).fetchone()[0]

            if (usable_pcs - reserved_count) > 0:
                has_available_slot = True
                break

        if has_available_slot:
            available_labs.append(lab)

    conn.close()
    return jsonify(available_labs)


@app.route('/student/available_slots')
@app.route('/student/available_slots')
def student_available_slots():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    lab  = request.args.get('lab', '').strip()
    date = request.args.get('date', '').strip()

    if not lab or not date:
        return jsonify({'error': 'Missing params'}), 400

    ALL_SLOTS = [
        '07:00 AM - 09:00 AM', '09:00 AM - 11:00 AM', '11:00 AM - 01:00 PM',
        '01:00 PM - 03:00 PM', '03:00 PM - 05:00 PM', '05:00 PM - 07:00 PM',
    ]

    id_number = session['user']
    conn      = get_db_connection()

    maint_count = conn.execute(
        'SELECT COUNT(*) FROM pc_maintenance WHERE lab=?', (lab,)
    ).fetchone()[0]
    usable_pcs = 40 - maint_count

    slot_counts = conn.execute("""
        SELECT timeSlot, COUNT(*) as cnt FROM reservations
        WHERE lab=? AND date=? AND status != 'cancelled' AND idNumber != ?
        GROUP BY timeSlot
    """, (lab, date, id_number)).fetchall()

    my_slots = conn.execute("""
        SELECT timeSlot FROM reservations
        WHERE lab=? AND date=? AND idNumber=? AND status != 'cancelled'
    """, (lab, date, id_number)).fetchall()
    my_slot_set = {r['timeSlot'] for r in my_slots}

    conn.close()

    slot_map = {r['timeSlot']: r['cnt'] for r in slot_counts}
    result   = []

    # ── BAG-ONG DUGANG: i-check kung past na ang slot kung today ang date ──
    today_str = datetime.now().strftime('%Y-%m-%d')

    def is_slot_past(slot):
        if date != today_str:
            return False
        slot_end_str = slot.split(' - ')[1]  # e.g. "09:00 AM"
        slot_end = datetime.strptime(date + ' ' + slot_end_str, '%Y-%m-%d %I:%M %p')
        return datetime.now() > slot_end

    for slot in ALL_SLOTS:
        if slot in my_slot_set:
            continue
        if is_slot_past(slot):  # ← skip na ang past slots kung today
            continue
        used      = slot_map.get(slot, 0)
        available = max(0, usable_pcs - used)
        result.append({'slot': slot, 'used': used, 'available': available, 'full': available == 0})

    return jsonify(result)

@app.route('/student/pc_status')
def student_pc_status():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    lab      = request.args.get('lab', '').strip()
    date     = request.args.get('date', '').strip()
    timeslot = request.args.get('timeslot', '').strip()

    if not lab or not date or not timeslot:
        return jsonify({'error': 'Missing params'}), 400

    conn = get_db_connection()

    reserved = conn.execute("""
        SELECT pcNumber FROM reservations
        WHERE lab=? AND date=? AND timeSlot=? AND status != 'cancelled'
    """, (lab, date, timeslot)).fetchall()
    reserved_pcs = {r['pcNumber'] for r in reserved}

    maint = conn.execute(
        "SELECT pcNumber, status, reason FROM pc_maintenance WHERE lab=?", (lab,)
    ).fetchall()
    maint_map = {
        r['pcNumber']: {
            'status': r['status'] or 'maintenance',
            'reason': r['reason'] or ''
        }
        for r in maint
    }

    # ── Auto IN USE based on approved reservations ──
    now       = datetime.now()
    today_str = now.strftime('%Y-%m-%d')

    if date == today_str:
        approved_now = conn.execute("""
            SELECT pcNumber, timeSlot FROM reservations
            WHERE lab=? AND date=? AND status='approved'
        """, (lab, today_str)).fetchall()

        for rsv in approved_now:
            pc       = rsv['pcNumber']
            timeslot_rsv = rsv['timeSlot']
            try:
                start_str, end_str = timeslot_rsv.split(' - ')
                slot_start = datetime.strptime(today_str + ' ' + start_str.strip(), '%Y-%m-%d %I:%M %p')
                slot_end   = datetime.strptime(today_str + ' ' + end_str.strip(),   '%Y-%m-%d %I:%M %p')
            except Exception:
                continue
            if slot_start <= now <= slot_end:
                maint_map[pc] = {'status': 'in_use', 'reason': 'Reserved (Approved)'}

    conn.close()

    pcs = []
    for i in range(1, 41):
        if i in maint_map:
            status = maint_map[i]['status']
            reason = maint_map[i]['reason']
        elif i in reserved_pcs:
            status = 'reserved'
            reason = ''
        else:
            status = 'available'
            reason = ''
        pcs.append({'pc': i, 'status': status, 'reason': reason})

    return jsonify(pcs)

@app.route('/student/reserve', methods=['POST'])
def student_reserve():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in.'})

    # ✅ I-ADD DIRI — check if reservations are enabled
    conn = get_db_connection()
    setting = conn.execute(
        "SELECT value FROM app_settings WHERE key='reservation_enabled'"
    ).fetchone()
    conn.close()
    if setting and setting['value'] == '0':
        return jsonify({'success': False, 'message': 'Reservations are currently disabled by the admin.'})

    data      = request.get_json()
    lab       = data.get('lab', '').strip()
    date      = data.get('date', '').strip()
    timeslot  = data.get('timeslot', '').strip()
    pc_number = data.get('pcNumber')

    if not all([lab, date, timeslot, pc_number]):
        return jsonify({'success': False, 'message': 'All fields are required.'})

    from datetime import date as dobj, timedelta
    try:
        chosen = dobj.fromisoformat(date)
    except Exception:
        return jsonify({'success': False, 'message': 'Invalid date.'})

    today    = dobj.today()
    max_date = today.replace(year=today.year + 1) - timedelta(days=1)

    if chosen < today:
        return jsonify({'success': False, 'message': 'Cannot reserve a past date.'})
    if chosen > max_date:
        return jsonify({'success': False, 'message': 'Cannot reserve beyond this year.'})

    id_number = session['user']
    conn      = get_db_connection()

    blocked = conn.execute(
        "SELECT id FROM lab_availability WHERE lab=? AND available=0", (lab,)
    ).fetchone()
    if blocked:
        conn.close()
        return jsonify({'success': False, 'message': f'Lab {lab} is currently unavailable.'})

    user = conn.execute('SELECT firstName, lastName FROM users WHERE idNumber=?', (id_number,)).fetchone()
    student_name = f"{user['firstName']} {user['lastName']}" if user else 'Unknown'

    conflict = conn.execute("""
        SELECT id FROM reservations
        WHERE lab=? AND date=? AND timeSlot=? AND pcNumber=? AND status != 'cancelled'
    """, (lab, date, timeslot, pc_number)).fetchone()
    if conflict:
        conn.close()
        return jsonify({'success': False, 'message': 'That PC is already reserved for this slot.'})

    # Block reservation if PC has ANY non-available status
    maint = conn.execute(
        "SELECT id FROM pc_maintenance WHERE lab=? AND pcNumber=?", (lab, pc_number)
    ).fetchone()
    if maint:
        conn.close()
        return jsonify({'success': False, 'message': 'That PC is currently unavailable.'})

    own = conn.execute("""
        SELECT id FROM reservations
        WHERE idNumber=? AND date=? AND timeSlot=? AND status != 'cancelled'
    """, (id_number, date, timeslot)).fetchone()
    if own:
        conn.close()
        return jsonify({'success': False, 'message': 'You already have a reservation for this date and time slot.'})

    created_at = datetime.now().strftime('%Y-%m-%d %I:%M %p')
    conn.execute("""
        INSERT INTO reservations (idNumber, studentName, lab, date, timeSlot, pcNumber, status, createdAt)
        VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)
    """, (id_number, student_name, lab, date, timeslot, pc_number, created_at))
    conn.commit()
    conn.close()

    send_notification(
        id_number,
        '📅 Reservation Submitted',
        f'Your reservation for Lab {lab}, PC #{pc_number} on {date} at {timeslot} is now pending approval.',
        'reservation'
    )

    return jsonify({'success': True, 'message': f'PC {pc_number} in Lab {lab} reserved for {date} at {timeslot}!'})


@app.route('/student/my_reservations')
def student_my_reservations():
    if 'user' not in session:
        return jsonify([])

    id_number = session['user']
    conn      = get_db_connection()
    rows      = conn.execute("""
        SELECT id, lab, date, timeSlot, pcNumber, status, createdAt
        FROM reservations WHERE idNumber=? ORDER BY date DESC, timeSlot DESC
    """, (id_number,)).fetchall()
    conn.close()

    return jsonify([dict(r) for r in rows])


@app.route('/student/cancel_reservation', methods=['POST'])
def student_cancel_reservation():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in.'})

    data      = request.get_json()
    res_id    = data.get('id')
    id_number = session['user']

    conn = get_db_connection()
    res  = conn.execute(
        'SELECT * FROM reservations WHERE id=? AND idNumber=?', (res_id, id_number)
    ).fetchone()
    if not res:
        conn.close()
        return jsonify({'success': False, 'message': 'Reservation not found.'})

    conn.execute("UPDATE reservations SET status='cancelled' WHERE id=?", (res_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Reservation cancelled.'})


# ════════════════════════════════════════
#  ADMIN RESERVATION ROUTES
# ════════════════════════════════════════

@app.route('/admin/reservations')
def admin_reservations():
    if not session.get('admin'):
        return jsonify([])

    conn = get_db_connection()
    rows = conn.execute("""
        SELECT r.id, r.idNumber, r.studentName, r.lab, r.date, r.timeSlot,
               r.pcNumber, r.status, r.createdAt,
               u.course, u.courseLevel, u.email, u.profilePic, u.sessions
        FROM reservations r
        LEFT JOIN users u ON r.idNumber = u.idNumber
        ORDER BY r.date DESC, r.timeSlot, r.lab
    """).fetchall()
    conn.close()

    return jsonify([dict(r) for r in rows])


@app.route('/admin/update_reservation_status', methods=['POST'])
def admin_update_reservation_status():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data   = request.get_json()
    res_id = data.get('id')
    status = data.get('status')

    if status not in ('pending', 'approved', 'cancelled'):
        return jsonify({'success': False, 'message': 'Invalid status.'})

    conn = get_db_connection()
    res = conn.execute('SELECT * FROM reservations WHERE id=?', (res_id,)).fetchone()
    if not res:
        conn.close()
        return jsonify({'success': False, 'message': 'Reservation not found.'})

    conn.execute('UPDATE reservations SET status=? WHERE id=?', (status, res_id))
    conn.commit()
    conn.close()

    id_number = res['idNumber']
    lab       = res['lab']
    date      = res['date']
    timeslot  = res['timeSlot']
    pc_number = res['pcNumber']

    if status == 'approved':
        send_notification(
            id_number,
            '✅ Reservation Approved',
            f'Your reservation for Lab {lab}, PC #{pc_number} on {date} at {timeslot} has been APPROVED.',
            'success'
        )
    elif status == 'cancelled':
        send_notification(
            id_number,
            '❌ Reservation Declined',
            f'Your reservation for Lab {lab}, PC #{pc_number} on {date} at {timeslot} has been declined.',
            'error'
        )

    return jsonify({'success': True, 'message': f'Reservation {status}.'})


# ════════════════════════════════════════
#  PC STATUS ROUTES  (replaces old PC Maintenance)
# ════════════════════════════════════════

@app.route('/admin/pc_maintenance', methods=['GET'])
def admin_get_maintenance():
    if not session.get('admin'):
        return jsonify([])

    conn = get_db_connection()
    rows = conn.execute(
        'SELECT lab, pcNumber, status, reason FROM pc_maintenance ORDER BY lab, pcNumber'
    ).fetchall()
    
    # ── Auto IN USE based on approved reservations ──
    now       = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    
    approved = conn.execute("""
        SELECT lab, pcNumber, timeSlot FROM reservations
        WHERE date = ? AND status = 'approved'
    """, (today_str,)).fetchall()
    conn.close()

    # Build result from pc_maintenance
    result = [dict(r) for r in rows]
    manual_keys = {(r['lab'], r['pcNumber']) for r in rows}

    for rsv in approved:
        lab      = rsv['lab']
        pc       = rsv['pcNumber']
        timeslot = rsv['timeSlot']  # e.g. "01:00 PM - 03:00 PM"

        try:
            start_str, end_str = timeslot.split(' - ')
            slot_start = datetime.strptime(today_str + ' ' + start_str.strip(), '%Y-%m-%d %I:%M %p')
            slot_end   = datetime.strptime(today_str + ' ' + end_str.strip(),   '%Y-%m-%d %I:%M %p')
        except Exception:
            continue

        # If current time is within the reserved slot
        if slot_start <= now <= slot_end:
            key = (lab, pc)
            if key not in manual_keys:
                # Not manually set, so auto mark as in_use
                result.append({
                    'lab':      lab,
                    'pcNumber': pc,
                    'status':   'in_use',
                    'reason':   'Reserved (Approved)'
                })
            else:
                # Override existing manual status with in_use
                for r in result:
                    if r['lab'] == lab and r['pcNumber'] == pc:
                        r['status'] = 'in_use'
                        r['reason'] = 'Reserved (Approved)'
                        break

    return jsonify(result)


@app.route('/admin/pc_maintenance/set', methods=['POST'])
def admin_set_maintenance():
    """Set a PC to any non-available status: in_use | not_working | maintenance"""
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data      = request.get_json()
    lab       = data.get('lab')
    pc_number = data.get('pcNumber')
    status    = data.get('status', 'maintenance')
    reason    = data.get('reason', '')

    VALID_STATUSES = {'maintenance', 'in_use', 'not_working'}
    if status not in VALID_STATUSES:
        return jsonify({'success': False, 'message': 'Invalid status.'})

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO pc_maintenance (lab, pcNumber, status, reason)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(lab, pcNumber) DO UPDATE SET status=excluded.status, reason=excluded.reason
    """, (lab, pc_number, status, reason))
    conn.commit()
    conn.close()

    labels = {
        'maintenance': 'Under Maintenance',
        'in_use':      'In Use',
        'not_working': 'Not Working'
    }
    return jsonify({
        'success': True,
        'message': f'PC {pc_number} in Lab {lab} marked as {labels[status]}.'
    })


@app.route('/admin/pc_maintenance/clear', methods=['POST'])
def admin_clear_maintenance():
    """Mark a PC back to available by removing it from pc_maintenance."""
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data      = request.get_json()
    lab       = data.get('lab')
    pc_number = data.get('pcNumber')

    conn = get_db_connection()
    conn.execute('DELETE FROM pc_maintenance WHERE lab=? AND pcNumber=?', (lab, pc_number))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': f'PC {pc_number} is now Available.'})


# ════════════════════════════════════════
#  LAB AVAILABILITY ROUTES
# ════════════════════════════════════════

@app.route('/admin/lab_availability', methods=['GET'])
def admin_get_lab_availability():
    if not session.get('admin'):
        return jsonify([])

    ALL_LABS = ['524', '526', '528', '530', '544', '542']
    conn = get_db_connection()
    rows = conn.execute('SELECT lab, available, reason, updatedAt FROM lab_availability').fetchall()
    conn.close()

    lab_map = {row['lab']: dict(row) for row in rows}
    result = []
    for lab in ALL_LABS:
        if lab in lab_map:
            result.append(lab_map[lab])
        else:
            result.append({'lab': lab, 'available': 1, 'reason': None, 'updatedAt': None})
    return jsonify(result)

@app.route('/admin/auto_logout_all', methods=['POST'])
def admin_auto_logout_all():
    """Auto-logout all active sit-ins at 8PM — no points, no evaluation."""
    conn = get_db_connection()
    active = conn.execute('SELECT * FROM sitin_active').fetchall()

    if not active:
        conn.close()
        return jsonify({'success': True, 'message': 'No active sit-ins.'})

    time_out = datetime.now().strftime('%Y-%m-%d %I:%M %p')

# ── Process all records first ──
    notifications_to_send = []
    for record in active:
        id_number = record['idNumber']

        conn.execute('''
            INSERT INTO sitin_log (idNumber, studentName, purpose, lab, timeIn, timeOut)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (id_number, record['studentName'], record['purpose'],
              record['lab'], record['timeIn'], time_out))

        conn.execute('UPDATE users SET sessions = MAX(0, sessions - 1) WHERE idNumber = ?', (id_number,))
        conn.execute('DELETE FROM sitin_active WHERE id = ?', (record['id'],))

        notifications_to_send.append(id_number)

    conn.commit()
    conn.close()

    # ── Send notifications AFTER closing connection ──
    for id_number in notifications_to_send:
        send_notification(
            id_number,
            '⚠️ Auto Logged Out',
            'You were automatically logged out at 8:00 PM. Your session was not counted. Please inform the admin next time before leaving.',
            'warning'
        )

    return jsonify({'success': True, 'message': f'{len(active)} student(s) auto-logged out.'})


@app.route('/admin/lab_availability/set', methods=['POST'])
def admin_set_lab_availability():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})

    data       = request.get_json()
    lab        = data.get('lab')
    available  = data.get('available', 1)
    reason     = data.get('reason', '')
    updated_at = datetime.now().strftime('%Y-%m-%d %I:%M %p')

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO lab_availability (lab, available, reason, updatedAt)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(lab) DO UPDATE SET available=excluded.available, reason=excluded.reason, updatedAt=excluded.updatedAt
    """, (lab, available, reason, updated_at))
    conn.commit()
    conn.close()

    if not available:
        send_notification_to_all(
            f'🚫 Lab {lab} Unavailable',
            f'Lab {lab} has been marked as unavailable. Reason: {reason or "Maintenance"}. Please choose another lab for your reservations.',
            'warning'
        )
    else:
        send_notification_to_all(
            f'✅ Lab {lab} Now Available',
            f'Lab {lab} is now open for reservations again.',
            'success'
        )

    status_word = 'unavailable' if not available else 'available'
    return jsonify({'success': True, 'message': f'Lab {lab} marked as {status_word}.'})

@app.route('/student/sitin_summary')
def student_sitin_summary():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    id_number = session['user']
    conn = get_db_connection()

    records = conn.execute('''
        SELECT timeIn, timeOut FROM sitin_log
        WHERE idNumber = ? AND timeIn IS NOT NULL AND timeOut IS NOT NULL
    ''', (id_number,)).fetchall()

    conn.close()

    fmt = '%Y-%m-%d %I:%M %p'
    total_minutes = 0
    longest_minutes = 0
    valid_sessions = 0

    for r in records:
        try:
            t_in  = datetime.strptime(r['timeIn'],  fmt)
            t_out = datetime.strptime(r['timeOut'], fmt)
            mins  = max(0, int((t_out - t_in).total_seconds() / 60))
            total_minutes   += mins
            valid_sessions  += 1
            if mins > longest_minutes:
                longest_minutes = mins
        except Exception:
            pass

    total_sessions = len(records)
    avg_minutes    = round(total_minutes / valid_sessions, 1) if valid_sessions > 0 else 0
    total_hours    = round(total_minutes / 60, 1)

    def fmt_duration(mins):
        h = int(mins) // 60
        m = int(mins) % 60
        if h > 0 and m > 0:
            return f'{h}h {m}m'
        elif h > 0:
            return f'{h}h'
        else:
            return f'{m}m'

    return jsonify({
        'totalSessions':   total_sessions,
        'totalHours':      total_hours,
        'totalMinutes':    total_minutes,
        'avgMinutes':      avg_minutes,
        'avgFormatted':    fmt_duration(avg_minutes),
        'longestMinutes':  longest_minutes,
        'longestFormatted': fmt_duration(longest_minutes),
    })

# ════════════════════════════════════════
#  SOFTWARE AVAILABILITY ROUTES
# ════════════════════════════════════════

@app.route('/admin/lab_software', methods=['GET'])
def admin_get_lab_software():
    if not session.get('admin'):
        return jsonify([])
    conn = get_db_connection()
    rows = conn.execute(
        'SELECT id, lab, name, version, status FROM lab_software ORDER BY lab, name'
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/admin/lab_software/add', methods=['POST'])
def admin_add_lab_software():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    data    = request.get_json()
    lab     = data.get('lab', '').strip()
    name    = data.get('name', '').strip()
    version = data.get('version', '').strip()
    status  = data.get('status', 'available')
    if not lab or not name:
        return jsonify({'success': False, 'message': 'Lab and software name are required.'})
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO lab_software (lab, name, version, status) VALUES (?, ?, ?, ?)',
        (lab, name, version, status)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

        # ✅ Notify all students
    send_notification_to_all(
        f'🖥️ New Software Available — {name}',
        f'{name} (v{version}) has been added to {lab} and is now {status}.',
        'info'
    )

    return jsonify({'success': True, 'message': 'Software added.', 'id': new_id})


@app.route('/admin/lab_software/update', methods=['POST'])
def admin_update_lab_software():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    data    = request.get_json()
    sw_id   = data.get('id')
    name    = data.get('name', '').strip()
    version = data.get('version', '').strip()
    status  = data.get('status', 'available')
    if not sw_id or not name:
        return jsonify({'success': False, 'message': 'ID and name are required.'})
    conn = get_db_connection()
    conn.execute(
        'UPDATE lab_software SET name=?, version=?, status=? WHERE id=?',
        (name, version, status, sw_id)
    )
    conn.commit()
    
    
        # ✅ Notify if status changed
    updated = conn.execute(
        'SELECT lab, name, version, status FROM lab_software WHERE id=?', (sw_id,)
    ).fetchone()
    conn.close()

    if updated:
        status_word = 'now available ✅' if updated['status'] == 'available' else 'currently unavailable ❌'
        send_notification_to_all(
            f'🖥️ Software Update — {updated["name"]}',
            f'{updated["name"]} (v{updated["version"] or "—"}) in {updated["lab"]} is {status_word}.',
            'info'
        )
    

    return jsonify({'success': True, 'message': 'Software updated.'})


@app.route('/admin/lab_software/delete', methods=['POST'])
def admin_delete_lab_software():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    data  = request.get_json()
    sw_id = data.get('id')
    conn  = get_db_connection()
    conn.execute('DELETE FROM lab_software WHERE id=?', (sw_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Software deleted.'})


@app.route('/student/lab_software')
def student_lab_software():
    """Public endpoint — students can view software list."""
    conn = get_db_connection()
    rows = conn.execute(
        'SELECT lab, name, version, status FROM lab_software ORDER BY lab, name'
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/admin/lab_software/upload', methods=['POST'])
def admin_upload_lab_software():
    """
    Accepts CSV, Excel (.xlsx/.xls), or PDF file.
    Expected columns: lab, software_name, version, status
    Returns JSON with inserted count and any skipped rows.
    """
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
 
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded.'})
 
    file = request.files['file']
    if not file or not file.filename:
        return jsonify({'success': False, 'message': 'Empty file.'})
 
    filename  = file.filename.lower()
    file_bytes = file.read()
 
    rows    = []   # list of (lab, name, version, status)
    errors  = []
 
    try:
        # ── CSV ──────────────────────────────────────────────────────────
        if filename.endswith('.csv'):
            import csv, io
            text    = file_bytes.decode('utf-8-sig')   # handle BOM
            reader  = csv.DictReader(io.StringIO(text))
            # Normalize header names (strip spaces, lower)
            reader.fieldnames = [f.strip().lower().replace(' ', '_') for f in (reader.fieldnames or [])]
            for i, row in enumerate(reader, start=2):
                result = _parse_software_row(row, i)
                if isinstance(result, str):
                    errors.append(result)
                else:
                    rows.append(result)
 
        # ── EXCEL (.xlsx / .xls) ─────────────────────────────────────────
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            import io
            try:
                import openpyxl
                wb    = openpyxl.load_workbook(io.BytesIO(file_bytes), read_only=True, data_only=True)
                ws    = wb.active
                headers = None
                for r_idx, row in enumerate(ws.iter_rows(values_only=True), start=1):
                    if r_idx == 1:
                        headers = [str(c).strip().lower().replace(' ', '_') if c else '' for c in row]
                        continue
                    if not any(row):
                        continue
                    row_dict = dict(zip(headers, [str(c).strip() if c is not None else '' for c in row]))
                    result   = _parse_software_row(row_dict, r_idx)
                    if isinstance(result, str):
                        errors.append(result)
                    else:
                        rows.append(result)
            except Exception:
                # Fallback for .xls
                import pandas as pd
                df = pd.read_excel(io.BytesIO(file_bytes), engine='xlrd')
                df.columns = [str(c).strip().lower().replace(' ', '_') for c in df.columns]
                for i, (_, row) in enumerate(df.iterrows(), start=2):
                    result = _parse_software_row(row.to_dict(), i)
                    if isinstance(result, str):
                        errors.append(result)
                    else:
                        rows.append(result)
 
        # ── PDF ──────────────────────────────────────────────────────────
        elif filename.endswith('.pdf'):
            import io, pdfplumber
            all_text_rows = []
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    # Try table extraction first
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            all_text_rows.extend(table)
                    else:
                        # Fall back to raw text line-by-line
                        text  = page.extract_text() or ''
                        lines = [l.strip() for l in text.splitlines() if l.strip()]
                        for line in lines:
                            # Split by 2+ spaces or tab
                            import re
                            parts = re.split(r'\t|  +', line)
                            all_text_rows.append(parts)
 
            # Find header row
            headers = None
            REQUIRED = {'lab', 'software_name', 'version', 'status'}
            for r_idx, row in enumerate(all_text_rows):
                if not row:
                    continue
                norm = [str(c).strip().lower().replace(' ', '_') if c else '' for c in row]
                if REQUIRED.issubset(set(norm)):
                    headers = norm
                    data_rows = all_text_rows[r_idx + 1:]
                    break
 
            if not headers:
                return jsonify({
                    'success': False,
                    'message': 'PDF header row not found. Make sure the PDF table has columns: lab, software_name, version, status'
                })
 
            for i, row in enumerate(data_rows, start=2):
                if not row or not any(row):
                    continue
                row_dict = dict(zip(headers, [str(c).strip() if c else '' for c in row]))
                result   = _parse_software_row(row_dict, i)
                if isinstance(result, str):
                    errors.append(result)
                else:
                    rows.append(result)
 
        else:
            return jsonify({'success': False, 'message': 'Unsupported file type. Upload CSV, XLSX, XLS, or PDF.'})
 
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error reading file: {str(e)}'})
 
    if not rows:
        return jsonify({
            'success': False,
            'message': 'No valid rows found in file.',
            'errors':  errors
        })
 
    # ── Insert into DB ────────────────────────────────────────────────────
    conn      = get_db_connection()
    inserted  = 0
    for (lab, name, version, status) in rows:
        try:
            conn.execute(
                'INSERT INTO lab_software (lab, name, version, status) VALUES (?, ?, ?, ?)',
                (lab, name, version, status)
            )
            inserted += 1
        except Exception as e:
            errors.append(f'DB error for "{name}": {str(e)}')
    conn.commit()
    conn.close()
 
    msg = f'{inserted} software record(s) imported successfully!'
    if errors:
        msg += f' ({len(errors)} row(s) skipped)'
 
    return jsonify({
        'success': True,
        'message': msg,
        'inserted': inserted,
        'skipped':  len(errors),
        'errors':   errors[:10]   # max 10 error details
    })
 
 
# ── Helper: validate and normalize one row ──────────────────────────────
def _parse_software_row(row, row_num):
    """
    row     – dict with normalized keys (lowercase, underscore)
    row_num – for error messages
    Returns tuple (lab, name, version, status) or error string.
    """
    # Accept both 'software_name' and 'name'
    lab     = str(row.get('lab', '') or '').strip()
    name    = str(row.get('software_name', '') or row.get('name', '') or '').strip()
    version = str(row.get('version', '') or '').strip()
    status  = str(row.get('status', 'available') or 'available').strip().lower()
 
    if not lab:
        return f'Row {row_num}: missing lab'
    if not name:
        return f'Row {row_num}: missing software_name'
 
    # Normalize lab — accept "524" or "Lab 524"
    lab = lab.strip()
    if not lab.lower().startswith('lab'):
        lab = 'Lab ' + lab   # e.g. "524" → "Lab 524"
 
    # Normalize status
    if status in ('available', 'yes', '1', 'true', 'ok'):
        status = 'available'
    else:
        status = 'unavailable'
 
    return (lab, name, version, status)

# ════════════════════════════════════════
#  RESERVATION SYSTEM TOGGLE
# ════════════════════════════════════════

@app.route('/admin/reservation_toggle', methods=['GET'])
def admin_get_reservation_toggle():
    if not session.get('admin'):
        return jsonify({'enabled': True})
    conn = get_db_connection()
    row = conn.execute("SELECT value FROM app_settings WHERE key='reservation_enabled'").fetchone()
    conn.close()
    return jsonify({'enabled': row['value'] == '1' if row else True})

@app.route('/admin/reservation_toggle/set', methods=['POST'])
def admin_set_reservation_toggle():
    if not session.get('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    data    = request.get_json()
    enabled = data.get('enabled', True)
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO app_settings (key, value)
        VALUES ('reservation_enabled', ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value
    """, ('1' if enabled else '0',))
    conn.commit()
    conn.close()

    if enabled:
        send_notification_to_all(
            '✅ Reservations Now Open',
            'Lab reservations are now enabled. You can book your PC slot anytime!',
            'success'
        )
    else:
        send_notification_to_all(
            '🚫 Reservations Disabled',
            'Lab reservations have been temporarily disabled by the admin. Please check back later.',
            'warning'
        )

    return jsonify({'success': True, 'enabled': enabled})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))