import replicate
import requests
import io
from PIL import Image
from .config import Config

class OpenAIService:
    def __init__(self):
        self.replicate_api_key = Config.REPLICATE_API_KEY
        
    def process_image_with_replicate(self, image, keywords):
        prompt = self.generate_prompt(keywords)
        
        try:
            # Initialize replicate client
            client = replicate.Client(api_token=self.replicate_api_key)
            
            # Run the model
            output = client.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "image": image,
                    "prompt": prompt,
                    "num_outputs": 1,
                    "guidance_scale": 7.5,
                    "prompt_strength": 0.8,
                }
            )
            
            # Convert the output to a list if it isn't already
            if not isinstance(output, list):
                output = list(output)
            
            # Get the first URL from the output
            for item in output:
                if isinstance(item, str) and item.startswith('http'):
                    return item
                    
            raise Exception("No valid image URL found in the response")
            
        except Exception as e:
            print(f"Replicate API error: {str(e)}")
            raise e

    def generate_prompt(self, keywords):
        # OpenAI's max token limit is approximately 4000 characters for image edits
        MAX_PROMPT_LENGTH = 1000  # Using a conservative limit

        base_prompt = """Transform into dark industrial steampunk architecture. 
        Replace natural elements with dark industrial material like cobblestone. 
        Make the sky darker with haze and pollution.
        Add massive turning gears, steam-belching pipes, and industrial machinery. 
        Make it dystopian with soot-stained metal and copper oxidation."""

        if keywords:
            keywords_str = ', '.join(keywords)
            full_prompt = f"Transform into dark steampunk architecture with: {keywords_str}. {base_prompt}"
            
            # If prompt is too long, truncate keywords while keeping base prompt
            if len(full_prompt) > MAX_PROMPT_LENGTH:
                available_length = MAX_PROMPT_LENGTH - len(base_prompt) - len("Transform into dark steampunk architecture with: . ")
                truncated_keywords = keywords_str[:available_length - 3] + "..."
                return f"Transform into dark steampunk architecture with: {truncated_keywords}. {base_prompt}"
            
            return full_prompt
        
        return base_prompt

    def prepare_image_for_replicate(self, image_file):
        try:
            # Read the image file and convert it to RGBA
            image = Image.open(image_file).convert("RGBA")
            
            # Create a BytesIO object
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            
            return image_bytes
            
        except Exception as e:
            raise Exception(f"Error preparing image: {str(e)}")
    