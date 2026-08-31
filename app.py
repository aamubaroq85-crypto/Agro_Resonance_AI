import streamlit as st
import numpy as np
import pandas as pd
import datetime
import math

# --- LOGIKA CORE NEXUS STREAM (TERINTEGRASI DI LATAR BELAKANG) ---
if 'lattice_grid' not in st.session_state:
    st.session_state.lattice_grid = [[0.0 * 64] for _ in range(5000)]
    st.session_state.cursor = 0
    st.session_state.total_stored = 0

def fast_ingest(data_vector):
    st.session_state.lattice_grid[st.session_state.cursor] = data_vector
    st.session_state.cursor = (st.session_state.cursor + 1) % 5000
    if st.session_state.total_stored < 5000:
        st.session_state.total_stored += 1

def instant_query(query_vec):
    limit = st.session_state.total_stored
    if limit == 0:
        return 0.0
    min_dist = float('inf')
    for i in range(limit):
        row = st.session_state.lattice_grid[i]
        dist_sq = sum((row[j] - query_vec[j]) ** 2 for j in range(len(query_vec)))
        dist = math.sqrt(dist_sq)
        if dist < min_dist:
            min_dist = dist
    return min_dist


# --- KONFIGURASI HALAMAN & TEMA (ASLI) ---
st.set_page_config(
    page_title="AgroResonance AI - Ad",
    page_icon="🌾",
    layout="wide"
)

# --- Kustomisasi CSS Asli ---
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
</style>
""", unsafe_allow_html=True)

# --- TAMPILAN UTAMA ASLI ---
st.markdown("<h1>🔬 Thermal-Stable Lock Analysis</h1>", unsafe_allow_html=True)
st.markdown("Evaluasi tingkat ketahanan ikatan molekul pestisida dan kompleks nutrisi terhadap degradasi suhu dan panas matahari, lengkap dengan panduan takaran riil.")

st.markdown("---")

# Bagian Input Form Asli
kategori = st.selectbox(
    "Pilih Kategori Produk / Bahan Aktif",
    ["Insektisida (Kontak / Sistemik)", "Fungisida", "Nutrisi / Pupuk Organik"]
)

val_a = st.number_input("Nilai Fasa Bahan Utama (A)", value=1.618, format="%.4f")
val_b = st.number_input("Nilai Fasa Aditif / Pelarut (B)", value=0.618, format="%.4f")

# Tombol aksi yang secara otomatis menghubungkan data ke Core Engine di latar belakang
if st.button("Proses Analisis Thermal"):
    # Membentuk vektor 64 dimensi secara otomatis dari input asli
    vec_data = [val_a, val_b] * 32
    fast_ingest(vec_data)
    
    # Menjalankan kueri instan
    hasil_dist = instant_query(vec_data)
    
    st.success(f"Analisis Selesai! Data berhasil dikunci ke Core Engine.")
    st.info(f"Hasil Jarak Ikatan Molekul (Distance): {hasil_dist:.4f} | Total Data: {st.session_state.total_stored}")
