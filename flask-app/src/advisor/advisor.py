from flask import Blueprint, request, jsonify
from src import db

advisor_bp = Blueprint('advisor', __name__)

# List all advisors
@advisor_bp.route('/advisors', methods=['GET'])
def get_advisors():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Advisor')
    row_headers = [x[0] for x in cursor.description] 
    json_data = []
    advisors = cursor.fetchall()
    for advisor in advisors:
        json_data.append(dict(zip(row_headers, advisor)))
    cursor.close()
    return jsonify(json_data), 200

# Add advisor
@advisor_bp.route('/advisors', methods=['POST'])
def add_advisor():
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO Advisor (FirstName, LastName, DepartmentKey, Colleagues) VALUES (%s, %s, %s, %s)', 
                   (data['FirstName'], data['LastName'], data['DepartmentKey'], data['Colleagues']))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Advisor added successfully"}), 201

# Get specific advisor
@advisor_bp.route('/advisors/<int:advisor_id>', methods=['GET'])
def get_advisor(advisor_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Advisor WHERE Advisor_ID = %s', (advisor_id,))
    row_headers = [x[0] for x in cursor.description]  
    json_data = []
    advisor = cursor.fetchone()
    if advisor:
        json_data.append(dict(zip(row_headers, advisor)))
    cursor.close()
    return jsonify(json_data), 200 if advisor else ('', 404)

# Update advisor information
@advisor_bp.route('/advisors/<int:advisor_id>', methods=['PUT'])
def update_advisor(advisor_id):
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE Advisor SET FirstName = %s, LastName = %s, DepartmentKey = %s, Colleagues = %s WHERE Advisor_ID = %s', 
                   (data['FirstName'], data['LastName'], data['DepartmentKey'], data['Colleagues'], advisor_id))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Advisor details updated successfully"}), 200

# Create new degree audit
@advisor_bp.route('/advisors/<int:advisor_id>/degreeaudit', methods=['POST'])
def create_degree_audit(advisor_id):
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO DegreeAudit (startTerm, gradTerm, status, advisorID) VALUES (%s, %s, %s, %s)', 
                   (data['startTerm'], data['gradTerm'], data['status'], advisor_id))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Degree audit created successfully"}), 201

# Update degree audit
@advisor_bp.route('/advisors/<int:advisor_id>/degreeaudit/<int:audit_id>', methods=['PUT'])
def update_degree_audit(advisor_id, audit_id):
    data = request.json
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE DegreeAudit SET startTerm = %s, gradTerm = %s, status = %s WHERE auditID = %s AND advisorID = %s', 
                   (data['startTerm'], data['gradTerm'], data['status'], audit_id, advisor_id))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Degree audit updated successfully"}), 200

# Delete advisor
@advisor_bp.route('/advisors/<int:advisor_id>', methods=['DELETE'])
def delete_advisor(advisor_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Advisor WHERE Advisor_ID = %s', (advisor_id,))
    db.get_db().commit()
    cursor.close()
    return jsonify({"message": "Advisor deleted successfully"}), 200

