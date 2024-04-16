from flask import Blueprint, request, jsonify, make_response
from src import db

registrar = Blueprint('registrar', __name__)

# Error response function
def error_response(message, status_code):
    response = jsonify({'error': message})
    response.status_code = status_code
    return response

# List all registar
@registrar.route('/registrar', methods=['GET'])
def get_registrars():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT * FROM registrar')
        row_headers = [x[0] for x in cursor.description]
        json_data = []
        theData = cursor.fetchall()
        for row in theData:
            json_data.append(dict(zip(row_headers, row)))
        the_response = make_response(jsonify(json_data))
        the_response.status_code = 200
        the_response.mimetype = 'application/json'
        return the_response
    except Exception as e:
        return error_response(str(e), 500)

# Adding a registar
@registrar.route('/registrar', methods=['POST'])
def add_registrar():
    try:
        # Collecting data from the request object
        data = request.json

        # Extracting variables
        phone_num = data.get('PhoneNum')
        email = data.get('Email')
        first_name = data.get('FirstName')
        last_name = data.get('LastName')
        access_level = data.get('AccessLevel')

        # Constructing the query
        query = 'INSERT INTO Registrar (PhoneNum, Email, FirstName, LastName, AccessLevel) VALUES (?, ?, ?, ?, ?)'
        current_app.logger.info(query)

        # Executing and committing the insert statement
        cursor = db.get_db().cursor()
        cursor.execute(query, values)
        db.get_db().commit()

        return jsonify({'message': 'Registrar added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Updating registrar details
@registrar.route('/registrar/<int:registrar_id>', methods=['PUT'])
def update_registrar(registrar_id):
    try:
        # Collect data from the request object
        data = request.json

        # Extract updated details from the data
        updated_details = {}
        if 'PhoneNum' in data:
            updated_details['PhoneNum'] = data['PhoneNum']
        if 'Email' in data:
            updated_details['Email'] = data['Email']
        if 'FirstName' in data:
            updated_details['FirstName'] = data['FirstName']
        if 'LastName' in data:
            updated_details['LastName'] = data['LastName']
        if 'AccessLevel' in data:
            updated_details['AccessLevel'] = data['AccessLevel']

        # Construct the update query
        query = 'UPDATE Registrar SET '
        set_values = []
        for key, value in updated_details.items():
            set_values.append('{} = "{}"'.format(key, value))
        query += ', '.join(set_values)
        query += ' WHERE RegistarID = {}'.format(registrar_id)

        # Execute the update query
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()

        return jsonify({'message': 'Registrar details updated successfully for ID {}'.format(registrar_id)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get updated registrar details
@registrar.route('/registrar/<int:registrar_id>', methods=['GET'])
def get_registrar(registrar_id):
    try:
        # Construct the query to retrieve details of the specific registrar
        query = 'SELECT * FROM Registrar WHERE RegistarID = {}'.format(registrar_id)

        # Execute the query
        cursor = db.get_db().cursor()
        cursor.execute(query)

        # Fetch the result
        registrar = cursor.fetchone()

        # Check if registrar exists
        if registrar:
            # Convert result to dictionary for JSON response
            registrar_details = {
                'RegistarID': registrar[0],
                'PhoneNum': registrar[1],
                'Email': registrar[2],
                'FirstName': registrar[3],
                'LastName': registrar[4],
                'AccessLevel': registrar[5]
            }
            return jsonify(registrar_details), 200
        else:
            return jsonify({'error': 'Registrar with ID {} not found'.format(registrar_id)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@registrar.route('/registrar/<int:registrar_id>', methods=['DELETE'])
def remove_registrar(registrar_id):
    try:
        # Construct the delete query
        query = 'DELETE FROM Registrar WHERE RegistarID = {}'.format(registrar_id)

        # Execute the delete query
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()

        return jsonify({'message': 'Registrar with ID {} removed successfully'.format(registrar_id)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@registrar.route('/registrar/<int:registrar_id>/courses', methods=['GET'])
def list_courses_for_registrar(registrar_id):
    try:
        # Construct the query to retrieve courses managed by the specific registrar
        query = 'SELECT c.* FROM Course c INNER JOIN RegistrarCourseBridge rcb ON c.CourseID = rcb.CourseID WHERE rcb.RegistarID = {}'.format(registrar_id)

        # Execute the query
        cursor = db.get_db().cursor()
        cursor.execute(query)

        # Fetch the result
        courses = cursor.fetchall()

        # Check if courses exist
        if courses:
            # Convert result to list of dictionaries for JSON response
            courses_list = []
            for course in courses:
                course_details = {
                    'CourseID': course[0],
                    'Name': course[1],
                    'Credit_Hours': course[2],
                    'Description': course[3],
                    'Pre_req': course[4],
                    'Teacher_ID': course[5],
                    'DepartmentKey': course[6]
                    # Add more attributes as needed
                }
                courses_list.append(course_details)
            return jsonify(courses_list), 200
        else:
            return jsonify({'message': 'No courses managed by registrar with ID {}'.format(registrar_id)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update courses in specific registrar
@registrar.route('/registrar/<int:registrar_id>/courses', methods=['PUT'])
def update_courses_for_registrar(registrar_id):
    try:
        # Collect data from the request object
        data = request.json

        # Extract updated course details from the data
        updated_courses = data.get('courses', [])

        # Iterate over the updated courses and update them in the database
        for updated_course in updated_courses:
            course_id = updated_course.get('CourseID')
            new_description = updated_course.get('Description')

            # Construct the update query
            query = 'UPDATE Course SET Description = "{}" WHERE CourseID = {} AND Teacher_ID = {}'.format(new_description, course_id, registrar_id)

            # Execute the update query
            cursor = db.get_db().cursor()
            cursor.execute(query)
            db.get_db().commit()

        return jsonify({'message': 'Courses managed by registrar with ID {} updated successfully'.format(registrar_id)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500