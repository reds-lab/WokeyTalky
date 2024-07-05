#!/bin/bash

# Set the default values for the arguments
input_dir="../0_outputs/hex_category_1/stage_4_woke_batch_request"
output_dir="../0_outputs/hex_category_1/stage_5_woke_batch_processing"
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
    --output_dir)
      output_dir="$2"
      shift
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

# Run the Python script with the directory path as an argument
python stage_5_woke_batch_processing.py \
  --input_dir "$input_dir" \
  --output_dir "$output_dir" \
