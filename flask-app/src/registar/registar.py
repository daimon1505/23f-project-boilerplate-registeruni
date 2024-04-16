from flask import Blueprint, request, jsonify, make_response
from src import db

registrar = Blueprint('registrar', __name__)

# List all registrars
@registrar.route('/registrar', methods=['GET'])
def get_registrars():
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

# Add new registrar
@registrar.route('/registrar', methods=['POST'])
def add_registrar():
    # Implement logic to add a new registrar
    return jsonify({'message': 'Add new registrar'})

# Update registrar details
@registrar.route('/registrar/<int:registrar_id>', methods=['PUT'])
def update_registrar(registrar_id):
    # Implement logic to update registrar details
    return jsonify({'message': 'Update registrar details for registrar with ID {}'.format(registrar_id)})

# Get registrar detail
@registrar.route('/registrar/<int:registrar_id>', methods=['GET'])
def get_registrar(registrar_id):
    # Implement logic to get details of a specific registrar
    return jsonify({'message': 'Get details of registrar with ID {}'.format(registrar_id)})

# Remove a registrar
@registrar.route('/registrar/<int:registrar_id>', methods=['DELETE'])
def remove_registrar(registrar_id):
    # Implement logic to remove a registrar
    return jsonify({'message': 'Remove registrar with ID {}'.format(registrar_id)})

# List courses managed by a specific registrar
@registrar.route('/registrar/<int:registrar_id>/courses', methods=['GET'])
def list_courses_for_registrar(registrar_id):
    # Implement logic to list courses managed by a specific registrar
    return jsonify({'message': 'List courses managed by registrar with ID {}'.format(registrar_id)})

# Update courses managed by a specific registrar
@registrar.route('/registrar/<int:registrar_id>/courses', methods=['PUT'])
def update_courses_for_registrar(registrar_id):
    # Implement logic to update courses managed by a specific registrar
    return jsonify({'message': 'Update courses managed by registrar with ID {}'.format(registrar_id)})