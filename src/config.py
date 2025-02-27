# src/config.py

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model configuration
MODEL_CONFIG = {
    "model_name": "Qwen/Qwen2.5-Coder-3B-Instruct",
    "max_new_tokens": 2048,
}

# Database configuration
DB_CONFIG = {
    "temp_file_name": "temp_db.db",
    "analysis_file_name": "temp_analysis_data.csv",
}

# Application configuration
APP_CONFIG = {
    "title": "Data Analysis Copilot 🤖",
    "max_retries": 3,
}

# File paths
PATHS = {
    "temp_dir": "temp",
    "logs_dir": "logs",
}

# Create necessary directories
for directory in PATHS.values():
    os.makedirs(directory, exist_ok=True)
