from flask import Blueprint, jsonify, request
from app.openai_service import OpenAIService
import io
import requests

api_bp = Blueprint('api', __name__)
openai_service = OpenAIService()


@api_bp.route('/example', methods=['GET'])
def example_route():
    return jsonify({"message": "This is a test example route!"})


@api_bp.route('/generate-image', methods=['POST'])
def generate_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    keywords = request.form.get('prompt', '').split(',') if request.form.get('prompt') else None

    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Prepare the image for OpenAI
        image_bytes = openai_service.prepare_image_for_openai(image_file)
        
        # Process the image with OpenAI
        response = openai_service.process_image_with_openai(image=image_bytes, keywords=keywords)
        
        # Get the URL from the response
        image_url = response.data[0].url
        
        return jsonify({'image_url': image_url}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
