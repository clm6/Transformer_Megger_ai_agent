import openai
import os
import json
from dotenv import load_dotenv
from datetime import datetime

def analyze_trax_report_json(text, document_date=None, filename=None):
    """
    Advanced TRAX report analyzer with PREDICTIVE MAINTENANCE ENHANCEMENTS v3.0
    Based on Master Improvement Prompt with Predictive Maintenance (July 28, 2025)
    
    Predictive Maintenance v3.0:
    - Asset Health Score calculation (0-100%) with weighting breakdown
    - Predictive maintenance planning with component-specific timelines
    - Anomaly scoring (0-10) and replacement cycle recommendations
    - Template-based variable substitution for comprehensive reporting
    - Enhanced condition assessment with degradation trend analysis
    - All v2.4 technical completeness features retained + critical fixes applied
    """
    # Use protected environment loading to prevent API key conflicts
    try:
        from env_protection import setup_protected_environment
        api_key = setup_protected_environment()
        if not api_key:
            raise ValueError("No valid API key found. Please check your .env file and ensure no corrupted system environment variables exist.")
    except ImportError:
        # Fallback to regular loading if protection module not available
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Please check your .env file.")
    
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)
    
    # Use provided date or current date
    if not document_date:
        document_date = datetime.now().strftime('%Y-%m-%d')
    
    if not filename:
        filename = "TRAX - Test report"
    
    prompt = f"""You are a transformer diagnostics expert. Generate comprehensive JSON analysis with:
- Asset health scoring (0-100%) 
- Predictive maintenance planning
- Enhanced TTR logic: OK ≤0.5%, WARNING 0.5-1%, CRITICAL >1%
- PF thresholds: OK <0.3%, WARNING 0.3-0.5%, CRITICAL >0.5%
- Demagnetization: INEFFECTIVE if Initial <20%

REQUIRED JSON OUTPUT:

```json
{{
  "report_metadata": {{
    "file_name": "{filename}",
    "document_date": "{document_date}",
    "analysis_date": "{datetime.now().strftime('%Y-%m-%d')}",
    "analysis_type": "Predictive Maintenance Enhanced v3.0 - Asset Health & Lifecycle Analysis",
    "generated_by": "TRAX AI Analyzer v3.0",
    "predictive_features": "Asset health scoring, maintenance planning, anomaly detection, replacement forecasting",
    "template_variables_included": "Comprehensive variable set for advanced reporting"
  }},
  "winding_resistance": {{
    "lv_windings": [
      {{
        "phase": "[PHASE]",
        "tap_position": "[TAP]",
        "resistance_mohm": "[VALUE]",
        "range_mohm": "[MIN-MAX]",
        "status": "[OK ✅/WARNING ⚠️/CRITICAL 🚨]",
        "confidence_score": "[85-100]"
      }}
    ],
    "hv_windings": [
      {{
        "phase": "[PHASE]",
        "tap_position": "[TAP]",
        "resistance_ohm": "[VALUE]",
        "range_ohm": "[MIN-MAX]",
        "status": "[OK ✅/WARNING ⚠️/CRITICAL 🚨]",
        "confidence_score": "[85-100]"
      }}
    ]
  }},
  "turns_ratio": [
    {{
      "tap_position": "[TAP]",
      "nominal_ttr": "[VALUE]",
      "measured_ttr": "[VALUE]",
      "error_percent": "[VALUE]",
      "status": "[OK ✅ if ≤0.5%, WARNING ⚠️ if 0.5-1%, CRITICAL 🚨 if >1%]",
      "excitation_current_ma": "[CONVERTED_4_DECIMALS]",
      "phase_displacement_deg": "[VALUE]",
      "confidence_score": "[85-100]"
    }}
  ],
  "tan_delta_main_insulation": {{
    "extraction_method": "Corrected %PF to 20°C - STRICT THRESHOLDS v2.3 (RETAINED)",
    "CHL": {{
      "pf_corrected_20c_percent": "[EXACT_VALUE]",
      "status": "[OK ✅ if <0.3%, WARNING ⚠️ if 0.3-0.5%, CRITICAL 🚨 if >0.5%]",
      "temperature_correction": "[Available/Missing]",
      "confidence_score": "[NUMERIC_85-100]",
      "visual_indicator": "[✅/⚠️/🚨]",
      "monitoring_recommendation": "[Quarterly/Next cycle/Immediate based on value]"
    }},
    "CLG": {{
      "pf_corrected_20c_percent": "[EXACT_VALUE]",
      "status": "[STRICTLY: CRITICAL 🚨 if >0.5%, WARNING ⚠️ if 0.3-0.5%, OK ✅ if <0.3%]",
      "temperature_correction": "[Available/Missing]",
      "confidence_score": "[NUMERIC_85-100]",
      "visual_indicator": "[✅/⚠️/🚨]",
      "moisture_risk_flag": "[TRUE if >0.5% + other insulation >0.4%]",
      "monitoring_recommendation": "[Based on STRICT thresholds]"
    }},
    "CLH": {{
      "pf_corrected_20c_percent": "[EXACT_VALUE]",
      "status": "[STRICTLY: CRITICAL 🚨 if >0.5%, WARNING ⚠️ if 0.3-0.5%, OK ✅ if <0.3%]",
      "temperature_correction": "[Available/Missing]",
      "confidence_score": "[NUMERIC_85-100]",
      "visual_indicator": "[✅/⚠️/🚨]",
      "monitoring_recommendation": "[Based on STRICT thresholds]"
    }},
    "CHG": {{
      "pf_corrected_20c_percent": "[EXACT_VALUE]",
      "status": "[STRICTLY: CRITICAL 🚨 if >0.5%, WARNING ⚠️ if 0.3-0.5%, OK ✅ if <0.3%]",
      "temperature_correction": "[Available/Missing]",
      "confidence_score": "[NUMERIC_85-100]",
      "visual_indicator": "[✅/⚠️/🚨]",
      "moisture_combination_flag": "[TRUE if CLG >0.5% AND CHG >0.25%]",
      "monitoring_recommendation": "[Based on STRICT thresholds]"
    }},
    "pattern_detection": {{
      "moisture_risk_detected": "[TRUE if any 2 of CLG/CLH/CHG >0.4% AND one >0.5%]",
      "confidence_inheritance": "[HIGH if all components HIGH confidence]"
    }}
  }},
  "bushing_pf_c1": {{
    "extraction_method": "Corrected %PF - ZERO TOLERANCE v2.3 (RETAINED)",
    "H1": {{
      "designation": "H1",
      "pf_test_temp_percent": "[RAW_VALUE]",
      "pf_corrected_20c_percent": "[CORRECTED_VALUE]",
      "status": "[STRICTLY: OK ✅ <0.3%, WARNING ⚠️ 0.3-0.5%, CRITICAL 🚨 >0.5%]",
      "confidence_score": "[NUMERIC_85-100]",
      "visual_indicator": "[✅/⚠️/🚨/❓]",
      "phase_stress_pattern": "[TRUE if WARNING insulation + CRITICAL bushing same phase]"
    }},
    "H2": {{
      "designation": "H2",
      "pf_test_temp_percent": "[RAW_VALUE]",
      "pf_corrected_20c_percent": "[CORRECTED_VALUE]",
      "status": "[EXAMPLE: 0.52% = CRITICAL 🚨 NOT OK]",
      "confidence_score": "[NUMERIC_85-100]",
      "visual_indicator": "[✅/⚠️/🚨/❓]",
      "monitoring_recommendation": "[IMMEDIATE if >0.5%]"
    }},
    "H3": {{
      "designation": "H3",
      "pf_test_temp_percent": "[RAW_VALUE]",
      "pf_corrected_20c_percent": "[CORRECTED_VALUE]",
      "status": "[STRICTLY ENFORCED THRESHOLDS]",
      "confidence_score": "[NUMERIC_85-100]",
      "visual_indicator": "[✅/⚠️/🚨/❓]"
    }},
    "X0": {{
      "designation": "X0",
      "pf_corrected_20c_percent": "[CORRECTED_VALUE]",
      "status": "[STRICTLY ENFORCED THRESHOLDS]",
      "confidence_score": "[NUMERIC]",
      "visual_indicator": "[✅/⚠️/🚨/❓]"
    }},
    "X1": {{
      "designation": "X1", 
      "pf_corrected_20c_percent": "[CORRECTED_VALUE]",
      "status": "[STRICTLY ENFORCED THRESHOLDS]",
      "confidence_score": "[NUMERIC]",
      "visual_indicator": "[✅/⚠️/🚨/❓]"
    }},
    "X2": {{
      "designation": "X2",
      "pf_corrected_20c_percent": "[CORRECTED_VALUE]",
      "status": "[STRICTLY ENFORCED THRESHOLDS]",
      "confidence_score": "[NUMERIC]",
      "visual_indicator": "[✅/⚠️/🚨/❓]"
    }},
    "X3": {{
      "designation": "X3",
      "pf_corrected_20c_percent": "[CORRECTED_VALUE]",
      "status": "[STRICTLY ENFORCED THRESHOLDS]",
      "confidence_score": "[NUMERIC]",
      "visual_indicator": "[✅/⚠️/🚨/❓]"
    }},
    "cluster_analysis": {{
      "hv_cluster_degradation": "[TRUE if 2+ H bushings >0.5%]",
      "lv_cluster_degradation": "[TRUE if 2+ X bushings >0.5%]",
      "critical_bushings_count": "[COUNT_OF_BUSHINGS_>0.5%]",
      "immediate_action_required": "[AUTO-FLAG: TRUE if 2+ bushings >0.5%]",
      "cluster_pattern": "[HV Cluster Critical/LV Cluster Critical/Mixed Pattern]",
      "overall_bushing_health": "[POOR if 2+ bushings >0.5%, else GOOD/FAIR]"
    }}
  }},
  "demagnetization": {{
    "initial_remanence_percent": "[EXACT_VALUE]",
    "final_remanence_percent": "[EXACT_VALUE]",
    "effectiveness": "[CRITICAL FIX: INEFFECTIVE if Initial <20%, EFFECTIVE only if Initial >20% AND Final <1%]",
    "validation_logic": "[If Initial <20% then INEFFECTIVE regardless of final, else check both criteria]",
    "effectiveness_criteria": "EFFECTIVE only if Initial >20% AND Final <1%, otherwise INEFFECTIVE",
    "confidence_score": "[95-100 if both values clear]"
  }},
  "health_assessment_technical_complete": {{
    "overall_status": "[AUTO-CRITICAL if 2+ bushings OR any insulation >0.5%]",
    "critical_findings_count": "[COUNT: All PF >0.5% + TTR >1% components]",
    "warning_findings_count": "[COUNT: All PF 0.3-0.5% + TTR 0.5-1% components]",
    "immediate_action_auto_flag": "[TRUE if 2+ bushings CRITICAL OR any insulation CRITICAL OR TTR >1%]",
    "pattern_alerts": [
      "[Moisture Risk if CLG >0.5% + others >0.4%]",
      "[HV Cluster Critical if all H bushings >0.5% - Immediate Replacement Recommended]",
      "[LV Cluster Critical if all X bushings >0.5% - Immediate Replacement Recommended]",
      "[Phase Stress if WARNING insulation + CRITICAL bushing same phase]",
      "[TTR Critical if any tap error >1%]"
    ],
    "cluster_auto_flagging": {{
      "hv_cluster_critical": "[TRUE if ALL H bushings >0.5%]",
      "lv_cluster_critical": "[TRUE if ALL X bushings >0.5%]",
      "immediate_replacement_recommended": "[TRUE if cluster degradation detected]"
    }},
    "confidence_score_overall": "[WEIGHTED average of all subsystem confidences]",
    "visual_status": "[🚨 CRITICAL / ⚠️ WARNING / ✅ OK]",
    "risk_level": "[CRITICAL/HIGH/MODERATE/LOW with visual indicators]",
    "technical_completeness_validation": {{
      "completeness_score_percent": "[0-100% based on sections included]",
      "winding_resistance_complete": "[TRUE if HV and LV phases with taps included]",
      "turns_ratio_complete": "[TRUE if all taps with TTR, excitation current included]",
      "excitation_current_validated": "[TRUE if properly converted to mA with 4 decimals]",
      "tan_delta_complete": "[TRUE if CHL, CLG, CLH, CHG all included]",
      "bushing_analysis_complete": "[TRUE if H1-H3, X0-X3 analyzed]",
      "demagnetization_complete": "[TRUE if effectiveness determined]",
      "tap_coverage_validated": "[Coverage range and any warnings]",
      "zero_tolerance_reinforced": "[TRUE if all PF >0.5% = CRITICAL enforced]",
      "technical_completeness_verified": "[✅ if all components found, ⚠️ if partial, ❌ if incomplete]"
    }},
    "unit_consistency_validation": {{
      "resistance_units_correct": "[mΩ for LV, Ω for HV verified]",
      "excitation_current_units": "[µA to mA conversion with 4 decimals verified]",
      "pf_units_consistent": "[% values with proper thresholds verified]"
    }}
  }},
  "asset_health_score": {{
    "calculated_score": "[0-100 overall health score]",
    "condition_category": "[Excellent 90-100, Good 75-89, Moderate 60-74, Degraded 40-59, Critical <40]",
    "component_scores": {{
      "winding_resistance": "[0-20 points based on balance and acceptability]",
      "turns_ratio": "[0-20 points based on TTR errors and excitation current]",
      "main_insulation": "[0-25 points based on PF values and trends]",
      "bushing_pf": "[0-25 points based on bushing conditions and clusters]",
      "demagnetization": "[0-10 points based on effectiveness and remanence levels]"
    }},
    "weighting_rationale": "Critical components (insulation, bushings) weighted higher due to failure impact",
    "degradation_trend": "[Stable/Improving/Slow decline/Accelerating decline based on component analysis]",
    "estimated_remaining_life": "[Years based on current condition and degradation rate]"
  }},
  "predictive_maintenance_plan": {{
    "immediate_actions": [
      "[List components requiring immediate attention with specific actions]"
    ],
    "next_maintenance_interval": {{
      "recommended_timeframe": "[3 months/6 months/12 months based on findings]",
      "components_to_monitor": "[Specific components requiring attention]",
      "tests_required": "[Specific tests needed at next interval]"
    }},
    "quarterly_monitoring": [
      "[Components requiring quarterly monitoring with specific parameters]"
    ],
    "replacement_forecast": {{
      "high_priority": "[Components needing replacement within 12 months]",
      "medium_priority": "[Components needing replacement within 24 months]",
      "long_term": "[Components for long-term replacement planning 3-5 years]",
      "estimated_costs": "[Relative cost categories: Low/Medium/High for planning]"
    }},
    "anomaly_score": "[0-10 risk score: 0-2 Normal, 3-5 Elevated, 6-8 High, 9-10 Critical]",
    "risk_factors": [
      "[Specific risk factors identified: moisture, cluster degradation, aging, etc.]"
    ]
  }},
  "template_variables": {{
    "transformer_name": "[Equipment name for template]",
    "transformer_age": "[Estimated age in years if determinable]",
    "overall_status": "[Overall technical status summary]",
    "critical_findings": "[Count and description of critical findings]",
    "warning_findings": "[Count and description of warning findings]",
    "moisture_flags": "[Moisture risk indicators]",
    "pattern_flags": "[Cluster or pattern risk flags]",
    "health_score": "[Asset health score 0-100]",
    "anomaly_score": "[Anomaly risk score 0-10]",
    "replacement_window": "[Months until recommended replacement for critical components]",
    "ahs_condition": "[Excellent/Good/Moderate/Degraded/Critical based on score]",
    "predictive_plan_table": "[Formatted table of component statuses and timelines]",
    "overall_summary_text": "[Comprehensive summary for executive reporting]",
    "winding_resistance_summary": "[Formatted WR analysis for template]",
    "turns_ratio_summary": "[Formatted TTR analysis for template]",
    "tan_delta_summary": "[Formatted tan delta analysis for template]",
    "bushing_summary": "[Formatted bushing analysis for template]",
    "demagnetization_summary": "[Formatted demagnetization analysis for template]"
  }}
}}
```

CRITICAL REQUIREMENTS:
• Calculate 0-100% asset health score
• Generate predictive maintenance plan with timelines
• Apply strict PF thresholds and TTR logic
• Include all technical sections with confidence scores

```

CRITICAL: After the JSON, generate a COMPREHENSIVE PREDICTIVE MAINTENANCE REPORT using this EXACT template:

# TRANSFORMER DIAGNOSTIC REPORT
Equipment: {{transformer_name}}  
Analysis Date: {{analysis_date}}  
Source File: {{source_file}}

## WINDING RESISTANCE ANALYSIS
{{winding_resistance_summary}}

## TURNS RATIO ANALYSIS
{{turns_ratio_summary}}

## TAN DELTA / MAIN INSULATION
{{tan_delta_summary}}

## BUSHING POWER FACTOR ANALYSIS
{{bushing_summary}}

## DEMAGNETIZATION ANALYSIS
{{demagnetization_summary}}

## TECHNICAL COMPLETENESS VALIDATION
- **Completeness Score**: {{completeness_score}}%
- **All Required Sections**: {{section_check}}

---

## 🔍 OVERALL SUMMARY
- **Transformer Age**: {{transformer_age}} years
- **Overall Technical Status**: {{overall_status}}
- **Critical Findings**: {{critical_findings}}
- **Warning Findings**: {{warning_findings}}
- **Moisture Risk Flags**: {{moisture_flags}}
- **Cluster or Pattern Risk Flags**: {{pattern_flags}}

---

## 🔧 PREDICTIVE MAINTENANCE PLAN
- **Immediate Action Items**: {{critical_action_items}}
- **Next Maintenance Interval**: {{warning_retest_schedule}}
- **Quarterly Monitoring Targets**: {{quarterly_monitoring}}
- **Replacement Cycle Recommendation**: {{replacement_window}} months
- **Anomaly Score**: {{anomaly_score}} / 10

---

## 🧠 ASSET HEALTH SCORE
- **Calculated Score**: {{health_score}} / 100
- **Interpretation**: {{ahs_condition}}

## 📋 FORMATTED SUMMARY BLOCK
{{overall_summary_text}}

🧠 **ASSET HEALTH SCORE (AHS):** {{health_score}} / 100  
**Condition:** {{ahs_condition}}

🔧 **PREDICTIVE MAINTENANCE PLAN**  
{{predictive_plan_table}}

REPORT TEXT:
{text}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert transformer diagnostics engineer. Generate valid JSON with asset health scores, predictive maintenance plans, and detailed technical analysis. Apply strict thresholds: PF (OK <0.3%, WARNING 0.3-0.5%, CRITICAL >0.5%), TTR (OK ≤0.5%, WARNING 0.5-1%, CRITICAL >1%), Demagnetization (INEFFECTIVE if Initial <20%)."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.1
        )
        
        return response.choices[0].message.content 
        
    except Exception as e:
        return f"Error analyzing report: {str(e)}" 