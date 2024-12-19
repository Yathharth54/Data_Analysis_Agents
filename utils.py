# utils.py
import os
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from fpdf import FPDF
from typing import Dict, List, Annotated

def download_dataset_via_git(
    repo_url: Annotated[str, "The Hugging Face dataset repository URL."],
    local_path: Annotated[str, "Directory to save the cloned dataset."] = "/Users/yathharthkaranjikar/datasets"
) -> str:
    try:
        local_path = os.path.abspath(local_path)
        os.makedirs(local_path, exist_ok=True)
        subprocess.run(["git", "lfs", "install"], check=True)
        subprocess.run(["git", "clone", repo_url, local_path], check=True)
        return f"Dataset successfully cloned to {local_path}"
    except Exception as e:
        raise ValueError(f"Error during download: {e}")

def get_dataset_file_paths(
    dataset_path: Annotated[str, "Dataset Path"] = "/Users/yathharthkaranjikar/datasets",
    file_extensions: str = None
) -> Dict[str, List[str]]:
    try:
        if not os.path.exists(dataset_path):
            raise ValueError(f"Dataset path does not exist: {dataset_path}")
        
        file_paths = {}
        for root, _, files in os.walk(dataset_path):
            if '.git' in root:
                continue
            for filename in files:
                full_path = os.path.join(root, filename)
                file_ext = os.path.splitext(filename)[1].lower()
                if file_extensions is None or file_ext in file_extensions:
                    if file_ext not in file_paths:
                        file_paths[file_ext] = []
                    file_paths[file_ext].append(full_path)
        return file_paths
    except Exception as e:
        raise ValueError(f"Error finding files: {e}")

def assess_data_quality(dataset_path: str) -> Dict:
    try:
        df = pd.read_csv(dataset_path)
        
        def calculate_completeness_score(df):
            total_score = 0
            non_missing_ratio = 1 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]))
            total_score += non_missing_ratio * 10
            
            complete_records_ratio = 1 - (df.isnull().any(axis=1).sum() / len(df))
            total_score += complete_records_ratio * 5
            
            key_fields = df.columns[:2]
            key_completeness = 1 - (df[key_fields].isnull().sum().sum() / (len(df) * len(key_fields)))
            total_score += key_completeness * 5
            
            required_fields_present = sum([1 for col in df.columns if col in df.columns]) / len(df.columns)
            total_score += required_fields_present * 5
            
            return total_score

        def calculate_consistency_score(df):
            total_score = 0
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            format_consistency = len(numeric_cols) / len(df.columns)
            total_score += format_consistency * 7
            
            for col in numeric_cols:
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                within_range = (z_scores < 3).mean()
                total_score += (within_range * 6) / len(numeric_cols)
            
            total_score += 12  # Simplified scores for cross-field and temporal consistency
            
            return total_score

        def calculate_accuracy_score(df):
            total_score = 0
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            valid_values = df[numeric_cols].apply(lambda x: np.sum(~np.isnan(x)) / len(x))
            total_score += valid_values.mean() * 7
            
            outlier_scores = []
            for col in numeric_cols:
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outlier_ratio = 1 - (np.sum(z_scores > 3) / len(df))
                outlier_scores.append(outlier_ratio)
            total_score += np.mean(outlier_scores) * 6
            
            total_score += 12  # Simplified scores for distribution and business rules
            
            return total_score

        def calculate_uniqueness_score(df):
            total_score = 0
            
            duplicate_ratio = 1 - (df.duplicated().sum() / len(df))
            total_score += duplicate_ratio * 7
            
            unique_ratios = df.nunique() / len(df)
            total_score += unique_ratios.mean() * 6
            
            if 'Id' in df.columns:
                pk_integrity = len(df['Id'].unique()) == len(df)
                total_score += 6 if pk_integrity else 0
            
            total_score += 6  # Simplified score for referential integrity
            
            return total_score

        quality_scores = {
            'completeness': calculate_completeness_score(df),
            'consistency': calculate_consistency_score(df),
            'accuracy': calculate_accuracy_score(df),
            'uniqueness': calculate_uniqueness_score(df)
        }
        
        total_score = sum(quality_scores.values())
        quality_report = {
            'scores': quality_scores,
            'total_score': total_score,
            'metadata': {
                'total_rows': len(df),
                'missing_values': df.isnull().sum().to_dict(),
                'duplicates': df.duplicated().sum(),
                'data_types': df.dtypes.to_dict(),
                'unique_values': {col: df[col].nunique() for col in df.columns}
            }
        }
        
        quality_dir = os.path.join(os.path.dirname(dataset_path), 'quality_assessment')
        os.makedirs(quality_dir, exist_ok=True)
        with open(os.path.join(quality_dir, 'quality_assessment.txt'), 'w') as f:
            f.write("Data Quality Assessment\n")
            f.write("=====================\n\n")
            f.write("Quality Scores:\n")
            for category, score in quality_scores.items():
                f.write(f"{category.title()}: {score:.2f}/25\n")
            f.write(f"\nTotal Score: {total_score:.2f}/100\n\n")
            f.write("\nDetailed Metrics:\n")
            for metric, value in quality_report['metadata'].items():
                f.write(f"{metric}:\n{value}\n\n")
        
        return quality_report
    
    except Exception as e:
        raise ValueError(f"Error in quality assessment: {e}")

def perform_statistical_analysis(dataset_path: str) -> str:
    try:
        df = pd.read_csv(dataset_path)
        insights_dir = os.path.join(os.path.dirname(dataset_path), 'insights')
        os.makedirs(insights_dir, exist_ok=True)
        
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        stats_report = {
            'descriptive_stats': df[numerical_cols].describe(),
            'correlations': df[numerical_cols].corr()
        }
        
        with open(os.path.join(insights_dir, 'insights.txt'), 'a') as f:
            f.write("\nStatistical Analysis\n")
            f.write("===================\n\n")
            for metric, value in stats_report.items():
                f.write(f"{metric}:\n{value}\n\n")
        
        return "Statistical analysis completed and saved."
    except Exception as e:
        raise ValueError(f"Error in statistical analysis: {e}")

def perform_qualitative_analysis(dataset_path: str) -> str:
    try:
        df = pd.read_csv(dataset_path)
        categorical_cols = df.select_dtypes(include=['object']).columns
        qual_report = {
            'categorical_summaries': {col: df[col].value_counts() for col in categorical_cols},
            'missing_patterns': df.isnull().sum(),
            'data_structure': df.dtypes
        }
        
        with open(os.path.join(os.path.dirname(dataset_path), 'insights', 'insights.txt'), 'a') as f:
            f.write("\nQualitative Analysis\n")
            f.write("===================\n\n")
            for metric, value in qual_report.items():
                f.write(f"{metric}:\n{value}\n\n")
        
        return "Qualitative analysis completed and saved."
    except Exception as e:
        raise ValueError(f"Error in qualitative analysis: {e}")

def create_visualizations(dataset_path: str) -> str:
    try:
        df = pd.read_csv(dataset_path)
        vis_dir = os.path.join(os.path.dirname(dataset_path), 'visualizations')
        os.makedirs(vis_dir, exist_ok=True)
        
        numerical_cols = df.select_dtypes(include=['number']).columns
        
        for col in numerical_cols[:5]:
            plt.figure(figsize=(10, 6))
            sns.histplot(df[col], kde=True)
            plt.title(f'Distribution of {col}')
            plt.savefig(os.path.join(vis_dir, f'{col}_distribution.png'))
            plt.close()
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(df[numerical_cols].corr(), annot=True, cmap='coolwarm')
        plt.title('Correlation Heatmap')
        plt.savefig(os.path.join(vis_dir, 'correlation_heatmap.png'))
        plt.close()
        
        return "Visualizations created and saved."
    except Exception as e:
        raise ValueError(f"Error creating visualizations: {e}")
    
def generate_pdf_report(dataset_dir: str) -> str:
    try:
        # Initialize PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Create output directory
        output_dir = os.path.join(dataset_dir, 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Title page
        pdf.add_page()
        pdf.set_font('Arial', 'B', 24)
        pdf.cell(0, 20, 'Data Analysis Report', ln=True, align='C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d")}', ln=True, align='C')
        
        # Quality Assessment
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Quality Assessment', ln=True)
        pdf.set_font('Arial', '', 12)
        
        quality_path = os.path.join(dataset_dir, 'quality_assessment', 'quality_assessment.txt')
        if os.path.exists(quality_path):
            with open(quality_path, 'r') as f:
                pdf.multi_cell(0, 10, f.read())
        
        # Analysis Insights
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Analysis Insights', ln=True)
        pdf.set_font('Arial', '', 12)
        
        insights_path = os.path.join(dataset_dir, 'insights', 'insights.txt')
        if os.path.exists(insights_path):
            with open(insights_path, 'r') as f:
                pdf.multi_cell(0, 10, f.read())
        
        # Visualizations
        vis_dir = os.path.join(dataset_dir, 'visualizations')
        if os.path.exists(vis_dir):
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, 'Visualizations', ln=True)
            
            for img_file in os.listdir(vis_dir):
                if img_file.endswith('.png'):
                    pdf.add_page()
                    pdf.set_font('Arial', 'B', 12)
                    title = img_file.replace('.png', '').replace('_', ' ').title()
                    pdf.cell(0, 10, title, ln=True)
                    pdf.image(os.path.join(vis_dir, img_file), x=10, w=190)
        
        # Save the report
        output_path = os.path.join(output_dir, 'analysis_report.pdf')
        pdf.output(output_path)
        
        return f"Report successfully generated at {output_path} TERMINATE"
    except Exception as e:
        raise ValueError(f"Error generating PDF report: {e}")