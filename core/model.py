# src/core/model.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class LLMModel:
    def __init__(self):
        """Initialize the LLM model with configurations"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        self.setup_model()

    def setup_model(self):
        """Set up the model with quantization configuration"""
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            "Qwen/Qwen2.5-Coder-3B-Instruct",
            use_safetensors=True,
            low_cpu_mem_usage=True,
            quantization_config=quantization_config,
            device_map=self.device
        )
        
        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-3B-Instruct")

    def generate_response(self, prompt: str, max_new_tokens: int = 2048) -> str:
        """
        Generate response from the model for a given prompt
        
        Args:
            prompt (str): Input prompt for the model
            max_new_tokens (int): Maximum number of tokens to generate
            
        Returns:
            str: Generated response
        """
        messages = [
            {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=max_new_tokens
        )
        
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response.strip()

# Create a singleton instance
_model_instance = None

def get_model_instance():
    """Get or create a singleton instance of LLMModel"""
    global _model_instance
    if _model_instance is None:
        _model_instance = LLMModel()
    return _model_instance
