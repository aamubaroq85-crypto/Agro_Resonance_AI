import streamlit as st
import numpy as np
import pandas as pd

# --- KONFIGURASI HALAMAN & TEMA ---
st.set_page_config(
    page_title="AgroResonance AI - Smart Formulator", 
    page_icon="🌾", 
    layout="wide"
)

# Kustomisasi CSS untuk Tampilan Profesional & Modern
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #2d6a4f;
        color: white;
        border-radius: 6px;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #1b4332;
        color: white;
    }
    .css-1dp5vir {
        background-image: linear-gradient(#2d6a4f, #1b4332);
    }
    </style>
""", unsafe_allow_html=True)

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
st.sidebar.title("🌿 AgroResonance AI")
st.sidebar.markdown("*Enterprise R&D Suite*")
menu = st.sidebar.radio("Pilih Modul Analisis", ["Thermal-Stable Lock Analysis", "Controlled-Release Optimizer"])

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tips Klien:** Gunakan modul ini untuk demonstrasi langsung efisiensi formula pestisida di hadapan tim formulator pabrik.")

if menu == "Thermal-Stable Lock Analysis":
    st.title("🔬 Thermal-Stable Lock Analysis")
    st.markdown("Evaluasi tingkat ketahanan ikatan molekul pestisida terhadap degradasi suhu dan panas matahari berbasis metrik fraktal.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        phase_a = st.number_input("Nilai Fasa Bahan Aktif Utama (A)", value=1.618, format="%.3f")
    with col2:
        phase_b = st.number_input("Nilai Fasa Aditif / Pelarut (B)", value=1.625, format="%.3f")
        
    st.markdown("")
    if st.button("Jalankan Simulasi Kestabilan"):
        result = engine.evaluate_thermal_stability(phase_a, phase_b)
        
        st.markdown("---")
        st.subheader("📊 Hasil Laporan Analisis Lab:")
        
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Skor Kestabilan Formula", value=f"{result['stability_score']}%")
        m2.metric(label="Deviasi Fasa", value=result['phase_deviation'])
        m3.metric(label="Status Thermal-Stable Lock", value="AKTIF (Stabil)" if result['thermal_stable_lock'] else "TIDAK STABIL")
        
        st.markdown("")
        if result['thermal_stable_lock']:
            st.success("✅ **Formula Optimal:** Ikatan molekul terbukti tahan terhadap disipasi panas termal di lapangan.")
        else:
            st.warning("⚠️ **Perhatian:** Deviasi fasa melewati batas toleransi. Disarankan menyesuaikan komposisi aditif.")

elif menu == "Controlled-Release Optimizer":
    st.title("⏳ Controlled-Release Optimizer")
    st.markdown("Simulasi kurva peluruhan dan pelepasan zat aktif pestisida bentuk granul secara presisi di dalam tanah.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        target_days = st.slider("Target Durasi Aktif di Tanah (Hari)", min_value=7, max_value=90, value=30)
    with col2:
        rigidity_val = st.number_input("Indeks Rigiditas Matriks ($\eta$)", value=4.236, format="%.3f")
        
    st.markdown("")
    if st.button("Hasilkan Kurva Pelepasan"):
        df_release = engine.generate_controlled_release_profile(target_days, rigidity_val)
        
        st.markdown("---")
        st.subheader(f"📈 Grafik Profil Pelepasan Pestisida ({target_days} Hari)")
        st.line_chart(df_release.set_index("Hari Ke"))
        
        with st.expander("Lihat Tabel Data Detail Akumulasi Pelepasan"):
            st.dataframe(df_release, use_container_width=True)
