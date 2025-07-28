import openai
import os
from dotenv import load_dotenv

def analyze_trax_report(text):
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found. Please check your .env file.")
    
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)
    
    prompt = f"""You are a transformer diagnostic expert. Given the TRAX report text below, extract all critical data,
analyze the windings, bushing tan delta, and turns ratio, and return a diagnostic report with:
- Key findings
- Pass/Fail tests
- Winding & insulation condition
- Bushing analysis
- Recommended actions

TRAX REPORT:
{text[:10000]}
"""
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    return response.choices[0].message.content
