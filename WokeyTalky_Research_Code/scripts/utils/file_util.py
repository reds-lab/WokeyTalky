import csv
import json
import pandas as pd

def find_file_processor(file_path):
    file_path = str.lower(file_path)
    print(f"File path: {file_path}")

    if "harmful_behaviors_test.csv" in file_path or "harmful_behaviors_train.csv" in file_path:
        print("Selected file processor: adv_train_set_file_processor")
        return adv_train_set_file_processor
    elif"woke_43.json" in file_path or "xstest_43.json" in file_path or "xstest_25.json" in file_path or "xstest_63.json" in file_path or "hex_693.json" in file_path or "adv_63.json" in file_path or "top_woke_prompts.json" in file_path or "top_woke_prompts_10_percent.json" in file_path or "woke_arena_53.json" in file_path or "xstest_240.json" in file_path or "xstest_53.json" in file_path or "xstest_15.json" in file_path:
        print("Selected file processor: woke_prompt_file_processor")
        return woke_prompt_file_processor
    elif "generated_adv_bench.csv" in file_path:
        print("Selected file processor: woke_adv_set_file_processor")
        return woke_adv_set_file_processor
    elif "xstest_v2_prompts.csv" in file_path or "safe_xstest_v2_prompts.csv" in file_path:
        print("Selected file processor: xstest_set_file_processor")
        return xstest_set_file_processor
    elif "0_datasets/case_study_1/generated_adv_bench.csv" in file_path:
        print("Selected file processor: wokey_hex_phi_file_processor")
        return wokey_hex_phi_file_processor
    elif "wokeytalkey_adv_bench.csv" in file_path:
        print("Selected file processor: wokey_adv_bench_file_processor")
        return wokey_adv_bench_file_processor
    elif "hex-phi" in file_path:
        print("Selected file processor: hex_phi_file_processor")
        return hex_phi_file_processor
    elif "adv-bench" in file_path:
        print("Selected file processor: adv_bench_processor")
        return adv_bench_processor
    else:
        raise ValueError(f"Unknown file name: {file_path}")
    
def woke_prompt_file_processor(file_path):
    with open(file_path, "r") as file:
        prompts = json.load(file)
    return prompts

def xstest_set_file_processor(file_path):
    # Load the CSV file into a DataFrame, ensuring it reads the first line as headers
    df = pd.read_csv(file_path)

    # Check if 'goal' and 'type' columns exist in the DataFrame
    if 'prompt' in df.columns and 'type' in df.columns:
        # Filter out rows where 'type' column contains the word 'contrast'
        df = df[~df['type'].astype(str).str.contains('contrast', case=False)]

        # Convert the 'goal' column to a list of strings
        prompts = df['prompt'].tolist()
    else:
        # If 'goal' or 'type' column is not present, return an empty list
        prompts = []

    return prompts

def woke_adv_set_file_processor(file_path):
    # Load the CSV file into a DataFrame, ensuring it reads the first line as headers
    df = pd.read_csv(file_path)

    # Check if 'goal' column exists in the DataFrame
    if 'prompt' in df.columns:
        # Convert the 'goal' column to a list of strings
        prompts = df['prompt'].tolist()
    else:
        # If 'goal' column is not present, return an empty list
        prompts = []
    return prompts
def adv_train_set_file_processor(file_path):
     # Load the CSV file into a DataFrame, ensuring it reads the first line as headers
    df = pd.read_csv(file_path)

    # Check if 'goal' column exists in the DataFrame
    if 'goal' in df.columns:
        # Convert the 'goal' column to a list of strings
        prompts = df['goal'].tolist()
    else:
        # If 'goal' column is not present, return an empty list
        prompts = []
    return prompts
def hex_phi_file_processor(file_path):
    """
    Loads prompts from a CSV file, where each prompt is in a new line.
    Assumes that the CSV file has no header and each line contains one prompt.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    list[str]: A list containing all prompts as strings.
    """
    prompts = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        # Create a reader object which will iterate over lines in the given csvfile
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # checking if the row is not empty
                prompts.append(row[0])  # assuming each row contains one prompt

    return prompts

def adv_bench_processor(file_path):
    """
    Loads prompts from a CSV file using pandas, where each prompt is in the 'goal' column.
    Assumes that the CSV file has headers including 'goal' and possibly others like 'target'.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    list[str]: A list containing all prompts from the 'goal' column as strings.
    """
    # Load the CSV file into a DataFrame, ensuring it reads the first line as headers
    df = pd.read_csv(file_path)

    # Check if 'goal' column exists in the DataFrame
    if 'goal' in df.columns:
        # Convert the 'goal' column to a list of strings
        prompts = df['goal'].tolist()
    else:
        # If 'goal' column is not present, return an empty list
        prompts = []

    return prompts
def wokey_adv_bench_file_processor(file_path):
    # Load the CSV file into a DataFrame, ensuring it reads the first line as headers
    df = pd.read_csv(file_path)
    
    # Check if 'prompt' and 'keep' columns exist in the DataFrame
    if 'prompt' in df.columns and 'keep' in df.columns:
        # Filter the DataFrame to keep only the rows where 'keep' is 1
        filtered_df = df[df['keep'] == 1]
        
        # Convert the 'prompt' column of the filtered DataFrame to a list of strings
        prompts = filtered_df['prompt'].tolist()
    else:
        # If 'prompt' or 'keep' column is not present, return an empty list
        prompts = []
    
    return prompts

def wokey_hex_phi_file_processor(file_path):
    # Load the CSV file into a DataFrame, ensuring it reads the first line as headers
    df = pd.read_csv(file_path)
    
    # Check if 'prompt' and 'keep' columns exist in the DataFrame
    if 'prompt' in df.columns and 'keep' in df.columns:
        # Filter the DataFrame to keep only the rows where 'keep' is 1
        filtered_df = df[df['keep'] == 1]
        
        # Convert the 'prompt' column of the filtered DataFrame to a list of strings
        prompts = filtered_df['prompt'].tolist()
    else:
        # If 'prompt' or 'keep' column is not present, return an empty list
        prompts = []
    
    return prompts

def load_woke_template(file_path="../configs/woke_templates.json", name="woke-template-v1"):

    with open(file_path, "r") as file:
        templates = json.load(file)

    return templates[name]
