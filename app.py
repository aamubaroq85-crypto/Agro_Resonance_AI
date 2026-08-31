import streamlit as st
import numpy as np
import pandas as pd
import datetime
import math

# --- KELAS LOGIKA CORE NEXUS STREAM ---
class NexusStreamCoreLightweight:
    def __init__(self, vector_dim=64, capacity=5000):
        self.vector_dim = vector_dim
        self.capacity = capacity
        if 'lattice_grid' not in st.session_state:
            st.session_state.lattice_grid = [[0.0 * vector_dim] for _ in range(capacity)]
            st.session_state.cursor = 0
            st.session_state.total_stored = 0
            # Menyimpan riwayat metrik untuk grafik
            st.session_state.history_distance = []

    def fast_ingest(self, data_vector):
        if len(data_vector) != self.vector_dim:
            return False
        st.session_state.lattice_grid[st.session_state.cursor] = data_vector
        st.session_state.cursor = (st.session_state.cursor + 1) % self.capacity
        if st.session_state.total_stored < self.capacity:
            st.session_state.total_stored += 1
        return True

    def instant_query(self, query_vec):
        limit = st.session_state.total_stored
        if limit == 0:
            return 0.0, 0.0
        
        min_dist = float('inf')
        for i in range(limit):
            row = st.session_state.lattice_grid[i]
            dist_sq = sum((row[j] - query_vec[j]) ** 2 for j in range(len(query_vec)))
            dist = math.sqrt(dist_sq)
            if dist < min_dist:
                min_dist = dist
        
        # Simpan ke riwayat untuk visualisasi grafik
        st.session_state.history_distance.append({
            "waktu": datetime.datetime.now().strftime("%H:%M:%S"),
            "jarak_min": min_dist
        })
        return min_dist, limit

# Inisialisasi Engine
engine = NexusStreamCoreLightweight(vector_dim=64, capacity=5000)

# --- KONFIGURASI HALAMAN & TEMA ---
st.set_page_config(
    page_title="AgroResonance AI - Advanced",
    page_icon="🌾",
    layout="wide"
)

# --- KUSTOMISASI CSS ---
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 6px; background-color: #2e7d32; color: white; }
    .stButton>button:hover { background-color: #1b5e20; color: white; }
</style>
""", unsafe_allow_html=True)

# --- ANTARMUKA UTAMA APLIKASI ---
st.title("🌾 AgroResonance AI & Thermal-Stable Lock Analysis")
st.markdown("Evaluasi tingkat ketahanan ikatan molekul pestisida dan kompleks nutrisi terhadap degradasi suhu, lengkap dengan metrik analitik dan grafik interaktif.")

# --- METRIK UTAMA ATAS ---
m1, m2, m3 = st.columns(3)
m1.metric(label="Total Vektor Tersimpan", value=f"{st.session_state.get('total_stored', 0)} Record")
m2.metric(label="Dimensi Matriks Core", value="64 Dimensi")
m3.metric(label="Status Mesin", value="Online / Siap")

st.markdown("---")

# Layout Kontrol Utama
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚙️ Pengaturan Fasa Parameter")
    val_a = st.number_input("Nilai Fasa Bahan Utama (A)", value=1.618, format="%.4f")
    val_b = st.number_input("Nilai Fasa Aditif / Pelarut (B)", value=0.618, format="%.4f")
    
    if st.button("Simpan Data ke Core Engine"):
        mock_vector = [val_a, val_b] * 32
        success = engine.fast_ingest(mock_vector)
        if success:
            st.success(f"Berhasil memasukkan data vektor! Total record: {st.session_state.total_stored}")

with col2:
    st.subheader("🔍 Analisis Kemiripan Vektor")
    if st.button("Jalankan Instant Query & Rekam Metrik"):
        mock_query = [val_a, val_b] * 32
        min_dist, total = engine.instant_query(mock_query)
        if total > 0:
            st.info(f"Hasil Analisis Terakhir:\n- Jarak Minimum (Distance): **{min_dist:.4f}**")
        else:
            st.warning("Belum ada data di dalam memori core. Silakan simpan data terlebih dahulu.")

# --- VISUALISASI GRAFIK ANALITIK ---
st.markdown("---")
st.subheader("📈 Grafik Tren Jarak Analitik (Real-Time History)")

if len(st.session_state.get('history_distance', [])) > 0:
    df_history = pd.DataFrame(st.session_state.history_distance)
    # Menampilkan grafik garis interaktif
    st.line_chart(df_history.set_index('waktu')['jarak_min'])
else:
    st.info("Belum ada riwayat kueri. Jalankan 'Instant Query' untuk memunculkan grafik tren analitik.")

st.markdown("---")
st.caption("Nexus Stream Core Engine - Integrated with Streamlit Cloud")
