import streamlit as st

st.set_page_config(
    page_title="SPK Airbnb Fuzzy",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}

h1, h2, h3 {
    color: #ffffff;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}

.stMetric {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
# Airbnb Decision System  
### Fuzzy Mamdani Based Recommendation System
""")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
### About This Application

This system helps users choose the best Airbnb listing in Europe  
using the Fuzzy Mamdani method.

The decision is based on several criteria:

- Price  
- Distance to city center  
- Cleanliness  
- Guest satisfaction  
- Capacity  

Use the sidebar menu to explore the dataset and run the decision system.
""")

with col2:
    st.info("Start from the Dataset menu, then continue to SPK Fuzzy")

st.markdown("## System Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Number of Criteria", value="5")

with col2:
    st.metric(label="Method", value="Fuzzy Mamdani")

with col3:
    st.metric(label="Platform", value="Streamlit")

st.markdown("## Main Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
### Dataset
View Airbnb data directly
""")

with col2:
    st.markdown("""
### Decision System
Run fuzzy calculation
""")

with col3:
    st.markdown("""
### Ranking
Display best recommendations
""")

st.markdown("---")

if st.button("Start"):
    st.success("Please use the sidebar menu")
