# src/utils/helpers.py

import re
from typing import Optional

def extract_python_code(text: str) -> str:
    """
    Extract Python code from text that may contain markdown code blocks
    
    Args:
        text (str): Text containing Python code
        
    Returns:
        str: Extracted Python code
    """
    # Try to find code between ```python and ``` markers
    pattern = r"```python\s*(.*?)\s*```"
    code_snippets = re.findall(pattern, text, re.DOTALL)
    
    if code_snippets:
        return code_snippets[0]
    
    # If no code blocks found, return the original text
    # after removing any potential ``` markers
    return text.replace("```", "").strip()

def clean_sql_response(response: str) -> str:
    """
    Clean SQL response from the model
    
    Args:
        response (str): Raw response from the model
        
    Returns:
        str: Cleaned SQL query
    """
    # Remove backticks and extra whitespace
    cleaned = response.strip('`').strip()
    
    # Remove "sql" prefix if present
    if cleaned.lower().startswith("sql\n"):
        cleaned = cleaned[4:]
    
    return cleaned.strip()
