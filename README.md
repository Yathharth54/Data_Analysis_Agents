# Automated Data Analysis Pipeline

This project implements an automated data analysis pipeline using Microsoft's AutoGen framework. It orchestrates multiple AI agents to perform comprehensive data analysis, visualization, and report generation.

## Features

- Automated dataset download from Hugging Face
- Multi-agent architecture for specialized tasks:
  - Data source management
  - Data quality assessment
  - Statistical analysis
  - Qualitative analysis
  - Data visualization
  - PDF report generation
- Quality scoring system for data assessment
- Automated visualization generation
- Comprehensive PDF report generation

## Prerequisites

- Python 3.8+
- Git LFS (for downloading large datasets)
- Required Python packages:
  ```
  autogen
  pandas
  numpy
  matplotlib
  seaborn
  fpdf
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd [repository-name]
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure API key:
   - Replace the API key in the `llm_config` dictionary with your own key

## Usage

1. Basic usage:
   ```python
   from safe1 import process_dataset
   
   dataset_url = "https://huggingface.co/datasets/your-dataset"
   process_dataset(dataset_url)
   ```

2. The pipeline will automatically:
   - Download the dataset
   - Assess data quality
   - Perform statistical analysis
   - Generate visualizations
   - Create a comprehensive PDF report

## Project Structure

- `safe1.py`: Main script containing all agent definitions and functions
- Generated directories:
  - `datasets/`: Downloaded dataset files
  - `quality_assessment/`: Data quality reports
  - `insights/`: Statistical and qualitative analysis results
  - `visualizations/`: Generated plots and charts
  - `output/`: Final PDF reports

## Agent Descriptions

1. **Data Source Manager**
   - Handles dataset downloading and file management
   - Uses Git LFS for large file handling

2. **Data Quality Assessment Agent**
   - Evaluates data completeness, consistency, accuracy, and uniqueness
   - Generates quality scores and detailed metrics

3. **Statistical Analysis Agent**
   - Performs descriptive statistics
   - Analyzes distributions and correlations

4. **Qualitative Analysis Agent**
   - Analyzes data structure and relationships
   - Handles categorical data analysis

5. **Visualization Agent**
   - Creates distribution plots
   - Generates correlation heatmaps

6. **Report Generation Agent**
   - Compiles analyses into a structured PDF report
   - Includes visualizations and metrics

## Quality Assessment Metrics

The quality assessment system evaluates four main aspects:

1. **Completeness** (25 points)
   - Non-missing values ratio
   - Complete records ratio
   - Key field completeness
   - Required field coverage

2. **Consistency** (25 points)
   - Format consistency
   - Value range compliance
   - Cross-field validation
   - Temporal consistency

3. **Accuracy** (25 points)
   - Valid value percentage
   - Outlier ratio
   - Statistical distribution fitness
   - Business rule compliance

4. **Uniqueness** (25 points)
   - Duplicate record ratio
   - Unique constraint validation
   - Primary key integrity
   - Referential integrity

## Output

The pipeline generates:
1. Quality assessment report (`quality_assessment.txt`)
2. Analysis insights (`insights.txt`)
3. Visualization files (PNG format)
4. Comprehensive PDF report combining all analyses

## Error Handling

The pipeline includes comprehensive error handling:
- Each function includes try-catch blocks
- Detailed error messages for debugging
- Graceful termination on critical errors

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

[Add your license information here]

## Contact

[Add your contact information here]
