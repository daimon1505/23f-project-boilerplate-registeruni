from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


Teacher = Blueprint('Teacher', __name__)

# Get all teachers from the DB
@Teacher.route('/Teacher', methods=['GET'])
def get_teachers():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT FirstName, LastName, Email, TeacherId, DepartmentKey FROM Teacher')
    row_headers = [x[0] for x in cursor.description]  
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))  
    the_response.mimetype = 'application/json'
    return the_response

# Add a new teacher
@Teacher.route('/teachers', methods=['POST'])
def add_teacher():
    the_data = request.json
    current_app.logger.info(the_data)

    first_name = the_data['FirstName']
    last_name = the_data['LastName']
    email = the_data['Email']
    department_key = the_data['DepartmentKey']

    query = 'INSERT INTO Teacher (FirstName, LastName, Email, DepartmentKey) VALUES ("'
    query += first_name + '", "'
    query += last_name + '", "'
    query += email + '", '
    query += str(department_key) + ')'
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Success!'

# Get courses taught by a specific teacher
@Teacher.route('/teachers/<int:teacher_id>/courses', methods=['GET'])
def get_courses_by_teacher(teacher_id):
    query = 'SELECT c.CourseID, c.Name, c.Description FROM Course c WHERE c.Teacher_ID = {}'.format(teacher_id)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))

    the_response = make_response(jsonify(json_data))
    the_response.mimetype = 'application/json'
    return the_response


# Remove a specific teacher
@Teacher.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def remove_teacher(teacher_id):
    query = 'DELETE FROM Teacher WHERE TeacherId = ' + str(teacher_id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    if cursor.rowcount == 0:
        return jsonify({"message": "No teacher found with the provided ID"}), 404

    return jsonify({"message": "Teacher removed successfully"})

# List all teachers in a specific department
@Teacher.route('/departments/<int:department_key>/teachers', methods=['GET'])
def get_teachers_by_department(department_key):
    query = '''
    SELECT t.TeacherId, t.FirstName, t.LastName, t.Email
    FROM Teacher t
    WHERE t.DepartmentKey = {}
    '''.format(department_key)
    current_app.logger.info(query)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(row_headers, row)))
    
    return jsonify(json_data)


# Update a specific teacher's details
@Teacher.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    the_data = request.json
    current_app.logger.info(the_data)

    first_name = the_data['FirstName']
    last_name = the_data['LastName']
    email = the_data['Email']
    department_key = the_data['DepartmentKey']

    query = "UPDATE Teacher SET "
    query += "FirstName = '" + first_name + "', "
    query += "LastName = '" + last_name + "', "
    query += "Email = '" + email + "', "
    query += "DepartmentKey = " + str(department_key) + " "
    query += "WHERE TeacherId = " + str(teacher_id)

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Success'
