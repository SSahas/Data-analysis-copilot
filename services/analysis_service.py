# src/services/analysis_service.py

import pandas as pd
from typing import Optional, Tuple
from core.model import get_model_instance
from utils.prompts import get_analysis_prompt
from utils.helpers import extract_python_code
import os

class AnalysisService:
    def __init__(self):
        """Initialize AnalysisService"""
        self.model = get_model_instance()

    def generate_analysis(
        self,
        user_query: str,
        data: pd.DataFrame,
        previous_code: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate and execute data analysis code
        
        Args:
            user_query (str): User's natural language query
            data (pd.DataFrame): Data to analyze
            previous_code (Optional[str]): Previously failed code
            error_message (Optional[str]): Previous error message
            
        Returns:
            Tuple[Optional[str], Optional[str]]:
                - Generated Python code if successful, None if failed
                - Error message if failed, None if successful
        """
        max_attempts = 3
        attempts = 0
        
        # Save data temporarily for analysis
        temp_csv_path = "temp_analysis_data.csv"
        data.to_csv(temp_csv_path, index=False)
        
        try:
            while attempts < max_attempts:
                # Generate prompt
                prompt = get_analysis_prompt(
                    user_query,
                    data.head().to_string(),
                    previous_code,
                    error_message
                )
                
                # Get response from model
                python_response = self.model.generate_response(prompt)
                code = extract_python_code(python_response)
                
                try:
                    # Create a local namespace for execution
                    local_namespace = {'pd': pd}
                    
                    # Execute the code
                    exec(code, {}, local_namespace)
                    
                    return code, None
                    
                except Exception as e:
                    error_message = f"Error executing code: {str(e)}"
                    previous_code = code
                    attempts += 1
            
            return None, f"Failed after {max_attempts} attempts. Last error: {error_message}"
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_csv_path):
                os.remove(temp_csv_path)
