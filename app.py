from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "super_secret_student_tracker"

# ─── MySQL Configuration ───────────────────────────────────────────────────────
app.config['MYSQL_HOST']     = 'localhost'       # Change to RDS endpoint on AWS
app.config['MYSQL_USER']     = 'root'            # Your MySQL username
app.config['MYSQL_PASSWORD'] = ''    # Your MySQL password
app.config['MYSQL_DB']       = 'studentdb'       # Database name
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'   # Returns rows as dicts
# ──────────────────────────────────────────────────────────────────────────────

mysql = MySQL(app)

@app.before_request
def init_db():
    if not getattr(app, 'db_initialized', False):
        try:
            cur = mysql.connection.cursor()
            # Create users table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL
                )
            ''')
            # Check for students table and user_id column
            cur.execute("SHOW TABLES LIKE 'students'")
            if not cur.fetchone():
                cur.execute('''
                    CREATE TABLE students (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        subject VARCHAR(100) NOT NULL,
                        grade INT NOT NULL,
                        user_id INT
                    )
                ''')
            else:
                cur.execute("SHOW COLUMNS FROM students LIKE 'user_id'")
                if not cur.fetchone():
                    cur.execute("ALTER TABLE students ADD COLUMN user_id INT")
            
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            print(f"Database initialization error: {e}")
        finally:
            app.db_initialized = True

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def get_stats(students):
    total = len(students)
    avg   = round(sum(s['grade'] for s in students) / total, 1) if total else 0
    passed = sum(1 for s in students if s['grade'] >= 40)
    return total, avg, passed, total - passed

@app.route("/")
@login_required
def index():
    user_id = session.get("user_id")
    username = session.get("username", "User")
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE user_id = %s ORDER BY id DESC", (user_id,))
    students = cur.fetchall()
    cur.close()
    
    total, avg, passed, failed = get_stats(students)
    return render_template("index.html",
                           students=students,
                           total=total, avg=avg,
                           passed=passed, failed=failed,
                           username=username)

@app.route("/add", methods=["POST"])
@login_required
def add_student():
    name    = request.form.get("name", "").strip()
    subject = request.form.get("subject", "").strip()
    grade   = request.form.get("grade", "").strip()
    user_id = session.get("user_id")
    
    if name and subject and grade:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO students (name, subject, grade, user_id) VALUES (%s, %s, %s, %s)",
            (name, subject, int(grade), user_id)
        )
        mysql.connection.commit()
        cur.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:student_id>")
@login_required
def delete_student(student_id):
    user_id = session.get("user_id")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id = %s AND user_id = %s", (student_id, user_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("index"))

@app.route("/edit/<int:student_id>", methods=["POST"])
@login_required
def edit_student(student_id):
    name    = request.form.get("name", "").strip()
    subject = request.form.get("subject", "").strip()
    grade   = request.form.get("grade", "").strip()
    user_id = session.get("user_id")
    
    if name and subject and grade:
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE students SET name=%s, subject=%s, grade=%s WHERE id=%s AND user_id=%s",
            (name, subject, int(grade), student_id, user_id)
        )
        mysql.connection.commit()
        cur.close()
    return redirect(url_for("index"))

@app.route("/api/students")
@login_required
def api_students():
    user_id = session.get("user_id")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE user_id = %s ORDER BY id DESC", (user_id,))
    students = cur.fetchall()
    cur.close()
    return jsonify(list(students))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if username and password:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cur.fetchone():
                flash("Username already exists", "error")
            else:
                hashed_pw = generate_password_hash(password)
                cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_pw))
                mysql.connection.commit()
                flash("Registration successful! Please log in.", "success")
                cur.close()
                return redirect(url_for("login"))
            cur.close()
        else:
            flash("Please fill out all fields", "error")
            
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if username and password:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()
            
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for("index"))
            else:
                flash("Invalid credentials", "error")
        else:
            flash("Please fill out all fields", "error")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
