import streamlit as st

st.title("Profile")
st.markdown("---")

st.subheader("Project Information")

st.write("""
**Sistem Pendukung Keputusan (SPK)** untuk menentukan rekomendasi 
penginapan Airbnb terbaik menggunakan metode **Fuzzy Mamdani**.

Sistem ini mempertimbangkan beberapa kriteria:
- Price (Harga)
- Distance (Jarak)
- Cleanliness (Kebersihan)
- Satisfaction (Kepuasan)
- Capacity (Kapasitas)
""")

st.subheader("Team Members")

col1, col2 = st.columns(2)

with col1:
    st.write("**Nama:** Marvel Valensiano")
    st.write("**NIM:**  123240019")

with col2:
    st.write("**Nama:** Rio Prasetio")
    st.write("**NIM:**  123240136")

st.subheader("Course Information")

st.write("""
Mata Kuliah: Sistem Pendukung Keputusan  
Metode: Fuzzy Mamdani  
Tools: Python, Streamlit, Scikit-Fuzzy  
Dataset: Airbnb Europe Dataset
""")

st.markdown("---")
st.write("© 2026 - Final Project SCPK")