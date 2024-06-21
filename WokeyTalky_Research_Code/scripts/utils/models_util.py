from transformers import AutoTokenizer
from vllm import LLM
import os




def load_model_and_tokenizer(model_id):
    if "chatglm3-6b" in model_id:
        tokenizer = AutoTokenizer.from_pretrained(
            model_id, trust_remote_code=True)
    else:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
    

    vllm_model = LLM(model=model_id,
                     trust_remote_code=True,
                     tensor_parallel_size=len(os.environ["CUDA_VISIBLE_DEVICES"].split(",")),
                    #  disable_custom_all_reduce=True,
                     gpu_memory_utilization=0.9,
                     dtype='bfloat16',
                     swap_space=8,
                     )
    return vllm_model, tokenizer
