#!/usr/bin/env python3
"""
Test script to verify TRAX analyzer setup
"""

import os
from dotenv import load_dotenv
import openai

def test_setup():
    print("🔧 Testing TRAX Analyzer Setup...")
    print("-" * 40)
    
    # Test 1: Load environment
    try:
        load_dotenv()
        print("✅ Environment file loaded successfully")
    except Exception as e:
        print(f"❌ Environment loading failed: {e}")
        return False
    
    # Test 2: Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OpenAI API key found")
        print(f"   Key starts with: {api_key[:20]}...")
        if api_key.endswith("02.2."):
            print("⚠️  WARNING: API key format appears incomplete")
            print("   OpenAI keys typically don't end with '02.2.'")
            print("   Please verify your complete API key")
    else:
        print("❌ OpenAI API key not found")
        return False
    
    # Test 3: Test imports
    try:
        import fitz
        import pandas
        print("✅ PDF processing (PyMuPDF) available")
        print("✅ Data processing (Pandas) available")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 4: Test OpenAI client initialization
    try:
        client = openai.OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized")
    except Exception as e:
        print(f"❌ OpenAI client error: {e}")
        return False
    
    print("-" * 40)
    print("🎉 Setup verification complete!")
    print()
    print("📋 Next steps:")
    print("1. Place your TRAX PDF files in a folder")
    print("2. Run: python main.py /path/to/your/pdf/folder")
    print("3. Check the generated CSV file for analysis results")
    
    return True

if __name__ == "__main__":
    test_setup() 