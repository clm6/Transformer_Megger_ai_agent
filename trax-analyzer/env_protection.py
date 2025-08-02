#!/usr/bin/env python3
"""
Environment Protection System - Permanent Fix for API Key Issues
Prevents corrupted system environment variables from overriding .env files
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import warnings

class EnvironmentProtector:
    """Robust environment variable management with protection against conflicts"""
    
    def __init__(self):
        self.env_file_path = None
        self.system_key = None
        self.env_file_key = None
        self.final_key = None
        self.issues = []
    
    def validate_api_key(self, key):
        """Validate API key format"""
        if not key:
            return False, "Key is empty or None"
        
        if not isinstance(key, str):
            return False, "Key is not a string"
        
        if not key.startswith("sk-"):
            return False, "Key doesn't start with 'sk-'"
        
        if len(key) < 50:
            return False, "Key too short (should be ~164 characters)"
        
        if len(key) > 200:
            return False, "Key too long"
        
        # Check for common corruption patterns
        if "_ckaxM5gA" in key:
            return False, "This appears to be the known corrupted key"
        
        if not key.replace('-', '').replace('_', '').isalnum():
            return False, "Key contains invalid characters"
        
        return True, "Valid format"
    
    def check_system_environment(self):
        """Check for system environment variables"""
        # Check current process environment
        self.system_key = os.environ.get('OPENAI_API_KEY')
        
        if self.system_key:
            valid, reason = self.validate_api_key(self.system_key)
            if not valid:
                self.issues.append(f"❌ CORRUPTED system environment variable detected: {reason}")
                self.issues.append(f"   System key: {self.system_key[:20]}...{self.system_key[-10:] if len(self.system_key) > 30 else ''}")
                return False
            else:
                self.issues.append(f"⚠️ System environment variable found (but valid): {self.system_key[:20]}...")
                return True
        
        return True
    
    def load_env_file(self):
        """Load .env file with validation"""
        # Find .env file
        self.env_file_path = find_dotenv()
        
        if not self.env_file_path:
            self.issues.append("❌ No .env file found")
            return False
        
        # Load .env file
        load_dotenv(self.env_file_path, override=True)  # Force override system vars
        
        # Read directly from file to get the true value
        try:
            with open(self.env_file_path, 'r') as f:
                content = f.read().strip()
                if content.startswith("OPENAI_API_KEY="):
                    self.env_file_key = content.replace("OPENAI_API_KEY=", "").strip()
                    
                    valid, reason = self.validate_api_key(self.env_file_key)
                    if valid:
                        self.issues.append(f"✅ Valid .env file key found: {self.env_file_key[:20]}...")
                        return True
                    else:
                        self.issues.append(f"❌ Invalid .env file key: {reason}")
                        return False
        except Exception as e:
            self.issues.append(f"❌ Error reading .env file: {e}")
            return False
        
        return False
    
    def clean_system_environment(self):
        """Remove corrupted system environment variables"""
        if self.system_key:
            valid, reason = self.validate_api_key(self.system_key)
            if not valid:
                # Remove from current process
                if 'OPENAI_API_KEY' in os.environ:
                    del os.environ['OPENAI_API_KEY']
                    self.issues.append("🔧 Removed corrupted key from current process")
                
                # Warn about persistent system variables
                self.issues.append("⚠️ RECOMMENDATION: Check Windows Environment Variables and remove OPENAI_API_KEY")
                return True
        return False
    
    def setup_protected_environment(self):
        """Setup protected environment with proper API key"""
        self.issues.append("🔍 ENVIRONMENT PROTECTION SYSTEM STARTING...")
        
        # Step 1: Check for system environment issues
        system_ok = self.check_system_environment()
        
        # Step 2: Load .env file
        env_file_ok = self.load_env_file()
        
        # Step 3: Clean corrupted system variables
        if not system_ok:
            self.clean_system_environment()
        
        # Step 4: Determine final key to use
        if env_file_ok:
            # Force use .env file key (even if system key exists)
            os.environ['OPENAI_API_KEY'] = self.env_file_key
            self.final_key = self.env_file_key
            self.issues.append(f"✅ Using .env file key: {self.final_key[:20]}...")
            return True
        elif system_ok and self.system_key:
            # Use system key only if .env file is missing and system key is valid
            self.final_key = self.system_key
            self.issues.append(f"✅ Using system key: {self.final_key[:20]}...")
            return True
        else:
            self.issues.append("❌ No valid API key found!")
            return False
    
    def print_report(self):
        """Print protection report"""
        print("🛡️ ENVIRONMENT PROTECTION REPORT")
        print("=" * 50)
        for issue in self.issues:
            print(f"  {issue}")
        print("=" * 50)
    
    def get_protected_key(self):
        """Get the protected API key"""
        return self.final_key

def setup_protected_environment():
    """Main function to setup protected environment"""
    protector = EnvironmentProtector()
    success = protector.setup_protected_environment()
    protector.print_report()
    
    if success:
        return protector.get_protected_key()
    else:
        print("❌ ENVIRONMENT PROTECTION FAILED!")
        print("🔧 Please check your .env file and API key configuration")
        return None

def test_protection():
    """Test the protection system"""
    print("🧪 Testing Environment Protection System...")
    key = setup_protected_environment()
    
    if key:
        print(f"\n✅ Protection successful! Key: {key[:20]}...")
        
        # Test API call
        try:
            from openai import OpenAI
            client = OpenAI(api_key=key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": "Say 'Protection test successful'"}],
                max_tokens=10
            )
            result = response.choices[0].message.content
            if "Protection test successful" in result:
                print("🎉 PROTECTION SYSTEM WORKING PERFECTLY!")
                return True
            else:
                print(f"⚠️ Unexpected API response: {result}")
                return False
        except Exception as e:
            print(f"❌ API test failed: {e}")
            return False
    else:
        print("❌ Protection system failed")
        return False

if __name__ == "__main__":
    test_protection()