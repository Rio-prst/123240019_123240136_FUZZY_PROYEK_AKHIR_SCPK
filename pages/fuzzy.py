import streamlit as st
import pandas as pd
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

#Load Data
@st.cache_data
def load_data():
    return pd.read_csv("dataset/paris_weekdays.csv")

df = load_data()

#Kriteria
data = df[[
    "realSum",
    "dist",
    "cleanliness_rating",
    "guest_satisfaction_overall",
    "person_capacity"
]].copy()

data.columns = ["Price", "Distance", "Cleanliness", "Satisfaction", "Capacity"]

#Normalisasi
data_norm = (data - data.min()) / (data.max() - data.min())

st.title("Fuzzy Mamdani Calculation")
st.markdown("---")

#Input Bobot
st.subheader("Input Weight")

w_price = st.slider("Weight Price", 1, 10, 5)
w_distance = st.slider("Weight Distance", 1, 10, 5)
w_cleanliness = st.slider("Weight Cleanliness", 1, 10, 5)
w_satisfaction = st.slider("Weight Satisfaction", 1, 10, 5)
w_capacity = st.slider("Weight Capacity", 1, 10, 5)

# Normalisasi Bobot
total_w = w_price + w_distance + w_cleanliness + w_satisfaction + w_capacity
w_price /= total_w
w_distance /= total_w
w_cleanliness /= total_w
w_satisfaction /= total_w
w_capacity /= total_w

#Universe
x = np.linspace(0, 1, 100)

#Membership Function
price_low = fuzz.trimf(x, [0, 0, 0.5])
price_high = fuzz.trimf(x, [0.5, 1, 1])

dist_near = fuzz.trimf(x, [0, 0, 0.5])
dist_far = fuzz.trimf(x, [0.5, 1, 1])

sat_low = fuzz.trimf(x, [0, 0, 0.5])
sat_high = fuzz.trimf(x, [0.5, 1, 1])

clean_high = fuzz.trimf(x, [0.5, 1, 1])
cap_high = fuzz.trimf(x, [0.5, 1, 1])

#Output
out_low = fuzz.trimf(x, [0, 0, 0.5])
out_med = fuzz.trimf(x, [0.25, 0.5, 0.75])
out_high = fuzz.trimf(x, [0.5, 1, 1])

if st.button("Run Calculation"):

    scores = []

    for i in range(len(data_norm)):

        p = data_norm.iloc[i]["Price"]
        d = data_norm.iloc[i]["Distance"]
        c = data_norm.iloc[i]["Cleanliness"]
        s = data_norm.iloc[i]["Satisfaction"]
        cap = data_norm.iloc[i]["Capacity"]

        #Fuzzifikasi
        p_low = fuzz.interp_membership(x, price_low, p)
        p_high = fuzz.interp_membership(x, price_high, p)

        d_near = fuzz.interp_membership(x, dist_near, d)
        d_far = fuzz.interp_membership(x, dist_far, d)

        s_low = fuzz.interp_membership(x, sat_low, s)
        s_high = fuzz.interp_membership(x, sat_high, s)

        c_high = fuzz.interp_membership(x, clean_high, c)
        cap_high_val = fuzz.interp_membership(x, cap_high, cap)

        #Rule Base
        rule1 = np.fmin(p_low, d_near)
        rule2 = np.fmin(p_high, d_far)
        rule3 = np.fmin(s_high, c_high)
        rule4 = np.fmin(p_low, s_high)
        rule5 = np.fmin(d_near, s_high)
        rule6 = np.fmin(cap_high_val, c_high)
        rule7 = np.fmin(p_low, cap_high_val)
        rule8 = np.fmin(d_far, s_low)
        rule9 = np.fmin(p_high, s_low)
        rule10 = np.fmin(d_near, c_high)

        #Agregasi
        agg_low = np.fmax(rule2, np.fmax(rule8, rule9))
        agg_med = np.fmax(rule6, rule7)
        agg_high = np.fmax(rule1, np.fmax(rule3, np.fmax(rule4, np.fmax(rule5, rule10))))

        agg_low = np.fmin(agg_low, out_low)
        agg_med = np.fmin(agg_med, out_med)
        agg_high = np.fmin(agg_high, out_high)

        aggregated = np.fmax(agg_low, np.fmax(agg_med, agg_high))

        #Defuzzifikasi
        if np.sum(aggregated) == 0:
            score = 0
        else:
            score = fuzz.defuzz(x, aggregated, 'centroid')

        #Final Score + Bobot
        final_score = (
            score * 0.5 +
            (1 - p) * w_price +
            (1 - d) * w_distance +
            c * w_cleanliness +
            s * w_satisfaction +
            cap * w_capacity
        )

        scores.append(final_score)

    #Ranking
    data["Score"] = scores
    ranking = data.sort_values(by="Score", ascending=False)

    st.success("Calculation Completed")

    st.subheader("Ranking Result")
    st.dataframe(ranking, use_container_width=True)

    st.subheader("Top 10 Recommendation")
    top10 = ranking.head(10)
    st.dataframe(top10, use_container_width=True)

    #Visualisasi Barchart
    st.subheader("Visualization")

    fig, ax = plt.subplots()
    ax.barh(range(len(top10)), top10["Score"])
    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels(top10.index)
    ax.invert_yaxis()

    st.pyplot(fig)

#Visualisasi Membership
st.subheader("Membership Function Example")

fig, ax = plt.subplots()
ax.plot(x, price_low, label="Price Low")
ax.plot(x, price_high, label="Price High")
ax.legend()

st.pyplot(fig)