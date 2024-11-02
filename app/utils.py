import requests
from PIL import Image


def save_image(image):
    image = request.files['image'] # Get the image from the request
    filename = secure_filename(image.filename) # Sanitize the filename
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # Define the path to save
    image.save(image_path) # Save the image