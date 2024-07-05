#!/bin/bash

# Set the default values for the arguments
judge_input_dir="../0_outputs/stage_0_prompt_loss_rankings/unspecified"
output_dir="../0_outputs/hex_category_1/stage_3_batch_outputs"
generated_input_dir=""
# Path to the models configuration file
models_config_path="../configs/specific_models.txt"

# Parse the command-line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --judge_input_dir)
      judge_input_dir="$2"
      shift
      shift
      ;;
    --generated_input_dir)
      generated_input_dir="$2"
      shift
      shift
      ;;
    --output_dir)
      output_dir="$2"
      shift
      shift
      ;;
    --models_config_path)
      models_config_path="$2"
      shift
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

# Read the models list from the configuration file
mapfile -t models_list < "$models_config_path"

# Iterate over each model in the models list
# Print the array elements
for model in "${models_list[@]}"
do
    success=0
    while [ $success -eq 0 ]; do
        echo "Running prompt loss ranking for model: $model"
        python ./stage_3_prompt_loss_ranking.py \
        --model "$model" \
        --judge_input_dir "$judge_input_dir" \
        --generated_input_dir "$generated_input_dir" \
        --output_dir "$output_dir"
        
        if [ $? -eq 0 ]; then
            success=1
        else
            echo "Error encountered with model $model. Retrying..."
            sleep 1 # Delay before retrying
        fi
    done
done
