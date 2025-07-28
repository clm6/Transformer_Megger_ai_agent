from trax_parser import extract_text_from_pdf
from trax_analyzer import analyze_trax_report
import os
import csv

def process_file(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    report = analyze_trax_report(text)
    return report

def main(folder_path):
    results = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            print(f"Processing: {filename}")
            report = process_file(full_path)
            results.append({
                "Filename": filename,
                "Analysis": report
            })

    # Write all results to CSV
    csv_path = os.path.join(folder_path, "trax_diagnostics_summary.csv")
    with open(csv_path, mode="w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["Filename", "Analysis"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"\n✅ All reports exported to {csv_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py /path/to/folder")
    else:
        main(sys.argv[1])
