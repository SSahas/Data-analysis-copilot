# src/utils/prompts.py

from typing import Optional

def get_sql_prompt(
    user_input: str,
    table_statement: str,
    previous_sql_query: Optional[str] = None,
    execution_error: Optional[str] = None
) -> str:
    """
    Generate SQL query prompt
    
    Args:
        user_input (str): User's natural language query
        table_statement (str): Database table schema
        previous_sql_query (Optional[str]): Previous failed query
        execution_error (Optional[str]): Previous error message
        
    Returns:
        str: Generated prompt
    """
    return f"""
You are an SQL query generator. Given the table schema below, generate an SQL query to retrieve the relevant columns to answer the user's request if a query is necessary. If a query is not required, output a suitable reply for the user input. Only output the SQL query or reply without extra commentary.

USER INPUT: {user_input}

TABLE INFORMATION: {table_statement}

{f"Below is the information regarding the previous SQL query generated and error when executed, modify the query to fix the error while maintaining the original intent." if execution_error else ""}
{f"SQL Error: {execution_error}" if execution_error else ""}
{f"Previous SQL Query: {previous_sql_query}" if previous_sql_query else ""}

<sql_query>
"""

def get_analysis_prompt(
    user_input: str,
    table_info: str,
    previous_code: Optional[str] = None,
    execution_error: Optional[str] = None
) -> str:
    """
    Generate analysis code prompt
    
    Args:
        user_input (str): User's natural language query
        table_info (str): Sample data information
        previous_code (Optional[str]): Previous failed code
        execution_error (Optional[str]): Previous error message
        
    Returns:
        str: Generated prompt
    """
    return f"""
You are a data analysis assistant. Use the table information below to generate Python code that performs the analysis for the user's request. The code should load the CSV file from "temp_analysis_data.csv" and compute the main result, assigning it to a variable named 'result' which is returned at the end. Do not use print statements. Only output the Python code.
Generate the code such that the results should be shown on the streamlit app, like plotted graphs should be shown using "st.image()" function.


USER INPUT: {user_input}

TABLE INFORMATION:
{table_info}

{f"Below is the information regarding the previous code generated and error when executed, modify the code to fix the error while maintaining the original intent." if execution_error else None}
{f"Execution Error: {execution_error}" if execution_error else ""}
{f"Previous Python Code: {previous_code}" if previous_code else ""}

<python_code>
"""
