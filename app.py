import streamlit as st
import numpy as np
import pandas as pd

# --- 1. CORE ENGINE AGRORESONANCE AI ---
class AgroResonanceEngine:
    def __init__(self):
        self.phi = (1 + np.sqrt(5)) / 2
        self.attenuation_factor = self.phi ** -2  # ~0.381966

    def evaluate_thermal_stability(self, phase_angle_a, phase_angle_b):
        phase_difference = np.abs(phase_angle_a - phase_angle_b)
        stability_score = max(0.0, 100.0 - (phase_difference * 150.0))
        is_stable_lock = True if phase_difference < 0.05 else False
        
        return {
            "stability_score": round(stability_score, 2),
            "thermal_stable_lock": is_stable_lock,
            "phase_deviation": round(phase_difference, 4)
        }

    def generate_controlled_release_profile(self, target_days, initial_rigidity):
        days = np.arange(1, target_days + 1)
        release_rate = initial_rigidity * (days ** (-self.attenuation_factor))
        cumulative_release = np.cumsum(release_rate)
        cumulative_release = (cumulative_release / cumulative_release[-1]) * 100
        
        return pd.DataFrame({
            "Hari Ke": days,
            "Akumulasi Pelepasan (%)": np.round(cumulative_release, 2)
        })

engine = AgroResonanceEngine()

# --- 2. TAMPILAN ANTARMUKA (FRONTEND DASHBOARD) ---
st.set_page_config(page_title="AgroResonance AI - Formulator", layout="wide")

st.title("🌾 AgroResonance AI: Smart Pesticide Formulation Suite")
st.markdown("Platform simulasi R&D berbasis metrik fraktal untuk optimasi kestabilan termal dan profil pelepasan pestisida.")

menu = st.sidebar.selectbox("Pilih Modul Analisis", ["Thermal-Stable Lock Analysis", "Controlled-Release Optimizer"])

if menu == "Thermal-Stable Lock Analysis":
    st.header("🔬 Modul Analisis Kestabilan Termal (Thermal-Stable Lock)")
    st.write("Evaluasi tingkat ketahanan ikatan molekul pestisida terhadap degradasi suhu dan panas matahari.")
    
    col1, col2 = st.columns(2)
    with col1:
        phase_a = st.number_input("Nilai Fasa Bahan Aktif Utama (A)", value=1.618, format="%.3f")
    with col2:
        phase_b = st.number_input("Nilai Fasa Aditif / Pelarut (B)", value=1.625, format="%.3f")
        
    if st.button("Jalankan Simulasi Kestabilan"):
        result = engine.evaluate_thermal_stability(phase_a, phase_b)
        
        st.markdown("---")
        st.subheader("Hasil Laporan Analisis:")
        
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Skor Kestabilan Formula", value=f"{result['stability_score']}%")
        m2.metric(label="Deviasi Fasa", value=result['phase_deviation'])
        m3.metric(label="Status Thermal-Stable Lock", value="AKTIF (Stabil)" if result['thermal_stable_lock'] else "TIDAK STABIL")
        
        if result['thermal_stable_lock']:
            st.success("✅ Formula optimal! Ikatan molekul tahan terhadap disipasi panas termal.")
        else:
            st.warning("⚠️ Peringatan: Deviasi fasa terlalu tinggi. Disarankan menyesuaikan komposisi pelarut.")

elif menu == "Controlled-Release Optimizer":
    st.header("⏳ Modul Pengoptimal Pelepasan Terkendali (Controlled-Release Optimizer)")
    st.write("Merancang kurva peluruhan dan pelepasan zat aktif pestisida granul di dalam tanah secara presisi.")
    
    col1, col2 = st.columns(2)
    with col1:
        target_days = st.slider("Target Durasi Aktif di Tanah (Hari)", min_value=7, max_value=90, value=30)
    with col2:
        rigidity_val = st.number_input("Indeks Rigiditas Matriks (η)", value=4.236, format="%.3f")
        
    if st.button("Hasilkan Kurva Pelepasan"):
        df_release = engine.generate_controlled_release_profile(target_days, rigidity_val)
        
        st.markdown("---")
        st.subheader(f"Grafik Profil Pelepasan Pestisida ({target_days} Hari)")
        st.line_chart(df_release.set_index("Hari Ke"))
        
        st.subheader("Tabel Data Akumulasi Pelepasan")
        st.dataframe(df_release)
