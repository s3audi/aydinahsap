import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="🌧️ Hatim Yağmuru",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Deployment için cache temizleme
@st.cache_data(ttl=3600)  # 1 saatte bir cache temizle
def load_app_config():
    return {
        "app_version": "1.0.0",
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "environment": os.getenv("STREAMLIT_ENV", "production")
    }

# CSS Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #059669, #0d9488);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .progress-card {
        background: #ecfdf5;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #10b981;
        margin-bottom: 1rem;
    }
    .person-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        margin-bottom: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .btn-evet {
        background-color: #10b981;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        cursor: default;
    }
    .btn-hayir {
        background-color: #fee2e2;
        color: #dc2626;
        border: 1px solid #fca5a5;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        cursor: pointer;
    }
    .tab-selected {
        background-color: #10b981;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Veri yapıları
@st.cache_data
def get_initial_data():
    # Yasin dönemleri
    yasin_donemleri = [
        {"id": 1, "tarih": "16 Mayıs 2025", "haftalik_sayi": 36, "toplam_sayi": 226},
        {"id": 2, "tarih": "9 Mayıs 2025", "haftalik_sayi": 35, "toplam_sayi": 190},
        {"id": 3, "tarih": "2 Mayıs 2025", "haftalik_sayi": 34, "toplam_sayi": 155}
    ]
    
    # Hatim dönemleri
    hatim_donemleri = [
        {"id": 1, "ay": "Mayıs 2025"},
        {"id": 2, "ay": "Nisan 2025"},
        {"id": 3, "ay": "Mart 2025"}
    ]
    
    # Hatim verileri (30 cüz)
    hatim_verileri = [
        {"cuz_no": i+1, "okuyan": ["Tamer", "Emre", "Gülnhal"][i % 3], "okunma": i % 2 == 0}
        for i in range(30)
    ]
    
    # Yasin verileri (40 kişi)
    yasin_isimleri = [
        "Yunus Emre", "Tamer", "Sabahat", "Emre", "Hacer", "Fatih", "Özgür Yaşam", "Dural",
        "Esra", "Merve", "Serap", "Rümeysa", "Nursel", "Zekeriya", "Mustafa", "Ünzile",
        "Hikmet", "Esra Gelin", "Ahmet", "Ayşegül", "Sevgi", "Talha", "Büşra", "Osman",
        "Zeynep", "Tuğba", "Esin", "Fikret", "Yusuf", "Şeyma", "Burak Enes", "Dürnev",
        "İsmail", "Havva", "Eren", "Ayşe", "Melih", "Yiğit", "Saniye", "Elfize"
    ]
    
    yasin_verileri = [
        {"sira_no": i+1, "okuyan": yasin_isimleri[i], "okunma": i % 2 == 0}
        for i in range(40)
    ]
    
    return yasin_donemleri, hatim_donemleri, hatim_verileri, yasin_verileri

# Session state initialization
if 'yasin_donemleri' not in st.session_state:
    yasin_donemleri, hatim_donemleri, hatim_verileri, yasin_verileri = get_initial_data()
    st.session_state.yasin_donemleri = yasin_donemleri
    st.session_state.hatim_donemleri = hatim_donemleri
    st.session_state.hatim_verileri = hatim_verileri
    st.session_state.yasin_verileri = yasin_verileri
    st.session_state.secili_yasin_donem = 0
    st.session_state.secili_hatim_donem = 0

# Header
st.markdown("""
<div class="main-header">
    <h1>🌧️ Hatim Yağmuru</h1>
    <p>Bereket ve rahmet dolu okumalar</p>
</div>
""", unsafe_allow_html=True)

# Tab seçimi
tab1, tab2 = st.tabs(["📖 Hatim Cüz", "📿 Yasin"])

with tab1:
    st.markdown("### 📖 Hatim Cüz Takibi")
    
    # Dönem seçici
    col1, col2 = st.columns([2, 1])
    with col1:
        secili_hatim_index = st.selectbox(
            "Hatim Cüz Dönem:",
            range(len(st.session_state.hatim_donemleri)),
            format_func=lambda x: st.session_state.hatim_donemleri[x]["ay"],
            index=st.session_state.secili_hatim_donem,
            key="hatim_donem_select"
        )
        st.session_state.secili_hatim_donem = secili_hatim_index
    
    # İlerleme durumu
    tamamlanan_hatim = sum(1 for item in st.session_state.hatim_verileri if item["okunma"])
    ilerleme_yuzde = (tamamlanan_hatim / 30) * 100
    
    st.markdown('<div class="progress-card">', unsafe_allow_html=True)
    st.markdown(f"**İlerleme Durumu:** {tamamlanan_hatim}/30 (%{ilerleme_yuzde:.0f})")
    st.progress(ilerleme_yuzde / 100)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Hatim listesi
    st.markdown("---")
    for i, item in enumerate(st.session_state.hatim_verileri):
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        
        with col1:
            st.markdown(f"**{item['cuz_no']}**")
        with col2:
            st.markdown(f"**{item['okuyan']}**")
        with col3:
            st.markdown(f"{item['cuz_no']}. Cüz")
        with col4:
            if item["okunma"]:
                st.markdown('<span class="btn-evet">✅ EVET</span>', unsafe_allow_html=True)
            else:
                if st.button("❌ HAYIR", key=f"hatim_{i}", type="secondary"):
                    st.session_state.hatim_verileri[i]["okunma"] = True
                    st.rerun()

with tab2:
    st.markdown("### 📿 Yasin Takibi")
    
    # Dönem seçici
    col1, col2 = st.columns([2, 1])
    with col1:
        secili_yasin_index = st.selectbox(
            "Yasin Dönem:",
            range(len(st.session_state.yasin_donemleri)),
            format_func=lambda x: f"{st.session_state.yasin_donemleri[x]['tarih']} (H:{st.session_state.yasin_donemleri[x]['haftalik_sayi']}, T:{st.session_state.yasin_donemleri[x]['toplam_sayi']})",
            index=st.session_state.secili_yasin_donem,
            key="yasin_donem_select"
        )
        st.session_state.secili_yasin_donem = secili_yasin_index
    
    # Seçili dönem bilgileri
    secili_donem = st.session_state.yasin_donemleri[secili_yasin_index]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 Tarih", secili_donem["tarih"])
    with col2:
        st.metric("📊 Haftalık", secili_donem["haftalik_sayi"])
    with col3:
        st.metric("📈 Toplam", secili_donem["toplam_sayi"])
    
    # İlerleme durumu
    tamamlanan_yasin = sum(1 for item in st.session_state.yasin_verileri if item["okunma"])
    ilerleme_yuzde = (tamamlanan_yasin / 40) * 100
    
    st.markdown('<div class="progress-card">', unsafe_allow_html=True)
    st.markdown(f"**İlerleme Durumu:** {tamamlanan_yasin}/40 (%{ilerleme_yuzde:.0f})")
    st.progress(ilerleme_yuzde / 100)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Yasin listesi
    st.markdown("---")
    for i, item in enumerate(st.session_state.yasin_verileri):
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        
        with col1:
            st.markdown(f"**{item['sira_no']}**")
        with col2:
            st.markdown(f"**{item['okuyan']}**")
        with col3:
            st.markdown(f"{item['sira_no']}. Sıra")
        with col4:
            if item["okunma"]:
                st.markdown('<span class="btn-evet">✅ EVET</span>', unsafe_allow_html=True)
            else:
                if st.button("❌ HAYIR", key=f"yasin_{i}", type="secondary"):
                    st.session_state.yasin_verileri[i]["okunma"] = True
                    st.rerun()

# Sidebar - Ek Bilgiler
with st.sidebar:
    st.markdown("### 📊 Özet Bilgiler")
    
    # Genel istatistikler
    toplam_hatim = sum(1 for item in st.session_state.hatim_verileri if item["okunma"])
    toplam_yasin = sum(1 for item in st.session_state.yasin_verileri if item["okunma"])
    
    st.metric("📖 Tamamlanan Hatim", f"{toplam_hatim}/30")
    st.metric("📿 Tamamlanan Yasin", f"{toplam_yasin}/40")
    
    # Veri sıfırlama
    st.markdown("---")
    if st.button("🔄 Verileri Sıfırla", type="secondary"):
        yasin_donemleri, hatim_donemleri, hatim_verileri, yasin_verileri = get_initial_data()
        st.session_state.hatim_verileri = hatim_verileri
        st.session_state.yasin_verileri = yasin_verileri
        st.rerun()
    
    # Veri export
    st.markdown("---")
    st.markdown("### 📥 Veri Export")
    
    # JSON export
    export_data = {
        "hatim_verileri": st.session_state.hatim_verileri,
        "yasin_verileri": st.session_state.yasin_verileri,
        "export_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    st.download_button(
        label="📄 JSON olarak İndir",
        data=json.dumps(export_data, ensure_ascii=False, indent=2),
        file_name=f"hatim_yasin_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

# Footer
st.markdown("---")
config = load_app_config()
st.markdown(f"""
<div style="text-align: center; color: #6b7280; padding: 1rem;">
    🌧️ Hatim Yağmuru - Bereket ve rahmet dolu okumalar<br>
    <small>v{config['app_version']} | Son güncelleme: {config['last_updated']} | Made with ❤️ using Streamlit</small>
</div>
""", unsafe_allow_html=True)