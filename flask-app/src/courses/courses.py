from flask import Blueprint, request, jsonify, make_response
import json
from src import db


Course = Blueprint('Course', __name__)

# Get all courses from the DB
@Course.route('/Course', methods=['GET'])
def get_courses():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT CourseID, Name, Credit_Hours FROM Course')
    row_headers = [x[0] for x in cursor.description]  
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))  
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


#add new course
@Course.route('/course', methods=['POST'])
def add_new_course():
    
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['Name']
    credit_hours = the_data['Credit_Hours']
    description = the_data.get('Description', '')  
    pre_req = the_data.get('Pre_req', None)
    teacher_id = the_data['Teacher_ID']
    department_key = the_data['DepartmentKey']

    query = 'INSERT INTO Course (Name, Credit_Hours, Description, Pre_req, Teacher_ID, DepartmentKey) VALUES ('
    query += f'"{name}", {credit_hours}, "{description}", {pre_req if pre_req is not None else "NULL"}, {teacher_id}, {department_key})'
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return jsonify({"message": "Course added successfully"}), 201

#get details of a specific course
@Course.route('/courses/<int:course_id>', methods=['GET'])
def get_course_detail(course_id):
    query = 'SELECT CourseID, Name, Credit_Hours, Description, Pre_req, Teacher_ID, DepartmentKey FROM Course WHERE CourseID = ' + str(course_id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description] 
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    
    return jsonify(json_data)

#bulk update courses
@Course.route('/courses/bulk_update', methods=['PUT'])
def bulk_update_courses():
    updates = request.get_json()

    if not isinstance(updates, list):
        return jsonify({"error": "Request data should be a list of updates"}), 400

    cursor = db.get_db().cursor()

    for update in updates:
        course_id = update.get('CourseID')
        fields = {k: v for k, v in update.items() if k != 'CourseID' and v is not None}

        if fields:
            set_clause = ', '.join([f"{key} = %s" for key in fields.keys()])
            query = f"UPDATE Course SET {set_clause} WHERE CourseID = %s"
            current_app.logger.info(query)
            cursor.execute(query, list(fields.values()) + [course_id])

    # Commit all updates
    db.get_db().commit()
    return jsonify({"message": "Courses updated successfully"}), 200


#Update a specific course
@Course.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting the course details from the data
    name = the_data['name']
    credit_hours = the_data['credit_hours']
    description = the_data['description']
    pre_req = the_data.get('pre_req', None)  
    teacher_id = the_data['teacher_id']
    department_key = the_data['department_key']

    # Constructing the SQL update query
    query = "UPDATE Course SET "
    query += "name = '" + name + "', "
    query += "credit_hours = " + str(credit_hours) + ", "
    query += "description = '" + description + "', "
    query += "pre_req = " + (str(pre_req) if pre_req is not None else 'NULL') + ", "
    query += "teacher_id = " + str(teacher_id) + ", "
    query += "department_key = " + str(department_key) + " "
    query += "WHERE CourseID = " + str(course_id)

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Success'




#remove a specific course
@Course.route('/courses/<int:course_id>', methods=['DELETE'])
def remove_course(course_id):
    query = 'DELETE FROM Course WHERE CourseID = ' + str(course_id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query, (course_id,))
    db.get_db().commit()
    
    return jsonify({"message": "Course deleted successfully"}), 200