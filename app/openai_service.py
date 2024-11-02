import os
import requests
import openai
import base64
import io
from PIL import Image, ImageDraw
from .config import Config

client = openai.OpenAI(api_key=Config.OPENAI_SECRET_KEY)

class OpenAIService:
    def __init__(self):
        # self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def process_image_with_openai(self, image, keywords):
        prompt = self.generate_prompt(keywords)
        
        try:
            # Get the image size from the input image
            img = Image.open(image)
            img_size = img.size  # This will be (1200, 1200)
            image.seek(0)  # Reset file pointer after reading
            
            # Generate mask with matching size
            mask = self.generate_mask(size=img_size)

            response = client.images.edit(
                image=image,
                mask=mask,
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            
            return response
            
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            raise e

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}
    

    def generate_prompt(self, keywords):
        base_modifications = [
            "transform this image into steampunk style",
            "add brass and copper metallic elements",
            "incorporate vintage Victorian industrial aesthetics",
            "include gears, pipes, and steam machinery",
            "maintain the original composition but add steampunk overlays",
            "add weathered metal textures",
            "include steam-powered mechanical modifications"
        ]
        
        if keywords:
            keywords_str = ', '.join(keywords)
            prompt = f"Transform this image into steampunk style by adding: {keywords_str}. {' '.join(base_modifications)}. Make sure to blend the steampunk elements seamlessly with the original image. The modifications should look realistic and integrated, not like stickers or overlays. Maintain the quality and clarity of the original image while adding these steampunk elements."
        else:
            prompt = f"Please {' and '.join(base_modifications)}. The modifications should look realistic and integrated, not like stickers or overlays. Maintain the quality and clarity of the original image while adding these steampunk elements."
        
        return prompt
    
    def blobify_image_from_url(self, image_url):
        response = requests.get(image_url)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode('utf-8')
        else:
            return None
        
    def prepare_image_for_openai(self, image_file):
        try:
            # Read the image file and convert it to RGBA
            image = Image.open(image_file).convert("RGBA")
            
            # Ensure the image is square
            width, height = image.size
            if width != height:
                new_size = min(width, height)
                left = (width - new_size) // 2
                top = (height - new_size) // 2
                image = image.crop((left, top, left + new_size, top + new_size))
            
            # Create a BytesIO object
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            
            return image_bytes
            
        except Exception as e:
            raise Exception(f"Error preparing image: {str(e)}")

    def generate_mask(self, size=(1024, 1024), border_width=100):
        """
        Generate a mask image with a transparent center and white border.
        
        Args:
            size (tuple): Width and height of the mask (default: 1024x1024)
            border_width (int): Width of the white border in pixels (default: 100)
        
        Returns:
            BytesIO: Mask image as bytes object
        """
        # Create new transparent image
        mask = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(mask)
        
        # Draw white border
        draw.rectangle([(0, 0), (size[0]-1, size[1]-1)], 
                      fill=(255, 255, 255, 255))
        # Draw transparent center
        draw.rectangle([(border_width, border_width), 
                       (size[0]-border_width-1, size[1]-border_width-1)], 
                      fill=(0, 0, 0, 0))
        
        # Convert to bytes
        mask_bytes = io.BytesIO()
        mask.save(mask_bytes, format='PNG')
        mask_bytes.seek(0)
            
        return mask_bytes
    


