# TRAX Transformer Diagnostic Analyzer

This project uses AI to analyze TRAX transformer test reports and extract critical diagnostic information.

## Features

- **Batch PDF Processing**: Analyzes multiple TRAX PDF reports from a folder
- **AI-Powered Analysis**: Uses OpenAI GPT-4o to interpret transformer diagnostic data
- **Multiple Output Formats**: 
  - CSV files for data analysis
  - Professional Word documents for reporting
- **Three Analysis Levels**:
  - Basic Analysis: General diagnostic overview
  - Enhanced Technical Analysis: Detailed engineering assessment
  - Word Reports: Professional formatted documents

## Output Formats

### 📊 CSV Analysis Files
- `trax_diagnostics_summary.csv` - Basic analysis results
- `trax_enhanced_diagnostics_summary.csv` - Enhanced technical analysis

### 📄 Word Document Reports
- `TRAX_Diagnostic_Report.docx` - Professional formatted report
- `TRAX_Report_[filename].docx` - Individual reports per PDF

## Usage Options

### 1. Basic Analysis
```bash
python main.py "C:\path\to\pdf\folder"
```
Generates: CSV file with general diagnostic overview

### 2. Enhanced Technical Analysis
```bash
python main_enhanced.py "C:\path\to\pdf\folder"
```
Generates: CSV file with detailed technical analysis including:
- Winding resistance analysis with specific values
- Turns ratio & excitation current assessment
- Tan delta/power factor tables
- Bushing analysis with status indicators
- Demagnetization assessment
- Summary health assessment
- Specific technical recommendations

### 3. Complete Analysis with Word Reports
```bash
python main_with_word_report.py "C:\path\to\pdf\folder"
```
Generates: Both CSV analysis AND professional Word documents

### 4. Generate Word Report from Existing Analysis
```bash
python generate_word_report.py
```
Converts existing CSV analysis to professional Word document

## Enhanced Analysis Features

### 🔍 Winding Resistance Analysis
- **LV Side (X1-X0, X2-X0, X3-X0)**: Complete resistance mapping across tap positions
- **HV Side (H1-H3, H2-H1, H3-H2)**: Variation analysis and symmetry assessment
- **Calculations**: Max deviation, variation percentages, stability assessment
- **Diagnostics**: Turn-to-turn shorting, contact resistance, electrical balance

### ⚡ Turns Ratio & Excitation Current
- Error percentage analysis vs. specification limits (~0.5%)
- Excitation current ranges and assessment
- Phase displacement verification
- Tap changer functionality evaluation

### 🔌 Tan Delta / Power Factor Analysis
```
Section          PF @ 20°C    Status      Diagnostic Insight
CHL (LV to GND)  X.XXX%      ✅/⚠️/❌    Detailed assessment
CLG (LV-Ground)  X.XXX%      ✅/⚠️/❌    Detailed assessment
CLH (LV-HV)      X.XXX%      ✅/⚠️/❌    Detailed assessment
CHG (HV-GND)     X.XXX%      ✅/⚠️/❌    Detailed assessment
```

**Thresholds:**
- ✅ Acceptable: <0.3%
- ⚠️ Watch: 0.3-0.5%
- 🟨 Concern: 0.5-1.0%
- ❌ Critical: >1.0%

### 🧯 Bushing Analysis
Complete C1 power factor assessment for all bushings (H1-H3, X0-X3)

### 🧠 Summary Health Assessment
Structured status table with specific recommendations and timeframes

## Professional Word Reports Include

- **Title Page**: Professional formatting with report metadata
- **Executive Summary**: Key findings and recommendations
- **Detailed Technical Sections**: All analysis categories with proper formatting
- **Tables and Charts**: Formatted data presentation
- **Specific Recommendations**: Prioritized action items with timeframes

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure OpenAI API Key
The project requires an OpenAI API key. This is configured in the `.env` file.

### 3. Verify Installation
```bash
python test_setup.py
```

## File Structure

- `main.py`: Basic analysis application
- `main_enhanced.py`: Enhanced technical analysis
- `main_with_word_report.py`: Complete analysis with Word reports
- `generate_word_report.py`: Convert existing analysis to Word
- `trax_parser.py`: PDF text extraction using PyMuPDF
- `trax_analyzer.py`: Basic AI analysis using OpenAI GPT-4o
- `trax_analyzer_enhanced.py`: Enhanced technical analysis engine
- `requirements.txt`: Python dependencies
- `.env`: OpenAI API key configuration

## Analysis Capabilities

The AI analyzer focuses on:
- **Winding Analysis**: Insulation condition, winding resistance with numerical analysis
- **Bushing Assessment**: Tan delta values, insulation integrity with thresholds
- **Turns Ratio Testing**: Ratio accuracy, variations, and tap changer functionality
- **Overall Condition**: Pass/fail status with specific status indicators (✅⚠️❌)
- **Maintenance Recommendations**: Prioritized actions with specific timeframes

## Requirements

- Python 3.7+
- OpenAI API access
- PDF files containing TRAX test reports
- python-docx for Word document generation

## Example Output

### Basic Analysis
General narrative format suitable for quick overview

### Enhanced Technical Analysis
```
🔍 WINDING RESISTANCE ANALYSIS
LV Side (X1-X0, X2-X0, X3-X0)
Normal expected range: ~48–52 mΩ
Max deviation: 0.55% for X3-X0 at tap 9R
Stability: >99.9% in all cases
✅ Conclusion: No signs of abnormal resistance
```

### Word Document Features
- Professional title page with metadata
- Structured sections with proper headings
- Formatted tables for technical data
- Status indicators and recommendations
- Print-ready formatting

## Notes

- The analyzer processes up to 15,000 characters of text per PDF for optimal analysis
- Enhanced analysis provides specific numerical breakdowns and calculations
- Word reports are formatted for professional presentation and archival
- API usage costs apply based on OpenAI pricing for GPT-4o model
- All reports include specific recommendations with timeframes for maintenance planning 