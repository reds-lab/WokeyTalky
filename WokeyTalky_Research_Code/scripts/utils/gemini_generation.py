import vertexai
import json
import time
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models

locations = ["us-central1", "us-west1", "us-west2", "us-west3", "us-west4", "us-east1", "us-east2"] 
def get_response_gemini(prompt, model_name):
    def get_response(text, location):
        try:
            # Initialize Vertex AI
            vertexai.init(project="", location=location)
            
            # Load the model
            gemini_pro_model = GenerativeModel(model_name)
            
            safety_settings = {
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            }
            
            # Query the model
            generation_config = {
                "max_output_tokens": 256,
                "temperature": 0,
                "top_p": 0.0,
            }
            
            model_response = gemini_pro_model.generate_content(text, safety_settings=safety_settings, generation_config=generation_config)
            return model_response.text
        except Exception as e:
            return e

    attempts = 0
    response_obtained = False
    dataline = None

    while attempts < 6 and not response_obtained:
        location = locations[attempts % len(locations)]  # Cycle through locations
        result = get_response(prompt, location)
        
        if isinstance(result, Exception):
            print(f"Attempt {attempts+1} failed in {location}: {result}. Retrying...")
            time.sleep(10)  # Wait for 10 seconds before retrying
        else:
            print("Prompt: " + prompt + " User: " + result)
            response_obtained = True
            dataline = {"prompt": prompt, "response": result, "category": "adv-bench"}
        
        attempts += 1

    if not response_obtained:
        print("All attempts failed. Appending no response.")
        dataline = {"prompt": prompt, "response": "#No response", "category": "adv-bench"}

    response = dataline["response"]
    print(response)
    return response