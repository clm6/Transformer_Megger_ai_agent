from trax_parser import extract_text_from_pdf
from trax_analyzer_enhanced import analyze_trax_report_enhanced
import os
import csv

def process_file_enhanced(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    report = analyze_trax_report_enhanced(text)
    return report

def main_enhanced(folder_path):
    results = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            print(f"🔍 Processing: {filename}")
            report = process_file_enhanced(full_path)
            results.append({
                "Filename": filename,
                "Enhanced_Technical_Analysis": report
            })

    # Write all results to CSV
    csv_path = os.path.join(folder_path, "trax_enhanced_diagnostics_summary.csv")
    with open(csv_path, mode="w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["Filename", "Enhanced_Technical_Analysis"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"\n✅ Enhanced analysis exported to {csv_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main_enhanced.py /path/to/folder")
        print("This will generate detailed technical analysis with numerical breakdowns")
    else:
        main_enhanced(sys.argv[1]) 