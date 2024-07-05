#!/bin/bash

# Set the default values for the arguments
input_dir="../0_outputs/hex_category_1/stage_0_prompt_loss_rankings"
woke_template_file_name="../configs/woke_templates.json"
output_dir="../0_outputs/hex_category_1/stage_1_generation_outputs"
batch_name="batch_output"
dataset_file_path=""
# Parse command-line arguments
while [[ $# -gt 0 ]]
do
  key="$1"
  case $key in
    --input_dir)
      input_dir="$2"
      shift
      shift
      ;;
    --woke_template_file_name)
      woke_template_file_name="$2"
      shift
      shift
      ;;
    --output_dir)
      output_dir="$2"
      shift
      shift
      ;;
    --batch_name)
      batch_name="$2"
      shift
      shift
      ;;
    --dataset_file_path)
      dataset_file_path="$2"
      shift
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

# Run the Python script with the provided arguments
python ./stage_4_woke_batch_request.py \
  --input_dir "$input_dir" \
  --woke_template_file_name "$woke_template_file_name" \
  --output_dir "$output_dir" \
  --batch_name "$batch_name" \
  --dataset_file_path "$dataset_file_path"
  