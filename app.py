import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Aadhaar Friction Command Center", layout="wide")

st.title("Aadhaar Last-Mile Friction Index")
st.markdown("**AI-Powered System Efficiency Monitoring Dashboard**")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("processed_analytics_data.csv")
    except FileNotFoundError:
        return None
    
    cluster_names = {
        0: "🟢 Healthy Growth",
        1: "🟠 High Maintenance",
        2: "🔴 Critical Friction"
    }
    
    if 'Cluster_Label' in df.columns:
        df['Cluster_Name'] = df['Cluster_Label'].map(cluster_names)
    else:
        df['Cluster_Name'] = "Unknown"
        
    return df

df = load_data()

if df is None:
    st.error("File 'AADHAAR_DASHBOARD_FINAL.csv' not found! Run 'day5_geo_merger.py' first.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Avg Friction Score", f"{df['Friction_Score'].mean():.1f}%")
with col2:
    if 'Cluster_Label' in df.columns:
        crit_count = df[df['Cluster_Label'] == 2].shape[0]
    else:
        crit_count = 0
    st.metric("Critical Friction Districts", crit_count, delta="Require Immediate Action", delta_color="inverse")
with col3:
    risk_count = df[df['Child_Risk_Score'] > 90].shape[0]
    st.metric("Child Exclusion Risks", risk_count, delta="School Camps Needed", delta_color="inverse")
with col4:
    st.metric("Total Updates Processed", f"{df['Total_Updates'].sum():,}")

st.markdown("---")

col_left, col_right = st.columns([3, 1])

with col_left:
    st.subheader(" Live Friction Map")
    
    if 'Latitude' in df.columns and 'Longitude' in df.columns:
        map_data = df.dropna(subset=['Latitude', 'Longitude'])
        
        fig = px.scatter_map(
            map_data,
            lat="Latitude",
            lon="Longitude",
            color="Cluster_Name",
            size="Total_Updates", 
            hover_name="district_clean",
            hover_data={
                "Friction_Score": ":.1f", 
                "Child_Risk_Score": ":.1f",
                "Latitude": False, 
                "Longitude": False
            },
            color_discrete_map={
                "🟢 Healthy Growth": "green",
                "🟠 High Maintenance": "orange", 
                "🔴 Critical Friction": "red"
            },
            zoom=3.5,
            center={"lat": 22.0, "lon": 82.0},
            height=600,
            title="Geospatial Risk Analysis (Size = Activity Volume)"
        )
        
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r":0,"t":40,"l":0,"b":0} 
        )
        
        st.plotly_chart(
            fig, 
            key="map_chart", 
            config={'scrollZoom': True, 'displayModeBar': True},
            width="stretch" 
        )
    else:
        st.warning("Geospatial data missing. Showing Scatter Plot instead.")
        fig = px.scatter(df, x="Total_Enrolment", y="Friction_Score", color="Cluster_Name")
        st.plotly_chart(fig, key="scatter_fallback", width="stretch")

with col_right:
    st.subheader(" Priority Action List")
    if 'Cluster_Label' in df.columns:
        priority_df = df[df['Cluster_Label'] == 2][['district_clean', 'Friction_Score']]
    else:
        priority_df = df.head(10)

    st.dataframe(
        priority_df.sort_values('Friction_Score', ascending=False).style.background_gradient(cmap="Reds"),
        hide_index=True,
        width="stretch"
    )

st.markdown("---")
st.subheader(" District Diagnostics")
selected_district = st.selectbox("Select District", df['district_clean'].unique())

if selected_district:
    d_row = df[df['district_clean'] == selected_district].iloc[0]
    
    c1, c2, c3 = st.columns(3)
    c1.info(f"**Cluster:** {d_row['Cluster_Name']}")
    c2.warning(f"**Friction Score:** {d_row['Friction_Score']:.1f}")
    c3.error(f"**Child Risk:** {d_row['Child_Risk_Score']:.1f}%")
    
    if 'Cluster_Label' in df.columns and d_row['Cluster_Label'] == 2:
        st.error(" **Recommendation:** Deploy specialized Correction Camp immediately.")
    elif d_row['Child_Risk_Score'] > 50:
        st.warning(" **Recommendation:** Contact District Education Officer for School Biometric Drive.")
    else:
        st.success(" **Recommendation:** Continue standard monitoring.")

st.markdown("---")
st.subheader(" District Comparator")
col_a, col_b = st.columns(2)

with col_a:
    dist_a = st.selectbox("Select District A", df['district_clean'].unique(), index=0, key='dist_a')
with col_b:
    dist_b = st.selectbox("Select District B", df['district_clean'].unique(), index=1, key='dist_b')

if dist_a and dist_b:
    a_data = df[df['district_clean'] == dist_a].iloc[0]
    b_data = df[df['district_clean'] == dist_b].iloc[0]

    comp_data = {
        "Metric": ["Friction Score", "Child Risk Score", "Total Updates", "Risk Category"],
        f"{dist_a}": [
            f"{a_data['Friction_Score']:.1f}%", 
            f"{a_data['Child_Risk_Score']:.1f}%", 
            f"{int(a_data['Total_Updates']):,}",
            a_data['Cluster_Name']
        ],
        f"{dist_b}": [
            f"{b_data['Friction_Score']:.1f}%", 
            f"{b_data['Child_Risk_Score']:.1f}%", 
            f"{int(b_data['Total_Updates']):,}",
            b_data['Cluster_Name']
        ]
    }
    st.table(pd.DataFrame(comp_data))

st.markdown("---")
col_export, _ = st.columns([1, 2])
with col_export:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=" Download Full Report (CSV)",
        data=csv,
        file_name="Aadhaar_Friction_Report.csv",
        mime="text/csv",
        type="primary"

    )
