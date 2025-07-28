import fitz  # PyMuPDF
import re

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_substation_name(text):
    """Extract substation or equipment name from TRAX report text"""
    
    # Split text into lines for better analysis
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Strategy 1: Look for "Substation" followed by a number or name in next few lines
    for i, line in enumerate(lines[:20]):
        if line.lower() == 'substation' and i + 1 < len(lines):
            # Check next few lines for a name/number
            for j in range(1, min(4, len(lines) - i)):
                next_line = lines[i + j].strip()
                # Check if it's a reasonable substation identifier
                if next_line and len(next_line) < 30 and not next_line.lower() in ['position', 'location', 'test', 'conditions', 'weather', 'temperature']:
                    return clean_filename(f"Substation_{next_line}")
    
    # Strategy 2: Look for "Test Asset" section pattern
    for i, line in enumerate(lines[:15]):
        if 'test asset' in line.lower() and i + 1 < len(lines):
            # Look for substation info in next few lines
            for j in range(1, min(5, len(lines) - i)):
                next_line = lines[i + j].strip()
                if 'substation' in next_line.lower():
                    if j + 1 < len(lines) - i:
                        substation_id = lines[i + j + 1].strip()
                        if substation_id and len(substation_id) < 20:
                            return clean_filename(f"Substation_{substation_id}")
    
    # Strategy 3: Common regex patterns for substation/equipment identification
    patterns = [
        r'Substation[:\s]+([A-Za-z0-9\s\-_]+?)(?:\n|Location|Date|Test|Position|Job)',
        r'Station[:\s]+([A-Za-z0-9\s\-_]+?)(?:\n|Location|Date|Test)',
        r'Equipment[:\s]+([A-Za-z0-9\s\-_]+?)(?:\n|Location|Date|Test)',
        r'Transformer[:\s]+([A-Za-z0-9\s\-_]+?)(?:\n|Location|Date|Test)',
        r'Unit[:\s]+([A-Za-z0-9\s\-_]+?)(?:\n|Location|Date|Test)',
        r'Site[:\s]+([A-Za-z0-9\s\-_]+?)(?:\n|Location|Date|Test)',
        r'Location[:\s]+([A-Za-z0-9\s\-_]+?)(?:\n|Substation|Date|Test)',
        r'Asset[:\s]+([A-Za-z0-9\s\-_]+?)(?:\n|Location|Date|Test)',
        # More specific patterns
        r'at\s+([A-Za-z0-9\s\-_]+?)\s+(?:Substation|Station)',
        r'Test\s+Report\s+for\s+([A-Za-z0-9\s\-_]+?)(?:\n|at|Substation)',
        # Serial number patterns as fallback
        r'Serial\s*[#No.]*\s*[:\s]*([A-Za-z0-9\-_]+)',
        r'S/N[:\s]*([A-Za-z0-9\-_]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            name = match.group(1).strip()
            # Clean up the extracted name
            name = re.sub(r'\s+', ' ', name)  # Replace multiple spaces with single space
            name = name.strip()
            if len(name) > 1 and len(name) < 50:  # Reasonable length check
                return clean_filename(name)
    
    # Strategy 4: Look for Asset ID or similar identifiers
    for i, line in enumerate(lines[:25]):
        if 'asset id' in line.lower() and i + 1 < len(lines):
            asset_id = lines[i + 1].strip()
            if asset_id and len(asset_id) < 30 and asset_id.lower() not in ['test', 'conditions', 'weather']:
                return clean_filename(f"Asset_{asset_id}")
    
    # Strategy 5: Look for any numbered identifier in early lines
    for line in lines[:10]:
        # Look for standalone numbers that could be substation numbers
        if line.isdigit() and 1 <= int(line) <= 9999:
            return clean_filename(f"Substation_{line}")
        # Look for alphanumeric codes
        if re.match(r'^[A-Z0-9\-_]{2,15}$', line):
            return clean_filename(f"Equipment_{line}")
    
    # Final fallback - use generic name with timestamp
    from datetime import datetime
    return f"Transformer_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def clean_filename(name):
    """Clean a string to make it suitable for use as a filename"""
    # Remove or replace invalid filename characters
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Replace spaces with underscores
    name = re.sub(r'\s+', '_', name)
    # Remove multiple consecutive underscores
    name = re.sub(r'_+', '_', name)
    # Remove leading/trailing underscores
    name = name.strip('_')
    # Ensure reasonable length
    if len(name) > 50:
        name = name[:50]
    
    return name if name else "Unknown_Equipment"
