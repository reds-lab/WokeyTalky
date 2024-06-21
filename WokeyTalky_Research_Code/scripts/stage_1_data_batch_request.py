import json
from dotenv import load_dotenv
import os
load_dotenv()
from utils.eval_util import load_prompt_format
import argparse
from utils.progress_util import progress_bar
from utils.gpt_batch_request import save_requests_to_file,upload_file_to_openai,create_batch,retrieve_batch,get_file_content,parse_multiple_json_objects,save_as_jsonl,confirm_action
def process_json_files(input_dir, judge_prompt_filename):
    requests = []
    file_names = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    for filename in file_names:
        json_objects = []

        with open(os.path.join(input_dir, filename), 'r') as file:
            for line in file:
                try:
                    json_object = json.loads(line.strip())
                    json_objects.append(json_object)
                except json.JSONDecodeError as e:
                    print(
                        f"Failed to decode JSON from line: {line}, error: {e}")

        model_name = filename.split('_')[0]
        for i, object in enumerate(json_objects):
            answer = object['generated']
            raw_prompt = object['raw_prompt']
            QA_Pair = (raw_prompt, answer)

            custom_id = f"{model_name}_{i}"
            method = "POST"
            url = "/v1/chat/completions"
            model = "gpt-4-turbo"
            prompt_template, outputformat = load_prompt_format(
                judge_prompt_filename, 'base-#thescore')

            content = prompt_template % QA_Pair
            messages = [{"role": "user", "content": content}]

            request = {
                "custom_id": custom_id,
                "method": method,
                "url": url,
                "body": {
                    "model": model,
                    "messages": messages,
                    "temperature": 0, "max_tokens": 10, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 0
                }
            }

            requests.append(request)

    return requests




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process JSON files and create OpenAI batch requests.')
    parser.add_argument('--input_dir', type=str, default='./0_bash_files/0_outputs/more_woke_model_900_outputs/',
                        help='Path to the directory containing JSON files to process.')
    parser.add_argument('--judge_prompt_filename', type=str, default='./judge_prompt.jsonl',
                        help='Path to the judge prompt file.')
    parser.add_argument('--output_dir', type=str, default='./0_bash_files/0_batch_data/',
                        help='Path and name of the output file to save the requests.')
    parser.add_argument('--batch_name', type=str, default='batch_output',
                        help='Name of the batch output file.')
    args = parser.parse_args()

    input_dir = args.input_dir
    judge_prompt_filename = args.judge_prompt_filename
    output_dir = args.output_dir
    batch_name = args.batch_name

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "API Key not found. Please set the OPENAI_API_KEY environment variable.")

    batch_ids_file = f"{output_dir}/batch_ids.jsonl"

    if os.path.exists(batch_ids_file):
        with open(batch_ids_file, "r") as f:
            batch_ids = [json.loads(line) for line in f]
        if batch_ids:
            print("Available batch IDs:")
            for i, batch_id in enumerate(batch_ids, start=1):
                print(f"{i}. {batch_id['batch_id']}")
            while True:
                batch_index = input("Enter the number of the batch ID you want to retrieve (or press Enter to create a new batch): ")
                if batch_index == "":
                    break
                try:
                    batch_index = int(batch_index) - 1
                    if 0 <= batch_index < len(batch_ids):
                        selected_batch_id = batch_ids[batch_index]["batch_id"]
                        client = OpenAI(api_key=api_key)
                        while True:
                            try:
                                retrieved_batch = retrieve_batch(client, selected_batch_id)
                                if retrieved_batch.status == 'completed':
                                    break
                                else:
                                    raise Exception(
                                        f"Batch processing failed with status: {retrieved_batch.status}")
                            except Exception as e:
                                print(f"Error retrieving batch: {e}")
                                print("Retrying in 30 seconds...\n")
                                progress_bar(30)
                        text_content = get_file_content(client, retrieved_batch)
                        if text_content:
                            parsed_objects = parse_multiple_json_objects(text_content)
                            save_as_jsonl(parsed_objects, f"{output_dir}/batch_raw_outputs.jsonl")
                        exit(0)
                    else:
                        print("Invalid batch number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

    requests = process_json_files(input_dir, judge_prompt_filename)
    save_requests_to_file(requests, f'{output_dir}/batch_request.jsonl')

    if not confirm_action("Do you want to proceed with sending the request to OpenAI?"):
        print("Request canceled.")
        exit(0)

    client, response = upload_file_to_openai(
        f'{output_dir}/batch_request.jsonl', api_key)
    batch = create_batch(client, response)

    with open(batch_ids_file, "a") as f:
        f.write(json.dumps({"batch_id": batch.id}) + "\n")

    while True:
        try:
            retrieved_batch = retrieve_batch(client, batch.id)
            if retrieved_batch.status == 'completed':
                break
            else:
                raise Exception(
                    f"Batch processing failed with status: {retrieved_batch.status}")
        except Exception as e:
            print(f"Error retrieving batch: {e}")
            print("Retrying in 30 seconds...\n")
            progress_bar(30)

    text_content = get_file_content(client, retrieved_batch)
    if text_content:
        parsed_objects = parse_multiple_json_objects(text_content)
        save_as_jsonl(parsed_objects, f"{output_dir}/batch_raw_outputs.jsonl")
