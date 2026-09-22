"""
India Air Quality Index (AQI) Analysis - Complete Data Analytics Project
Project Objective: Analyse air quality patterns, identify risks, and provide actionable insights
Dataset: India AQI Index 2023-2025 from Kaggle
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

# Set visualization style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Streamlit page configuration
st.set_page_config(
    page_title="India AQI Analysis Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 1. LOAD DATASET
# ============================================================================

@st.cache_data
def load_data():
    """Load AQI dataset from CSV"""
    try:
        df = pd.read_csv('aqi.csv')
        return df
    except FileNotFoundError:
        st.error("❌ Dataset file 'aqi.csv' not found. Please download it and place it in the project directory.")
        st.stop()

df_raw = load_data()

# ============================================================================
# 2. DATA CLEANING
# ============================================================================

def clean_data(df):
    """
    Comprehensive data cleaning with documentation
    """
    df = df.copy()
    
    # Record initial state
    initial_rows = len(df)
    
    # 2.1: Remove complete duplicates
    duplicates_before = df.duplicated().sum()
    df = df.drop_duplicates()
    duplicates_removed = duplicates_before - df.duplicated().sum()
    
    # 2.2: Convert date column
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    date_nulls = df['date'].isna().sum()
    
    # 2.3: Strip whitespace from string columns
    string_cols = df.select_dtypes(include='object').columns
    for col in string_cols:
        df[col] = df[col].str.strip()
    
    # 2.4: Standardize state names (capitalize first letter)
    if 'state' in df.columns:
        df['state'] = df['state'].str.title()
    
    # 2.5: Standardize area names
    if 'area' in df.columns:
        df['area'] = df['area'].str.title()
    
    # 2.6: Standardize air_quality_status
    if 'air_quality_status' in df.columns:
        df['air_quality_status'] = df['air_quality_status'].str.title()
    
    # 2.7: Standardize prominent_pollutants
    if 'prominent_pollutants' in df.columns:
        df['prominent_pollutants'] = df['prominent_pollutants'].str.title()
    
    # 2.8: Convert AQI value to numeric
    if 'aqi_value' in df.columns:
        df['aqi_value'] = pd.to_numeric(df['aqi_value'], errors='coerce')
    
    # 2.9: Remove rows with invalid AQI values (negative or unrealistic)
    if 'aqi_value' in df.columns:
        invalid_aqi = df[(df['aqi_value'] < 0) | (df['aqi_value'] > 500)].shape[0]
        df = df[(df['aqi_value'] >= 0) & (df['aqi_value'] <= 500)]
    
    # 2.10: Convert monitoring stations to numeric
    if 'number_of_monitoring_stations' in df.columns:
        df['number_of_monitoring_stations'] = pd.to_numeric(
            df['number_of_monitoring_stations'], 
            errors='coerce'
        )
    
    # 2.11: Remove rows with missing critical columns
    critical_cols = ['date', 'state', 'aqi_value']
    df = df.dropna(subset=critical_cols)
    
    # 2.12: Handle missing values in other columns (fill with 'Unknown' for categoricals)
    if 'area' in df.columns:
        df['area'] = df['area'].fillna('Unknown')
    if 'prominent_pollutants' in df.columns:
        df['prominent_pollutants'] = df['prominent_pollutants'].fillna('Unknown')
    if 'air_quality_status' in df.columns:
        df['air_quality_status'] = df['air_quality_status'].fillna('Unknown')
    
    # 2.13: Extract year and month for analysis
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%B')
    
    final_rows = len(df)
    rows_removed = initial_rows - final_rows
    
    # Log cleaning summary
    cleaning_log = f"""
    DATA CLEANING SUMMARY:
    =====================
    Initial rows: {initial_rows}
    Final rows: {final_rows}
    Rows removed: {rows_removed} ({100*rows_removed/initial_rows:.1f}%)
    
    Duplicates removed: {duplicates_removed}
    Invalid dates: {date_nulls}
    Invalid AQI values: {invalid_aqi if 'invalid_aqi' in locals() else 0}
    
    Missing values handled:
    - Whitespace stripped from all text columns
    - State/Area names standardized (Title Case)
    - Text values standardized (Title Case)
    """
    
    return df, cleaning_log

df_clean, cleaning_log = clean_data(df_raw)

# ============================================================================
# 3. KPI CALCULATIONS
# ============================================================================

def calculate_kpis(df):
    """Calculate key performance indicators"""
    
    kpis = {
        'Total Observations': len(df),
        'Date Range': f"{df['date'].min().date()} to {df['date'].max().date()}",
        'Unique States': df['state'].nunique(),
        'Unique Areas': df['area'].nunique(),
        'Total Monitoring Stations': int(df['number_of_monitoring_stations'].sum()),
        'Average AQI': round(df['aqi_value'].mean(), 2),
        'Median AQI': round(df['aqi_value'].median(), 2),
        'Max AQI': int(df['aqi_value'].max()),
        'Min AQI': int(df['aqi_value'].min()),
        'Std Dev AQI': round(df['aqi_value'].std(), 2),
    }
    
    # Air Quality Status Distribution
    status_dist = df['air_quality_status'].value_counts()
    for status in status_dist.index:
        pct = (status_dist[status] / len(df)) * 100
        kpis[f'{status} (%)'] = round(pct, 1)
    
    # Most common pollutant
    if df['prominent_pollutants'].nunique() > 0:
        most_common_pollutant = df['prominent_pollutants'].value_counts().index[0]
        kpis['Most Common Pollutant'] = most_common_pollutant
    
    return kpis

kpis = calculate_kpis(df_clean)

# ============================================================================
# 4. EXPLORATORY DATA ANALYSIS
# ============================================================================

def perform_eda(df):
    """Generate exploratory data analysis statistics"""
    
    eda_report = {
        'Dataset Shape': df.shape,
        'Data Types': df.dtypes.to_dict(),
        'Missing Values': df.isnull().sum().to_dict(),
        'AQI Statistics': df['aqi_value'].describe().to_dict(),
        'Date Range': (df['date'].min(), df['date'].max()),
        'States Covered': sorted(df['state'].unique()),
        'Air Quality Status': df['air_quality_status'].value_counts().to_dict(),
        'Top 10 Pollutants': df['prominent_pollutants'].value_counts().head(10).to_dict(),
    }
    
    return eda_report

eda_report = perform_eda(df_clean)

# ============================================================================
# 5. TIME ANALYSIS
# ============================================================================

def time_trend_analysis(df):
    """Analyse AQI trends over time"""
    
    # Daily trends
    daily_aqi = df.groupby('date')['aqi_value'].agg(['mean', 'max', 'min', 'count']).reset_index()
    daily_aqi.columns = ['Date', 'Mean AQI', 'Max AQI', 'Min AQI', 'Observations']
    
    # Monthly trends
    monthly_aqi = df.groupby(['year', 'month', 'month_name'])['aqi_value'].agg(
        ['mean', 'max', 'min', 'count']
    ).reset_index()
    monthly_aqi.columns = ['Year', 'Month', 'Month Name', 'Mean AQI', 'Max AQI', 'Min AQI', 'Count']
    
    # Yearly trends
    yearly_aqi = df.groupby('year')['aqi_value'].agg(['mean', 'max', 'min', 'count']).reset_index()
    yearly_aqi.columns = ['Year', 'Mean AQI', 'Max AQI', 'Min AQI', 'Count']
    
    return daily_aqi, monthly_aqi, yearly_aqi

daily_aqi, monthly_aqi, yearly_aqi = time_trend_analysis(df_clean)

# ============================================================================
# 6. STATE & AREA ANALYSIS
# ============================================================================

def state_area_analysis(df):
    """Analyse AQI by state and area"""
    
    # State-wise analysis
    state_analysis = df.groupby('state').agg({
        'aqi_value': ['mean', 'max', 'min', 'median', 'count'],
        'number_of_monitoring_stations': 'sum',
        'air_quality_status': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown'
    }).round(2)
    state_analysis.columns = ['Mean AQI', 'Max AQI', 'Min AQI', 'Median AQI', 'Observations', 
                               'Total Stations', 'Most Common Status']
    state_analysis = state_analysis.sort_values('Mean AQI', ascending=False)
    
    # Area-wise analysis
    area_analysis = df.groupby('area').agg({
        'aqi_value': ['mean', 'max', 'min', 'count'],
        'state': lambda x: ', '.join(x.unique()),
        'air_quality_status': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown'
    }).round(2)
    area_analysis.columns = ['Mean AQI', 'Max AQI', 'Min AQI', 'Observations', 'States', 'Most Common Status']
    area_analysis = area_analysis.sort_values('Mean AQI', ascending=False)
    
    return state_analysis, area_analysis

state_analysis, area_analysis = state_area_analysis(df_clean)

# ============================================================================
# 7. POLLUTANT ANALYSIS
# ============================================================================

def pollutant_analysis(df):
    """Analyse prominent pollutants"""
    
    # Overall pollutant frequency
    pollutant_freq = df['prominent_pollutants'].value_counts().reset_index()
    pollutant_freq.columns = ['Pollutant', 'Frequency']
    pollutant_freq['Percentage'] = (pollutant_freq['Frequency'] / len(df) * 100).round(1)
    
    # Pollutant by state (top states)
    top_states = df['state'].value_counts().head(5).index
    pollutant_by_state = {}
    
    for state in top_states:
        state_data = df[df['state'] == state]
        pollutant_by_state[state] = state_data['prominent_pollutants'].value_counts().head(3).to_dict()
    
    # Average AQI by pollutant
    aqi_by_pollutant = df.groupby('prominent_pollutants')['aqi_value'].agg(['mean', 'max', 'min', 'count']).round(2)
    aqi_by_pollutant = aqi_by_pollutant.sort_values('mean', ascending=False)
    
    return pollutant_freq, pollutant_by_state, aqi_by_pollutant

pollutant_freq, pollutant_by_state, aqi_by_pollutant = pollutant_analysis(df_clean)

# ============================================================================
# 8. RISK & OPPORTUNITY ANALYSIS
# ============================================================================

def risk_opportunity_analysis(df, state_analysis):
    """Identify risks and opportunities"""
    
    risks = {}
    opportunities = {}
    
    # RISK: States with consistently high AQI
    high_aqi_states = state_analysis[state_analysis['Mean AQI'] > state_analysis['Mean AQI'].quantile(0.75)]
    risks['High AQI States'] = high_aqi_states.index.tolist()
    risks['High AQI States Mean'] = high_aqi_states['Mean AQI'].values
    
    # RISK: Areas with poor air quality status
    poor_status_areas = df[df['air_quality_status'].isin(['Poor', 'Very Poor', 'Severe'])]['area'].value_counts()
    risks['High Risk Areas'] = poor_status_areas.head(10).to_dict()
    
    # RISK: Periods with elevated AQI
    monthly_high_aqi = monthly_aqi[monthly_aqi['Mean AQI'] > df['aqi_value'].quantile(0.75)]
    risks['High AQI Months'] = monthly_high_aqi[['Year', 'Month Name', 'Mean AQI']].to_dict('records')
    
    # RISK: Monitoring station distribution gap
    low_station_areas = df.groupby('area')['number_of_monitoring_stations'].mean()
    low_station_areas = low_station_areas[low_station_areas < low_station_areas.quantile(0.25)]
    risks['Areas with Limited Monitoring'] = low_station_areas.head(5).to_dict()
    
    # OPPORTUNITY: States showing improvement
    if len(yearly_aqi) > 1:
        improvement = {}
        for state in df['state'].unique():
            state_yearly = df[df['state'] == state].groupby('year')['aqi_value'].mean()
            if len(state_yearly) > 1:
                trend = state_yearly.iloc[-1] - state_yearly.iloc[0]
                improvement[state] = trend
        
        improving_states = sorted(improvement.items(), key=lambda x: x[1])[:5]
        opportunities['Improving States'] = improving_states
    
    # OPPORTUNITY: Areas where targeted interventions could help
    moderate_aqi_areas = df[(df['aqi_value'] > 100) & (df['aqi_value'] < 200)]['area'].value_counts().head(5)
    opportunities['Areas for Targeted Intervention'] = moderate_aqi_areas.to_dict()
    
    # OPPORTUNITY: Enhance monitoring in undermonitored areas
    undermonitored = df.groupby('area').agg({
        'number_of_monitoring_stations': 'mean',
        'aqi_value': 'mean'
    }).sort_values('number_of_monitoring_stations')
    undermonitored = undermonitored[undermonitored['aqi_value'] > df['aqi_value'].median()]
    opportunities['Undermonitored High-Risk Areas'] = undermonitored.head(5).to_dict()
    
    return risks, opportunities

risks, opportunities = risk_opportunity_analysis(df_clean, state_analysis)

# ============================================================================
# 9. GENERATE INSIGHTS & RECOMMENDATIONS
# ============================================================================

def generate_insights(df, kpis, state_analysis, area_analysis, risks, opportunities):
    """Generate actionable insights from analysis"""
    
    insights = []
    
    # Insight 1: Overall AQI Status
    avg_aqi = kpis['Average AQI']
    if avg_aqi > 200:
        severity = "Poor to Very Poor"
    elif avg_aqi > 150:
        severity = "Moderate to Poor"
    elif avg_aqi > 100:
        severity = "Moderate"
    else:
        severity = "Good to Moderate"
    
    insights.append({
        'Title': 'Overall Air Quality Assessment',
        'Finding': f"Average AQI across India is {avg_aqi} ({severity})",
        'Evidence': f"Mean AQI: {avg_aqi}, Median: {kpis['Median AQI']}, Range: {kpis['Min AQI']}-{kpis['Max AQI']}",
        'Meaning': 'Indicates widespread air quality concerns requiring systematic action',
        'Action': 'Implement nation-wide air quality monitoring and periodic review of pollution control measures'
    })
    
    # Insight 2: State Disparities
    top_polluted = state_analysis.head(3)
    insights.append({
        'Title': 'State-Level Air Quality Disparities',
        'Finding': f"Significant variation in AQI across states: Top 3 most polluted are {', '.join(top_polluted.index[:3])}",
        'Evidence': f"Mean AQI ranges from {state_analysis['Mean AQI'].min():.1f} to {state_analysis['Mean AQI'].max():.1f}",
        'Meaning': 'Pollution hotspots require targeted regional interventions',
        'Action': 'Prioritize resources and stricter emission controls in high-AQI states'
    })
    
    # Insight 3: Pollutant Patterns
    top_pollutant = pollutant_freq.iloc[0]
    insights.append({
        'Title': 'Dominant Pollutant Patterns',
        'Finding': f"'{top_pollutant['Pollutant']}' is the most commonly observed pollutant ({top_pollutant['Percentage']}% of observations)",
        'Evidence': f"Frequency distribution: {pollutant_freq.head(3)[['Pollutant', 'Percentage']].to_dict()}",
        'Meaning': 'Points to specific emission sources that could be targeted for reduction',
        'Action': 'Conduct source apportionment studies and implement sector-specific pollution controls'
    })
    
    # Insight 4: Monitoring Coverage
    total_stations = kpis['Total Monitoring Stations']
    total_areas = kpis['Unique Areas']
    coverage = total_stations / total_areas if total_areas > 0 else 0
    
    insights.append({
        'Title': 'Monitoring Infrastructure Assessment',
        'Finding': f"Current monitoring infrastructure includes {total_stations} stations across {total_areas} areas ({coverage:.1f} stations per area)",
        'Evidence': f"Total observations: {kpis['Total Observations']}, Geographic spread: {kpis['Unique States']} states, {total_areas} areas",
        'Meaning': 'Uneven coverage may limit early warning capabilities in undermonitored regions',
        'Action': 'Expand real-time monitoring in undermonitored high-risk areas, especially in industrialized zones'
    })
    
    # Insight 5: Temporal Patterns
    max_month = monthly_aqi.loc[monthly_aqi['Mean AQI'].idxmax()]
    min_month = monthly_aqi.loc[monthly_aqi['Mean AQI'].idxmin()]
    
    insights.append({
        'Title': 'Seasonal and Temporal Patterns',
        'Finding': f"AQI peaks in {min_month['Month Name']} (mean {min_month['Mean AQI']:.1f}) and reaches lowest in other seasons",
        'Evidence': f"Monthly average AQI variation: {monthly_aqi['Mean AQI'].min():.1f} to {monthly_aqi['Mean AQI'].max():.1f}",
        'Meaning': 'Seasonal patterns indicate meteorological and emission influences that require predictive management',
        'Action': 'Implement seasonal air quality forecasting and pre-emptive pollution controls during high-risk periods'
    })
    
    return insights

insights = generate_insights(df_clean, kpis, state_analysis, area_analysis, risks, opportunities)

# ============================================================================
# 10. STREAMLIT DASHBOARD
# ============================================================================

def main():
    """Main Streamlit application"""
    
    st.title("🌍 India Air Quality Index (AQI) Analysis Dashboard")
    st.markdown("*Data-Driven Analysis of Air Quality Patterns (2023-2025)*")
    
    # Sidebar navigation
    page = st.sidebar.radio(
        "Select Analysis Section",
        ["📊 Executive Overview", "📈 State & Area Analysis", "💨 Pollutant & Risk Analysis", "📋 Insights & Recommendations"]
    )
    
    # ========================================================================
    # PAGE 1: EXECUTIVE OVERVIEW
    # ========================================================================
    
    if page == "📊 Executive Overview":
        st.header("Executive Summary")
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Average AQI", f"{kpis['Average AQI']:.0f}", delta="Nation-wide")
        with col2:
            st.metric("States Covered", kpis['Unique States'], delta="Geographic spread")
        with col3:
            st.metric("Total Observations", kpis['Total Observations'], delta="Data points")
        with col4:
            st.metric("Max AQI Recorded", kpis['Max AQI'], delta="Peak pollution")
        
        st.markdown("---")
        
        # AQI Trend
        st.subheader("📈 AQI Trend Over Time")
        fig_trend, ax = plt.subplots(figsize=(12, 5))
        ax.plot(daily_aqi['Date'], daily_aqi['Mean AQI'], linewidth=2, label='Daily Mean', alpha=0.7)
        ax.fill_between(daily_aqi['Date'], daily_aqi['Min AQI'], daily_aqi['Max AQI'], alpha=0.2, label='Range (Min-Max)')
        ax.set_xlabel('Date')
        ax.set_ylabel('AQI Value')
        ax.set_title('Daily AQI Trend')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig_trend)
        
        # Air Quality Status Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Air Quality Status Distribution")
            status_counts = df_clean['air_quality_status'].value_counts()
            fig_status, ax = plt.subplots(figsize=(8, 6))
            colors = ['green', 'yellow', 'orange', 'red', 'darkred']
            ax.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', 
                   colors=colors[:len(status_counts)], startangle=90)
            ax.set_title('Distribution of Air Quality Status')
            st.pyplot(fig_status)
        
        with col2:
            st.subheader("📊 AQI Distribution")
            fig_dist, ax = plt.subplots(figsize=(8, 6))
            ax.hist(df_clean['aqi_value'], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
            ax.set_xlabel('AQI Value')
            ax.set_ylabel('Frequency')
            ax.set_title('Distribution of AQI Values')
            ax.axvline(kpis['Average AQI'], color='red', linestyle='--', linewidth=2, label=f"Mean: {kpis['Average AQI']:.0f}")
            ax.legend()
            st.pyplot(fig_dist)
        
        # Key Metrics
        st.subheader("📌 Key Metrics Summary")
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.write(f"**Median AQI:** {kpis['Median AQI']}")
            st.write(f"**Min AQI:** {kpis['Min AQI']}")
            st.write(f"**Std Dev:** {kpis['Std Dev AQI']}")
        
        with metrics_col2:
            st.write(f"**Date Range:** {kpis['Date Range']}")
            st.write(f"**Unique Areas:** {kpis['Unique Areas']}")
            st.write(f"**Most Common Status:** {df_clean['air_quality_status'].value_counts().index[0]}")
        
        with metrics_col3:
            st.write(f"**Total Stations:** {int(kpis['Total Monitoring Stations'])}")
            st.write(f"**Most Common Pollutant:** {kpis['Most Common Pollutant']}")
    
    # ========================================================================
    # PAGE 2: STATE & AREA ANALYSIS
    # ========================================================================
    
    elif page == "📈 State & Area Analysis":
        st.header("State & Area Level Analysis")
        
        # State Analysis
        st.subheader("🏙️ State-wise AQI Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Top 10 Most Polluted States**")
            fig_top_states, ax = plt.subplots(figsize=(10, 6))
            top_10_states = state_analysis.head(10)['Mean AQI'].sort_values()
            ax.barh(range(len(top_10_states)), top_10_states.values, color='steelblue')
            ax.set_yticks(range(len(top_10_states)))
            ax.set_yticklabels(top_10_states.index)
            ax.set_xlabel('Mean AQI')
            ax.set_title('Top 10 Most Polluted States')
            ax.grid(True, alpha=0.3, axis='x')
            st.pyplot(fig_top_states)
        
        with col2:
            st.write("**Top 10 Least Polluted States**")
            fig_bottom_states, ax = plt.subplots(figsize=(10, 6))
            bottom_10_states = state_analysis.tail(10)['Mean AQI'].sort_values(ascending=False)
            ax.barh(range(len(bottom_10_states)), bottom_10_states.values, color='lightgreen')
            ax.set_yticks(range(len(bottom_10_states)))
            ax.set_yticklabels(bottom_10_states.index)
            ax.set_xlabel('Mean AQI')
            ax.set_title('Top 10 Least Polluted States')
            ax.grid(True, alpha=0.3, axis='x')
            st.pyplot(fig_bottom_states)
        
        # State comparison table
        st.write("**Detailed State Analysis**")
        st.dataframe(state_analysis.head(15), use_container_width=True)
        
        # Area Analysis
        st.subheader("🗺️ Area-wise AQI Analysis")
        
        st.write("**Top 15 Most Polluted Areas**")
        fig_top_areas, ax = plt.subplots(figsize=(12, 7))
        top_15_areas = area_analysis.head(15)['Mean AQI'].sort_values()
        colors_areas = plt.cm.Reds(np.linspace(0.4, 0.9, len(top_15_areas)))
        ax.barh(range(len(top_15_areas)), top_15_areas.values, color=colors_areas)
        ax.set_yticks(range(len(top_15_areas)))
        ax.set_yticklabels(top_15_areas.index, fontsize=9)
        ax.set_xlabel('Mean AQI')
        ax.set_title('Top 15 Most Polluted Areas')
        ax.grid(True, alpha=0.3, axis='x')
        st.pyplot(fig_top_areas)
        
        st.dataframe(area_analysis.head(20), use_container_width=True)
    
    # ========================================================================
    # PAGE 3: POLLUTANT & RISK ANALYSIS
    # ========================================================================
    
    elif page == "💨 Pollutant & Risk Analysis":
        st.header("Pollutant & Risk Analysis")
        
        # Pollutant Analysis
        st.subheader("💨 Prominent Pollutants Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Pollutant Frequency Distribution**")
            fig_pollutants, ax = plt.subplots(figsize=(10, 6))
            top_pollutants = pollutant_freq.head(10)
            ax.bar(range(len(top_pollutants)), top_pollutants['Frequency'].values, color='coral')
            ax.set_xticks(range(len(top_pollutants)))
            ax.set_xticklabels(top_pollutants['Pollutant'].values, rotation=45, ha='right')
            ax.set_ylabel('Frequency')
            ax.set_title('Top 10 Most Frequent Pollutants')
            ax.grid(True, alpha=0.3, axis='y')
            st.pyplot(fig_pollutants)
        
        with col2:
            st.write("**Average AQI by Pollutant**")
            fig_aqi_pollutant, ax = plt.subplots(figsize=(10, 6))
            top_pollutants_aqi = aqi_by_pollutant.head(10)['mean'].sort_values()
            ax.barh(range(len(top_pollutants_aqi)), top_pollutants_aqi.values, color='darkred')
            ax.set_yticks(range(len(top_pollutants_aqi)))
            ax.set_yticklabels(top_pollutants_aqi.index)
            ax.set_xlabel('Mean AQI')
            ax.set_title('Average AQI by Pollutant (Top 10)')
            ax.grid(True, alpha=0.3, axis='x')
            st.pyplot(fig_aqi_pollutant)
        
        st.dataframe(pollutant_freq.head(15), use_container_width=True)
        
        # Risk Analysis
        st.subheader("⚠️ Risk Assessment")
        
        st.write("**High-Risk Areas (Poor/Very Poor/Severe Status)**")
        if risks['High Risk Areas']:
            risk_df = pd.DataFrame(list(risks['High Risk Areas'].items()), columns=['Area', 'Occurrences'])
            risk_df = risk_df.sort_values('Occurrences', ascending=False).head(15)
            st.dataframe(risk_df, use_container_width=True)
        
        st.write("**High-AQI States Requiring Attention**")
        high_aqi_info = state_analysis.loc[state_analysis.index.isin(risks['High AQI States'])]
        st.dataframe(high_aqi_info, use_container_width=True)
    
    # ========================================================================
    # PAGE 4: INSIGHTS & RECOMMENDATIONS
    # ========================================================================
    
    elif page == "📋 Insights & Recommendations":
        st.header("Key Insights & Recommended Actions")
        
        st.markdown("""
        This section presents data-driven insights discovered through rigorous analysis of the India AQI dataset.
        Each insight is supported by evidence from the data and linked to actionable recommendations.
        """)
        
        for i, insight in enumerate(insights, 1):
            with st.expander(f"📌 Insight {i}: {insight['Title']}", expanded=(i==1)):
                st.markdown(f"**Finding:** {insight['Finding']}")
                st.markdown(f"**Evidence:** {insight['Evidence']}")
                st.markdown(f"**Meaning:** {insight['Meaning']}")
                st.markdown(f"**Recommended Action:** {insight['Action']}")
                st.markdown("---")
        
        # Opportunities
        st.subheader("🎯 Opportunities for Improvement")
        
        if 'Improving States' in opportunities:
            st.write("**States Showing Air Quality Improvement**")
            improving = opportunities['Improving States']
            for state, trend in improving[:5]:
                change = "↓ Improving" if trend < 0 else "↑ Worsening"
                st.write(f"- {state}: {change} (change: {trend:.1f})")
        
        st.write("**Areas for Targeted Intervention**")
        if opportunities['Areas for Targeted Intervention']:
            intervention_df = pd.DataFrame(
                list(opportunities['Areas for Targeted Intervention'].items()),
                columns=['Area', 'Observations']
            )
            st.dataframe(intervention_df, use_container_width=True)
        
        st.write("**Undermonitored High-Risk Areas**")
        if opportunities['Undermonitored High-Risk Areas']:
            st.json(opportunities['Undermonitored High-Risk Areas'])
        
        # Summary Recommendations
        st.subheader("🎯 Summary of Recommended Actions")
        
        recommendations = [
            "1. **Strengthen Real-Time Monitoring:** Expand monitoring infrastructure in undermonitored regions, especially industrial and urban areas.",
            "2. **Implement Sector-Specific Controls:** Focus on controlling the most frequent pollutants identified in the analysis.",
            "3. **Seasonal Preparedness:** Develop and activate seasonal air quality management protocols during high-risk periods.",
            "4. **Regional Strategies:** Tailor pollution control measures for high-AQI states based on local sources and conditions.",
            "5. **Public Awareness:** Enhance communication about air quality status to drive individual and corporate behavior change.",
            "6. **Research Investment:** Conduct deeper source apportionment studies to guide long-term emission reduction strategies.",
        ]
        
        for rec in recommendations:
            st.markdown(rec)

# ============================================================================
# 11. EXECUTE DASHBOARD
# ============================================================================

if __name__ == "__main__":
    main()
