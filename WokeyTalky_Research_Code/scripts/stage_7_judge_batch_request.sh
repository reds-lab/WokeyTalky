#!/bin/bash



# Set the default values for the arguments
input_dir="../0_outputs/hex_category_1/stage_3_woke_feed_forward"
judge_prompt_filename="../configs/judge_prompt.jsonl"
output_dir="../0_outputs/hex_category_1/stage_4_batch_request"
batch_name="batch_output"

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
    --judge_prompt_filename)
      judge_prompt_filename="$2"
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
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

# Run the Python script with the provided arguments
python ./stage_7_judge_batch_request.py \
  --input_dir "$input_dir" \
  --judge_prompt_filename "$judge_prompt_filename" \
  --output_dir "$output_dir" \
  --batch_name "$batch_name"
  