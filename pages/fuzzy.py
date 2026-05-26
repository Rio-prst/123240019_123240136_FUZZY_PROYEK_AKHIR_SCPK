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

data = df[[
    "realSum",
    "dist",
    "cleanliness_rating",
    "guest_satisfaction_overall",
    "person_capacity"
]].copy()

data.columns = [
    "Price",
    "Distance",
    "Cleanliness",
    "Satisfaction",
    "Capacity"
]

st.title("Fuzzy Mamdani Calculation")
st.markdown("---")

#User Input
st.subheader("User Preference Input")

input_price = st.slider(
    "Preferred Price",
    int(data["Price"].min()),
    int(data["Price"].max()),
    int(data["Price"].mean())
)

input_distance = st.slider(
    "Preferred Distance",
    float(data["Distance"].min()),
    float(data["Distance"].max()),
    float(data["Distance"].mean())
)

input_cleanliness = st.slider(
    "Minimum Cleanliness",
    0, 10, 7
)

input_satisfaction = st.slider(
    "Minimum Satisfaction",
    0, 100, 80
)

input_capacity = st.slider(
    "Preferred Capacity",
    1, 10, 2
)

#Universe
x_price = np.arange(data["Price"].min(), data["Price"].max(),    1)
x_distance = np.arange(data["Distance"].min(), data["Distance"].max(), 0.1)
x_clean = np.arange(0,   11,  1)
x_satisfaction = np.arange(0,  101,  1)
x_capacity = np.arange(0,   11,  1)
x_score = np.arange(0,  101,  1)

#MEMBERSHIP FUNCTION

# Price
price_low  = fuzz.trimf(x_price, [x_price.min(), x_price.min(), input_price])
price_med  = fuzz.trimf(x_price, [x_price.min(), input_price,   x_price.max()])
price_high = fuzz.trimf(x_price, [input_price, x_price.max(), x_price.max()])

# Distance
dist_near = fuzz.trimf(x_distance, [x_distance.min(), x_distance.min(), input_distance])
dist_med  = fuzz.trimf(x_distance, [x_distance.min(), input_distance, x_distance.max()])
dist_far  = fuzz.trimf(x_distance, [input_distance, x_distance.max(), x_distance.max()])

# Cleanliness
mf_clean_low  = fuzz.trimf(x_clean, [0, 0, input_cleanliness])
mf_clean_med  = fuzz.trimf(x_clean, [0, input_cleanliness, 10])
mf_clean_high = fuzz.trimf(x_clean, [input_cleanliness, 10, 10])

# Satisfaction
mf_sat_low  = fuzz.trimf(x_satisfaction, [0, 0, input_satisfaction])
mf_sat_med  = fuzz.trimf(x_satisfaction, [0, input_satisfaction, 100])
mf_sat_high = fuzz.trimf(x_satisfaction, [input_satisfaction, 100, 100])

# Capacity
mf_cap_low  = fuzz.trimf(x_capacity, [0, 0, input_capacity])
mf_cap_med  = fuzz.trimf(x_capacity, [0, input_capacity, 10])
mf_cap_high = fuzz.trimf(x_capacity, [input_capacity, 10, 10])

# Output
out_low  = fuzz.trimf(x_score, [0,  0, 50])
out_med  = fuzz.trimf(x_score, [25, 50, 75])
out_high = fuzz.trimf(x_score, [50, 100, 100])

#Rule Base
rule_table = pd.DataFrame([
    # HIGH
    {"Rule": "R01", "Kondisi": "Price=Low AND Distance=Near", "Output": "HIGH"},
    {"Rule": "R02", "Kondisi": "Price=Low AND Distance=Near AND Cleanliness=High", "Output": "HIGH"},
    {"Rule": "R03", "Kondisi": "Cleanliness=High AND Satisfaction=High", "Output": "HIGH"},
    {"Rule": "R04", "Kondisi": "Capacity=High AND Satisfaction=High", "Output": "HIGH"},
    {"Rule": "R05", "Kondisi": "Price=Low AND Satisfaction=High", "Output": "HIGH"},
    {"Rule": "R06", "Kondisi": "Price=Low AND Cleanliness=High AND Satisfaction=High", "Output": "HIGH"},
    {"Rule": "R07", "Kondisi": "Distance=Near AND Cleanliness=High", "Output": "HIGH"},
    {"Rule": "R08", "Kondisi": "Distance=Near AND Satisfaction=High", "Output": "HIGH"},

    # MEDIUM
    {"Rule": "R09", "Kondisi": "Price=Med AND Distance=Med", "Output": "MEDIUM"},
    {"Rule": "R10", "Kondisi": "Cleanliness=Med AND Satisfaction=Med", "Output": "MEDIUM"},
    {"Rule": "R11", "Kondisi": "Capacity=Med AND Satisfaction=Med", "Output": "MEDIUM"},
    {"Rule": "R12", "Kondisi": "Price=Low AND Capacity=Low", "Output": "MEDIUM"},
    {"Rule": "R13", "Kondisi": "Price=Med AND Cleanliness=Med", "Output": "MEDIUM"},
    {"Rule": "R14", "Kondisi": "Price=Med AND Satisfaction=Med", "Output": "MEDIUM"},
    {"Rule": "R15", "Kondisi": "Distance=Med AND Cleanliness=Med", "Output": "MEDIUM"},
    {"Rule": "R16", "Kondisi": "Distance=Near AND Cleanliness=Med", "Output": "MEDIUM"},
    {"Rule": "R17", "Kondisi": "Price=Low AND Distance=Far", "Output": "MEDIUM"},
    {"Rule": "R18", "Kondisi": "Price=High AND Distance=Near AND Cleanliness=High", "Output": "MEDIUM"},

    # LOW
    {"Rule": "R19", "Kondisi": "Price=High AND Distance=Far", "Output": "LOW"},
    {"Rule": "R20", "Kondisi": "Cleanliness=Low AND Satisfaction=Low", "Output": "LOW"},
    {"Rule": "R21", "Kondisi": "Price=High AND Satisfaction=Low", "Output": "LOW"},
    {"Rule": "R22", "Kondisi": "Price=High AND Cleanliness=Low", "Output": "LOW"},
    {"Rule": "R23", "Kondisi": "Distance=Far AND Satisfaction=Low", "Output": "LOW"},
    {"Rule": "R24", "Kondisi": "Distance=Far AND Cleanliness=Low", "Output": "LOW"},
    {"Rule": "R25", "Kondisi": "Satisfaction=Low AND Cleanliness=Low", "Output": "LOW"},
    {"Rule": "R26", "Kondisi": "Price=High AND Distance=Far AND Satisfaction=Low", "Output": "LOW"}  
])

with st.expander("Lihat Rule Base (26 Rules)"):
    st.dataframe(rule_table, use_container_width=True)

#Kalkulasi
if st.button("Run Calculation"):

    scores = []

    for i in range(len(data)):
        p = data.iloc[i]["Price"]
        d = data.iloc[i]["Distance"]
        c = data.iloc[i]["Cleanliness"]
        s = data.iloc[i]["Satisfaction"]
        cap = data.iloc[i]["Capacity"]

        # ── FUZZIFIKASI ──────────────────
        p_low  = fuzz.interp_membership(x_price, price_low,  p)
        p_med  = fuzz.interp_membership(x_price, price_med,  p)
        p_high = fuzz.interp_membership(x_price, price_high, p)

        d_near = fuzz.interp_membership(x_distance, dist_near, d)
        d_med  = fuzz.interp_membership(x_distance, dist_med,  d)
        d_far  = fuzz.interp_membership(x_distance, dist_far,  d)

        c_low  = fuzz.interp_membership(x_clean, mf_clean_low,  c)
        c_med  = fuzz.interp_membership(x_clean, mf_clean_med,  c)
        c_high = fuzz.interp_membership(x_clean, mf_clean_high, c)

        s_low  = fuzz.interp_membership(x_satisfaction, mf_sat_low,  s)
        s_med  = fuzz.interp_membership(x_satisfaction, mf_sat_med,  s)
        s_high = fuzz.interp_membership(x_satisfaction, mf_sat_high, s)

        cap_low_val  = fuzz.interp_membership(x_capacity, mf_cap_low,  cap)
        cap_med_val  = fuzz.interp_membership(x_capacity, mf_cap_med,  cap)
        cap_high_val = fuzz.interp_membership(x_capacity, mf_cap_high, cap)

        # ── RULE BASE ────────────────────

        # --- HIGH ---
        r01 = np.fmin(p_low, d_near)
        r02 = np.fmin(np.fmin(p_low, d_near), c_high)
        r03 = np.fmin(c_high, s_high)
        r04 = np.fmin(cap_high_val, s_high)
        r05 = np.fmin(p_low, s_high)
        r06 = np.fmin(np.fmin(p_low, c_high), s_high)
        r07 = np.fmin(d_near, c_high)
        r08 = np.fmin(d_near, s_high)

        # --- MEDIUM ---
        r09 = np.fmin(p_med, d_med)
        r10 = np.fmin(c_med, s_med)
        r11 = np.fmin(cap_med_val, s_med)
        r12 = np.fmin(p_low, cap_low_val)
        r13 = np.fmin(p_med, c_med)
        r14 = np.fmin(p_med, s_med)
        r15 = np.fmin(d_med, c_med)
        r16 = np.fmin(d_near, c_med)
        r17 = np.fmin(p_low, d_far)
        r18 = np.fmin(np.fmin(p_high, d_near), c_high)

        # --- LOW ---
        r19 = np.fmin(p_high, d_far)
        r20 = np.fmin(c_low, s_low)
        r21 = np.fmin(p_high, s_low)
        r22 = np.fmin(p_high, c_low)
        r23 = np.fmin(d_far, s_low)
        r24 = np.fmin(d_far, c_low)
        r25 = np.fmin(s_low, c_low)
        r26 = np.fmin(np.fmin(p_high, d_far), s_low)

        # ── AGREGASI ─────────────────────
        agg_high = np.fmax(r01, np.fmax(r02, np.fmax(r03, np.fmax(
                    r04, np.fmax(r05, np.fmax(r06, np.fmax(r07, r08)))))))

        agg_med  = np.fmax(r09, np.fmax(r10, np.fmax(r11, np.fmax(
                    r12, np.fmax(r13, np.fmax(r14, np.fmax(r15, np.fmax(r16, np.fmax(r17, r18)))))))))

        agg_low  = np.fmax(r19, np.fmax(r20, np.fmax(r21, np.fmax(
                    r22, np.fmax(r23, np.fmax(r24, np.fmax(r25, r26)))))))

        # Clipping ke output MF
        high_result = np.fmin(float(agg_high), out_high)
        med_result  = np.fmin(float(agg_med),  out_med)
        low_result  = np.fmin(float(agg_low),  out_low)

        aggregated = np.fmax(low_result, np.fmax(med_result, high_result))

        # ── DEFUZZIFIKASI ─────────────────
        if np.sum(aggregated) == 0:
            strength_high = float(agg_high)
            strength_med  = float(agg_med)
            strength_low  = float(agg_low)
            total = strength_high + strength_med + strength_low

            if total == 0:
                final_score = 0.0
            else:
                final_score = (
                    strength_low  * 25 +
                    strength_med  * 50 +
                    strength_high * 75
                ) / total
        else:
            final_score = fuzz.defuzz(x_score, aggregated, 'centroid')

        scores.append(round(final_score, 4))

    data["Score"] = scores
    
    # MENYIMPAN INDEKS ASLI DATASET SEBELUM DI-SORTING
    data["ID"] = data.index

    ranking = data.sort_values(by="Score", ascending=False).reset_index(drop=True)
    ranking.index += 1  

    st.success("Calculation Completed") 

    # ── STATISTIK SKOR ───────────────────
    st.subheader("Score Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Max Score",  f"{data['Score'].max():.2f}")
    col2.metric("Min Score",  f"{data['Score'].min():.2f}")
    col3.metric("Mean Score", f"{data['Score'].mean():.2f}")
    col4.metric("Score = 0",  int((data['Score'] == 0).sum()))

    # ── TOP 10 ───────────────────────────
    st.subheader("Top 10 Recommendation")
    top10 = ranking.head(10)
    
    column_order = ["ID", "Price", "Distance", "Cleanliness", "Satisfaction", "Capacity", "Score"]
    st.dataframe(top10[column_order], use_container_width=True)

    # ── VISUALISASI BAR ──────────────────
    st.subheader("Top 10 Score Visualization")
    fig, ax = plt.subplots(figsize=(10, 5))
    
    y_labels = [f"Rank {r} (Baris Ke-{top10['ID'].iloc[r-1]})" for r in range(1, len(top10)+1)]
    
    bars = ax.barh(
        y_labels,
        top10["Score"],
        color="steelblue"
    )
    ax.bar_label(bars, fmt="%.2f", padding=3)
    ax.set_xlabel("Fuzzy Score")
    ax.set_title("Top 10 Listings by Fuzzy Mamdani Score")
    ax.invert_yaxis()
    st.pyplot(fig)

    # ── DISTRIBUSI SKOR ──────────────────
    st.subheader("Score Distribution")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.hist(data["Score"], bins=30, color="steelblue", edgecolor="white")
    ax2.set_xlabel("Score")
    ax2.set_ylabel("Jumlah Listing")
    ax2.set_title("Distribusi Skor Seluruh Listing")
    st.pyplot(fig2)

#VISUALISASI MEMBERSHIP FUNCTION
st.markdown("---")
st.subheader("Membership Function Visualization")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Price", "Distance", "Cleanliness", "Satisfaction", "Capacity"]
)

with tab1:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x_price, price_low,  label="Low",    color="blue")
    ax.plot(x_price, price_med,  label="Medium", color="orange")
    ax.plot(x_price, price_high, label="High",   color="red")
    ax.axvline(input_price, color="gray", linestyle="--", label=f"Input = {input_price}")
    ax.set_title("Price MF")
    ax.legend()
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x_distance, dist_near, label="Near",   color="blue")
    ax.plot(x_distance, dist_med,  label="Medium", color="orange")
    ax.plot(x_distance, dist_far,  label="Far",    color="red")
    ax.axvline(input_distance, color="gray", linestyle="--", label=f"Input = {input_distance:.2f}")
    ax.set_title("Distance MF")
    ax.legend()
    st.pyplot(fig)

with tab3:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x_clean, mf_clean_low,  label="Low",    color="blue")
    ax.plot(x_clean, mf_clean_med,  label="Medium", color="orange")
    ax.plot(x_clean, mf_clean_high, label="High",   color="red")
    ax.axvline(input_cleanliness, color="gray", linestyle="--", label=f"Input = {input_cleanliness}")
    ax.set_title("Cleanliness MF")
    ax.legend()
    st.pyplot(fig)

with tab4:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x_satisfaction, mf_sat_low,  label="Low",    color="blue")
    ax.plot(x_satisfaction, mf_sat_med,  label="Medium", color="orange")
    ax.plot(x_satisfaction, mf_sat_high, label="High",   color="red")
    ax.axvline(input_satisfaction, color="gray", linestyle="--", label=f"Input = {input_satisfaction}")
    ax.set_title("Satisfaction MF")
    ax.legend()
    st.pyplot(fig)

with tab5:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x_capacity, mf_cap_low,  label="Low",    color="blue")
    ax.plot(x_capacity, mf_cap_med,  label="Medium", color="orange")
    ax.plot(x_capacity, mf_cap_high, label="High",   color="red")
    ax.axvline(input_capacity, color="gray", linestyle="--", label=f"Input = {input_capacity}")
    ax.set_title("Capacity MF")
    ax.legend()
    st.pyplot(fig)