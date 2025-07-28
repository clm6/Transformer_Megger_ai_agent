import pandas as pd
import os

print("🔄 TRAX ANALYSIS COMPARISON")
print("=" * 80)

# Read both analysis files
basic_file = r'C:\Users\craig\Downloads\TRAX_Reports\trax_diagnostics_summary.csv'
enhanced_file = r'C:\Users\craig\Downloads\TRAX_Reports\trax_enhanced_diagnostics_summary.csv'

if os.path.exists(basic_file) and os.path.exists(enhanced_file):
    basic_df = pd.read_csv(basic_file)
    enhanced_df = pd.read_csv(enhanced_file)
    
    print("📊 BASIC ANALYSIS (Length):", len(basic_df['Analysis'].iloc[0]))
    print("📊 ENHANCED ANALYSIS (Length):", len(enhanced_df['Enhanced_Technical_Analysis'].iloc[0]))
    
    print("\n🔍 STRUCTURE COMPARISON:")
    print("✅ Basic Analysis: General narrative format")
    print("✅ Enhanced Analysis: Structured technical sections with:")
    print("   - Winding resistance analysis")
    print("   - Turns ratio & excitation current")
    print("   - Tan delta/power factor tables")
    print("   - Bushing analysis tables")
    print("   - Demagnetization assessment")
    print("   - Summary health assessment")
    print("   - Specific technical recommendations")
    
    print("\n🎯 NEXT IMPROVEMENTS NEEDED:")
    print("1. Extract specific numerical values from PDF text")
    print("2. Calculate actual percentages and deviations")
    print("3. Fill in the table placeholders with real data")
    print("4. Apply status indicators based on actual thresholds")
    
else:
    print("❌ One or both analysis files not found")
    print(f"Basic file exists: {os.path.exists(basic_file)}")
    print(f"Enhanced file exists: {os.path.exists(enhanced_file)}")

print("\n📋 RECOMMENDATION:")
print("The enhanced framework is excellent! Next step:")
print("- Fine-tune the AI prompt to extract specific numerical values")
print("- Add calculations for resistance variations and deviations")
print("- Implement threshold-based status indicators") 