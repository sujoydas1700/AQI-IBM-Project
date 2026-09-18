# India Air Quality Index (AQI) Analysis - Complete Data Analytics Project

## 1. Project Overview

This is a comprehensive **data analytics project** designed to analyse air quality patterns across India (2023-2025). The project transforms raw AQI data into actionable insights through systematic data cleaning, exploratory analysis, key performance indicator (KPI) measurement, trend analysis, risk assessment, and interactive visualization.

**Goal:** Identify air quality patterns, locate pollution hotspots, assess monitoring infrastructure, and recommend data-driven actions for pollution control and public health protection.

---

## 2. Real-World Problem Statement

India faces significant air quality challenges with widespread pollution affecting public health, agricultural productivity, and economic activity. However, understanding where pollution is worst, when it peaks, which pollutants dominate, and how monitoring infrastructure is distributed requires systematic data analysis.

**Key Questions:**
- Which states and areas experience the worst air quality?
- What are the dominant pollutants and how do they vary geographically?
- How has air quality changed over time (2023-2025)?
- Are monitoring stations adequately distributed?
- Which regions need urgent intervention?
- What seasonal patterns exist and how can they inform public health responses?

---

## 3. Project Objectives

1. **Understand Air Quality Status:** Calculate nation-wide and region-wise AQI metrics
2. **Identify Hotspots:** Pinpoint states and areas with consistent poor air quality
3. **Assess Pollutant Patterns:** Determine dominant pollutants and their geographic/temporal variation
4. **Evaluate Monitoring Infrastructure:** Assess coverage and identify monitoring gaps
5. **Trend Analysis:** Detect improvements, deterioration, and seasonal patterns
6. **Risk Assessment:** Identify high-risk locations and periods requiring urgent action
7. **Actionable Recommendations:** Provide evidence-based recommendations for policy, monitoring, and intervention

---

## 4. Dataset Description

**Source:** Kaggle - India AQI Index 2023-2025  
**URL:** https://www.kaggle.com/datasets/saikiranudayana/india-air-quality-index-aqi-dataset-20232025

**Dataset Columns:**

| Column | Description |
|--------|-------------|
| `date` | Date of AQI measurement (YYYY-MM-DD format) |
| `state` | Indian state name |
| `area` | Geographic area/city/locality |
| `number_of_monitoring_stations` | Count of air quality monitoring stations in the area |
| `prominent_pollutants` | Primary pollutant(s) observed (e.g., PM2.5, NO2, SO2) |
| `aqi_value` | Numerical Air Quality Index value |
| `air_quality_status` | Categorical status (Good, Moderate, Poor, Very Poor, Severe) |
| `unit` | Measurement unit (typically μg/m³ or ppb) |
| `note` | Additional contextual notes |

**Dataset Characteristics:**
- **Time Period:** January 2023 - December 2025
- **Geographic Coverage:** Multiple Indian states and areas
- **Frequency:** Daily observations (where available)
- **Records:** Thousands of AQI measurements

---

## 5. Dataset Source

**Official Kaggle Dataset:**  
https://www.kaggle.com/datasets/saikiranudayana/india-air-quality-index-aqi-dataset-20232025

**Download Instructions:**
1. Visit the Kaggle link above
2. Accept the dataset terms (if required)
3. Download `india_aqi_2023_2025.csv`
4. Place the CSV file in the project directory (same folder as `project.py`)

---

## 6. Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **Pandas** | Data loading, cleaning, transformation, aggregation |
| **NumPy** | Numerical computations and array operations |
| **Matplotlib** | Statistical visualizations (line plots, histograms, bar charts) |
| **Seaborn** | Enhanced statistical plots |
| **Streamlit** | Interactive web-based dashboard for real-time exploration |

**Why These Libraries?**
- **Pandas:** Industry-standard for data manipulation and analysis
- **Matplotlib & Seaborn:** Reliable, publication-quality visualizations
- **Streamlit:** Lightweight, Python-native interactive dashboard without JavaScript
- **NumPy:** Efficient numerical operations and statistical calculations

---

## 7. Project Workflow

```
Raw Data (CSV)
      ↓
  Data Cleaning (missing values, duplicates, type conversion, standardization)
      ↓
  Exploratory Data Analysis (distribution, missing values, basic statistics)
      ↓
  KPI Calculation (average AQI, monitoring coverage, status distribution)
      ↓
  Time Trend Analysis (daily, monthly, yearly trends; seasonal patterns)
      ↓
  State & Area Analysis (regional disparities, location-specific metrics)
      ↓
  Pollutant Analysis (frequency, patterns, AQI correlation)
      ↓
  Risk & Opportunity Assessment (hotspots, gaps, improvement opportunities)
      ↓
  Insight Generation (data-driven findings)
      ↓
  Recommendations (actionable policy/operational suggestions)
      ↓
  Interactive Dashboard (Streamlit-based exploration)
```

---

## 8. Data Cleaning Process

### Cleaning Steps Implemented:

**8.1 Duplicate Removal**
- Identified and removed complete row duplicates
- Preserved data integrity by removing only identical records

**8.2 Date Conversion**
- Converted date column to datetime format
- Identified invalid dates (logged but not removed to preserve row counts)
- Extracted year, month, and month name for temporal analysis

**8.3 Text Standardization**
- Stripped leading/trailing whitespace from all text columns
- Applied Title Case to state and area names for consistency
- Standardized air quality status and pollutant categories

**8.4 Data Type Conversion**
- Converted AQI values to numeric (handling non-numeric entries)
- Converted monitoring station counts to numeric format

**8.5 Invalid AQI Value Removal**
- Removed AQI values outside valid range (0-500)
- Negative or extremely high values indicate measurement errors

**8.6 Missing Value Handling**
- **Critical columns (date, state, aqi_value):** Rows with missing values removed
- **Categorical columns (area, pollutants, status):** Missing values filled with 'Unknown'
- **Numeric columns (monitoring stations):** Missing values handled during aggregation

**8.7 Consistency Checks**
- Verified date ranges align with expected period (2023-2025)
- Checked AQI value distributions for anomalies
- Confirmed monitoring station counts are non-negative

**Cleaning Impact:**
All cleaning operations include logging. The exact number of rows removed is reported in the Streamlit dashboard's Data Cleaning Summary section.

---

## 9. KPI Analysis

### Core KPIs Calculated:

**Coverage Metrics:**
- **Total Observations:** Number of AQI records analysed
- **Unique States:** Geographic regions represented
- **Unique Areas:** Specific locations/cities covered
- **Total Monitoring Stations:** Sum of stations across all areas
- **Date Range:** Period covered by data

**AQI Statistics:**
- **Average AQI:** Mean AQI across all observations
- **Median AQI:** Mid-point AQI value (robust to outliers)
- **Maximum AQI:** Highest recorded value (severity indicator)
- **Minimum AQI:** Lowest recorded value (baseline)
- **Standard Deviation:** Measure of AQI variability

**Status Distribution:**
- **Percentage in Each Status Category:** Good, Moderate, Poor, Very Poor, Severe
- **Most Common Status:** Primary air quality classification observed

**Pollutant KPI:**
- **Most Frequently Observed Pollutant:** Primary pollution concern

### Why These KPIs?
- **Coverage metrics** show data comprehensiveness and infrastructure reach
- **AQI statistics** characterize air quality centrally and variability
- **Status distribution** indicates severity and prevalence of poor conditions
- **Pollutant metrics** identify primary emission control priorities

---

## 10. Key Analysis Sections

### 10.1 Time Trend Analysis

**Daily Trends:**
- Mean, max, and min AQI per day
- Identifies acute pollution events

**Monthly Trends:**
- Aggregated by month and year
- Reveals seasonal patterns and inter-year comparisons
- Supports seasonal forecasting and preparedness planning

**Yearly Trends:**
- Year-over-year comparison
- Identifies long-term improvement or deterioration

**Interpretation:**
- Upward trends indicate worsening air quality (requires urgent action)
- Downward trends suggest effectiveness of control measures
- Seasonal peaks point to meteorological and emission factors

### 10.2 State Analysis

**Metrics:**
- Average, max, min, and median AQI per state
- Observation count (indicates data coverage in that state)
- Most common air quality status
- Total monitoring stations

**Key Findings:**
- Ranks states from most to least polluted
- Identifies disparities in air quality across regions
- Shows monitoring infrastructure distribution

### 10.3 Area Analysis

**Metrics:**
- Area-level AQI statistics
- States where area is located
- Dominant air quality status

**Key Findings:**
- Identifies specific pollution hotspots
- Highlights persistently poor-quality areas
- Reveals micro-level geographic disparities

### 10.4 Pollutant Analysis

**Metrics:**
- Frequency of each pollutant
- Percentage of observations featuring each pollutant
- Average AQI by pollutant type
- Top pollutants by state (for top 5 states)

**Key Findings:**
- PM2.5 and NO2 often dominate (typical for India)
- Pollutant patterns vary by state (industrial vs. vehicular sources)
- Certain pollutants correlate with higher AQI values

---

## 11. Key Insights

### Insight 1: Overall Air Quality Assessment
**Finding:** National average AQI typically indicates Moderate to Poor air quality.  
**Evidence:** Mean AQI, distribution of status categories across dataset.  
**Meaning:** Widespread pollution affecting large population; health and environmental impacts likely.  
**Action:** Prioritize cross-state coordinated pollution reduction and public awareness campaigns.

### Insight 2: State-Level Disparities
**Finding:** Significant variation in AQI across states; certain states consistently exceed safe limits.  
**Evidence:** State-wise mean AQI ranking; max AQI values vary from ~200 to ~400+.  
**Meaning:** Localized sources (industry, traffic, geography) require targeted state-level interventions.  
**Action:** Implement state-specific emission control roadmaps aligned with local sources.

### Insight 3: Seasonal Patterns
**Finding:** AQI peaks in specific months (typically winter months like November-January in northern India).  
**Evidence:** Monthly aggregated AQI comparison; meteorological factors (stable atmospheric layers) trap pollutants.  
**Meaning:** Predictable seasonal peaks enable proactive interventions and public warnings.  
**Action:** Launch seasonal air quality forecasting system; implement pre-winter pollution control measures.

### Insight 4: Pollutant Composition
**Finding:** Specific pollutants dominate (e.g., PM2.5); patterns vary by region.  
**Evidence:** Pollutant frequency distribution; pollutant-AQI correlation analysis.  
**Meaning:** Different sources in different regions (vehicular, industrial, agricultural); require targeted source control.  
**Action:** Conduct source apportionment studies; implement sector-specific emission standards.

### Insight 5: Monitoring Infrastructure Gaps
**Finding:** Monitoring stations are unevenly distributed; some high-risk areas are undermonitored.  
**Evidence:** Monitoring station count vs. observation frequency; identified gaps in specific areas.  
**Meaning:** Limited early-warning capability in undermonitored regions; missed opportunities for localized interventions.  
**Action:** Expand real-time monitoring in undermonitored high-AQI areas; consider portable air quality sensors.

---

## 12. Risk and Opportunity Analysis

### RISKS Identified:

**Risk 1: High-AQI States**
- Specific states consistently exceed safe AQI thresholds
- Health impacts on population in these regions
- Action: Declare high-alert status; activate emergency protocols

**Risk 2: Poor Air Quality Status Areas**
- Locations with recurring "Poor," "Very Poor," or "Severe" status
- Critical public health concern
- Action: Issue health advisories; restrict outdoor activities for vulnerable groups

**Risk 3: Seasonal AQI Peaks**
- Certain months show dramatically elevated AQI
- Winter meteorology traps pollutants; harvest burning and heating emissions peak
- Action: Implement seasonal pre-emptive measures; activate air quality forecasting

**Risk 4: Undermonitored High-Risk Areas**
- Areas with high AQI but limited monitoring infrastructure
- Blind spots in early warning system
- Action: Prioritize monitoring expansion in these areas

### OPPORTUNITIES Identified:

**Opportunity 1: Improving States**
- States showing declining AQI trends over time
- Evidence of effective interventions
- Action: Study successful practices; scale to other regions

**Opportunity 2: Areas for Targeted Intervention**
- Moderate-AQI areas (100-200) where targeted measures could prevent deterioration
- "Low-hanging fruit" for pollution reduction
- Action: Identify specific sources; implement localized emission controls

**Opportunity 3: Undermonitored High-Risk Areas**
- Expanding monitoring infrastructure can improve early warning and response
- Enables more granular pollution source analysis
- Action: Install additional monitoring stations with real-time data transmission

**Opportunity 4: Seasonal Forecasting**
- Predictable seasonal patterns enable proactive management
- Time-bounded interventions can be more cost-effective
- Action: Develop and deploy seasonal air quality forecasting system

---

## 13. Recommended Actions

### Strategic Recommendations:

**1. Establish Integrated Monitoring Network**
- Expand monitoring stations in undermonitored high-AQI areas
- Implement real-time data transmission and public dashboards
- Enables rapid response to acute pollution events

**2. Implement Sector-Specific Emission Controls**
- Target dominant pollutants identified in analysis (PM2.5, NO2, SO2, etc.)
- Differentiate controls by source: vehicular, industrial, agricultural, residential
- Example: Vehicle emission standards, industrial stack monitoring, crop residue management

**3. Activate Seasonal Air Quality Management**
- Develop seasonal protocols for high-risk periods (winter months in most regions)
- Pre-winter preparedness: reduce discretionary burning, increase traffic management
- Spring protocols: manage agricultural residue burning

**4. Prioritize High-AQI States**
- Allocate resources proportional to AQI severity
- Implement stricter emission standards in high-AQI regions
- Support local governments with capacity building and technology deployment

**5. Public Awareness and Health Protection**
- Communicate AQI levels and health impacts to public
- Issue early warnings for vulnerable groups (children, elderly, respiratory patients)
- Promote protective behaviors (N95 masks, air purifiers, indoor activities during peaks)

**6. Conduct Source Apportionment Studies**
- Determine relative contribution of different sources (traffic, industry, agriculture, heating)
- Informs targeted interventions most likely to reduce AQI
- Example: If 40% of PM2.5 is from traffic, aggressive vehicle management is prioritized

**7. Regional Collaboration**
- Air pollution does not respect state boundaries
- Implement inter-state coordination mechanisms
- Share best practices and coordinate policies for shared airsheds

---

## 14. Machine Learning

**ML Approach in This Project:** Not Implemented (Analysis-Focused)

**Rationale:**
This project is designed as a **comprehensive analysis** rather than a prediction model. The available columns (AQI value, status, pollutants, location, date) support descriptive and comparative analytics effectively. While a time-series forecast model (ARIMA, Prophet) could predict future AQI values, several factors make it non-essential here:

1. **Strong Descriptive Insights:** Data already reveals clear patterns (seasonal, geographic, temporal)
2. **Limited Features:** Only 9 columns; lack of external features (meteorology, traffic density, industry stats)
3. **Sufficient for Decision-Making:** The analysis already identifies hotspots, trends, and risks without prediction
4. **Complexity vs. Value Trade-off:** A simple trend-based model would add little beyond the monthly/seasonal analysis already performed

**If ML were to be implemented (optional future enhancement):**
- **Target:** Predict next-month AQI by state
- **Features:** Historical AQI, month, year, dominant pollutants, monitoring station count
- **Model:** ARIMA or Prophet for time-series forecasting
- **Challenge:** Would require external meteorological data not in current dataset
- **Use Case:** Seasonal forecasting for proactive planning

---

## 15. How to Install

### Prerequisites:
- Python 3.8 or higher
- pip (Python package manager)
- Windows, macOS, or Linux environment

### Installation Steps:

**Step 1: Download the Dataset**
```bash
# Visit Kaggle and download india_aqi_2023_2025.csv
# https://www.kaggle.com/datasets/saikiranudayana/india-air-quality-index-aqi-dataset-20232025
# Place the CSV file in your project directory
```

**Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

This installs:
- pandas
- numpy
- matplotlib
- seaborn
- streamlit

**Troubleshooting:**
- If `pip install` fails, try: `python -m pip install --upgrade pip`
- On macOS: May need to use `pip3` instead of `pip`
- On Linux: May need to use `pip3` or install via `apt-get` first

---

## 16. How to Run

### Running the Interactive Dashboard:

```bash
streamlit run project.py
```

This command:
1. Launches a local Streamlit web server
2. Opens the dashboard in your default browser (usually http://localhost:8501)
3. Displays interactive visualizations and analysis sections

**Dashboard Navigation:**
- Use the sidebar to select analysis sections
- Charts update dynamically as you explore
- No manual page refreshes needed

### Expected Output:
- **Executive Overview:** KPI cards, AQI trends, status distribution, AQI histogram
- **State & Area Analysis:** State-level rankings, area-level heatmaps, detailed tables
- **Pollutant & Risk Analysis:** Pollutant frequency, risk areas, monitoring gaps
- **Insights & Recommendations:** 5 key data-driven insights with evidence and actions

---

## 17. Project Output

### What You'll See When Running:

**Dashboard Sections:**

1. **Executive Overview**
   - KPI metrics (average AQI, states covered, total observations, max AQI recorded)
   - Daily AQI trend line chart with min-max range
   - Air quality status pie chart (percentage in each category)
   - AQI distribution histogram

2. **State & Area Analysis**
   - Bar chart: Top 10 most polluted states
   - Bar chart: Top 10 least polluted states
   - Detailed state comparison table (mean AQI, observations, monitoring stations)
   - Top 15 most polluted areas (bar chart)
   - Detailed area comparison table

3. **Pollutant & Risk Analysis**
   - Pollutant frequency bar chart (top 10)
   - Average AQI by pollutant
   - High-risk areas table (poor/very poor/severe status)
   - High-AQI states table

4. **Insights & Recommendations**
   - 5 expandable insight cards with:
     - Data-driven finding
     - Supporting evidence
     - Interpretation
     - Recommended action
   - Opportunities section (improving states, intervention areas)
   - Summary of actionable recommendations

**Data Files Generated:**
- Interactive dashboard (Streamlit web interface)
- Console output showing data cleaning summary and KPI values

---

## 18. Limitations

### Dataset Limitations:

**L1: Data Availability Gaps**
- Some areas may have missing data for certain dates
- Monitoring infrastructure variability between states
- Not all areas are uniformly monitored over entire 2023-2025 period

**L2: External Factors Not Captured**
- Dataset lacks meteorological data (temperature, humidity, wind speed)
- No information on emission sources (traffic density, industrial activity)
- Geographic factors (altitude, nearby mountains) not captured
- Socioeconomic and demographic context missing

**L3: Causal Analysis Not Possible**
- Analysis identifies correlations and patterns, not causation
- Cannot claim that Pollutant X "causes" AQI Y based on observation data alone
- Source apportionment requires specialized modeling (receptor modeling, isotopic analysis)

**L4: Temporal Aggregation**
- Monthly and yearly aggregations mask daily variations
- Extreme events (pollution episodes) may be smoothed out

**L5: Geographic Resolution**
- Area-level data may hide micro-level variations
- Different areas have different monitoring station densities

### Analytical Limitations:

**L6: No Prediction Model**
- This project focuses on descriptive and diagnostic analysis
- Does not predict future AQI values (would require time-series forecasting)
- Seasonal patterns are descriptive, not predictive

**L7: Status Assignment**
- Air quality status categories (Good/Moderate/Poor) are predefined
- Unclear what exact AQI ranges map to each status
- Analysis assumes status values are accurate per official standards

---

## 19. Conclusion

This **India AQI Analysis Project** transforms raw air quality data into actionable insights. Through systematic data cleaning, comprehensive exploratory analysis, KPI measurement, temporal and geographic analysis, risk assessment, and interactive visualization, the project identifies:

- **Where:** Geographic hotspots with consistently poor air quality
- **When:** Seasonal and temporal patterns of pollution peaks
- **What:** Dominant pollutants and their role in air quality degradation
- **Why:** Monitoring infrastructure gaps and underserved regions
- **How:** Data-driven recommendations for monitoring, intervention, and policy

**Key Takeaways:**
1. India's air quality requires urgent, coordinated action across multiple sectors
2. State and regional disparities suggest need for localized strategies
3. Seasonal patterns enable predictive management and proactive intervention
4. Monitoring infrastructure gaps limit early warning capability
5. Source-specific interventions (targeting dominant pollutants) offer high-impact opportunities

**Next Steps for Users:**
1. Run the project using provided instructions
2. Explore the interactive dashboard for region-specific insights
3. Use findings to inform policy, budget allocation, and intervention planning
4. Monitor progress using the same dataset and analytical framework quarterly
5. Extend analysis with meteorological and emission source data for deeper insights

---

## Project Metadata

- **Version:** 1.0
- **Created:** 2024
- **Last Updated:** 2024
- **Language:** Python
- **Dependencies:** pandas, numpy, matplotlib, seaborn, streamlit
- **Compatible Platforms:** Windows, macOS, Linux
- **Python Version:** 3.8+

---

## Support & Notes

- Ensure CSV file is named exactly: `india_aqi_2023_2025.csv`
- Place CSV in same directory as `project.py`
- First run may take 30-60 seconds as Streamlit initializes
- Dashboard works best on screens ≥1024px width
- For troubleshooting, check Streamlit documentation: https://docs.streamlit.io/

---

**End of README**
