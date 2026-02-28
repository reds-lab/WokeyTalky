import json

def load_api_models(filename="../configs/api_models_list.json"):
    # Load the JSON data from supported api models json
    with open(filename, 'r') as file:
        data = json.load(file)
    # Assuming the JSON structure is a dictionary at the root
    return data

def load_models_dict_json(filename="../configs/models_dict.json"):
    # Load the JSON data from the file
    with open(filename, 'r') as file:
        data = json.load(file)
    # Assuming the JSON structure is a dictionary at the root
    return data

def load_local_models_dict_json(filename="../configs/local_models_dict.json"):
    # Load the JSON data from the file
    with open(filename, 'r') as file:
        data = json.load(file)
    # Assuming the JSON structure is a dictionary at the root
    return data


def load_dataset_category_dict(dataset_file_path):
    
    if 'HEx-PHI' in dataset_file_path:
        with open("../configs/hex_phi_file_dict.json", 'r') as file:
            dict = json.load(file)
            filename = dataset_file_path.split('/')[-1]
            filename_without_extension = filename.replace('.csv', '')  # Remove the .csv extension
            return dict[filename_without_extension]
    else:
        return ""