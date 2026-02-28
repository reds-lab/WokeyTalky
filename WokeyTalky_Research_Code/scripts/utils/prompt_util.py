from tqdm import tqdm

def apply_prompt_template(prompt, model_name, tokenizer):
    model_name = model_name.lower()
    
    if 'llama-2' in model_name or 'meta-llama-3' in model_name:
        if "guard" in model_name:
            messages = [
                {"role": "system", "content": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."},
                {"role": "user", "content": prompt}
            ]
            PROMPT_TEMPLATE = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
            )

        else: 
            messages = [
                {"role": "system", "content": "You are a helpful, respectful and honest assistant."},
                {"role": "user", "content": prompt}
            ]
            PROMPT_TEMPLATE = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
            )
    
    elif 'gemma' in model_name:
        messages = [
            {"role": "user", "content": prompt},
        ]
        PROMPT_TEMPLATE = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True)
    elif 'qwen' in model_name:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        PROMPT_TEMPLATE = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
    elif 'vicuna' in model_name:
        # Manual Template
        PROMPT_TEMPLATE = f"A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: {prompt} ASSISTANT:"

    elif 'chatglm3-6b' in model_name:
        PROMPT_TEMPLATE = f"""<|system|>
                            You are ChatGLM3, a large language model trained by Zhipu.AI. Follow the user's instructions carefully. Respond using markdown.
                            <|user|>
                            {prompt}
                            <|assistant|>
                            """
    elif 'yi-6b-chat' == model_name:
        messages = [
            {"role": "user", "content": prompt}
        ]
        PROMPT_TEMPLATE = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
    elif "aurora-m-biden-harris-redteamed" == model_name:
        PROMPT_TEMPLATE = f"""### Instruction:
                            {prompt}
                            ### Response:
                            """
    elif "mistral-7b-instruct-v0.2" in model_name or "mistral-7b-instruct-v0.1" in model_name:
        if "guard" in model_name:

            system_prompt = "Always assist with care, respect, and truth. Respond with utmost utility yet securely. Avoid harmful, unethical, prejudiced, or negative content. Ensure replies promote fairness and positivity."
  
            PROMPT_TEMPLATE = f"""<s>[INST] {system_prompt} {prompt} [/INST]"""
        else:
            messages = [
                {"role": "user", "content": prompt}
            ]
            PROMPT_TEMPLATE = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
    elif "openchat-3.5-0106" == model_name:

        messages = [
            {"role": "user", "content": prompt},
        ]
        PROMPT_TEMPLATE = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True)
    elif "zephyr-7b-beta" == model_name:
        messages = [
            {"role": "user", "content": prompt},
        ]
        PROMPT_TEMPLATE = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True)
    elif "dolphin-2.2.1-mistral-7b" == model_name:
        PROMPT_TEMPLATE = f"""<|im_start|>system
        You are Dolphin, a helpful AI assistant.<|im_end|>
        <|im_start|>user
        {prompt}<|im_end|>
        <|im_start|>assistant
        """
    elif "phi-3-mini-128k-instruct" in model_name:
        if "guard" in model_name:
            
            PROMPT_TEMPLATE = f"""<|system|>
            You are a helpful digital assistant. Please provide safe, ethical and accurate information to the user.<|end|>
            <|user|>
            {prompt}<|end|>
            <|assistant|>
            """
        else:
            PROMPT_TEMPLATE = f"""<|system|>
            You are a helpful AI assistant.<|end|>
            <|user|>
            {prompt}<|end|>
            <|assistant|>
            """
    
    else:
        raise ValueError("Invalid model name")
    return PROMPT_TEMPLATE

def find_prompt_template(prompt_s, model_name, tokenizer):
    '''
    Returns a list of templated prompts. The function accepts either a single string or a list of strings.
    It applies a templating function to each prompt using the specified model and tokenizer.

    Args:
    prompt_s (str or list of str): A single prompt string or a list of prompt strings.
    model_name (str): The name of the model for which the prompt is being templated.
    tokenizer: The tokenizer being used for the prompts. model_dict[model_name]

vllm_model, tokenizer = load_model_and_tokenizer(
    model_id=model_id)
    ValueError: If the input is neither a string nor a list of strings.
    '''
    templated_prompts = []

    # Check if the input is a single string
    if isinstance(prompt_s, str) and not isinstance(prompt_s, list):
        templated_prompts.append(apply_prompt_template(
            prompt_s, model_name, tokenizer))

    # Check if the input is a list of strings
    elif isinstance(prompt_s, list) and all(isinstance(item, str) for item in prompt_s):
        for prompt in prompt_s:
            templated_prompt = apply_prompt_template(
                prompt, model_name, tokenizer)
            templated_prompts.append(templated_prompt)

    # Raise an error if the input is neither a single string nor a list of strings
    else:
        raise ValueError("Please provide a string or a list of strings.")

    return templated_prompts


def questions_prompt_template(questions, model_id, tokenizer):
    '''
    Works only for the question format
    '''
    templated_prompts = []

    for question in tqdm(questions):
        for j in range(len(question["turns"])):
            prompt = question["turns"][j]

            templated_prompt = apply_prompt_template(
                prompt, model_id, tokenizer)

            templated_prompts.append(templated_prompt)

    return templated_prompts