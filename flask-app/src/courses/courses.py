from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


Course = Blueprint('Course', __name__)

# Get all courses from the DB
@Course.route('/Course', methods=['GET'])
def get_courses():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Course')
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

    name = the_data['Name']
    credit_hours = the_data['Credit_Hours']
    description = the_data['Description']
    pre_req = the_data.get('Pre_req', None)  
    teacher_id = the_data['Teacher_ID']
    department_key = the_data['DepartmentKey']

    query = "UPDATE Course SET "
    query += "Name = '" + name + "', "
    query += "Credit_Hours = " + str(credit_hours) + ", "
    query += "Description = '" + description + "', "
    query += "Pre_req = " + (str(pre_req) if pre_req is not None else 'NULL') + ", "
    query += "Teacher_ID = " + str(teacher_id) + ", "
    query += "DepartmentKey = " + str(department_key) + " "
    query += "WHERE CourseID = " + str(course_id)

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Success'




#remove a specific course
@Course.route('/courses/<int:course_id>', methods=['DELETE'])
def remove_course(course_id):
    query = 'DELETE FROM Course WHERE CourseID = %s'
    current_app.logger.info("Attempting to delete course with CourseID: %s", course_id)

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

# Delete an academic policy
@Course.route('/academic_policies/<int:policy_id>', methods=['DELETE'])
def delete_academic_policy(policy_id):
    query = 'DELETE FROM Academic_Policies WHERE PolicyID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (policy_id,))
    db.get_db().commit()
    
    if cursor.rowcount == 0:
        return jsonify({"error": "No policy found with the given ID"}), 404

    return jsonify({"message": "Academic policy deleted successfully"})

    
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


# Get top 10 courses by total enrollment
@Course.route('/courses/top-enrollment', methods=['GET'])
def get_top_courses_by_enrollment():
    query = '''
    SELECT Course.CourseID, Course.Name, Enrollment_Status.Total_Enrollment
    FROM Course
    JOIN Enrollment_Status ON Course.CourseID = Enrollment_Status.CourseID
    ORDER BY Enrollment_Status.Total_Enrollment DESC
    LIMIT 10;
    '''
    current_app.logger.info("Fetching top 10 courses by total enrollment")

    cursor = db.get_db().cursor()
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]  # Extract the row headers
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))

    return jsonify(json_data)




# Get courses with the highest enrollment broken down by student majors
@Course.route('/courses/enrollment-by-major', methods=['GET'])
def get_enrollment_by_major():
    query = '''
    SELECT Students.major, Course.CourseID, Course.Name, COUNT(Students.studentID) AS EnrolledStudents
    FROM Students
    JOIN StudentsCourse ON Students.studentID = StudentsCourse.studentID
    JOIN Course ON StudentsCourse.courseID = Course.CourseID
    GROUP BY Students.major, Course.CourseID, Course.Name
    ORDER BY EnrolledStudents DESC;
    '''
    current_app.logger.info("Fetching courses with highest enrollment by major")

    cursor = db.get_db().cursor()
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]  # Extract the row headers
    json_data = []
    results = cursor.fetchall()
    for row in results:
        json_data.append(dict(zip(row_headers, row)))

    return jsonify(json_data)
