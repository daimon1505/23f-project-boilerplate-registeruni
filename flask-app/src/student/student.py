from flask import Blueprint, request, jsonify
from src import db

student = Blueprint('student', __name__)

@student.route('/students/<int:student_id>', methods=['GET'])
def get_student_info(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Students WHERE studentID = %s', (student_id,))
    row_headers = [x[0] for x in cursor.description]  
    json_data = []
    student_info = cursor.fetchone()  

    if student_info is not None:
        json_data.append(dict(zip(row_headers, student_info)))
        cursor.close()
        return jsonify(json_data), 200
    else:
        cursor.close()
        return jsonify({'message': 'Student not found'}), 404

@student.route('/students/<int:student_id>/plans', methods=['GET'])
def get_student_plans(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT planName, studentID, planID FROM Plan WHERE studentID = %s', (student_id,))
    row_headers = [x[0] for x in cursor.description]  
    json_data = []
    plans = cursor.fetchall()
    for plan in plans:
        json_data.append(dict(zip(row_headers, plan)))
    cursor.close()
    return jsonify(json_data), 200

@student.route('/students/<int:student_id>/plans', methods=['POST'])
def create_student_plan(student_id):
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO Plan (studentID, planName) VALUES (%s, %s )', (student_id, data['planName']))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Plan created"}), 201

@student.route('/students/<int:student_id>/course', methods=['GET'])
def get_student_courses(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT
        co.CourseID,
        co.Name,
        co.Description,
        co.Credit_Hours,
        CONCAT(te.FirstName, ' ', te.LastName) AS Instructor,
        de.Name as Department,
        SUM(es.Total_Enrollment) as Total_Enrollment,
        MAX(es.Maximum_Capacity) as Maximum_Capacity,
        MAX(es.Maximum_Capacity) - SUM(es.Total_Enrollment) AS AvailableSlots
    FROM 
        StudentsCourse sc
    INNER JOIN Course co ON sc.CourseID = co.CourseID
    INNER JOIN Teacher te ON co.Teacher_ID = te.TeacherId
    INNER JOIN Department de ON co.DepartmentKey = de.DepartmentKey
    INNER JOIN Enrollment_Status es ON co.CourseID = es.CourseID
    WHERE 
        sc.studentID = %s
    GROUP BY 
        co.CourseID,
        co.Name,
        co.Description,
        co.Credit_Hours,
        te.FirstName,
        te.LastName,
        de.Name
    ORDER BY
        co.Name
    ''', (student_id,))
    courses = cursor.fetchall()
    cursor.close()

    row_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(row_headers, course)) for course in courses]
    return jsonify(json_data), 200

@student.route('/students/<int:student_id>/completed_courses', methods=['GET'])
def get_completed_courses(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT 
            co.CourseID,
            co.Name,
            co.Description,
            co.Credit_Hours
        FROM 
            StudentsCourse sc
        INNER JOIN 
            Course co 
        ON 
            sc.CourseID = co.CourseID
        WHERE 
            sc.studentID = %s
        ORDER BY 
            co.CourseID
    ''', (student_id,))
    courses = cursor.fetchall()
    cursor.close()

    if not courses:
        return jsonify({"message": "No completed courses found for the student."}), 404

    row_headers = [x[0] for x in cursor.description]  
    json_data = [dict(zip(row_headers, course)) for course in courses]
    return jsonify(json_data), 200

@student.route('/students/<int:student_id>/courses/<int:course_id>', methods=['POST'])
def add_course_to_student_plan(student_id, course_id):
    cursor = db.get_db().cursor()

    try:
        cursor.execute(
            'INSERT INTO StudentsCourse (studentID, courseID) VALUES (%s, %s)',
            (student_id, course_id)
        )
        db.get_db().commit()
    except Exception as e:
        db.get_db().rollback()
        return jsonify({"message": "Course already taken"}), 400
    finally:
        cursor.close()

    return jsonify({"message": "Course added to student's plan successfully"}), 201


@student.route('/students/<int:student_id>/courses/<int:course_id>', methods=['DELETE'])
def delete_course_from_student(student_id, course_id):
    cursor = db.get_db().cursor()
    cursor.execute(
        'DELETE FROM StudentsCourse WHERE studentID = %s AND courseID = %s',
        (student_id, course_id)
    )
    db.get_db().commit()
    cursor.close()

    return jsonify({"message": "Course removed from student's plan successfully"}), 200



@student.route('/courses', methods=['GET'])
def get_all_courses():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT 
            Course.CourseID,
            Course.Name,
            Course.Credit_Hours,
            Course.Description,
            CONCAT(Teacher.FirstName, ' ', Teacher.LastName) AS Instructor,
            Department.Name AS DepartmentName
        FROM 
            Course
        INNER JOIN Teacher ON Course.Teacher_ID = Teacher.TeacherId
        INNER JOIN Department ON Course.DepartmentKey = Department.DepartmentKey;
    ''')
    row_headers = [x[0] for x in cursor.description] 
    json_data = []
    courses = cursor.fetchall()
    for course in courses:
        json_data.append(dict(zip(row_headers, course)))
    cursor.close()
    return jsonify(json_data), 200

@student.route('/students/<int:student_id>/plans/<int:plan_id>', methods=['PUT'])
def update_student_plan(student_id, plan_id):
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE Plan SET planName = %s WHERE studentID = %s AND planID = %s', (data['planName'], student_id, plan_id))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Plan updated"}), 200

@student.route('/students/<int:student_id>/plans/<int:plan_id>', methods=['DELETE'])
def delete_student_plan(student_id, plan_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Plan WHERE studentID = %s AND planID = %s', (student_id, plan_id))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Plan deleted"}), 200

@student.route('/students/<int:student_id>', methods=['GET'])
def get_student_academic_record(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM StudentAcademicRecord WHERE studentID = %s', (student_id,))
    row_headers = [x[0] for x in cursor.description]  
    json_data = []
    record = cursor.fetchall()
    for rec in record:
        json_data.append(dict(zip(row_headers, rec)))
    cursor.close()
    return jsonify(json_data), 200

@student.route('/students/<int:student_id>', methods=['PUT'])
def update_student_academic_record(student_id):
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE StudentAcademicRecord SET standing = %s, creditHours = %s WHERE studentID = %s', 
                   (data['standing'], data['creditHours'], student_id))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Academic record updated"}), 200

@student.route('/students/<int:student_id>/feedback', methods=['GET'])
def get_student_feedback(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Feedback WHERE studentID = %s', (student_id,))
    row_headers = [x[0] for x in cursor.description]  
    json_data = []
    feedbacks = cursor.fetchall()
    for feedback in feedbacks:
        json_data.append(dict(zip(row_headers, feedback)))
    cursor.close()
    return jsonify(json_data), 200

@student.route('/students/<int:student_id>/courses/<int:course_id>/feedback', methods=['POST'])
def submit_feedback(student_id, course_id):
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO Feedback (studentID, courseID, comments, rating) VALUES (%s, %s, %s, %s)', 
                   (student_id, course_id, data['comments'], data['rating']))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Feedback submitted"}), 201


@student.route('/students/<int:student_id>/degreeaudit', methods=['GET'])
def get_degree_audit_by_student(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM DegreeAudit WHERE studentID = %s', (student_id,))
    degree_audit = cursor.fetchone()  
    cursor.close()
    if degree_audit:
        return jsonify(degree_audit), 200
    else:
        return jsonify({"message": "Degree audit not found for the given student ID"}), 404

@student.route('/students', methods=['GET'])
def get_students():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT studentID, firstName, lastName, major FROM Students')
    students = cursor.fetchall()
    cursor.close()
    return jsonify([{'studentID': sid, 'firstName': fn, 'lastName': ln, 'major': m} for sid, fn, ln, m in students]), 200


@student.route('/students', methods=['POST'])
def add_student():
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO Students (firstName, lastName, major) VALUES (%s, %s, %s)', 
                   (data['firstName'], data['lastName'], data['major']))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Student added successfully"}), 201

@student.route('/students/<int:student_id>', methods=['PUT'])
def update_student_details(student_id):
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE Students SET firstName = %s, lastName = %s, major = %s WHERE studentID = %s', 
                   (data['firstName'], data['lastName'], data['major'], student_id))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Student details updated"}), 200

@student.route('/students/<int:student_id>', methods=['DELETE'])
def remove_student(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Students WHERE studentID = %s', (student_id,))
    db.get_db().commit()
    rows_deleted = cursor.rowcount
    cursor.close()
    if rows_deleted == 0:
        return jsonify({"message": "No student found with the provided ID"}), 404
    return jsonify({"message": "Student removed successfully"}), 200

@student.route('/courses/<int:course_id>/feedback/f', methods=['GET'])
def get_feedback_by_course(course_id):
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT f.feedbackID, f.comments, f.rating, f.studentID, f.courseID, c.Name as courseName
        FROM Feedback f
        JOIN Course c ON f.courseID = c.CourseID
        WHERE f.courseID = %s
    """, (course_id,))
    feedbacks = cursor.fetchall()  
    cursor.close()
    if feedbacks:
        feedback_list = [{'feedbackID': fb[0], 'comments': fb[1], 'rating': fb[2], 'studentID': fb[3], 'courseID': fb[4], 'courseName': fb[5]} for fb in feedbacks]
        return jsonify(feedback_list), 200
    else:
        return jsonify({"message": "Feedback not found for the given course ID"}), 404



@student.route('/students/major/<string:major>', methods=['GET'])
def get_students_by_major(major):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT studentID, firstName, lastName FROM Students WHERE major = %s', (major,))
    students = cursor.fetchall()
    cursor.close()
    return jsonify([{'studentID': sid, 'firstName': fn, 'lastName': ln} for sid, fn, ln in students]), 200

@student.route('/courses/<int:course_id>/average-rating', methods=['GET'])
def get_course_average_rating(course_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT AVG(rating) AS AverageRating
        FROM Feedback
        WHERE courseID = %s;
    ''', (course_id,))
    result = cursor.fetchone()
    cursor.close()

    if result and result[0] is not None:
        average_rating = float(result[0])
        return jsonify({'Course ID': course_id, 'Average Rating': average_rating}), 200
    else:
        return jsonify({'Course ID': course_id, 'message': 'No ratings found for this course'}), 404


