from flask import Blueprint, request, jsonify
from src import db

registrar_bp = Blueprint('registrar', __name__)

# List all registrars in database

@registrar_bp.route('/registrar', methods=['GET'])
def get_registrars():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Registrar')
    row_headers = [x[0] for x in cursor.description]  # Extract the row headers
    json_data = []
    registrars = cursor.fetchall()
    for result in registrars:
        json_data.append(dict(zip(row_headers, result)))
    cursor.close()
    return jsonify(json_data), 200

# Add registrar to database
@registrar_bp.route('/registrar', methods=['POST'])
def add_registrar():
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute(
        'INSERT INTO Registrar (PhoneNum, Email, FirstName, LastName, AccessLevel) VALUES (%s, %s, %s, %s, %s)',
        (data['PhoneNum'], data['Email'], data['FirstName'], data['LastName'], data['AccessLevel'])
    )
    db.get_db().commit()
    cursor.close()
    return jsonify({'message': 'Registrar added successfully'}), 201

# Update a specific registrar's information
@registrar_bp.route('/registrar/<int:registrar_id>', methods=['PUT'])
def update_registrar(registrar_id):
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute(
        'UPDATE Registrar SET PhoneNum = %s, Email = %s, FirstName = %s, LastName = %s, AccessLevel = %s WHERE RegistarID = %s',
        (data['PhoneNum'], data['Email'], data['FirstName'], data['LastName'], data['AccessLevel'], registrar_id)
    )
    db.get_db().commit()
    cursor.close()
    return jsonify({'message': 'Registrar updated successfully'}), 200

# List specific registrar
@registrar_bp.route('/registrar/<int:registrar_id>', methods=['GET'])
def get_registrar(registrar_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Registrar WHERE RegistarID = %s', (registrar_id,))
    row_headers = [x[0] for x in cursor.description]  # Extract the row headers
    json_data = []
    registrar = cursor.fetchone()
    if registrar:
        json_data.append(dict(zip(row_headers, registrar)))
    cursor.close()
    return jsonify(json_data), 200 if registrar else ('', 404)

# Delete registrar from database
@registrar_bp.route('/registrar/<int:registrar_id>', methods=['DELETE'])
def delete_registrar(registrar_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Registrar WHERE RegistarID = %s', (registrar_id,))
    db.get_db().commit()
    cursor.close()
    return jsonify({'message': 'Registrar deleted successfully'}), 200

# List courses in a registrar
@registrar_bp.route('/registrar/<int:registrar_id>/courses', methods=['GET'])
def get_registrar_courses(registrar_id):
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT Course.* FROM Course INNER JOIN RegistrarCourseBridge ON Course.CourseID = RegistrarCourseBridge.CourseID WHERE RegistrarCourseBridge.RegistarID = %s',
        (registrar_id,)
    )
    row_headers = [x[0] for x in cursor.description]  # Extract the row headers
    json_data = []
    courses = cursor.fetchall()
    for course in courses:
        json_data.append(dict(zip(row_headers, course)))
    cursor.close()
    return jsonify(json_data), 200

# Update courses in a registrar
@registrar_bp.route('/registrar/<int:registrar_id>/courses', methods=['PUT'])
def update_registrar_courses(registrar_id):
    data = request.json
    cursor = db.get_db().cursor()
    for course in data:
        cursor.execute(
            'UPDATE Course SET Name = %s, Credit_Hours = %s, Description = %s WHERE CourseID = %s AND EXISTS (SELECT 1 FROM RegistrarCourseBridge WHERE RegistrarCourseBridge.CourseID = Course.CourseID AND RegistrarCourseBridge.RegistarID = %s)',
            (course['Name'], course['Credit_Hours'], course['Description'], course['CourseID'], registrar_id)
        )
    db.get_db().commit()
    cursor.close()
    return jsonify({'message': 'Courses updated successfully'}), 200