#!/usr/bin/env python3
"""
AI Agent Debug Tool - Isolate API Key Issues
"""

import os
import sys
from pathlib import Path

def debug_environment():
    """Debug environment variable loading"""
    print("🔍 ENVIRONMENT DEBUG")
    print("=" * 50)
    
    # Check current working directory
    print(f"Current directory: {os.getcwd()}")
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print(f"✅ .env file found: {env_file.absolute()}")
        with open(env_file, 'r') as f:
            content = f.read().strip()
            print(f"📄 .env content length: {len(content)}")
            if content.startswith("OPENAI_API_KEY="):
                key_part = content.replace("OPENAI_API_KEY=", "")
                print(f"🔑 .env key: {key_part[:20]}...{key_part[-10:]}")
            else:
                print(f"⚠️ .env content: {content[:100]}")
    else:
        print("❌ .env file not found")
    
    # Check for other .env files
    for parent in [Path(".."), Path("../.."), Path("../../..")]:
        other_env = parent / ".env"
        if other_env.exists():
            print(f"⚠️ Found other .env: {other_env.absolute()}")
    
    # Check system environment
    sys_key = os.environ.get('OPENAI_API_KEY')
    if sys_key:
        print(f"🔑 System env key: {sys_key[:20]}...{sys_key[-10:]}")
    else:
        print("✅ No system OPENAI_API_KEY found")

def debug_dotenv_loading():
    """Debug dotenv loading process"""
    print("\n🔧 DOTENV LOADING DEBUG")
    print("=" * 50)
    
    try:
        from dotenv import load_dotenv, find_dotenv
        
        # Find .env file
        env_path = find_dotenv()
        print(f"📍 dotenv found: {env_path}")
        
        # Load and check
        loaded = load_dotenv(env_path, verbose=True)
        print(f"✅ Load successful: {loaded}")
        
        # Get the key
        key = os.getenv('OPENAI_API_KEY')
        if key:
            print(f"🔑 Loaded key: {key[:20]}...{key[-10:]}")
            print(f"📏 Key length: {len(key)}")
            
            # Validate key format
            if key.startswith("sk-"):
                print("✅ Key format looks correct")
            else:
                print("❌ Key format invalid")
        else:
            print("❌ No key loaded")
            
    except Exception as e:
        print(f"❌ dotenv error: {e}")

def test_direct_api():
    """Test direct API call with loaded key"""
    print("\n🤖 DIRECT API TEST")
    print("=" * 50)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from openai import OpenAI
        
        key = os.getenv('OPENAI_API_KEY')
        if not key:
            print("❌ No API key available")
            return
        
        print(f"🔑 Using key: {key[:20]}...{key[-10:]}")
        
        client = OpenAI(api_key=key)
        
        print("📡 Making test API call...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Say exactly: 'API test successful'"}
            ],
            max_tokens=10,
            temperature=0
        )
        
        result = response.choices[0].message.content
        print(f"✅ API Response: {result}")
        
        if "API test successful" in result:
            print("🎉 API is working correctly!")
            return True
        else:
            print("⚠️ Unexpected response")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_json_generation():
    """Test JSON generation with minimal prompt"""
    print("\n📄 JSON GENERATION TEST")
    print("=" * 50)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        simple_prompt = """Generate a simple JSON object for transformer analysis:

```json
{
  "test": "simple",
  "status": "OK",
  "value": 123
}
```

Return only the JSON above."""

        print("📡 Testing JSON generation...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a JSON generator. Return only valid JSON."},
                {"role": "user", "content": simple_prompt}
            ],
            max_tokens=200,
            temperature=0
        )
        
        result = response.choices[0].message.content
        print(f"📝 Response length: {len(result)}")
        print(f"📄 First 200 chars: {result[:200]}")
        
        # Try to parse as JSON
        import json
        if "```json" in result:
            # Extract JSON from markdown
            start = result.find("```json") + 7
            end = result.find("```", start)
            json_str = result[start:end].strip()
            print(f"🔍 Extracted JSON: {json_str}")
            
            try:
                parsed = json.loads(json_str)
                print("✅ JSON parsing successful!")
                print(f"📊 Parsed data: {parsed}")
                return True
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                return False
        else:
            print("❌ No JSON markers found")
            return False
            
    except Exception as e:
        print(f"❌ JSON test failed: {e}")
        return False

def fix_env_file():
    """Recreate .env file with correct format"""
    print("\n🔧 ENV FILE FIX")
    print("=" * 50)
    
    # Prompt user for their API key securely
    print("🔑 Please enter your OpenAI API key:")
    print("   (You can get this from https://platform.openai.com/api-keys)")
    print("   Note: Your key should start with 'sk-'")
    
    api_key = input("Enter API key: ").strip()
    
    # Basic validation
    if not api_key.startswith('sk-'):
        print("❌ Invalid API key format. Key should start with 'sk-'")
        return False
    
    if len(api_key) < 20:
        print("❌ API key appears to be too short")
        return False
    
    try:
        with open(".env", "w") as f:
            f.write(f"OPENAI_API_KEY={api_key}")
        
        print("✅ .env file recreated")
        
        # Verify (show only partial key for security)
        print(f"🔍 Verified key: {api_key[:20]}...{api_key[-10:]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to fix .env: {e}")
        return False

if __name__ == "__main__":
    print("🔍 AI AGENT DEBUG TOOL")
    print("=" * 60)
    
    # Run diagnostics
    debug_environment()
    debug_dotenv_loading()
    
    # Test API
    api_works = test_direct_api()
    
    if not api_works:
        print("\n🔧 Attempting to fix .env file...")
        if fix_env_file():
            print("\n🔄 Retesting after fix...")
            debug_dotenv_loading()
            api_works = test_direct_api()
    
    if api_works:
        print("\n📄 Testing JSON generation...")
        json_works = test_json_generation()
        
        if json_works:
            print("\n🎉 ALL TESTS PASSED - AI Agent is working!")
        else:
            print("\n⚠️ API works but JSON generation failed")
    else:
        print("\n❌ API still not working - manual intervention needed")
    
    print("\n🏁 Debug complete!")