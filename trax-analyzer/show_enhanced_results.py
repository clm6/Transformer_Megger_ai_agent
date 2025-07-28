import pandas as pd
import os

# Path to the enhanced analysis file
file_path = r'C:\Users\craig\Downloads\TRAX_Reports\trax_enhanced_diagnostics_summary.csv'

if os.path.exists(file_path):
    print("📊 ENHANCED TRAX TECHNICAL ANALYSIS")
    print("=" * 80)
    
    df = pd.read_csv(file_path)
    print(f"File: {df['Filename'].iloc[0]}")
    print("-" * 80)
    print(df['Enhanced_Technical_Analysis'].iloc[0])
else:
    print("❌ Enhanced analysis file not found at:", file_path)
    print("Available files in TRAX_Reports directory:")
    reports_dir = r'C:\Users\craig\Downloads\TRAX_Reports'
    if os.path.exists(reports_dir):
        for file in os.listdir(reports_dir):
            print(f"  - {file}") 