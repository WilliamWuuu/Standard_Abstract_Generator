import os
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

text_data_path = ""
summary_data_path = ""
model_path = ""

# Load the model and tokenizer from the local directory
def load_model(model_directory):
    """
    Loads the summarization model from a local directory.

    Args:
        model_directory (str): Path to the local model directory.

    Returns:
        pipeline: A Hugging Face pipeline object.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_directory)
    model = AutoModelForCausalLM.from_pretrained(model_directory)
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

# Summarize text using the local model and custom prompt
def summarize_text(model_pipeline, text, max_length=512, temperature=0.7):
    """
    Summarizes the given text using the model pipeline with a custom prompt.

    Args:
        model_pipeline (pipeline): The Hugging Face pipeline for text generation.
        text (str): The input text.
        max_length (int): Maximum length of the generated summary.
        temperature (float): Sampling temperature for text generation.

    Returns:
        str: The summarized text.
    """
    prompt = (
        f"目标：请总结以下文本的主要内容。\n\n"
        f"要求：\n"
        f"1. 提取每部分的核心要点，包括关键概念、目标或指导原则。\n"
        f"2. 确保总结结构清晰简洁，重点突出。\n\n"
        f"注意：\n"
        f"1. 避免使用过于复杂的术语。\n"
        f"2. 特别关注领域专业人士关心的信息，如：适用范围、专业术语定义、具体规范要求、关键技术指标\n\n"
        f"请确保总结准确传达原文的上下文和意图。\n\n"
        f"文本:\n{text}"
    )
    response = model_pipeline(prompt, max_length=max_length, temperature=temperature, num_return_sequences=1)
    return response[0]["generated_text"].split("文本:")[-1].strip()  # Adjust if the output format is different.

# Load the model
model_pipeline = load_model(model_path)

# Ensure the output directory exists
os.makedirs(summary_data_path, exist_ok=True)

# Process each text file in the input directory
for filename in os.listdir(text_data_path):
    if filename.endswith(".txt"):
        input_file_path = os.path.join(text_data_path, filename)
        output_file_path = os.path.join(summary_data_path, filename)
        
        # Read the input file
        with open(input_file_path, "r", encoding="utf-8") as file:
            text = file.read()
        
        # Summarize the text
        summary = summarize_text(model_pipeline, text)
        
        # Write the summary to the output file
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(summary)
        
        print(f"Processed {filename}: Summary saved to {output_file_path}")

print("Summarization complete.")