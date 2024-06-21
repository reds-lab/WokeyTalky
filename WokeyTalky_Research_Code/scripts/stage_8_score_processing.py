import os
import json
import argparse
from dotenv import load_dotenv
from utils.util import setup_env
from utils.eval_util import extract_and_convert




def main(input_dir, output_dir):

    filename = f'{input_dir}/batch_raw_outputs.jsonl'
    with open(filename, 'r') as f:
        all_results = [json.loads(line) for line in f]

    score_data = {}
    failed_num = 0
    failed_cases = []

    for result in all_results:
        custom_id_arr = result['custom_id'].split('_')
        base_name = custom_id_arr[0]
        idx = custom_id_arr[1]

        if base_name not in score_data:
            score_data[base_name] = []

        content = result['response']['body']['choices'][0]['message']['content']
        score = extract_and_convert(content)

        if score is not None:
            score_data[base_name].append({
                'index': idx,
                'score': score
            })
        else:
            failed_num += 1
            failed_cases.append(result)

    print("Number of failed cases:", failed_num)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save each model's data to a separate file
    for model_name, model_data in score_data.items():
        file_path = f"{output_dir}/{model_name}_judge_scores.json"
        with open(file_path, "w") as json_file:
            json.dump(model_data, json_file, indent=4)
        print(f"Model {model_name} data stored as JSON file: {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process model scores from zephyr_raw_generation.jsonl')
    parser.add_argument('--input_dir', type=str, default='./OAI_Batch_Requests/CompletedFIle',
                        help='Input directory containing the raw output batch')
    parser.add_argument('--output_dir', type=str, default='./0_outputs/model_scores',
                        help='Output directory to store model score files')
    args = parser.parse_args()

    main(args.input_dir, args.output_dir)
