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
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ['HF_TOKEN'] = os.getenv('HUGGINGFACE_TOKEN')

import argparse
from utils.prompt_util import apply_prompt_template, find_prompt_template, questions_prompt_template
import csv
import time
from vllm import LLM, SamplingParams
import json
import torch
from utils.models_util import load_model_and_tokenizer
from utils.config_util import load_models_dict_json
model_dict = load_models_dict_json()
from utils.file_util import find_file_processor
from utils.config_util import load_models_dict_json,load_api_models,load_local_models_dict_json
local_model_dict = load_local_models_dict_json()
def generate_outputs(model_name, input_dir, output_dir,data_file):
    
    model_name = str.lower(model_name)
    model_id = model_dict.get(model_name) or local_model_dict.get(model_name)
    print(f"here: {data_file}")
    dialogs =[]
    if data_file:
        print(f"here: {data_file}")
        data_processor = find_file_processor(data_file)
        print(data_processor)
        prompts = data_processor(data_file)
    else:
        with open(f'{input_dir}/woke_batch_processed.json') as file:
            batch = json.load(file)

        prompts = [object['woke_data'] for object in batch]
    vllm_model, tokenizer = load_model_and_tokenizer(model_id=model_id)
    
    
    
    dialogs = find_prompt_template(prompts, model_name, tokenizer)

    sampling_params = SamplingParams(temperature=0, max_tokens=256)

    vllm_outputs = vllm_model.generate(dialogs, sampling_params)

    answer_file = f'{output_dir}/{model_name}_generated_output.json'
    os.makedirs(os.path.dirname(answer_file), exist_ok=True)

    if data_file:
        with open(os.path.expanduser(answer_file), "w") as fout:
            for idx, vllm_output in enumerate(vllm_outputs):
                turns = [output.text.strip() for output in vllm_output.outputs]
                ans_json = {
                    "raw_prompt": prompts[idx],
                    "model_id": model_name,
                    "generated": turns[0],
                }             
                fout.write(json.dumps(ans_json, ensure_ascii=False) + "\n")
    else:
        with open(os.path.expanduser(answer_file), "w") as fout:
            for idx, vllm_output in enumerate(vllm_outputs):
                turns = [output.text.strip() for output in vllm_output.outputs]
                ans_json = {
                    "raw_prompt": prompts[idx],
                    "woke_id": batch[idx]['woke_idx'],
                    "woke_model": batch[idx]['woke_model'],
                    "model_id": model_name,
                    "generated": turns[0],
                    "tstamp": time.time(),
                }
                fout.write(json.dumps(ans_json, ensure_ascii=False) + "\n")

    del vllm_model
    del tokenizer
    torch.cuda.empty_cache()
    gc.collect()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate outputs for a given model using the specified data file")
    parser.add_argument("--model-name", type=str, required=True,
                        help="the model name to generate outputs for")
    parser.add_argument("--input_dir", type=str, default="/home/yizeng/Research/0_Overkill_Bench/Phase_4.5_ModelsPlus/0_outputs/wokey_data/wokey_data.json",
                        help="path to the input data file (default: /home/yizeng/Research/0_Overkill_Bench/Phase_4.5_ModelsPlus/0_outputs/wokey_data/wokey_data.json)")
    parser.add_argument("--output_dir", type=str, default="./0_outputs/more_woke_model_900_outputs",
                        help="directory to save the output files (default: ./0_outputs/more_woke_model_900_outputs)")
    parser.add_argument("--data_file", type=str, default="./0_outputs/more_woke_model_900_outputs",
                        help="directory to save the output files (default: ./0_outputs/more_woke_model_900_outputs)")
    args = parser.parse_args()

    print(f"Model name: {args.model_name}")
    generate_outputs(args.model_name, args.input_dir, args.output_dir,args.data_file)
