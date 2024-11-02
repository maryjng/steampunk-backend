from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__)

@api_bp.route('/example', methods=['GET'])
def example_route():
    return jsonify({"message": "This is an example route!"})

@api_bp.route('/modify-image', methods=['POST'])
def modify_image():
    data = request.json
    # Implement your image modification logic here
    return jsonify({"message": "Image modified!"})

# More routes can be added here
