# Multi-Agent Data Analysis System

## Overview
This project implements an automated data analysis system using multiple specialized agents. The system can download datasets from Hugging Face, perform comprehensive data analysis, and generate detailed reports automatically.

## Features
- Automated dataset download from Hugging Face repositories
- Comprehensive data quality assessment
- Statistical and qualitative analysis
- Automated visualization generation
- PDF report generation
- Multi-agent architecture for specialized tasks

## System Requirements
- Python 3.x
- Git LFS (for downloading datasets)
- Required Python packages:
  - autogen
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - fpdf

## Project Structure
```
├── agents.py           # Agent definitions and initialization
├── config.py          # Configuration settings
├── main.py            # Main application entry point
├── system_messages.py # Agent system messages/instructions
└── utils.py           # Utility functions for data processing
```

## Agent Roles
1. **Data Source Manager**: Handles dataset downloading and file management
2. **Data Quality Agent**: Assesses dataset quality and completeness
3. **Statistical Analysis Agent**: Performs numerical analysis and statistics
4. **Qualitative Analysis Agent**: Analyzes data structure and patterns
5. **Visualization Agent**: Creates data visualizations
6. **Report Generation Agent**: Compiles findings into PDF reports

## Setup Instructions

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Install dependencies:
```bash
pip install autogen pandas numpy matplotlib seaborn fpdf
```

3. Configure the API key:
   - Open `config.py`
   - Replace `"ENTER YOUR API KEY"` with your actual API key

## Usage

1. Basic usage:
```python
from main import process_dataset

# Process a dataset from Hugging Face
process_dataset("https://huggingface.co/datasets/scikit-learn/iris")
```

2. Output structure:
```
datasets/
├── quality_assessment/
│   └── quality_assessment.txt
├── insights/
│   └── insights.txt
├── visualizations/
│   ├── correlation_heatmap.png
│   └── feature_distributions.png
└── output/
    └── analysis_report.pdf
```

## Key Components

### agents.py
- Defines and initializes all agent types
- Configures agent behaviors and capabilities
- Registers execution functions for each agent

### config.py
- Contains LLM configuration
- API key settings
- Model specifications

### main.py
- Sets up the group chat between agents
- Manages the orchestration of the analysis workflow
- Provides the main entry point for processing datasets

### system_messages.py
- Defines the role and responsibilities of each agent
- Contains system prompts for agent behavior
- Establishes workflow protocols

### utils.py
- Implements core functionality for:
  - Dataset downloading
  - Quality assessment
  - Statistical analysis
  - Visualization generation
  - Report creation

## Quality Assessment Metrics

The system evaluates datasets on four key dimensions:
1. **Completeness** (25 points)
2. **Consistency** (25 points)
3. **Accuracy** (25 points)
4. **Uniqueness** (25 points)

Total quality score is calculated out of 100 points.

## Error Handling

The system includes comprehensive error handling for:
- Dataset download failures
- File access issues
- Data processing errors
- Report generation problems

Each function includes try-catch blocks with detailed error messages.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
