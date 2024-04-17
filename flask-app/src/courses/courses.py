from flask import Blueprint, request, jsonify, make_response, current_app
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
    
    return jsonify({"message": "Course added successfully"})

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
        return jsonify({"error": "Request data should be a list of updates"})

    cursor = db.get_db().cursor()

    for update in updates:
        course_id = update.get('CourseID')
        fields = {k: v for k, v in update.items() if k != 'CourseID' and v is not None}

        if fields:
            set_clause = ', '.join([f"{key} = %s" for key in fields.keys()])
            query = f"UPDATE Course SET {set_clause} WHERE CourseID = %s"
            current_app.logger.info(query)
            cursor.execute(query, list(fields.values()) + [course_id])

    db.get_db().commit()
    return jsonify({"message": "Courses updated successfully"})


#Update a specific course
@Course.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['name']
    credit_hours = the_data['credit_hours']
    description = the_data['description']
    pre_req = the_data.get('pre_req', None)  
    teacher_id = the_data['teacher_id']
    department_key = the_data['department_key']

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
    
    return jsonify({"message": "Course deleted successfully"})

#return all academic policies
@Course.route('/academic_policies', methods=['GET'])
def list_academic_policies():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT PolicyID, CourseID, Title, Description, EffectiveDate FROM Academic_Policies')
    policies = cursor.fetchall()
    cursor.close()

    if not policies:
        return jsonify([])

    column_headers = [x[0] for x in cursor.description]
    policies_list = [dict(zip(column_headers, policy)) for policy in policies]

    return jsonify(policies_list)

#return academic policy given specific courseID
@Course.route('/courses/<int:course_id>/academic_policies', methods=['GET'])
def get_academic_policies_for_course(course_id):
    cursor = db.get_db().cursor()
    query = 'SELECT PolicyID, CourseID, Title, Description, EffectiveDate FROM Academic_Policies WHERE CourseID = %s'
    cursor.execute(query, (course_id,))
    policies = cursor.fetchall()
    cursor.close()

    if not policies:
        return jsonify({"message": "No academic policies found for the given course ID"}), 404

    column_headers = [x[0] for x in cursor.description]
    policies_list = [dict(zip(column_headers, policy)) for policy in policies]

    return jsonify(policies_list)

#Add new acadmic policy
@Course.route('/academic_policies', methods=['POST'])
def add_academic_policy():
    policy_data = request.json
    course_id = policy_data['CourseID']
    title = policy_data['Title']
    description = policy_data['Description']
    effective_date = policy_data['EffectiveDate']
    
    query = '''
    INSERT INTO Academic_Policies (CourseID, Title, Description, EffectiveDate)
    VALUES (%s, %s, %s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (course_id, title, description, effective_date))
    db.get_db().commit()
    
    return jsonify({"message": "Academic policy added successfully"})

@Course.route('/academic_policies/<int:policy_id>', methods=['PUT'])
def update_academic_policy(policy_id):
    the_data = request.json
    current_app.logger.info(the_data)

    course_id = the_data['CourseID']
    title = the_data['Title']
    description = the_data['Description']
    effective_date = the_data['EffectiveDate']

    query = "UPDATE Academic_Policies SET "
    query += "CourseID = '" + str(course_id) + "', "
    query += "Title = '" + title + "', "
    query += "Description = '" + description + "', "
    query += "EffectiveDate = '" + effective_date + "' "
    query += "WHERE PolicyID = " + str(policy_id)

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return jsonify({"message": "Academic policy updated successfully"})

# Get enrollment status for a specific course
@Course.route('/courses/<int:course_id>/enrollment_status', methods=['GET'])
def get_enrollment_status(course_id):
    query = '''
    SELECT Total_Enrollment, Maximum_Capacity, Waitlist_Total 
    FROM Enrollment_Status 
    WHERE CourseID = {}
    '''.format(course_id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description] 
    json_data = []
    the_data = cursor.fetchall()
    if the_data:
        for row in the_data:
            json_data.append(dict(zip(column_headers, row)))
        return jsonify(json_data)
    else:
        return jsonify({"message": "No enrollment status found for this course"})

# Add enrollment status to a specific course
@Course.route('/courses/<int:course_id>/enrollment_status', methods=['POST'])
def add_enrollment_status(course_id):
    the_data = request.json
    total_enrollment = the_data['total_enrollment']
    maximum_capacity = the_data['maximum_capacity']
    waitlist_total = the_data['waitlist_total']

    query = '''
    INSERT INTO Enrollment_Status (Total_Enrollment, Maximum_Capacity, Waitlist_Total, CourseID) 
    VALUES (%s, %s, %s, %s)
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query, (total_enrollment, maximum_capacity, waitlist_total, course_id))
    db.get_db().commit()

    return 'success'

# Update enrollment status for a specific course
@Course.route('/courses/<int:course_id>/enrollment_status', methods=['PUT'])
def update_enrollment_status(course_id):
    the_data = request.json
    total_enrollment = the_data['total_enrollment']
    maximum_capacity = the_data['maximum_capacity']
    waitlist_total = the_data['waitlist_total']

    if total_enrollment > maximum_capacity:
        return jsonify({"error": "Total enrollment cannot exceed maximum capacity"}), 400

    query = '''
    UPDATE Enrollment_Status
    SET Total_Enrollment = %s, Maximum_Capacity = %s, Waitlist_Total = %s
    WHERE CourseID = %s
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query, (total_enrollment, maximum_capacity, waitlist_total, course_id))
    db.get_db().commit()

    return 'success'
