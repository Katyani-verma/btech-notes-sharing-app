import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Upload folder setup inside static
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Home / Dashboard
@app.route('/')
def home():
    return render_template('dashboard.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'student')
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Email already registered! Please login instead.')
            cursor.close()
            db.close()
            return redirect(url_for('register'))
            
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", 
            (name, email, password, role)
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('login'))
        
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = user['role']
            return redirect(url_for('notes'))
        else:
            flash('Invalid Email or Password!')
            
    return render_template('login.html')

# Upload Route
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        year = request.form['year']
        subject_id = request.form['subject_id']
        file = request.files['file']
        user_id = session.get('user_id', 1)
        
        if file and file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            cursor.execute("""
                INSERT INTO notes (title, description, year, file_name, subject_id, uploaded_by) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (title, description, year, file.filename, subject_id, user_id))
            db.commit()
            cursor.close()
            db.close()
            return redirect(url_for('notes'))

    cursor.execute("SELECT * FROM subjects")
    subjects_list = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('upload.html', subjects=subjects_list)

# View Notes Route (Notes tabhi aayenge jab Year aur Subject filter kiya gaya ho)
@app.route('/notes')
def notes():
    selected_year = request.args.get('year')
    selected_subject = request.args.get('subject_id')
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM subjects")
    subjects_list = cursor.fetchall()

    notes_list = []
    if selected_year or selected_subject:
        query = """
            SELECT notes.*, subjects.subject_name 
            FROM notes 
            LEFT JOIN subjects ON notes.subject_id = subjects.id 
            WHERE 1=1
        """
        params = []

        if selected_year:
            query += " AND notes.year = %s"
            params.append(selected_year)
        if selected_subject:
            query += " AND notes.subject_id = %s"
            params.append(selected_subject)

        cursor.execute(query, tuple(params))
        notes_list = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template(
        'notes.html', 
        notes=notes_list, 
        subjects=subjects_list,
        selected_year=selected_year,
        selected_subject=selected_subject
    )

# Delete Note Route
@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT file_name FROM notes WHERE id = %s", (note_id,))
    note = cursor.fetchone()
    
    if note:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], note['file_name'])
        if os.path.exists(file_path):
            os.remove(file_path)
            
        cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
        db.commit()
    
    cursor.close()
    db.close()
    return redirect(url_for('notes'))

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)