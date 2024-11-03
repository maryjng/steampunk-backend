from flask import Blueprint, jsonify, request
from app.openai_service import OpenAIService
from PIL import Image
import io
import base64

api_bp = Blueprint('api', __name__)
openai_service = OpenAIService()

@api_bp.route('/generate-image', methods=['POST'])
def generate_image():
    # Parse JSON request body
    data = request.get_json()

    # Check for the 'image' field in JSON payload
    if 'image' not in data:
        return jsonify({'error': 'No image provided in request'}), 400

    try:
        # Decode base64 image data
        image_data = data['image']
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        # Optional: extract keywords if provided
        keywords = data.get('prompt', '').split(',') if 'prompt' in data else None

        # Prepare the image for OpenAI
        image_bytes_for_openai = openai_service.prepare_image_for_openai(image)

        # Process the image with OpenAI
        response = openai_service.process_image_with_openai(image=image_bytes_for_openai, keywords=keywords)

        # Get the URL from the OpenAI response (assumes response.data[0].url structure)
        image_url = response.data[0].url if response and response.data else None

        return jsonify({'image_url': image_url}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
