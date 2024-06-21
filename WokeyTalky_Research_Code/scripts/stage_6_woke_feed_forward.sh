#!/bin/bash

# Set the default values for the arguments
input_dir="../0_outputs/stage_0_prompt_loss_rankings/unspecified"
output_dir="../0_outputs/hex_category_1/stage_3_batch_outputs"

# Path to the models configuration file
models_config_path="../configs/specific_models.txt"
data_file=""
# Parse the command-line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --input_dir)
      input_dir="$2"
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
    --data_file)
      data_file="$2"
      shift
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done
export RAY_TMPDIR="/tmp/ray"

# Read the models list from the configuration file
mapfile -t MODELS_LIST < "$models_config_path"

# Iterate over each model in the models list
for MODEL_NAME in "${MODELS_LIST[@]}"
do
    success=0
    while [ $success -eq 0 ]; do
        echo "Processing model: $MODEL_NAME"
        python ./stage_6_woke_feed_forward.py \
          --model-name "$MODEL_NAME" \
          --input_dir "$input_dir" \
          --output_dir "$output_dir" \
          --data_file "$data_file"
          
        if [ $? -eq 0 ]; then
            success=1
        else
            echo "Error encountered with model $MODEL_NAME. Retrying..."
            sleep 1 # Delay before retrying
        fi
    done
done
