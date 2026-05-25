# Sistem Pendukung Keputusan Pemilihan Airbnb Terbaik  
## Metode Fuzzy Mamdani Berbasis Streamlit

---

## Deskripsi Project

Project ini merupakan implementasi **Sistem Pendukung Keputusan (SPK)** untuk membantu pengguna dalam memilih listing Airbnb terbaik di Eropa.

Metode yang digunakan adalah **Fuzzy Mamdani**, yang mampu menangani ketidakpastian dalam pengambilan keputusan berdasarkan beberapa kriteria.

Aplikasi ini dibangun menggunakan **Python** dan **Streamlit** sebagai antarmuka interaktif.

---

## Tujuan

- Membantu pengguna menentukan Airbnb terbaik berdasarkan kriteria tertentu  
- Mengimplementasikan metode **Fuzzy Mamdani** dalam kasus nyata  
- Menampilkan hasil dalam bentuk **ranking rekomendasi**  

---

## Dataset

Dataset yang digunakan berasal dari Kaggle:

Airbnb Price Determinants in Europe

Berisi data listing Airbnb di beberapa kota Eropa dengan atribut seperti:

- Harga (`realSum`)
- Jarak ke pusat kota (`dist`)
- Kebersihan (`cleanliness_rating`)
- Kepuasan tamu (`guest_satisfaction_overall`)
- Kapasitas (`person_capacity`)

---

## Metode yang Digunakan

Metode: **Fuzzy Mamdani**

Tahapan:

1. **Fuzzifikasi**
   - Mengubah nilai numerik menjadi nilai linguistik
2. **Rule Base**
   - Aturan IF-THEN
3. **Inferensi**
   - Menggabungkan aturan
4. **Defuzzifikasi**
   - Menghasilkan nilai akhir (centroid)

---

## Kriteria Penilaian

| Kriteria | Tipe |
|--------|------|
| Harga | Cost |
| Jarak | Cost |
| Kebersihan | Benefit |
| Kepuasan Tamu | Benefit |
| Kapasitas | Benefit |

---

## Struktur Folder

```bash
project-airbnb-fuzzy/
│
├── app.py
├── dataset/
│   └── paris_weekdays.csv
│
├── pages/
│   ├── data.py
│   ├── fuzzy.py
│   └── profile.py
│
└── README.md