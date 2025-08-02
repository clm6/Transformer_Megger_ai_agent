### TRAX MASTER IMPROVEMENT PROMPT (UPDATED WITH PREDICTIVE MAINTENANCE)

---

This prompt enables enhanced transformer diagnostic reports with:

- Complete section-level parsing
- Threshold-based severity classification (OK, WARNING, CRITICAL)
- Pattern detection and reliability risk flags
- Selective section skipping if data is absent
- Confidence scoring
- Predictive maintenance plan and asset health score (0-100%)
- Full output formatting section for user-facing reports

---

### ⬇️ START OF REPORT TEMPLATE

# TRANSFORMER DIAGNOSTIC REPORT Equipment: {{transformer\_name}} Analysis Date: {{analysis\_date}} Source File: {{source\_file}}

```

## WINDING RESISTANCE ANALYSIS
{% if winding_resistance %}
{{winding_resistance}}
{% else %}
⚠️ Section not included in source document — skipped from analysis.
{% endif %}

## TURNS RATIO ANALYSIS
{% if turns_ratio %}
{{turns_ratio}}
{% else %}
⚠️ Section not included in source document — skipped from analysis.
{% endif %}

## TAN DELTA / MAIN INSULATION
{% if tan_delta %}
{{tan_delta}}
{% else %}
⚠️ Section not included in source document — skipped from analysis.
{% endif %}

## BUSHING POWER FACTOR ANALYSIS
{% if bushing_pf %}
{{bushing_pf}}
{% else %}
⚠️ Section not included in source document — skipped from analysis.
{% endif %}

## DEMAGNETIZATION ANALYSIS
{% if demagnetization %}
{{demagnetization}}
{% else %}
⚠️ Section not included in source document — skipped from analysis.
{% endif %}

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
- **Immediate Action Items**:
  - {{critical_action_items}}
- **Next Maintenance Interval**:
  - {{warning_retest_schedule}}
- **Quarterly Monitoring Targets**:
  - {{quarterly_monitoring}}
- **Replacement Cycle Recommendation**:
  - Based on component age, PF drift, and degradation slope, replace high-risk bushings/insulation within {{replacement_window}} months.
- **Anomaly Score**: {{anomaly_score}} / 10

---

## 🧠 ASSET HEALTH SCORE
- **Calculated Score**: {{health_score}} / 100
- **Interpretation**:
  - 90–100: Excellent
  - 75–89: Good
  - 60–74: Moderate
  - 40–59: Degraded
  - <40: Critical Risk

---

## 📋 FORMATTED SUMMARY BLOCK (for UI output or user copy-paste)

**WINDING RESISTANCE ANALYSIS**  
Tap {{tap_position_wr}}:
- H1-X0: {{wr_h1}} Ω  
- H2-X0: {{wr_h2}} Ω  
- H3-X0: {{wr_h3}} Ω  
- Max Deviation: {{wr_deviation}} ({{wr_pct}}%)  
- Stability: {{wr_stability}}  
- Status: {{wr_status}}

**TURNS RATIO ANALYSIS**  
Tap {{tap_position_ttr}}:
- Nominal TTR: {{ttr_nominal}}  
- Phase A: {{ttr_a}} ({{ttr_error_a}}%)  
- Phase B: {{ttr_b}} ({{ttr_error_b}}%)  
- Phase C: {{ttr_c}} ({{ttr_error_c}}%)  
- Excitation Currents: A: {{exc_a}} mA, B: {{exc_b}} mA, C: {{exc_c}} mA  
- Status: {{ttr_status}}

**TAN DELTA / MAIN INSULATION**  
- CHL: {{chl}} → {{chl_status}}  
- CLG: {{clg}} → {{clg_status}}  
- CLH: {{clh}} → {{clh_status}}  
- CHG: {{chg}} → {{chg_status}}  
- Moisture Pattern Detection: {{moisture_flag}}

**BUSHING POWER FACTOR ANALYSIS**  
- H1: {{bpf_h1}} → {{bpf_h1_status}}  
- H2: {{bpf_h2}} → {{bpf_h2_status}}  
- H3: {{bpf_h3}} → {{bpf_h3_status}}  
- X0–X3: {{bpf_x0_x3}} → {{bpf_x_cluster}}  
- Cluster Analysis: {{cluster_summary}}

**DEMAGNETIZATION**  
- Initial Remanence: {{demag_init}}  
- Final Remanence: {{demag_final}}  
- Status: {{demag_status}}

🔍 **OVERALL SUMMARY**  
{{overall_summary_text}}

🧠 **ASSET HEALTH SCORE (AHS):** {{ahs_score}} / 100  
**Weighting Breakdown:**
- Winding Resistance: {{score_wr}} pts  
- Turns Ratio: {{score_ttr}} pts  
- Main Insulation: {{score_ins}} pts  
- Bushing PF: {{score_bpf}} pts  
- Demagnetization: {{score_demag}} pts  
- Completeness & Confidence: {{score_confidence}} pts

📊 **Final Score:** {{ahs_score}} / 100 → Condition: {{ahs_condition}}

🔧 **PREDICTIVE MAINTENANCE PLAN**  
| Component       | Status     | Action     | Timeline       |
|----------------|------------|------------|----------------|
{{predictive_plan_table}}

---

End of diagnostic output.

```

