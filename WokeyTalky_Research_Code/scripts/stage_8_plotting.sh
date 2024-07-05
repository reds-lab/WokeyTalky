#!/bin/bash

# Set default values for input and output directories
input_dir="../0_outputs/hex_category_1/stage_4_batch_request/"
output_dir="../0_outputs/hex_category_1/stage_5_plotting"
dataset=""
input_dir_2=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --input_dir)
            input_dir="$2"
            shift 2
            ;;
        --output_dir)
            output_dir="$2"
            shift 2
            ;;
        --dataset)
            dataset="$2"
            shift 2
            ;;
        --input_dir_2)
            input_dir_2="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Run the Python script with the specified arguments
python stage_8_plotting_gpt_eval.py --input_dir "$input_dir" --output_dir "$output_dir"

# For keyword eval in the future
# python script.py --input_dir "$INPUT_DIR" --output_dir "$OUTPUT_DIR"

# Run the stage_8_extract_top_woke.py script with the specified arguments
python stage_8_extract_top_woke.py --input_dir "$input_dir" --output_dir "$output_dir" --dataset "$dataset" --input_dir_2 "$input_dir_2"
python stage_8_score_processing.py --input_dir "$input_dir" --output_dir "$output_dir"