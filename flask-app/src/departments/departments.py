from flask import Blueprint, request, jsonify, make_response
import json
from src import db


Department = Blueprint('Department', __name__)


# Get all departments from the DB
@Course.route('/Department', methods=['GET'])
def get_departments():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT Name FROM Department')
    row_headers = [x[0] for x in cursor.description]  
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))  
    the_response.mimetype = 'application/json'
    return the_response

#get details of a specific department
@Course.route('/Department/<int:DepartmentKey>', methods=['GET'])
def get_department_detail(DepartmentKey):
    query = 'SELECT DepartmentKey, Name, Chair FROM Department WHERE DepartmentKey = ' + str(DepartmentKey)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description] 
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    
    return jsonify(json_data)

#add new department
@Course.route('/Department', methods=['POST'])
def add_new_department():
    
    the_data = request.json
    current_app.logger.info(the_data)

    department_key = the_data['DepartmentKey']
    name = the_data['Name']
    chair = the_data['Chair']

    query = 'INSERT INTO Department (DepartmentKey, Name, Chair) VALUES ('
    query += f'"{department_key}", "{name}", "{chair}")'
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return jsonify({"message": "Department added successfully"})


# Update a specific department
@Course.route('/departments/<int:department_key>', methods=['PUT'])
def update_department(department_key):
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['name']
    chair = the_data['chair']

    query = "UPDATE Department SET "
    query += "Name = '" + name + "', "
    query += "Chair = '" + chair + "' "
    query += "WHERE DepartmentKey = " + str(department_key)

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Success'


# Remove a specific department
@Course.route('/departments/<int:department_key>', methods=['DELETE'])
def remove_department(department_key):
    query = 'DELETE FROM Department WHERE DepartmentKey = ' + str(department_key)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return jsonify({"message": "Department deleted successfully"})

# List all departments with the count of courses they offer
@Course.route('/departments/courses/count', methods=['GET'])
def list_departments_with_course_counts():
    query = '''
    SELECT d.DepartmentKey, d.Name, COUNT(c.CourseID) as CourseCount
    FROM Department d
    LEFT JOIN Course c ON d.DepartmentKey = c.DepartmentKey
    GROUP BY d.DepartmentKey
    ORDER BY CourseCount DESC;
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    
    return jsonify(json_data)

