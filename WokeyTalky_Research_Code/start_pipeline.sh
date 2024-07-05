#!/bin/bash

# main configuration
dataset_file="$(pwd)/data/HEx-PHI/category_1.csv"
project_name="Demo"
out_file="$(pwd)/out/$project_name"

# Environment Configs
export CUDA_DEVICE_ORDER="PCI_BUS_ID"
export CUDA_VISIBLE_DEVICES="0,1"
export RAY_TMPDIR="$HOME/tmp_ray"
mkdir -p "$RAY_TMPDIR"

#Pipeline configs
models_list_dir="$(pwd)/configs/open_models.txt"
judge_templates_file="$(pwd)/configs/judge_prompt.jsonl"
woke_templates_file="$(pwd)/configs/woke_templates.json"
scripts_dir="$(pwd)/scripts"
# stage_6_file="$(pwd)/0_datasets/case_study_1/safe_xstest_v2_prompts.csv"

# Create the out_file directory if it doesn't exist
mkdir -p "$out_file"

# Loop through each file in the scripts directory
for script_file in "$scripts_dir"/*.sh; do
    # Check if the file exists and is a regular file
    if [ -f "$script_file" ]; then
        # Extract the script name without the extension
        script_name=$(basename "$script_file" .sh)
        # Create a folder in the out_file directory with the script name
        mkdir -p "$out_file/$script_name"
        echo "Created folder: $out_file/$script_name"
    fi
done

# Change to the scripts directory
cd scripts/

# Ask the user for the insertion point
echo "Please choose the insertion point:"
echo "0. stage_0_data_feed_forward.sh"
echo "1. stage_1_data_batch_request.sh"
echo "2. stage_2_data_batch_processing.sh"
echo "3. stage_3_prompt_loss_ranking.sh"
echo "4. stage_4_woke_batch_request.sh"
echo "5. stage_5_woke_batch_processing.sh"
echo "6. stage_6_woke_feed_forward.sh"
echo "7. stage_7_judge_batch_request.sh"
echo "8. stage_8_plotting.sh"

read -p "Enter the stage number: " insertion_point
# Run the stages based on the insertion point
case $insertion_point in
    0)
        read -p "Press Enter to run stage_0_data_feed_forward.sh"
        ./stage_0_data_feed_forward.sh \
            --models_config_path "$models_list_dir" \
            --data_file "$dataset_file" \
            --output_dir "$out_file/stage_0_data_feed_forward"
        ;;
    1)
        read -p "Press Enter to run stage_1_data_batch_request.sh"
        ./stage_1_data_batch_request.sh \
            --input_dir "$out_file/stage_0_data_feed_forward" \
            --output_dir "$out_file/stage_1_data_batch_request" \
            --judge_prompt_filename "$judge_templates_file" \
            --batch_name "batch_output"
        ;;
    2)
        read -p "Press Enter to run stage_2_data_batch_processing.sh"
        ./stage_2_data_batch_processing.sh \
            --input_dir "$out_file/stage_1_data_batch_request" \
            --output_dir "$out_file/stage_2_data_batch_processing" \
        ;;
    3)
        read -p "Press Enter to run stage_3_prompt_loss_ranking.sh"
        ./stage_3_prompt_loss_ranking.sh \
            --generated_input_dir "$out_file/stage_0_data_feed_forward" \
            --judge_input_dir "$out_file/stage_2_data_batch_processing" \
            --output_dir "$out_file/stage_3_prompt_loss_ranking" \
            --models_config_path "$models_list_dir"
        ;;
    4)
        read -p "Press Enter to run stage_4_woke_batch_request.sh"
        ./stage_4_woke_batch_request.sh \
            --input_dir "$out_file/stage_3_prompt_loss_ranking" \
            --output_dir "$out_file/stage_4_woke_batch_request" \
            --dataset_file_path "$dataset_file"
        ;;
    5)
        read -p "Press Enter to run stage_5_woke_batch_processing.sh"
        ./stage_5_woke_batch_processing.sh \
            --input_dir "$out_file/stage_4_woke_batch_request" \
            --output_dir "$out_file/stage_5_woke_batch_processing" \
        ;;
    6)
        read -p "Press Enter to run stage_6_woke_feed_forward.sh"
            ./stage_6_woke_feed_forward.sh \
                --input_dir "$out_file/stage_5_woke_batch_processing" \
                --models_config_path "$models_list_dir" \
                --output_dir "$out_file/stage_6_woke_feed_forward" \
                --data_file "$stage_6_file"
        ;;
    7)
        read -p "Press Enter to run stage_7_judge_batch_request.sh"
        ./stage_7_judge_batch_request.sh \
            --input_dir "$out_file/stage_6_woke_feed_forward" \
            --judge_prompt_filename "$judge_templates_file" \
            --output_dir "$out_file/stage_7_judge_batch_request"
        ;;
    8)
        read -p "Press Enter to run stage_8_plotting.sh"
        ./stage_8_plotting.sh \
            --input_dir "$out_file/stage_7_judge_batch_request" \
            --output_dir "$out_file/stage_8_plotting" \
            --dataset "Case_study" \
            --input_dir_2 "$out_file/stage_6_woke_feed_forward"
        ;;
    *)
        echo "Invalid stage number. Exiting."
        exit 1
        ;;
esac

# Run the remaining stages after the insertion point
for ((i=insertion_point+1; i<=8; i++)); do
    case $i in
         1)
        ./stage_1_data_batch_request.sh \
            --input_dir "$out_file/stage_0_data_feed_forward" \
            --output_dir "$out_file/stage_1_data_batch_request" \
            --judge_prompt_filename "$judge_templates_file" \
            --batch_name "batch_output"
            ;;
        2)
            ./stage_2_data_batch_processing.sh \
                --input_dir "$out_file/stage_1_data_batch_request" \
                --output_dir "$out_file/stage_2_data_batch_processing" \
            ;;
        3)
            ./stage_3_prompt_loss_ranking.sh \
                --generated_input_dir "$out_file/stage_0_data_feed_forward" \
                --judge_input_dir "$out_file/stage_2_data_batch_processing" \
                --output_dir "$out_file/stage_3_prompt_loss_ranking" \
                --models_config_path "$models_list_dir"
            ;;
        4)
            ./stage_4_woke_batch_request.sh \
                --input_dir "$out_file/stage_3_prompt_loss_ranking" \
                --output_dir "$out_file/stage_4_woke_batch_request" \
                --dataset_file_path "$dataset_file"
            ;;
        5)
            ./stage_5_woke_batch_processing.sh \
                --input_dir "$out_file/stage_4_woke_batch_request" \
                --output_dir "$out_file/stage_5_woke_batch_processing" \
            ;;
        6)
            ./stage_6_woke_feed_forward.sh \
                --input_dir "$out_file/stage_5_woke_batch_processing" \
                --models_config_path "$models_list_dir" \
                --output_dir "$out_file/stage_6_woke_feed_forward" \ 
                --data_file "$stage_6_file"
            ;;
        7)
            ./stage_7_judge_batch_request.sh \
                --input_dir "$out_file/stage_6_woke_feed_forward" \
                --judge_prompt_filename "$judge_templates_file" \
                --output_dir "$out_file/stage_7_judge_batch_request"
            ;;
        8)
            ./stage_8_plotting.sh \
            --input_dir "$out_file/stage_7_judge_batch_request" \
            --output_dir "$out_file/stage_8_plotting" \
            --dataset "Case_study" \
            --input_dir_2 "$out_file/stage_6_woke_feed_forward"
            ;;
        *)
            echo "Invalid stage number. Exiting."
            exit 1
            ;;
    esac
done