# src/services/sql_service.py

from typing import Optional, Tuple
import pandas as pd
from core.model import get_model_instance
from core.database import DatabaseManager
from utils.prompts import get_sql_prompt

class SQLService:
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize SQLService with database manager
        
        Args:
            db_manager (DatabaseManager): Instance of DatabaseManager
        """
        self.db_manager = db_manager
        self.model = get_model_instance()

    def generate_sql_query(
        self, 
        user_query: str, 
        table_statement: str,
        previous_query: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> Tuple[Optional[pd.DataFrame], Optional[str], Optional[str]]:
        """
        Generate and execute SQL query based on user input
        
        Args:
            user_query (str): User's natural language query
            table_statement (str): Database table schema
            previous_query (Optional[str]): Previous failed query
            error_message (Optional[str]): Previous error message
            
        Returns:
            Tuple[Optional[pd.DataFrame], Optional[str], Optional[str]]:
                - DataFrame with results if successful, None if failed
                - Generated SQL query
                - Error message if failed, None if successful
        """
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            # Generate prompt
            prompt = get_sql_prompt(
                user_query,
                table_statement,
                previous_query,
                error_message
            )
            
            # Get response from model
            sql_response = self.model.generate_response(prompt)
            
            # Clean up response
            sql_query = sql_response.strip('`').strip()
            if sql_query.lower().startswith("sql\n"):
                sql_query = sql_query[4:]
            
            # Execute query
            df, error = self.db_manager.execute_query(sql_query)
            
            if df is not None:
                return df, sql_query, None
                
            previous_query = sql_query
            error_message = error
            attempts += 1
            
        return None, previous_query, f"Failed after {max_attempts} attempts. Last error: {error_message}"
