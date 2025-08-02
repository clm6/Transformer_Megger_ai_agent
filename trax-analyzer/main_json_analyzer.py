#!/usr/bin/env python3
"""
TRANSFORMER DIAGNOSTIC AGENT - Main JSON Analyzer v3.0 - Predictive Maintenance Enhanced
Purpose: Analyze transformer TRAX test reports and extract structured JSON data
for trend analytics, dashboard visualization, and predictive maintenance planning

PREDICTIVE MAINTENANCE v3.0:
- Asset Health Score calculation (0-100%) with component weighting breakdown
- Predictive maintenance planning with component-specific timelines
- Anomaly scoring (0-10) for operational risk assessment
- Replacement forecasting with cost category planning
- Template variable generation for comprehensive reporting
- Degradation trend analysis and remaining life estimation
- All v2.4 technical features retained: enhanced TTR, PF thresholds, completeness validation
- Advanced condition assessment with lifecycle management capabilities
"""

import sys
import os
import json
import csv
import pandas as pd
from datetime import datetime
from trax_parser import extract_text_from_pdf, extract_substation_name, extract_document_date
from trax_analyzer_json import analyze_trax_report_json

def process_file_json(file_path, equipment_name=None):
    """Process a single PDF file and return JSON analysis with document date"""
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(file_path)
        
        # Extract document date
        document_date = extract_document_date(file_path, text)
        
        # If equipment name not provided, extract it from the text
        if not equipment_name:
            equipment_name = extract_substation_name(text)
        
        # Get AI analysis with document date
        analysis = analyze_trax_report_json(text, document_date, os.path.basename(file_path))
        return analysis, equipment_name, document_date
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
        return None, None, None

def extract_json_from_response(response_text):
    """Extract JSON and human-readable parts from AI response"""
    try:
        # Find JSON part (between first { and last })
        start_idx = response_text.find('{')
        if start_idx == -1:
            print("❌ No JSON found in response")
            return None, response_text
        
        # Find the matching closing brace
        brace_count = 0
        end_idx = start_idx
        for i, char in enumerate(response_text[start_idx:], start_idx):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i
                    break
        
        json_str = response_text[start_idx:end_idx + 1]
        human_readable = response_text[end_idx + 1:].strip()
        
        # Parse JSON
        json_data = json.loads(json_str)
        
        return json_data, human_readable
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return None, response_text
    except Exception as e:
        print(f"❌ Error extracting JSON: {e}")
        return None, response_text

def create_organized_folders(base_path):
    """Create organized folder structure for outputs"""
    folders = {
        'reports': os.path.join(base_path, 'Reports'),
        'json_data': os.path.join(base_path, 'JSON_Data'),
        'dashboard_csvs': os.path.join(base_path, 'Dashboard_CSVs'),
        'word_reports': os.path.join(base_path, 'Word_Reports')
    }
    
    for folder_path in folders.values():
        os.makedirs(folder_path, exist_ok=True)
    
    return folders

def export_to_csv_for_dashboard(all_json_data, output_folder):
    """Export JSON data to CSV files for dashboard visualization"""
    
    # Prepare data for different CSV files
    winding_data = []
    tan_delta_data = []
    bushing_data = []
    turns_ratio_data = []
    health_data = []
    
    for equipment_name, json_data in all_json_data.items():
        # Extract winding resistance data
        if 'winding_resistance' in json_data:
            # LV windings
            if 'lv_windings' in json_data['winding_resistance']:
                for winding in json_data['winding_resistance']['lv_windings']:
                    winding_data.append({
                        'equipment_name': equipment_name,
                        'winding_type': 'LV',
                        'phase': winding.get('phase', ''),
                        'tap_position': winding.get('tap_position', ''),
                        'resistance': winding.get('resistance_mohm', 0),
                        'unit': 'mΩ',
                        'stability_percent': winding.get('stability_percent', 0),
                        'variation_percent': winding.get('variation_percent', 0)
                    })
            
            # HV windings
            if 'hv_windings' in json_data['winding_resistance']:
                for winding in json_data['winding_resistance']['hv_windings']:
                    winding_data.append({
                        'equipment_name': equipment_name,
                        'winding_type': 'HV',
                        'phase': winding.get('phase', ''),
                        'tap_position': winding.get('tap_position', ''),
                        'resistance': winding.get('resistance_ohm', 0),
                        'unit': 'Ω',
                        'stability_percent': winding.get('stability_percent', 0),
                        'variation_percent': winding.get('variation_percent', 0)
                    })
        
        # Extract tan delta data
        if 'tan_delta' in json_data:
            for section, data in json_data['tan_delta'].items():
                tan_delta_data.append({
                    'equipment_name': equipment_name,
                    'section': section,
                    'pf_20c_percent': data.get('pf_20c_percent', 0),
                    'status': data.get('status', ''),
                    'threshold': data.get('threshold_applied', '')
                })
        
        # Extract bushing data
        if 'bushing_pf' in json_data:
            for bushing_id, data in json_data['bushing_pf'].items():
                bushing_data.append({
                    'equipment_name': equipment_name,
                    'bushing_id': bushing_id,
                    'pf_20c_percent': data.get('pf_20c_percent', 0),
                    'pf_1hz_percent': data.get('pf_1hz_percent', 0),
                    'status': data.get('status', ''),
                    'remarks': data.get('remarks', '')
                })
        
        # Extract turns ratio data (robust handling of all formats)
        if 'turns_ratio' in json_data and json_data['turns_ratio']:
            ratio_list = json_data['turns_ratio']
            # Handle v2.4 format with 'measurements' key
            if isinstance(ratio_list, dict) and 'measurements' in ratio_list:
                ratio_list = ratio_list['measurements']
            # Handle both list and single measurement formats
            if not isinstance(ratio_list, list):
                ratio_list = [ratio_list]
            
            for ratio_data in ratio_list:
                # Skip if ratio_data is not a dictionary (malformed data)
                if not isinstance(ratio_data, dict):
                    continue
                    
                turns_ratio_data.append({
                    'equipment_name': equipment_name,
                    'tap_position': ratio_data.get('tap_position', ''),
                    'nominal_ttr': ratio_data.get('nominal_ttr', 0),
                    'measured_ttr': ratio_data.get('measured_ttr', 0),
                    'error_percent': ratio_data.get('error_percent', 0),
                    'excitation_current_ua': ratio_data.get('excitation_current_ua', 0),
                    'excitation_current_ma': ratio_data.get('excitation_current_ma', 0),
                    'phase_displacement_deg': ratio_data.get('phase_displacement_deg', 0)
                })
        
        # Extract health assessment data (handle both v2.3 and v2.4 formats)
        health_key = 'health_assessment_technical_complete' if 'health_assessment_technical_complete' in json_data else 'health_assessment_master_enhanced' if 'health_assessment_master_enhanced' in json_data else 'health_assessment'
        if health_key in json_data:
            for category, data in json_data[health_key].items():
                # Skip non-dict entries (like strings or other data types)
                if not isinstance(data, dict):
                    continue
                health_data.append({
                    'equipment_name': equipment_name,
                    'category': category.replace('_', ' ').title(),
                    'status': data.get('status', ''),
                    'comments': data.get('comments', '')
                })
    
    # Write CSV files
    csv_files = []
    
    # Winding resistance CSV
    winding_csv = os.path.join(output_folder, 'winding_resistance_dashboard.csv')
    with open(winding_csv, 'w', newline='', encoding='utf-8') as f:
        if winding_data:
            writer = csv.DictWriter(f, fieldnames=['equipment_name', 'winding_type', 'phase', 'tap_position', 'resistance', 'unit', 'stability_percent', 'variation_percent'])
            writer.writeheader()
            writer.writerows(winding_data)
    csv_files.append(winding_csv)
    
    # Tan delta CSV
    tan_delta_csv = os.path.join(output_folder, 'tan_delta_dashboard.csv')
    with open(tan_delta_csv, 'w', newline='', encoding='utf-8') as f:
        if tan_delta_data:
            writer = csv.DictWriter(f, fieldnames=['equipment_name', 'section', 'pf_20c_percent', 'status', 'threshold'])
            writer.writeheader()
            writer.writerows(tan_delta_data)
    csv_files.append(tan_delta_csv)
    
    # Bushing CSV
    bushing_csv = os.path.join(output_folder, 'bushing_pf_dashboard.csv')
    with open(bushing_csv, 'w', newline='', encoding='utf-8') as f:
        if bushing_data:
            writer = csv.DictWriter(f, fieldnames=['equipment_name', 'bushing_id', 'pf_20c_percent', 'pf_1hz_percent', 'status', 'remarks'])
            writer.writeheader()
            writer.writerows(bushing_data)
    csv_files.append(bushing_csv)
    
    # Turns ratio CSV
    turns_ratio_csv = os.path.join(output_folder, 'turns_ratio_dashboard.csv')
    with open(turns_ratio_csv, 'w', newline='', encoding='utf-8') as f:
        if turns_ratio_data:
            writer = csv.DictWriter(f, fieldnames=['equipment_name', 'tap_position', 'nominal_ttr', 'measured_ttr', 'error_percent', 'excitation_current_ua', 'excitation_current_ma', 'phase_displacement_deg'])
            writer.writeheader()
            writer.writerows(turns_ratio_data)
    csv_files.append(turns_ratio_csv)
    
    # Health assessment CSV
    health_csv = os.path.join(output_folder, 'health_assessment_dashboard.csv')
    with open(health_csv, 'w', newline='', encoding='utf-8') as f:
        if health_data:
            writer = csv.DictWriter(f, fieldnames=['equipment_name', 'category', 'status', 'comments'])
            writer.writeheader()
            writer.writerows(health_data)
    csv_files.append(health_csv)
    
    return csv_files

def main_json_analyzer(folder_path):
    """Main function to process TRAX reports and generate organized outputs"""
    
    print("🔍 TRANSFORMER DIAGNOSTIC AGENT v3.0 - PREDICTIVE MAINTENANCE ENHANCED")
    print("=" * 70)
    print("🧠 Asset Health Scoring + Predictive Planning + Lifecycle Management + All v2.4")
    print("=" * 70)
    
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return
    
    # Create organized folder structure
    folders = create_organized_folders(folder_path)
    
    # Get all PDF files
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"❌ No PDF files found in {folder_path}")
        return
    
    results = []
    all_json_data = {}
    
    for pdf_file in pdf_files:
        print(f"\n📄 Processing: {pdf_file}")
        file_path = os.path.join(folder_path, pdf_file)
        
        try:
            # Get analysis from JSON analyzer
            analysis, equipment_name, document_date = process_file_json(file_path)
            
            if not analysis:
                print(f"   ❌ Failed to analyze {pdf_file}")
                continue
            
            print(f"   📍 Equipment identified: {equipment_name}")
            print(f"   📅 Document date: {document_date}")
            
            # Extract JSON and human-readable parts
            json_data, human_readable = extract_json_from_response(analysis)
            
            if json_data:
                # Store for dashboard aggregation
                all_json_data[equipment_name] = json_data
                
                # Save individual JSON file
                json_filename = f"{equipment_name}_analysis.json"
                json_path = os.path.join(folders['json_data'], json_filename)
                
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
                
                # Save human-readable report
                report_filename = f"{equipment_name}_diagnostic_report.txt"
                report_path = os.path.join(folders['reports'], report_filename)
                
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(f"TRANSFORMER DIAGNOSTIC REPORT\n")
                    f.write(f"Equipment: {equipment_name}\n")
                    f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Source File: {pdf_file}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(human_readable)
                
                print(f"   ✅ JSON: {json_filename}")
                print(f"   ✅ Report: {report_filename}")
                
                results.append({
                    'equipment_name': equipment_name,
                    'source_file': pdf_file,
                    'json_file': json_filename,
                    'report_file': report_filename,
                    'status': 'Success'
                })
            else:
                print(f"   ❌ Failed to extract JSON from {pdf_file}")
                results.append({
                    'equipment_name': equipment_name or 'Unknown',
                    'source_file': pdf_file,
                    'json_file': 'N/A',
                    'report_file': 'N/A',
                    'status': 'Failed'
                })
                
        except Exception as e:
            print(f"   ❌ Error processing {pdf_file}: {str(e)}")
            results.append({
                'equipment_name': 'Error',
                'source_file': pdf_file,
                'json_file': 'N/A',
                'report_file': 'N/A',
                'status': f'Error: {str(e)}'
            })
    
    # Generate dashboard CSV files
    if all_json_data:
        print(f"\n📊 Generating dashboard CSV files...")
        csv_files = export_to_csv_for_dashboard(all_json_data, folders['dashboard_csvs'])
        print(f"   ✅ Generated {len(csv_files)} dashboard CSV files")
    
    # Create summary report
    summary_path = os.path.join(folders['reports'], 'processing_summary.csv')
    with open(summary_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['equipment_name', 'source_file', 'json_file', 'report_file', 'status'])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n🎉 ANALYSIS COMPLETE!")
    print("=" * 70)
    print(f"📊 Processed: {len(pdf_files)} PDF files")
    print(f"✅ Successful: {len([r for r in results if r['status'] == 'Success'])}")
    print(f"❌ Failed: {len([r for r in results if r['status'] != 'Success'])}")
    print(f"\n📁 Output Folders:")
    print(f"   📄 Reports: {folders['reports']}")
    print(f"   🔧 JSON Data: {folders['json_data']}")
    print(f"   📊 Dashboard CSVs: {folders['dashboard_csvs']}")
    print(f"   📝 Summary: processing_summary.csv")
    
    print(f"\n🔧 Dashboard Integration:")
    print(f"   • Import CSV files from Dashboard_CSVs folder")
    print(f"   • Use equipment_name as primary key for joining data")
    print(f"   • Set up alerts for CRITICAL status values")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main_json_analyzer.py <folder_path>")
        print("Example: python main_json_analyzer.py \"C:\\Users\\craig\\OneDrive\\Documents\\DPU\\Projects\\TRAX_Reports\"")
        sys.exit(1)
    
    main_json_analyzer(sys.argv[1]) 