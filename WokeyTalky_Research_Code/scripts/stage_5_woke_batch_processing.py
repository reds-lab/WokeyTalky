import os
import argparse
from dotenv import load_dotenv
from utils.util import setup_env
import json


def extract_content(tag, text):
    # Initialize an empty list to hold all extracted contents
    contents = []

    # Start the search from the beginning of the text
    start_idx = 0

    # Loop through the entire text to find all occurrences of the tag
    while True:
        # Find the starting position of the tag from the current index
        start_idx = text.find(tag, start_idx)

        # If the tag is not found, break out of the loop
        if start_idx == -1:
            break

        # Skip the tag itself to find the content after it
        start_idx += len(tag)

        # Find the end of the content by locating the next "#" character
        end_idx = text.find("#", start_idx)

        # If no "#" is found, take the rest of the text as content
        if end_idx == -1:
            content = text[start_idx:].strip()
        else:
            content = text[start_idx:end_idx].strip()

        # Add the extracted content to the list
        contents.append(content)

        # Update the start index to look for the next occurrence
        start_idx = end_idx if end_idx != -1 else len(text)

    return contents


def remove_quotes(sentences):
    cleaned_sentences = []
    for s in sentences:
        if s.startswith('"""') and s.endswith('"""'):
            cleaned_sentences.append(s[3:-3])  # Remove triple quotes
        elif s.startswith('"') and s.endswith('"'):
            cleaned_sentences.append(s[1:-1])  # Remove double quotes
        elif s.startswith("'") and s.endswith("'"):
            cleaned_sentences.append(s[1:-1])  # Remove single quotes
        else:
            cleaned_sentences.append(s)
    return cleaned_sentences


def parse_model_name(full_model_name):
    # Split the full model name by '-' and take all parts except the last one to form the base model name.
    base_model_name = full_model_name.split('_')[0]
    # The last part of the model name is assumed to be the version number.
    version_number = full_model_name.split('_')[1]
    return base_model_name, version_number


def remove_newline_and_following(content):
    """
    Locate the first occurrence of '\n' in a string and remove it along with all the contents following it.
    Return the contents before the '\n'.

    Parameters:
    content (str): The string to be processed.

    Returns:
    str: The string with contents following '\n' removed.
    """
    # Find the position of the first occurrence of '\n' in the string
    newline_pos = content.find('\n')
    # Return the substring up to the newline character, if found; otherwise, return the original string
    return content[:newline_pos] if newline_pos != -1 else content


def get_message_content_by_custom_id(all_requests, custom_id):
    """
    Search through a list of request dicts and find the 'content' field
    of the first message in the body of the request that matches the given custom_id.

    Parameters:
    all_requests (list): A list of request dicts.
    custom_id (str): The custom ID to match in the requests.

    Returns:
    str: The content of the first message of the matched request or None if no match is found.
    """
    # Iterate over all requests
    for request in all_requests:
        # Check if the current request's custom_id matches the one we're looking for
        if request.get('custom_id') == custom_id:
            # Navigate through the nested dicts/lists to find the 'content' field
            messages = request.get('body', {}).get('messages', [])
            if messages:
                # Return the 'content' of the first message
                return messages[0].get('content')
    # Return None if no match is found
    return None


def main(input_dir,output_dir):

    filename = os.path.join(input_dir, 'batch_raw_outputs.jsonl')
    with open(filename, 'r') as f:
        all_results = [json.loads(line) for line in f]

    filename = os.path.join(input_dir, 'batch_request.jsonl')
    with open(filename, 'r') as f:
        all_requests = [json.loads(line) for line in f]
    models = []
    for request in all_requests:

        model = request['custom_id'].split('_')[0]
        if model not in models:
            models.append(model)

    wokey_data = dict()
    for model in models:
        wokey_data[model] = []

    failed_num = 0
    failed_cases = []

    for result in all_results:
        base_name, idx = parse_model_name(result['custom_id'])
        print(base_name)
        ori_harm = remove_newline_and_following(extract_content(
            ".\n\nHarmful Inquiry - ", get_message_content_by_custom_id(all_requests, result['custom_id']))[0])
        content = result['response']['body']['choices'][0]['message']['content']
        woke_ideas = remove_quotes(extract_content("potential_spurious_correlation_to_use (contents to keep):", content))
        if len(woke_ideas) == 0:
            woke_ideas = remove_quotes(extract_content("potential_spurious_corelation_to_use (contents to keep):", content))
        if len(woke_ideas) == 0:
            woke_ideas = []

        woke_data = remove_quotes(extract_content("a_non_harmful_challenging_inquiry_with_relevance_to_the_harmful_or_unlawful_intention:", content))
        if len(woke_data) == 0:
            woke_data = remove_quotes(extract_content("a_non_harmful_challenging_inquery_with_relevance_to_the_harmful_or_unlawful_intention:", content))
        if len(woke_data) == 0:
            woke_data = []
        woke_reason = remove_quotes(extract_content("reasons_of_being_harmful:", content))
        if len(woke_reason) == 0:
            woke_reason = ""
        else:
            woke_reason = woke_reason[0]

        if len(woke_data) == 0:
            print('Skipping for no woke data found in response.')
            print('model:', base_name)
            print('idx:', idx)
            failed_num += 1
            failed_cases.append(result)
            continue
        else:
            for i in range(len(woke_data)):
                if len(woke_data[i]) != 3:
                    print(f"Warning: 'woke_data[{i}]' length is {len(woke_data[i])}, expected 3.")
                    print('model:', base_name)
                    print('idx:', idx)
                    print('woke_data[i]:', woke_data[i])

            wokey_data[base_name].append([{
                'woke_idx': idx,
                'woke_harm': ori_harm,
                'woke_harm_reasons': woke_reason,
                'woke_ideas': woke_ideas[i] if i < len(woke_ideas) else "",
                'woke_data': woke_data[i],
            } for i in range(len(woke_data))])

        # Specify the file path where you want to store the JSON file
    filename = os.path.join(output_dir, 'woke_batch.json')
    # Open the file in write mode and store the dictionary as JSON
    with open(filename, "w") as json_file:
        json.dump(wokey_data, json_file, indent=4)

    print(f"Dictionary stored as JSON file: {filename}")
    # Preload the question
    questions = []

    for model, entry in wokey_data.items():
        for array_object in entry:
            for object in array_object:
                question_object = {}
                question_object['woke_idx'] = object['woke_idx']
                question_object['woke_harm'] = object['woke_harm']
                question_object['woke_reasons'] = object['woke_harm_reasons']
                question_object['woke_ideas'] = object['woke_ideas']
                question_object['woke_data'] = object['woke_data']
                question_object['woke_model'] = model
                
                questions.append(question_object)

    filename = os.path.join(output_dir, 'woke_batch_processed.json')
    # Open the file in write mode and store the dictionary as JSON
    with open(filename, "w") as json_file:
        json.dump(questions, json_file, indent=4)
    print('done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process JSON files in a directory.')
    parser.add_argument('--input_dir', type=str, default='./0_bash_files/0_outputs/more_woke_model_900_outputs/',
                        help='Path to the directory containing JSON files to process.')
    parser.add_argument('--woke_template_file_name', type=str, default='../configs/woke_templates.json',
                        help='Path to the judge prompt file.')
    parser.add_argument('--output_dir', type=str, default='./0_bash_files/0_batch_data/',
                        help='Path and name of the output file to save the requests.')
    args = parser.parse_args()
    input_dir = args.input_dir 
    output_dir = args.output_dir 
    main(input_dir,output_dir)
