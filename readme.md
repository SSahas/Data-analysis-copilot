# Data Analysis Copilot

Data Analysis Copilot is an AI-powered tool that helps you analyze data using natural language queries. It combines the power of LLMs with SQL and Python to provide interactive data analysis capabilities.

## Features

- Natural language to SQL query conversion
- Automated data analysis code generation
- Interactive Streamlit interface
- Support for SQLite databases
- Visualization capabilities

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/data-analysis-copilot.git
cd data-analysis-copilot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run src/app.py
```

2. Upload your SQLite database file through the interface.

3. Enter your analysis questions in natural language.

4. View the generated SQL queries, analysis code, and results.

## Project Structure

```
data-analysis-copilot/
├── src/                    # Source code
│   ├── app.py             # Streamlit application
│   ├── config.py          # Configuration settings
│   ├── core/              # Core functionality
│   ├── services/          # Business logic services
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## Dependencies

- Python 3.8+
- Streamlit
- Transformers
- PyTorch
- Pandas
- SQLite3
- Other dependencies listed in requirements.txt

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
