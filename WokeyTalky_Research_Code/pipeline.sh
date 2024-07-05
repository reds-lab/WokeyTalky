#!/bin/bash

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --dataset_file)
      dataset_file="$2"
      shift 2
      ;;
    --project_name)
      project_name="$2"
      shift 2
      ;;
    --models_list_dir)
      models_list_dir="$2"
      shift 2
      ;;
    --judge_templates_file)
      judge_templates_file="$2"
      shift 2
      ;;
    --woke_templates_file)
      woke_templates_file="$2"
      shift 2
      ;;
    --scripts_dir)
      scripts_dir="$2"
      shift 2
      ;;
    --stage_6_file)
      stage_6_file="$2"
      shift 2
      ;;
    --insertion_point)
      insertion_point="$2"
      shift 2
      ;;
    --cuda_visible_devices)
      cuda_visible_devices="$2"
      shift 2
      ;;
    --ray_tmpdir)
      ray_tmpdir="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

# Set default values if not provided
dataset_file="${dataset_file:-$(pwd)/data/HEx-PHI/category_1.csv}"
project_name="${project_name:-Demo}"
models_list_dir="${models_list_dir:-$(pwd)/configs/open_models.txt}"
judge_templates_file="${judge_templates_file:-$(pwd)/configs/judge_prompt.jsonl}"
woke_templates_file="${woke_templates_file:-$(pwd)/configs/woke_templates.json}"
scripts_dir="${scripts_dir:-$(pwd)/scripts}"
stage_6_file="${stage_6_file:-}"
insertion_point="${insertion_point:-0}"
cuda_visible_devices="${cuda_visible_devices:-0,1,2,3}"
ray_tmpdir="${ray_tmpdir:-$HOME/tmp_ray}"

out_file="$(pwd)/out/$project_name"

# Environment Configs
export CUDA_DEVICE_ORDER="PCI_BUS_ID"
export CUDA_VISIBLE_DEVICES="$cuda_visible_devices"
export RAY_TMPDIR="$ray_tmpdir"
mkdir -p "$RAY_TMPDIR"

# Create the out_file directory if it doesn't exist
mkdir -p "$out_file"

# Loop through each file in the scripts directory
for script_file in "$scripts_dir"/*.sh; do
    if [ -f "$script_file" ]; then
        script_name=$(basename "$script_file" .sh)
        mkdir -p "$out_file/$script_name"
        echo "Created folder: $out_file/$script_name"
    fi
done

# Change to the scripts directory
cd "$scripts_dir"

# Function to run a stage
run_stage() {
    stage=$1
    case $stage in
        0)
            ./stage_0_data_feed_forward.sh \
                --models_config_path "$models_list_dir" \
                --data_file "$dataset_file" \
                --output_dir "$out_file/stage_0_data_feed_forward"
            ;;
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
                --output_dir "$out_file/stage_2_data_batch_processing"
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
                --output_dir "$out_file/stage_5_woke_batch_processing"
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
}

# Run stages from insertion point
for ((i=insertion_point; i<=8; i++)); do
    run_stage $i
done