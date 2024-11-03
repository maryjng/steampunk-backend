import os
import requests
import openai
import base64
import io
from PIL import Image, ImageDraw, ImageEnhance
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
            # Open and convert image to RGBA
            img = Image.open(image).convert('RGBA')
            
            # First convert to grayscale as a base
            grayscale = img.convert('L')
            
            # Create a gray-tinted effect
            width, height = grayscale.size
            gray = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            
            # Define the gray tones (more pronounced gray)
            highlight = (200, 200, 205, 255)  # Darker light gray
            midtone = (150, 150, 155, 255)    # More pronounced medium gray
            shadow = (100, 100, 105, 255)      # Darker shadow gray
            
            # Apply the toning effect
            pixels = grayscale.load()
            gray_pixels = gray.load()
            
            for x in range(width):
                for y in range(height):
                    pixel_value = pixels[x, y]
                    if pixel_value > 170:
                        gray_pixels[x, y] = highlight
                    elif pixel_value > 85:
                        gray_pixels[x, y] = midtone
                    else:
                        gray_pixels[x, y] = shadow
            
            # Blend with original image
            img = Image.blend(img, gray, 0.85)  # Increased blend for stronger gray effect
            
            # Adjust contrast and brightness
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.15)  # Slightly reduced contrast
            
            brightness = ImageEnhance.Brightness(img)
            img = brightness.enhance(0.95)  # Less darkening
            
            # Resize to 1024x1024
            img = img.resize((1024, 1024))
            
            # Convert to PNG bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Generate mask
            mask = self.generate_mask(size=(1024, 1024))
            
            print(f"Sending prompt: {prompt}")
            
            response = client.images.edit(
                image=img_bytes,
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
        base_prompt = """Transform into Victorian steampunk while preserving architecture:
        1. Keep elegant building shapes, add metal/brass/copper materials
        2. Add clockworks, gears, steam pipes along architectural lines
        3. Dark polluted sky, brown cobblestone ground
        4. Aged industrial materials but maintain Victorian elegance"""

        if keywords:
            keywords_str = ', '.join(keywords)
            full_prompt = f"{base_prompt} Additional elements: {keywords_str}"
            
            if len(full_prompt) > 1000:
                available_length = 1000 - len(base_prompt) - len(" Additional elements: ")
                truncated_keywords = keywords_str[:available_length - 3] + "..."
                return f"{base_prompt} Additional elements: {truncated_keywords}"
            
            return full_prompt
        
        return base_prompt
        
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
        Generate a mask image with a white border and center.
        
        Args:
            size (tuple): Width and height of the mask (default: 1024x1024)
            border_width (int): Width of the white border in pixels (default: 100)
        
        Returns:
            BytesIO: Mask image as bytes object
        """
        # Create new white image (everything modifiable)
        mask = Image.new('RGBA', size, (255, 255, 255, 255))
        draw = ImageDraw.Draw(mask)
        
        # Draw black rectangle for the area we want to protect (original composition)
        inner_box = [(border_width, border_width), 
                    (size[0]-border_width-1, size[1]-border_width-1)]
        draw.rectangle(inner_box, fill=(0, 0, 0, 0))
        
        # Debug: Save a copy of the mask
        mask.save('debug_mask.png')
        
        # Convert to bytes
        mask_bytes = io.BytesIO()
        mask.save(mask_bytes, format='PNG')
        mask_bytes.seek(0)
        
        return mask_bytes
    