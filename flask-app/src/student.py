from flask import Blueprint, request, jsonify
from src import db

student_bp = Blueprint('student', __name__)


@student_bp.route('/students/<int:student_id>/plans', methods=['GET'])
def get_student_plans(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Plan WHERE studentID = %s', (student_id,))
    plans = cursor.fetchall()
    cursor.close()
    return jsonify(plans), 200

@student_bp.route('/students/<int:student_id>/plans', methods=['POST'])
def create_student_plan(student_id):
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO Plan (studentID, planName) VALUES (%s, %s)', (student_id, data['planName']))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Plan created"}), 201

@student_bp.route('/students/<int:student_id>/plans/<int:plan_id>', methods=['PUT'])
def update_student_plan(student_id, plan_id):
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE Plan SET planName = %s WHERE studentID = %s AND planID = %s', (data['planName'], student_id, plan_id))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Plan updated"}), 200

@student_bp.route('/students/<int:student_id>/plans/<int:plan_id>', methods=['DELETE'])
def delete_student_plan(student_id, plan_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Plan WHERE studentID = %s AND planID = %s', (student_id, plan_id))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Plan deleted"}), 200

@student_bp.route('/students/<int:student_id>', methods=['GET'])
def get_student_academic_record(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM StudentAcademicRecord WHERE studentID = %s', (student_id,))
    record = cursor.fetchall()
    cursor.close()
    return jsonify(record), 200


@student_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student_academic_record(student_id):
    data = request.json
    cursor = db.get_db().cursor()
    # Example of updating the academic standing and credit hours
    cursor.execute('UPDATE StudentAcademicRecord SET standing = %s, creditHours = %s WHERE studentID = %s', 
                   (data['standing'], data['creditHours'], student_id))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Academic record updated"}), 200


@student_bp.route('/students/<int:student_id>/feedback', methods=['GET'])
def get_student_feedback(student_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Feedback WHERE studentID = %s', (student_id,))
    feedback = cursor.fetchall()
    cursor.close()
    return jsonify(feedback), 200

@student_bp.route('/students/<int:student_id>/courses/<int:course_id>/feedback', methods=['POST'])
def submit_feedback(student_id, course_id):
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO Feedback (studentID, courseID, comments, rating) VALUES (%s, %s, %s, %s)', 
                   (student_id, course_id, data['comments'], data['rating']))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Feedback submitted"}), 201
