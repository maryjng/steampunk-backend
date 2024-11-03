from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        return response

    # Example route to test the CORS settings
    @app.route('/upload_screenshot', methods=['POST'])
    def upload_screenshot():
        # Sample response to simulate upload success
        return jsonify({"message": "Screenshot received"}), 200

    return app
