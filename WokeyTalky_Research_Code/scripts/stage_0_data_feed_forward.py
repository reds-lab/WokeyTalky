import gc
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# load_hugging_config()
# Set the default cache directory for Hugging Face models and datasets.
# please keep 0 away in this list as somehow it does not support muti-gpu
os.environ["HF_HUB_CACHE"] = os.path.join(os.environ["HF_HOME"], 'hub')
os.environ["HF_ASSETS_CACHE"] = os.path.join(os.environ["HF_HOME"], 'assets')

os.environ['HF_TOKEN'] = os.getenv('HUGGINGFACE_TOKEN')

import argparse
from utils.prompt_util import apply_prompt_template, find_prompt_template, questions_prompt_template
import time
import torch
from tqdm import tqdm
import json
from utils.models_util import load_model_and_tokenizer
from utils.config_util import load_models_dict_json,load_api_models,load_local_models_dict_json
from utils.file_util import find_file_processor
from vllm import LLM, SamplingParams
from utils.claude_generation import get_response_claude
from utils.gemini_generation import get_response_gemini
from utils.gpt_generation import get_response_gpt
model_dict = load_models_dict_json()
api_models_list = load_api_models()
local_model_dict = load_local_models_dict_json()


def save_response(model_name, model_id, prompt, response, output_dir):
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

def generate_outputs(model_name, data_file, output_dir):
    
    data_processor = find_file_processor(data_file)
    prompts = data_processor(data_file)

    answer_file = os.path.join(output_dir, f"{model_name}_generated_output.json")
    os.makedirs(os.path.dirname(answer_file), exist_ok=True)

    existing_prompts = set()

    # Load existing prompts from the file if it exists
    if os.path.exists(os.path.expanduser(answer_file)):
        with open(os.path.expanduser(answer_file), "r") as fin:
            for line in fin:
                ans_json = json.loads(line)
                existing_prompts.add(ans_json["raw_prompt"])

    # Filter new prompts based on existing prompts
    prompts = [prompt for prompt in prompts if prompt not in existing_prompts]
    

    responses = []
    model_name = model_name.lower().strip()
    model_id = model_name
    if model_name in model_dict.keys() or model_name in local_model_dict.keys():
        model_id = model_dict.get(model_name) or local_model_dict.get(model_name)

        vllm_model, tokenizer = load_model_and_tokenizer(model_id=model_id)

        dialogs = find_prompt_template(prompts, model_name, tokenizer)
    
        if 'llama-3' in model_name:
            sampling_params = SamplingParams(temperature=0, max_tokens=256, stop_token_ids=[
                                            tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|eot_id|>")])
        else:
            sampling_params = SamplingParams(temperature=0, max_tokens=256)

        vllm_outputs = vllm_model.generate(dialogs, sampling_params)
        

        

        responses = [output.outputs[0].text.strip() for output in vllm_outputs]
        del vllm_model
        del tokenizer
        torch.cuda.empty_cache()
        gc.collect()
    elif model_name in api_models_list:
        print(f"API Model: {model_name}")
        for prompt in tqdm(prompts):
            while True:
                try:
                    if "claude" in model_name:
                        response = get_response_claude(prompt, model_name)
                    elif "gpt" in model_name:
                        response = get_response_gpt(prompt, model_name)
                    elif "gemini" in model_name:
                        response = get_response_gemini(prompt, model_name)
                    
                    responses.append(response)
                    save_response(model_name, model_id, prompt, response, output_dir)
                    break
                except Exception as e:
                    print(f"Error occurred: {str(e)}")
                    print("Waiting for 30 seconds before retrying...")
                    time.sleep(30)
        
        return
    else:
        raise ValueError("Model Name not supported/included")
    
    answer_file = os.path.join(output_dir, f"{model_name}_generated_output.json")
    os.makedirs(os.path.dirname(answer_file), exist_ok=True)
    with open(os.path.expanduser(answer_file), "a") as fout:
        for idx, response in enumerate(responses):
            ans_json = {
                "raw_prompt": prompts[idx],
                "model_id": model_id,
                "generated": response,
                "tstamp": time.time(),
            }
            fout.write(json.dumps(ans_json, ensure_ascii=False) + "\n")
    print(f"Complete {model_name}")
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate outputs for a given model using the specified data file")
    parser.add_argument(
        "--model-name",
        type=str,
        required=True,
        help="the model name to generate outputs for",
    )

    parser.add_argument(
        "--data-file",
        type=str,
        default="/home/yizeng/Research/0_Overkill_Bench/Phase_4.5_ModelsPlus/0_outputs/wokey_data/wokey_data.json",
        help="path to the input data file (default: /home/yizeng/Research/0_Overkill_Bench/Phase_4.5_ModelsPlus/0_outputs/wokey_data/wokey_data.json)",
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./0_outputs/more_woke_model_900_outputs",
        help="directory to save the output files (default: ./0_outputs/more_woke_model_900_outputs)",
    )
 
    args = parser.parse_args()
    
    print(f"Model name: {args.model_name}")
    generate_outputs(args.model_name, args.data_file, args.output_dir)