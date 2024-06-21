from openai import OpenAI
import json
def save_requests_to_file(requests, output_file_name):
    with open(output_file_name, 'w') as f:
        for request in requests:
            json_string = json.dumps(request)
            f.write(json_string + '\n')


def upload_file_to_openai(file_path, api_key):
    client = OpenAI(api_key=api_key)
    with open(file_path, "rb") as file:
        response = client.files.create(file=file, purpose="batch")
    return client, response


def create_batch(client, response):
    batch = client.batches.create(
        input_file_id=response.id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )
    return batch


def retrieve_batch(client, batch_id):
    return client.batches.retrieve(batch_id)


def get_file_content(client, batch):
    response = client.files.content(batch.output_file_id)
    if hasattr(response, 'content'):
        text_content = response.content.decode('utf-8')
        return text_content
    return None


def parse_multiple_json_objects(json_string):
    objects = []
    remaining_string = json_string.strip()
    while remaining_string:
        try:
            obj, idx = json.JSONDecoder().raw_decode(remaining_string)
            objects.append(obj)
            remaining_string = remaining_string[idx:].strip()
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            break
    return objects


def save_as_jsonl(objects, filename):
    with open(filename, 'a') as file:
        for obj in objects:
            json_line = json.dumps(obj)
            file.write(json_line + '\n')


def confirm_action(message):
    while True:
        user_input = input(f"{message} (y/n): ")
        if user_input.lower() == 'y':
            return True
        elif user_input.lower() == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
