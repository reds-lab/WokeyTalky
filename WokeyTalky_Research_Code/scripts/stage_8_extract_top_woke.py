# %%
import json
import os
import re
from collections import defaultdict
from utils.config_util import load_models_dict_json
from utils.eval_util import extract_and_convert
import argparse
import random
# %%
models_dict = load_models_dict_json()
models = list(models_dict.keys())



def main(input_dir,input_dir_2, output_dir, dataset,):
    models_dict = load_models_dict_json()
    models = list(models_dict.keys())

    with open(f"{input_dir}/batch_raw_outputs.jsonl", "r") as f:
        raw_judge_results = [json.loads(line) for line in f]

    prompt_scores = defaultdict(list)

    for result in raw_judge_results:
        custom_id = result['custom_id']
        models_unclean = custom_id.split('_')
        model_x = models_unclean[3]
        model_y = models_unclean[0]
        model_number = int(models_unclean[1])
        if models_unclean[4] != "None":
            model_number2 = int(models_unclean[4])
        else:
            model_number2 = 0
        score = extract_and_convert(result['response']['body']['choices'][0]['message']['content'])

        folder_path = f"{input_dir_2}/{model_y}_generated_output.json"

        with open(folder_path, "r") as jsonl_file:
            for line_number, line in enumerate(jsonl_file):
                if line_number == model_number:
                    print(f'Line: {line_number}')
                    print(f'generating model: {model_y}_{model_number}')
                    print(f"generating model: {model_x}_{model_number2}")
                    print(line)
                    data = json.loads(line)
                    prompt = data["raw_prompt"]
                    break
            else:
                print(f"Model number {model_number} is out of range for {model_x}")
                continue

        prompt_scores[prompt].append({
            'generating_model': f"{model_y}_{model_number}",
            'woke_model': f"{model_x}_{model_number2}",
            'score': score,
            'generated': data['generated']
        })
    all_results = []
    results = []
    woke_prompts = []
    woke_prompts_10_per = []

    # Sort the prompts based on the number of rejections in descending order
    sorted_prompts = sorted(prompt_scores.items(), key=lambda x: sum(item['score'] == 0 for item in x[1]), reverse=True)

    # Calculate the number of prompts in the top 10%
    top_10_percent_count = 63 #int(len(sorted_prompts) * 0.10)
    top_25_count = 25 #int(len(sorted_prompts) * 0.10)
    # Extract the top 10% of the prompts
    woke_prompts_10_per = [prompt for prompt, _ in sorted_prompts[:top_10_percent_count]]
    woke_prompts_25 = [prompt for prompt, _ in sorted_prompts[:top_25_count]]
    for prompt, scores in prompt_scores.items():
        zero_score_count = sum(item['score'] == 0 for item in scores)
        result = {
                'prompt': prompt,
                'dataset': dataset,
                'models': scores,
                'num_models': len(scores),
                'num_rejections': zero_score_count
            }
        all_results.append(result)
        if zero_score_count >= 10:
            results.append(result)
            
    all_results.sort(key=lambda x: x['num_rejections'], reverse=True)
    num_samples = 10
    sampled_results = random.sample(all_results, num_samples)
    results.sort(key=lambda x: x['num_rejections'], reverse=True)
    sampled_results_from_25 = random.sample(all_results[:25], num_samples)
    woke_prompts = [result["prompt"] for result in results ]
    print(len(results))

    with open(f"{output_dir}/top_woke_results_more_than_10_rejs.json", "w") as file:
        json.dump(results, file, indent=2)
    with open(f"{output_dir}/top_woke_prompts_more_than_10_rejs.json", "w") as file:
        json.dump(woke_prompts, file, indent=2)
    with open(f"{output_dir}/top_woke_prompts_10_percent.json", "w") as file:
        json.dump(woke_prompts_10_per, file, indent=2)
    with open(f"{output_dir}/top_woke_prompts_25.json", "w") as file:
        json.dump(woke_prompts_25, file, indent=2)
    with open(f"{output_dir}/top_woke_prompts_10_random_all.json", "w") as file:
        json.dump(sampled_results, file, indent=2)
    with open(f"{output_dir}/top_woke_prompts_10_random_top_25.json", "w") as file:
        json.dump(sampled_results_from_25, file, indent=2)
    with open(f"{output_dir}/all_woke_prompts.json", "w") as file:
        json.dump(all_results, file, indent=2)
    print(f"{output_dir}/top_woke_results.json saved")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process batch raw outputs and generate results.')
    parser.add_argument('--input_dir', type=str, required=True,
                        help='Path to the batch raw outputs file')
    parser.add_argument('--output_dir', type=str, required=True,
                        help='Path to the output file')
    parser.add_argument('--dataset', type=str, required=True,
                        help='Path to the output file')
    parser.add_argument('--input_dir_2', type=str, required=True,
                        help='Path to the output file')

    args = parser.parse_args()
    if len(args.input_dir_2) == 0:
        raise ValueError("bad input")
    main(args.input_dir,args.input_dir_2, args.output_dir,args.dataset)

