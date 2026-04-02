from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "secret123"

# ==========================================
# 📧 EMAIL FUNCTIONS
# ==========================================

# 1. Welcome Email (Only for the Registered User)
def send_welcome_email(user_email, user_name):
    try:
        sender_email = "vinothini14005@gmail.com"
        app_password = "kxruplrnhdymuuce" 

        subject = "Welcome to Course Hub! 🚀"
        body = f"Hi {user_name},\n\nThank you for registering with us! Your account has been successfully created. You can now login and explore our courses.\n\nBest Regards,\nCourse Hub Team"

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = user_email  # User kudutha email address-ku mattum pogum

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Welcome mail sent to User: {user_email}")
    except Exception as e:
        print("❌ WELCOME MAIL ERROR:", e)

# 2. Course Booking Email (Only for the User who reserved)
def send_booking_email(user_email, course_data, mode):
    try:
        sender_email = "vinothini14005@gmail.com"
        app_password = "kxruplrnhdymuuce" 

        subject = "Course Reservation Confirmation 🎓"
        body = f"""
Hi,

We are pleased to confirm your reservation for the following course:

Course Name: {course_data['title']}
Start Date: May 1
Timing: {course_data['timing']}
Mode: {mode.capitalize()}

Thank you for choosing us!
"""
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = user_email # User-oda email-ku mattum pogum

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Booking mail sent to User: {user_email}")
    except Exception as e:
        print("❌ BOOKING MAIL ERROR:", e)

# ==========================================
# 🗄️ DATABASE SETUP
# ==========================================

def init_db():
    conn = sqlite3.connect("database.db")
    # Users Table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)
    # Reservations Table (with mode column)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS reservations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        course TEXT,
        mode TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# 🚀 ROUTES
# ==========================================

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form.get('email') # User register panna use pannum email
        password = request.form.get('password')

        conn = get_db()
        conn.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)", (name, email, password))
        conn.commit()
        conn.close()

        # IMPORTANT: User-ku mattum dhaan mail pogum
        send_welcome_email(email, name)

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def check_login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password)).fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['user_email'] = user['email']
        return redirect(url_for('course_mode'))
    return "Invalid Login ❌"

@app.route('/courses')
def course_mode():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('course_mode.html')

@app.route('/courses/<mode>')
def course_list(mode):
    if 'user_id' not in session: return redirect(url_for('login'))
    session['selected_mode'] = mode
    courses = [
        {"name": "python", "title": "Python Programming"},
        {"name": "ai", "title": "Artificial Intelligence"},
        {"name": "ds", "title": "Data Science"},
        {"name": "ml", "title": "Machine Learning"}
    ]
    return render_template('course_list.html', courses=courses, mode=mode)

@app.route('/course/<name>', methods=['GET', 'POST'])
def course_detail(name):
    if 'user_id' not in session: return redirect(url_for('login'))

    courses_data = {
        "python": {"title": "Python Programming", "duration": "3 Months", "fees": "₹5000", "timing": "6PM - 8PM", "advantages": ["Easy to learn", "High demand"]},
        "ai": {"title": "Artificial Intelligence", "duration": "6 Months", "fees": "₹8000", "timing": "5PM - 7PM", "advantages": ["Future tech", "High salary"]},
        "ds": {"title": "Data Science", "duration": "5 Months", "fees": "₹7000", "timing": "7PM - 9PM", "advantages": ["Data analysis", "Trending"]},
        "ml": {"title": "Machine Learning", "duration": "4 Months", "fees": "₹6000", "timing": "6PM - 7PM", "advantages": ["AI skills", "Automation"]}
    }

    course = courses_data.get(name)
    if request.method == 'POST':
        mode = session.get('selected_mode', 'Online')
        user_email = session.get('user_email') # Logged-in user email

        conn = get_db()
        conn.execute("INSERT INTO reservations(user_id, course, mode) VALUES(?,?,?)", (session['user_id'], course['title'], mode))
        conn.commit()
        conn.close()

        # IMPORTANT: User-ku mattum booking confirmation pogum
        send_booking_email(user_email, course, mode)

        return redirect(url_for('payment'))
    return render_template('course_detail.html', course=course)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST': return redirect(url_for('success'))
    return render_template('payment.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)