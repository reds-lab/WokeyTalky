# %%
import vertexai
import json
import time
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models

def get_response(text, location):
    try:
        # Initialize Vertex AI
        vertexai.init(project="", location=location)
        # Load the model
        gemini_pro_model = GenerativeModel("gemini-1.5-pro-preview-0409")
        
        safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
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
        return e  # Return exception to handle it outside

test_data = []

# Open the file and read each line
with open("/home/yizeng/Research/0_Rigor_LLM/LLamaGuard/data/sorrybench/question.jsonl", 'r') as file:
    for line in file:
        # Convert line from JSON format to dictionary
        json_object = json.loads(line.strip())
        test_data.append(json_object)

# %%
responses = []
locations = ["us-central1", "us-west1", "us-west2", "us-west3", "us-west4", "us-east1", "us-east2"]  # List of locations to try

for row in test_data:
    attempts = 0
    response_obtained = False
    while attempts < 6 and not response_obtained:
        location = locations[attempts % len(locations)]  # Cycle through locations
        result = get_response(row['turns'][0], location)
        
        if isinstance(result, Exception):
            print(f"Attempt {attempts+1} failed in {location}: {result}. Retrying...")
            time.sleep(10)  # Wait for 10 seconds before retrying
        else:
            print("Prompt: " + row['turns'][0] + " User: " + result)
            response_obtained = True
            dataline = {"prompt": row['turns'][0], "response": result, "category": row['category']}
            responses.append(dataline)
        
        attempts += 1
    
    if not response_obtained:
        print("All attempts failed. Appending no response.")
        dataline = {"prompt": row['turns'][0], "response": "#No response", "category": row['category']}
        responses.append(dataline)


# %%
# Save the responses to a file
with open('./result/gemini_sorrybench_responses.json', 'w') as f:
    json.dump(responses, f, indent=4)
