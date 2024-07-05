# Running the Code

## Environment Setup
Using Conda is recommended for managing dependencies and creating the virtual environment.

### Prerequisites
- Ensure you have [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installed on your system.

### Steps
1. **Create a new Conda environment:**
    ```sh
    conda create --name myenv python=3.x
    ```
2. **Activate the environment:**
    ```sh
    conda activate myenv
    ```
3. **Install required packages:**
    ```sh
    # If you have a requirements file, use:
    pip install -r requirements.txt
    ```

## Running the Script

### Default Values and Variables
The script uses the following default values. You can modify these as needed:
- `DATASET_FILE`: Path to your dataset file.
- `PROJECT_NAME`: Name of your project.
- `MODELS_LIST_DIR`: Directory containing model configurations.
- `JUDGE_TEMPLATES_FILE`: Path to the judge templates file.
- `WOKE_TEMPLATES_FILE`: Path to the woke templates file.
- `SCRIPTS_DIR`: Directory of your scripts.
- `STAGE_6_FILE`: Optional stage 6 file.
- `INSERTION_POINT`: Default insertion point.
- `CUDA_VISIBLE_DEVICES`: GPUs allocated for the task.
- `RAY_TMPDIR`: Temporary directory for Ray.

### Example `setup.sh` Script
```bash
#!/bin/bash

# Set your default values here
DATASET_FILE="$(pwd)/data/HEx-PHI/category_1.csv"
PROJECT_NAME="Demo"
MODELS_LIST_DIR="$(pwd)/configs/open_models.txt"
JUDGE_TEMPLATES_FILE="$(pwd)/configs/judge_prompt.jsonl"
WOKE_TEMPLATES_FILE="$(pwd)/configs/woke_templates.json"
SCRIPTS_DIR="$(pwd)/scripts"
STAGE_6_FILE=""
INSERTION_POINT=0
CUDA_VISIBLE_DEVICES="0,1,2,3"
RAY_TMPDIR="$HOME/tmp_ray"

# Run the main pipeline script with arguments
./main_pipeline.sh \
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
```

### Running the Script
To execute the pipeline, navigate to the directory containing `setup.sh` and run:
```sh
./setup.sh
```

---

This documentation provides clear, step-by-step instructions for setting up the environment and running the code. Follow these instructions to quickly get your pipeline up and runnin