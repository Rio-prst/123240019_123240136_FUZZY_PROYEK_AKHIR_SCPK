import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("dataset/paris_weekdays.csv")
    return df

df = load_data()

criteria_df = df[[
    "realSum",
    "dist",
    "cleanliness_rating",
    "guest_satisfaction_overall",
    "person_capacity",
]]

# Rename biar lebih readable
criteria_df.columns = [
    "Price",
    "Distance",
    "Cleanliness",
    "Satisfaction",
    "Capacity"
]

st.title("Dataset")
st.markdown("---")

#Filter
st.subheader("Filter Data")

col1, col2, col3 = st.columns(3)

with col1:
    max_price = st.slider(
        "Maximum Price",
        int(criteria_df["Price"].min()),
        int(criteria_df["Price"].max()),
        int(criteria_df["Price"].max())
    )

with col2:
    min_satisfaction = st.slider(
        "Minimum Satisfaction",
        int(criteria_df["Satisfaction"].min()),
        int(criteria_df["Satisfaction"].max()),
        int(criteria_df["Satisfaction"].min())
    )

with col3:
    min_capacity = st.slider(
        "Minimum Capacity",
        int(criteria_df["Capacity"].min()),
        int(criteria_df["Capacity"].max()),
        int(criteria_df["Capacity"].min())
    )

#Apply Filter
filtered_df = criteria_df[
    (criteria_df["Price"] <= max_price) &
    (criteria_df["Satisfaction"] >= min_satisfaction) &
    (criteria_df["Capacity"] >= min_capacity)
]

#Summary
st.markdown("## Data Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Data", len(filtered_df))

with col2:
    st.metric("Average Price", round(filtered_df["Price"].mean(), 2))

with col3:
    st.metric("Average Satisfaction", round(filtered_df["Satisfaction"].mean(), 2))

st.markdown("## Data Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.markdown("## Top 10 (Highest Satisfaction)")

top_data = filtered_df.sort_values(
    by="Satisfaction",
    ascending=False
).head(10)

st.dataframe(top_data, use_container_width=True)