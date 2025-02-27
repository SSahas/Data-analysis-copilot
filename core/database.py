# src/core/database.py

import sqlite3
import pandas as pd
from typing import Tuple, Optional
import os

class DatabaseManager:
    def __init__(self, db_path: str):
        """
        Initialize DatabaseManager with database path
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self._validate_db_path()

    def _validate_db_path(self):
        """Validate that the database file exists"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found at: {self.db_path}")

    def execute_query(self, query: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Execute an SQL query and return results as a DataFrame
        
        Args:
            query (str): SQL query to execute
            
        Returns:
            Tuple[Optional[pd.DataFrame], Optional[str]]: 
                - DataFrame with results if successful, None if failed
                - Error message if failed, None if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df, None
        except Exception as e:
            error_message = f"Error executing query: {str(e)}"
            return None, error_message

    def get_table_schema(self, table_name: str) -> Optional[str]:
        """
        Get the schema of a specific table
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            Optional[str]: Table schema if successful, None if failed
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            schema = cursor.fetchone()
            conn.close()
            return schema[0] if schema else None
        except Exception as e:
            print(f"Error getting table schema: {e}")
            return None
