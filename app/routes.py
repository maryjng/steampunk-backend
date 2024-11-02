from flask import Blueprint, jsonify, request
from app.openai_service import OpenAIService
import io
import requests

api_bp = Blueprint('api', __name__)
openai_service = OpenAIService()


@api_bp.route('/example', methods=['GET'])
def example_route():
    return jsonify({"message": "This is an example route!"})


@api_bp.route('/generate-image', methods=['POST'])
def generate_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    keywords = request.form.get('prompt', '').split(',') if request.form.get('prompt') else None

    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Read the file content
        image_content = image_file.read()
        
        # Create a BytesIO object
        image_bytes = io.BytesIO(image_content)
        image_bytes.name = image_file.filename  # Some APIs need the filename
        
        # Process the image with Replicate
        image_url = openai_service.process_image_with_replicate(
            image=image_bytes, 
            keywords=keywords
        )
        
        # Verify we got a string URL back
        if not isinstance(image_url, str):
            raise Exception(f"Unexpected response type: {type(image_url)}")
        
        return jsonify({
            'success': True,
            'image_url': image_url
        }), 200
    
    except Exception as e:
        print(f"Error in generate_image: {type(e)} - {str(e)}")  # Detailed error logging
        return jsonify({'error': str(e)}), 500
