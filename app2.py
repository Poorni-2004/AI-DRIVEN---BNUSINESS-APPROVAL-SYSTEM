from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost",
    user="YOUR USER NAME",
    password="YOUR PASSWORD",
    database="business_portal"
)
cursor = db.cursor()

@app.route('/api/submit_application', methods=['POST'])
def submit_application():
    data = request.json
    query = """
        INSERT INTO applications 
        (approval_type, business_name, business_type, business_address, tax_id, registration_number, business_description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['approval_type'],
        data['business_name'],
        data['business_type'],
        data['business_address'],
        data['tax_id'],
        data['registration_number'],
        data['business_description']
    )
    cursor.execute(query, values)
    db.commit()
    return jsonify({"message": "Application submitted successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
