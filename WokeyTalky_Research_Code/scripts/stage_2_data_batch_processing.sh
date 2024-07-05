#!/bin/bash

# Set default values for input and output directories
input_dir="../0_outputs/hex_category_1/stage_0_batch_request"
output_dir="../0_outputs/hex_category_1/stage_0_batch_processing"

# Parse command-line arguments
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --input_dir)
    input_dir="$2"
    shift # past argument
    shift # past value
    ;;
    --output_dir)
    output_dir="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    echo "Unknown option: $1"
    exit 1
    ;;
esac
done

# Run the Python script with the provided arguments
python stage_2_data_batch_processing.py --input_dir "$input_dir" --output_dir "$output_dir"