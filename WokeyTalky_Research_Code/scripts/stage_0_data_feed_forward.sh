#!/bin/bash

# Default configuration path
models_config_path="../configs/specific_models.txt"
data_file_default="../0_datasets/HEx-PHI/category_1.csv"
output_dir_default="../0_outputs/stage_0_prompt_loss_rankings/hex_category_1"

# Parse command-line arguments for overrides
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        --models_config_path)
            models_config_path="$2"
            shift # past argument
            shift # past value
            ;;
        --data_file)
            data_file_default="$2"
            shift # past argument
            shift # past value
            ;;
        --output_dir)
            output_dir_default="$2"
            shift # past argument
            shift # past value
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done
echo "$models_config_path"

# Load model names into an array from the specified configuration file
if [[ ! -f "$models_config_path" ]]; then
    echo "Configuration file not found: $models_config_path"
    exit 1
fi

mapfile -t models_list < "$models_config_path"

# Check if models list is empty
if [ ${#models_list[@]} -eq 0 ]; then
    echo "No models found in the configuration file."
    exit 1
fi

# Print the array elements and execute the Python script for each model
for model in "${models_list[@]}"
do
    success=0
    while [ $success -eq 0 ]; do
        echo "Running dataset generation for model: $model"
        python ./stage_0_data_feed_forward.py --model-name "$model" --data-file "$data_file_default" --output-dir "$output_dir_default"
        if [ $? -eq 0 ]; then
            success=1
        else
            echo "Error encountered. Retrying..."
            sleep 1 # Optionally add a delay before retrying
        fi
    done
done