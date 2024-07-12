#!/bin/bash

# Set your default values here
DATASET_FILE="$(pwd)/data/HEx-PHI/category_1.csv"
PROJECT_NAME="GuardrailText"
MODELS_LIST_DIR="$(pwd)/configs/open_models.txt"
JUDGE_TEMPLATES_FILE="$(pwd)/configs/judge_prompt.jsonl"
WOKE_TEMPLATES_FILE="$(pwd)/configs/woke_templates.json"
SCRIPTS_DIR="$(pwd)/scripts"
STAGE_6_FILE=""
INSERTION_POINT=1
CUDA_VISIBLE_DEVICES="0,1,2,3"
RAY_TMPDIR="$HOME/tmp_ray"

# Run the main pipeline script with arguments
./pipeline.sh \
  --dataset_file "${1:-$DATASET_FILE}" \
  --project_name "${2:-$PROJECT_NAME}" \
  --models_list_dir "${3:-$MODELS_LIST_DIR}" \
  --judge_templates_file "${4:-$JUDGE_TEMPLATES_FILE}" \
  --woke_templates_file "${5:-$WOKE_TEMPLATES_FILE}" \
  --scripts_dir "${6:-$SCRIPTS_DIR}" \
  --stage_6_file "${7:-$STAGE_6_FILE}" \
  --insertion_point "${8:-$INSERTION_POINT}" \
  --cuda_visible_devices "${9:-$CUDA_VISIBLE_DEVICES}" \
  --ray_tmpdir "${10:-$RAY_TMPDIR}"