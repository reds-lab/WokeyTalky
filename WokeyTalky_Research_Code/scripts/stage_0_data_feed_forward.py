import os
from dotenv import load_dotenv
# Load environment variables and set up configurations
load_dotenv()
os.environ["HF_HUB_CACHE"] = os.path.join(os.environ["HF_HOME"], 'hub')
os.environ["HF_ASSETS_CACHE"] = os.path.join(os.environ["HF_HOME"], 'assets')
os.environ['HF_TOKEN'] = os.getenv('HUGGINGFACE_TOKEN')
import json
import time
import torch
import gc

from tqdm import tqdm
from vllm import SamplingParams
import argparse
from utils.prompt_util import find_prompt_template
from utils.models_util import load_model_and_tokenizer
from utils.config_util import load_api_models, load_local_models_dict_json
from utils.file_util import find_file_processor
from utils.claude_generation import get_response_claude
from utils.gemini_generation import get_response_gemini
from utils.gpt_generation import get_response_gpt



api_models_list = load_api_models()
local_model_dict = load_local_models_dict_json()

def save_response(model_id, prompt, response, output_dir):
    model_name = model_id.split("/")[-1]
    answer_file = os.path.join(output_dir, f"{model_name}_generated_output.json")
    os.makedirs(os.path.dirname(answer_file), exist_ok=True)
    
    ans_json = {
        "raw_prompt": prompt,
        "model_id": model_id,
        "generated": response,
        "tstamp": time.time(),
    }
    
    with open(os.path.expanduser(answer_file), "a") as fout:
        fout.write(json.dumps(ans_json, ensure_ascii=False) + "\n")

def load_existing_prompts(answer_file):
    existing_prompts = set()
    if os.path.exists(os.path.expanduser(answer_file)):
        with open(os.path.expanduser(answer_file), "r") as fin:
            for line in fin:
                ans_json = json.loads(line)
                existing_prompts.add(ans_json["raw_prompt"])
    return existing_prompts

def generate_api_response(prompt, model_id):
    if "claude" in model_id:
        return get_response_claude(prompt, model_id)
    elif "gpt" in model_id:
        return get_response_gpt(prompt, model_id)
    elif "gemini" in model_id:
        return get_response_gemini(prompt, model_id)
    else:
        raise ValueError(f"Unsupported API model: {model_id}")

def generate_vllm_responses(model_id, prompts):
    vllm_model, tokenizer = load_model_and_tokenizer(model_id=model_id)
    dialogs = find_prompt_template(prompts, model_id, tokenizer)
    
    sampling_params = SamplingParams(temperature=0, max_tokens=256)
    vllm_outputs = vllm_model.generate(dialogs, sampling_params)
    
    responses = [output.outputs[0].text.strip() for output in vllm_outputs]
    
    del vllm_model
    del tokenizer
    torch.cuda.empty_cache()
    gc.collect()
    
    return responses

def generate_outputs(model_id, data_file, output_dir):
    data_processor = find_file_processor(data_file)
    prompts = data_processor(data_file)
    
    model_name = model_id.split("/")[-1]
    answer_file = os.path.join(output_dir, f"{model_name}_generated_output.json")
    os.makedirs(os.path.dirname(answer_file), exist_ok=True)
    
    existing_prompts = load_existing_prompts(answer_file)
    prompts = [prompt for prompt in prompts if prompt not in existing_prompts]
    
    if model_id.lower().strip() in api_models_list:
        print(f"API Model: {model_id}")
        for prompt in tqdm(prompts):
            while True:
                try:
                    response = generate_api_response(prompt, model_id)
                    save_response(model_id, prompt, response, output_dir)
                    break
                except Exception as e:
                    print(f"Error occurred: {str(e)}")
                    print("Waiting for 30 seconds before retrying...")
                    time.sleep(30)
    else:
        print(f"vLLM Model: {model_id}")
        responses = generate_vllm_responses(model_id, prompts)
        
        for prompt, response in zip(prompts, responses):
            save_response(model_id, prompt, response, output_dir)
    
    print(f"Complete {model_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate outputs for a given model using the specified data file")
    parser.add_argument("--model-name", type=str, required=True, help="the model name to generate outputs for")
    parser.add_argument("--data-file", type=str, default="", help="path to the input data file")
    parser.add_argument("--output-dir", type=str, default="", help="directory to save the output files")
 
    args = parser.parse_args()
    
    print(f"Model name: {args.model_name}")
    generate_outputs(args.model_name, args.data_file, args.output_dir)