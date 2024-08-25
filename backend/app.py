from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome to the BFHL API"

@app.route('/bfhl', methods=['POST'])
def process_data():
    app.logger.info(f"Received POST request with data: {request.json}")
    try:
        data = request.json.get('data', [])

        if not isinstance(data, list):
            return jsonify({"is_success": False, "message": "Invalid input: data must be an array"}), 400

        numbers = [item for item in data if isinstance(item, str) and item.isdigit()]
        alphabets = [item for item in data if isinstance(item, str) and item.isalpha()]
        lowercase_alphabets = [item for item in alphabets if item.islower()]
        highest_lowercase_alphabet = max(lowercase_alphabets) if lowercase_alphabets else None

        response = {
            "is_success": True,
            "user_id": os.getenv('USER_ID'),
            "email": os.getenv('EMAIL'),
            "roll_number": os.getenv('ROLL_NUMBER'),
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_lowercase_alphabet": [highest_lowercase_alphabet] if highest_lowercase_alphabet else []
        }

        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({"is_success": False, "message": "Server error"}), 500

@app.route('/bfhl', methods=['GET'])
def get_operation_code():
    app.logger.info("Received GET request")
    return jsonify({"operation_code": 1})

if __name__ == '__main__':
    app.run(debug=True)
