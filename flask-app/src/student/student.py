from flask import Blueprint, request, jsonify
from src import db

student = Blueprint('student', __name__)

@student.route('/students/<int:student_id>/plans', methods=['GET'])
def get_student_plans(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Plan WHERE studentID = %s', (student_id,))
    row_headers = [x[0] for x in cursor.description]  # Extract the row headers
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
    cursor.execute('INSERT INTO Plan (studentID, planName) VALUES (%s, %s)', (student_id, data['planName']))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Plan created"}), 201

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
    row_headers = [x[0] for x in cursor.description]  # Extract the row headers
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
    row_headers = [x[0] for x in cursor.description]  # Extract the row headers
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
