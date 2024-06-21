from dotenv import load_dotenv
import json
import os

load_dotenv()

os.environ["HF_HUB_CACHE"] = os.path.join(os.environ["HF_HOME"], 'hub')
os.environ["HF_ASSETS_CACHE"] = os.path.join(os.environ["HF_HOME"], 'assets')
os.environ['HF_TOKEN'] = os.getenv('HUGGINGFACE_TOKEN')

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm
from utils.prompt_util import find_prompt_template
from utils.util import setup_env
from utils.config_util import load_models_dict_json
import argparse
from accelerate import Accelerator

def load_model_and_tokenizer_loss_compute(model_id, accelerator):
    if "chatglm3-6b" in model_id:
        tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        tokenizer.pad_token = tokenizer.eos_token
        model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
    else:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        tokenizer.pad_token = tokenizer.eos_token

        model = AutoModelForCausalLM.from_pretrained(  model_id,
        device_map="auto",
        )

    model = accelerator.prepare(model)
    return model, tokenizer


def loss_compute(input_ids, model, labels):
    device = model.device
    input_ids = input_ids.to(device)
    labels = labels.to(device)
    with torch.no_grad():
        outputs = model(input_ids=input_ids, labels=labels)
    return outputs.loss.item()


def main(model_name, judge_input_dir, generated_input_dir,output_dir):
    model_dict = load_models_dict_json()
    
    judge_results_filename = f"{judge_input_dir}/{model_name}_judge_scores.json"
    with open(judge_results_filename, 'r') as file:
        judge_results = json.load(file)

    # assumes sequential order
    rejected_indices = [int(result["index"])
                        for result in judge_results if result['score'] == 0]

    model_results_filename = f'{generated_input_dir}/{model_name}_generated_output.json'
    with open(model_results_filename, 'r') as file:
        model_results = [json.loads(line) for line in file]
    print(len(model_results))
    
    
    accelerator = Accelerator()
    model, tokenizer = load_model_and_tokenizer_loss_compute(
        model_dict[model_name], accelerator)

    # %%
    raw_model_questions = [line["raw_prompt"]
                           for line in model_results]
    model_questions = find_prompt_template(
        raw_model_questions, model_name, tokenizer)
    model_answers = [line["generated"] for line in model_results]

    # %%
    refusal_loss_record = 1e6 * np.ones(len(model_questions))

    for idx in tqdm(rejected_indices):
        input_ids = tokenizer(model_questions[idx], return_tensors="pt",
                              padding="max_length", max_length=256, truncation=True).input_ids
        target_safe_ids = tokenizer(
            model_answers[idx], return_tensors="pt", padding="max_length", max_length=256, truncation=True).input_ids

        refusal_labels = torch.cat(
            [target_safe_ids[:, 1:], torch.tensor([[tokenizer.eos_token_id]])], dim=1)
        refusal_loss_record[idx] = loss_compute(
            input_ids, model, refusal_labels)

    refusal_loss_record_filename = f'{output_dir}/{model_name}.npy'
    np.save(refusal_loss_record_filename, refusal_loss_record)

    def first_k_words(paragraphs, k=4):
        outputs = []
        for paragraph in paragraphs:
            # Split the paragraph into words and take the first k words
            words = paragraph.split()
            output = ' '.join(words[:k])
            outputs.append(output)
        return outputs
    top_general_refusal_indices = []
    top_refusal_indices = []


    if len(rejected_indices) < 10 and len(rejected_indices) != 0:
        top_refusal_indices = np.argsort(refusal_loss_record)[
            :len(rejected_indices)]
        num_of_additional_questions = 10 - len(rejected_indices)

        # compute the new rankings agaisnt rejecting keyworks sampled from the top ranked ones
        general_refusal_loss_record = 1e6 * np.ones(len(model_questions))
        combined_reject = ' '.join(first_k_words(
            [model_answers[i] for i in top_refusal_indices], 4)) 

            
        for idx in tqdm(range(len(model_questions))):
            input_ids = tokenizer(model_questions[idx], return_tensors="pt",
                                  padding="max_length", max_length=256, truncation=True).input_ids
            target_safe_ids = tokenizer(
                combined_reject, return_tensors="pt", padding="max_length", max_length=256, truncation=True).input_ids

            refusal_labels = torch.cat(
                [target_safe_ids[:, 1:], torch.tensor([[tokenizer.eos_token_id]])], dim=1)
            general_refusal_loss_record[idx] = loss_compute(
                input_ids, model, refusal_labels)
        general_refusal_indices = np.argsort(general_refusal_loss_record)
        top_general_refusal_indices = [
            i for i in general_refusal_indices if i not in top_refusal_indices][:num_of_additional_questions]
        top_refusal_indices = np.concatenate(
            (top_refusal_indices, top_general_refusal_indices))

    elif len(rejected_indices) == 0:
        num_of_additional_questions = 10

        # compute the new rankings agaisnt rejecting keyworks sampled from the top ranked ones
        general_refusal_loss_record = 1e6 * np.ones(len(model_questions))
        combined_reject = 'Sorry cannot not apologies'
        for idx in tqdm(range(len(model_questions))):
            input_ids = tokenizer(model_questions[idx], return_tensors="pt",
                                  padding="max_length", max_length=256, truncation=True).input_ids
            target_safe_ids = tokenizer(
                combined_reject, return_tensors="pt", padding="max_length", max_length=256, truncation=True).input_ids

            refusal_labels = torch.cat(
                [target_safe_ids[:, 1:], torch.tensor([[tokenizer.eos_token_id]])], dim=1)
            general_refusal_loss_record[idx] = loss_compute(
                input_ids, model, refusal_labels)
        general_refusal_indices = np.argsort(general_refusal_loss_record)
        top_general_refusal_indices = [
            i for i in general_refusal_indices if i not in top_refusal_indices][:num_of_additional_questions]
        top_refusal_indices = top_general_refusal_indices

    else:
        top_refusal_indices = np.argsort(refusal_loss_record)[:10]

    # Create a list to store the questions and their corresponding losses
    questions_and_losses = []

    for idx in top_refusal_indices:
        question = raw_model_questions[idx]
        if idx in top_general_refusal_indices:
            loss = general_refusal_loss_record[idx]
        else:
            loss = refusal_loss_record[idx]
        questions_and_losses.append({"question": question, "loss": loss})

    sorted_questions_and_losses = sorted(
        questions_and_losses, key=lambda x: x["loss"])

    # Save the sorted questions and losses to a JSON file
    output_filename = f"{output_dir}/{model_name}_questions_and_losses.json"
    with open(output_filename, "w") as file:
        json.dump(sorted_questions_and_losses, file, indent=4)

    # Print the questions and their losses in order of lowest loss
    for item in sorted_questions_and_losses:
        print(f"Question: {item['question']}")
        print(f"Loss: {item['loss']}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process model data and compute refusal loss.')
    parser.add_argument('--model', type=str, required=True,
                        help='Name of the model to use.')
    parser.add_argument('--output_dir', type=str, default='../0_outputs',
                        help='Output directory for the processed files.')
    parser.add_argument('--judge_input_dir', type=str, default='../0_outputs',
                        help='Output directory for the processed files.')
    parser.add_argument('--generated_input_dir', type=str, default='../0_outputs',
                        help='Output directory for the processed files.')
    args = parser.parse_args()

    main(args.model,args.judge_input_dir, args.generated_input_dir, args.output_dir)
