import re
import subprocess
from transformers import AutoTokenizer


def setup_env(os, devices=""):
    print("Entering setup_env")
    # Set the default cache directory for Hugging Face models and datasets.
    # This location is where downloaded models and datasets will be stored.


    if len(devices) == 0:
        return
    # Set the CUDA device order to PCI_BUS_ID to ensure that the CUDA device IDs
    # correspond directly to the physical order in the system. This helps in
    # predictable allocation of devices.
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"

    # Specify which CUDA devices are visible to the current process. This is useful
    # when there are multiple GPUs and only specific ones should be used by the process.
    # The 'devices' parameter can be a string like "0" or "0,1" to specify which GPUs to use.
    os.environ["CUDA_VISIBLE_DEVICES"] = devices


def get_least_used_gpu():
    # Run nvidia-smi command to get GPU memory usage
    smi_output = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,index', '--format=csv,noheader,nounits'],
                                capture_output=True, text=True).stdout

    # Find the GPU with the least memory used
    min_memory = float('inf')
    least_used_gpu = None
    for line in smi_output.strip().split('\n'):
        memory_used, index = re.split(r',\s*', line)
        memory_used = int(memory_used)
        if memory_used < min_memory:
            min_memory = memory_used
            least_used_gpu = int(index)

    return least_used_gpu


def load_model_and_tokenizer(model_id):
    if "chatglm3-6b" in model_id:
        tokenizer = AutoTokenizer.from_pretrained(
            model_id, trust_remote_code=True)
    else:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
    vllm_model = LLM(model=model_id,
                     trust_remote_code=True,
                     #  tensor_parallel_size=2,
                     #            tokenizer=model_id,
                     dtype='bfloat16',
                     swap_space=16)
    return vllm_model, tokenizer
