import streamlit as st
import numpy as np
import pandas as pd
import datetime

# --- KONFIGURASI HALAMAN & TEMA ---
st.set_page_config(
    page_title="AgroResonance AI - Advanced Formulator", 
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
    </style>
""", unsafe_allow_html=True)

# --- 1. CORE ENGINE AGRORESONANCE AI ---
class AgroResonanceEngine:
    def __init__(self):
        self.phi = (1 + np.sqrt(5)) / 2
        self.attenuation_factor = self.phi ** -2  # ~0.381966
        
        # Inisialisasi Riwayat Metrik di Session State Streamlit
        if 'history_distance' not in st.session_state:
            st.session_state.history_distance = []
        if 'total_simulasi' not in st.session_state:
            st.session_state.total_simulasi = 0

    def evaluate_thermal_stability(self, category, phase_angle_a, phase_angle_b):
        phase_difference = np.abs(phase_angle_a - phase_angle_b)
        stability_score = max(0.0, 100.0 - (phase_difference * 150.0))
        is_stable_lock = True if phase_difference < 0.05 else False
        
        # Catat riwayat untuk metrik dan grafik tren real-time
        st.session_state.total_simulasi += 1
        st.session_state.history_distance.append({
            "waktu": datetime.datetime.now().strftime("%H:%M:%S"),
            "deviasi": round(phase_difference, 4),
            "skor": round(stability_score, 2)
        })
        
        # Membuat DataFrame ringkasan hasil untuk diunduh
        result_df = pd.DataFrame([{
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Kategori_Produk": category,
            "Fasa_A": phase_angle_a,
            "Fasa_B": phase_angle_b,
            "Deviasi_Fasa": round(phase_difference, 4),
            "Skor_Kestabilan_Persen": round(stability_score, 2),
            "Status_Thermal_Lock": "AKTIF (Stabil)" if is_stable_lock else "TIDAK STABIL"
        }])

        return {
            "stability_score": round(stability_score, 2),
            "thermal_stable_lock": is_stable_lock,
            "phase_deviation": round(phase_difference, 4),
            "df_summary": result_df
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
st.sidebar.markdown("*Advanced Agro-Formulation Suite*")
menu = st.sidebar.radio("Pilih Modul Analisis", ["Thermal-Stable Lock Analysis", "Controlled-Release Optimizer"])

st.sidebar.markdown("---")
# Fitur 1: Kotak Metrik / Info Status di Sidebar/Dashboard
st.sidebar.info("💡 **Info R&D:** Dilengkapi fitur kalkulator takaran riil dan unduh laporan lab otomatis untuk dokumentasi lapangan.")
st.sidebar.metric(label="Total Simulasi Tersimpan", value=f"{st.session_state.total_simulasi} Record")

if menu == "Thermal-Stable Lock Analysis":
    st.title("🔬 Thermal-Stable Lock Analysis")
    st.markdown("Evaluasi tingkat ketahanan ikatan molekul pestisida dan kompleks nutrisi terhadap degradasi suhu dan panas matahari, lengkap dengan panduan takaran riil.")
    st.markdown("---")
    
    # Pemilihan Kategori Luas (Pestisida & Nutrisi)
    formulation_type = st.selectbox(
        "Pilih Kategori Produk / Bahan Aktif",
        [
            "Insektisida (Kontak / Sistemik)",
            "Fungisida (Protektan / Kuratif)",
            "Akarisida (Pengendali Tungau)",
            "Herbisida Pra-Tumbuh (Pencegah Biji Gulma)",
            "Herbisida Purna-Tumbuh Kontak (Pembakar Daun)",
            "Herbisida Purna-Tumbuh Sistemik (Mati Sampai Akar)",
            "Herbisida Selektif (Aman Tanaman Utama)",
            "Herbisida Non-Selektif (Spektrum Luas / Total)",
            "Pupuk Cair Organik (POC)",
            "Pupuk Tepung / Bubuk Larut Air",
            "Trace Elements / Unsur Hara Mikro (TE)"
        ]
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        phase_a = st.number_input("Nilai Fasa Bahan Utama (A)", value=1.618, format="%.3f")
    with col2:
        phase_b = st.number_input("Nilai Fasa Aditif / Pelarut (B)", value=1.620, format="%.3f")
    with col3:
        vol_total = st.number_input("Target Volume Total (ml)", value=1000.0, step=100.0)
        
    st.markdown("")
    if st.button("Jalankan Simulasi Kestabilan & Hitung Takaran"):
        result = engine.evaluate_thermal_stability(formulation_type, phase_a, phase_b)
        
        st.markdown("---")
        st.subheader(f"📊 Hasil Analisis Lab: {formulation_type}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Skor Kestabilan Formula", value=f"{result['stability_score']}%")
        m2.metric(label="Deviasi Fasa", value=result['phase_deviation'])
        m3.metric(label="Status Thermal-Stable Lock", value="AKTIF (Stabil)" if result['thermal_stable_lock'] else "TIDAK STABIL")
        
        # --- PERHITUNGAN TAKARAN RIIL OTOMATIS ---
        if "Insektisida" in formulation_type or "Fungisida" in formulation_type:
            vol_ba = vol_total * (32 / 1000)  # Mengikuti kelas pekat 32 g/l
        else:
            vol_ba = vol_total * (18 / 1000)  # Standar 18 g/l
            
        vol_aditif = vol_total * 0.035  # Porsi aditif / emulsifier 3.5%
        vol_pelarut = vol_total - (vol_ba + vol_aditif)  # Sisa pelarut
        
        st.markdown("---")
        st.subheader(f"📋 Panduan Takaran Riil (Untuk {vol_total:,.1f} ml)")
        
        deviasi = result['phase_deviation']
        
        if result['thermal_stable_lock']:
            st.success(f"STATUS: AKTIF (Thermal-Stable Lock Stabil | Deviasi: {deviasi:.3f})")
            
            t1, t2, t3 = st.columns(3)
            t1.metric("Bahan Utama (BA)", f"{vol_ba:.1f} ml")
            t2.metric("Aditif / Emulsifier", f"{vol_aditif:.1f} ml")
            t3.metric("Pelarut Organik", f"{vol_pelarut:.1f} ml")
            
            st.info("💡 **Instruksi Pencampuran:** Campurkan aditif ke pelarut, masukkan bahan utama perlahan, aduk rata hingga volume tercapai.")
        else:
            st.error(f"STATUS: TIDAK STABIL (Deviasi {deviasi:.3f} melewati batas toleransi 0.05). Sesuaikan kembali Fasa B!")
            
        # Tombol Unduh Laporan Kestabilan (CSV)
        st.markdown("---")
        csv_data = result['df_summary'].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Laporan Ringkasan Lab (CSV)",
            data=csv_data,
            file_name=f"Thermal_Stability_{formulation_type.split()[0]}.csv",
            mime="text/csv",
        )

    # --- FITUR 3: GRAFIK GARIS INTERAKTIF (RIWAYAT PENGUJIAN) ---
    st.markdown("---")
    st.subheader("📈 Grafik Tren Riwayat Deviasi & Pengujian Real-Time")
    if len(st.session_state.history_distance) > 0:
        df_history = pd.DataFrame(st.session_state.history_distance)
        st.line_chart(df_history.set_index("waktu")[["deviasi"]])
    else:
        st.caption("Grafik tren riwayat akan muncul secara otomatis setelah Anda menjalankan simulasi.")

elif menu == "Controlled-Release Optimizer":
    st.title("⏳ Controlled-Release Optimizer")
    st.markdown("Simulasi kurva peluruhan dan pelepasan zat aktif pestisida (cair/granul) serta pelepasan lambat pupuk/Trace Elements di tanah.")
    st.markdown("---")
    
    target_category = st.selectbox(
        "Pilih Target Profil Pelepasan",
        [
            "Herbisida Pra-Tumbuh (Granul / Suspensi Tanah)",
            "Herbisida Purna-Tumbuh Sistemik (Penetrasi Daun-Akar)",
            "Insektisida / Fungisida Granul (Slow-Release Tanah)",
            "Pupuk / Trace Elements (TE) Lepas-Terkendali (Controlled-Release Fertilizer)"
        ]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        target_days = st.slider("Target Durasi Aktif / Pelepasan (Hari)", min_value=7, max_value=90, value=30)
    with col2:
        rigidity_val = st.number_input("Indeks Rigiditas Matriks / Kepadatan Pembawa ($\eta$)", value=4.236, format="%.3f")
        
    st.markdown("")
    if st.button("Hasilkan Kurva Pelepasan"):
        df_release = engine.generate_controlled_release_profile(target_days, rigidity_val)
        
        st.markdown("---")
        st.subheader(f"📈 Grafik Profil Pelepasan ({target_category}) - {target_days} Hari")
        st.line_chart(df_release.set_index("Hari Ke"))
        
        with st.expander("Lihat Tabel Data Detail Akumulasi Pelepasan"):
            st.dataframe(df_release, use_container_width=True)
            
        # Tombol Unduh Kurva Pelepasan (CSV)
        st.markdown("---")
        csv_release = df_release.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Data Kurva Pelepasan (CSV)",
            data=csv_release,
            file_name=f"Release_Profile_{target_days}Hari.csv",
            mime="text/csv",
        )
