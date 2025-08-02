#!/usr/bin/env python3
"""
TRAX AI Analyzer v3.0 - Test Script
Quick diagnostic and testing tool
"""

import os
import sys
from main_json_analyzer import process_file_json
from trax_analyzer_json import analyze_trax_report_json
from trax_parser import extract_text_from_pdf

def test_single_file():
    """Test processing a single PDF file with detailed output"""
    
    # Find a test file
    base_path = r"C:\Users\craig\OneDrive\Documents\DPU\transformer-diagnostic-ai\Projects\TRAX_Reports"
    test_files = [
        "TRAX - Test report.pdf",
        "Sub 2 transformer.pdf", 
        "L 247439A WRM and TTR Results.pdf"
    ]
    
    test_file = None
    for filename in test_files:
        full_path = os.path.join(base_path, filename)
        if os.path.exists(full_path):
            test_file = full_path
            break
    
    if not test_file:
        print("❌ No test files found!")
        return False
    
    print(f"🧪 Testing with: {os.path.basename(test_file)}")
    print("=" * 60)
    
    try:
        # Step 1: Test PDF extraction
        print("📄 Step 1: Testing PDF text extraction...")
        text = extract_text_from_pdf(test_file)
        if text:
            print(f"✅ Extracted {len(text)} characters")
            print(f"📝 First 200 chars: {text[:200]}...")
        else:
            print("❌ Failed to extract text")
            return False
        
        # Step 2: Test AI analysis
        print("\n🤖 Step 2: Testing AI analysis...")
        response = analyze_trax_report_json(text, "2022-01-01", "test.pdf")
        if response:
            print(f"✅ AI response received ({len(response)} characters)")
            print(f"📝 First 300 chars: {response[:300]}...")
            
            # Check if it looks like JSON
            if "```json" in response:
                print("✅ Response contains JSON markers")
            else:
                print("⚠️ No JSON markers found in response")
        else:
            print("❌ No AI response received")
            return False
        
        # Step 3: Test full processing
        print("\n🔄 Step 3: Testing full processing pipeline...")
        result = process_file_json(test_file)
        if result[0]:  # JSON data
            print("✅ Full processing succeeded!")
            print(f"📊 JSON keys: {list(result[0].keys())}")
        else:
            print("❌ Full processing failed")
            return False
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_api_connection():
    """Test if OpenAI API is working"""
    print("🔑 Testing OpenAI API connection...")
    
    try:
        from openai import OpenAI
        import os
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Simple test request
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say 'API test successful'"}],
            max_tokens=10
        )
        
        if response.choices[0].message.content:
            print("✅ OpenAI API connection successful")
            return True
        else:
            print("❌ OpenAI API response empty")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {e}")
        return False

def run_quick_analysis():
    """Run analysis on just one file for quick testing"""
    base_path = r"C:\Users\craig\OneDrive\Documents\DPU\transformer-diagnostic-ai\Projects\TRAX_Reports"
    
    # Find the smallest/quickest file
    test_file = os.path.join(base_path, "TRAX - Test report.pdf")
    
    if not os.path.exists(test_file):
        print("❌ Test file not found")
        return
    
    print(f"🚀 Quick analysis of: {os.path.basename(test_file)}")
    print("=" * 50)
    
    try:
        result = process_file_json(test_file)
        if result[0]:
            print("✅ Analysis successful!")
            # Show key results
            data = result[0]
            if 'asset_health_score' in data:
                score = data['asset_health_score'].get('calculated_score', 'N/A')
                condition = data['asset_health_score'].get('condition_category', 'N/A')
                print(f"🧠 Asset Health: {score}/100 ({condition})")
            
            if 'predictive_maintenance_plan' in data:
                anomaly = data['predictive_maintenance_plan'].get('anomaly_score', 'N/A')
                print(f"⚠️ Anomaly Score: {anomaly}/10")
            
            print(f"📊 Report sections: {len(data)} main categories")
        else:
            print("❌ Analysis failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔍 TRAX AI Analyzer v3.0 - Test Suite")
    print("=" * 50)
    
    # Run tests
    print("\n1. Testing API connection...")
    api_ok = test_api_connection()
    
    if api_ok:
        print("\n2. Running comprehensive test...")
        test_ok = test_single_file()
        
        if test_ok:
            print("\n3. Running quick analysis...")
            run_quick_analysis()
    else:
        print("⚠️ Skipping further tests due to API issues")
    
    print("\n🏁 Test suite complete!")