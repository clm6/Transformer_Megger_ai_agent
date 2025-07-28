#!/usr/bin/env python3
"""
Test script to verify substation name extraction
"""

import sys
from trax_parser import extract_text_from_pdf, extract_substation_name

def test_name_extraction(pdf_path):
    """Test the substation name extraction function"""
    
    print("🔍 TESTING SUBSTATION NAME EXTRACTION")
    print("=" * 50)
    
    try:
        # Extract text from PDF
        print(f"📄 Loading: {pdf_path}")
        text = extract_text_from_pdf(pdf_path)
        
        print(f"📝 Extracted {len(text)} characters of text")
        
        # Show first few lines of text
        lines = text.split('\n')[:15]
        print(f"\n📋 First 15 lines of text:")
        for i, line in enumerate(lines, 1):
            if line.strip():
                print(f"   {i:2d}: {line.strip()}")
        
        # Extract substation name
        print(f"\n🎯 Extracting substation name...")
        substation_name = extract_substation_name(text)
        
        print(f"✅ Identified Equipment: '{substation_name}'")
        
        # Show what the clean filename would be
        print(f"📁 Clean filename base: '{substation_name}'")
        print(f"📄 Example files would be:")
        print(f"   - {substation_name}_analysis.json")
        print(f"   - {substation_name}_diagnostic_report.txt")
        print(f"   - {substation_name}_word_report.docx")
        
        return substation_name
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_name_extraction.py <pdf_path>")
        print("Example: python test_name_extraction.py \"C:\\Users\\craig\\Downloads\\TRAX_Reports\\TRAX - Test report (1).pdf\"")
        sys.exit(1)
    
    test_name_extraction(sys.argv[1]) 