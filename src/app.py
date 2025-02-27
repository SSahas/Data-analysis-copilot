# src/app.py

import streamlit as st
import pandas as pd
from core.database import DatabaseManager
from services.sql_service import SQLService
from services.analysis_service import AnalysisService
import os

def init_session_state():
    """Initialize session state variables"""
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = None
    if 'sql_service' not in st.session_state:
        st.session_state.sql_service = None
    if 'analysis_service' not in st.session_state:
        st.session_state.analysis_service = None

def setup_services(db_path):
    """Set up database and analysis services"""
    try:
        db_manager = DatabaseManager(db_path)
        st.session_state.db_manager = db_manager
        st.session_state.sql_service = SQLService(db_manager)
        st.session_state.analysis_service = AnalysisService()
        return True
    except Exception as e:
        st.error(f"Error setting up services: {str(e)}")
        return False

def main():
    st.title("Data Analysis Copilot 🤖")
    
    init_session_state()
    
    st.sidebar.header("Database Connection")
    uploaded_file = st.sidebar.file_uploader("Upload SQLite Database", type=['db'])
    
    if uploaded_file:
        with open("temp_db.db", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        if setup_services("temp_db.db"):
            st.sidebar.success("Database connected successfully!")
            
            table_schema = st.session_state.db_manager.get_table_schema("PEOPLE_DATA")
            if table_schema:
                st.sidebar.text("Table Schema:")
                st.sidebar.code(table_schema)
            
            st.header("Ask Your Question")
            user_query = st.text_area("What would you like to analyze?", 
                                    placeholder="e.g., Show me the average income by city")
            
            if st.button("Analyze"):
                if user_query:
                    with st.spinner("Generating SQL query..."):
                        df, sql_query, error = st.session_state.sql_service.generate_sql_query(
                            user_query, table_schema
                        )
                        
                        if error:
                            st.error(error)
                        else:
                            st.subheader("SQL Query")
                            st.code(sql_query, language="sql")
                            
                            st.subheader("Retrieved Data Sample")
                            st.dataframe(df.head())
                            
                            with st.spinner("Generating analysis..."):
                                analysis_code, analysis_error = st.session_state.analysis_service.generate_analysis(
                                    user_query, df
                                )
                                
                                if analysis_error:
                                    st.error(analysis_error)
                                else:
                                    st.subheader("Analysis Code")
                                    st.code(analysis_code, language="python")
                                    
                                    # Execute analysis and show results
                                    try:
                                        local_namespace = {'pd': pd, 'df': df}
                                        exec(analysis_code, {}, local_namespace)
                                        result = local_namespace.get('result')
                                        
                                        st.subheader("Analysis Result")
                                        if isinstance(result, pd.DataFrame):
                                            st.dataframe(result)
                                        else:
                                            st.write(result)
                                            
                                    except Exception as e:
                                        #st.error(f"Error displaying results: {str(e)}")
                                        pass
                else:
                    st.warning("Please enter a question to analyze.")
                    
        
        # Cleanup temporary file
        if os.path.exists("temp_db.db"):
            os.remove("temp_db.db")
    
    else:
        st.info("Please upload a SQLite database file to begin analysis.")
        
if __name__ == "__main__":
    main()
