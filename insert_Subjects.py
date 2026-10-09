from config import get_db_connection

subjects_data = [
    # ---------------- 1st Year (Semester 1 & 2) ----------------
    ('Engineering Mathematics - I', 1),
    ('Engineering Mathematics - II', 1),
    ('Engineering Physics', 1),
    ('Engineering Chemistry', 1),
    ('Programming for Problem Solving (PPS - C)', 1),
    ('Basic Electrical Engineering', 1),
    ('Emerging Technology for Engineering', 1),
    ('Fundamentals of Mechanical Engg & Mechatronics', 1),
    ('Environment & Ecology', 1),
    ('Soft Skills', 1),

    # ---------------- 2nd Year (Semester 3 & 4) ----------------
    ('Mathematics-IV (PDE, Probability & Statistics)', 2),
    ('Data Structures (DS)', 2),
    ('Computer Organization and Architecture (COA)', 2),
    ('Discrete Structures & Theory of Logic (DSTL)', 2),
    ('Technical Communication', 2),
    ('Universal Human Values (UHV)', 2),
    ('Operating Systems (OS)', 2),
    ('Theory of Automata and Formal Languages (TAFL)', 2),
    ('Object Oriented Programming with Java / C++', 2),
    ('Cyber Security', 2),
    ('Python Programming', 2),

    # ---------------- 3rd Year (Semester 5 & 6) ----------------
    ('Database Management System (DBMS)', 3),
    ('Design and Analysis of Algorithm (DAA)', 3),
    ('Compiler Design', 3),
    ('Artificial Intelligence (AI)', 3),
    ('Web Designing', 3),
    ('Object Oriented System Design', 3),
    ('Data Analytics', 3),
    ('Mathematical Foundation of AI & Data Science', 3),
    ('Data Warehousing & Data Mining', 3),
    ('Cloud Computing', 3),
    ('Natural Language Processing (NLP)', 3),
    ('Soft Computing', 3),
    ('Digital Image Processing', 3),
    ('Constitution of India', 3),
    ('Essence of Indian Traditional Knowledge', 3),
    ('Software Engineering', 3),
    ('Computer Networks', 3),
    ('Web Technology', 3),
    ('Machine Learning Techniques', 3),
    ('Image Analytics', 3),
    ('Cyber Forensic Analytics', 3),
    ('Big Data', 3),
    ('Deep Learning Foundations', 3),
    ('Open Elective - I', 3)
]

try:
    db = get_db_connection()
    cursor = db.cursor()
    
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("TRUNCATE TABLE subjects;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    
    for item in subjects_data:
        cursor.execute(
            "INSERT INTO subjects (subject_name, semester) VALUES (%s, %s)", 
            item
        )
        
    db.commit()
    print("Database Updated: All AKTU Subjects Seeded Successfully!")
    cursor.close()
    db.close()
except Exception as e:
    print("Error:", e)