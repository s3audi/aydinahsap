import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import plotly.express as px
import plotly.graph_objects as go

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="🌧️ Hatim Yağmuru",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Deployment için cache temizleme
@st.cache_data(ttl=3600)
def load_app_config():
    return {
        "app_version": "2.0.0",
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "environment": os.getenv("STREAMLIT_ENV", "production")
    }

# Gelişmiş CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(-50%, -50%) rotate(0deg); }
        50% { transform: translate(-50%, -50%) rotate(180deg); }
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    .progress-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #0ea5e9;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .progress-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #0ea5e9, #06b6d4, #0891b2);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .person-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .person-card:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .person-card.completed {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-color: #22c55e;
    }
    
    .person-card.pending {
        background: linear-gradient(135deg, #fef7f0 0%, #fed7aa 100%);
        border-color: #f97316;
    }
    
    .btn-evet {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
    }
    
    .btn-evet:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4);
    }
    
    .btn-hayir {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
    }
    
    .btn-hayir:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
    }
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .tab-container {
        background: white;
        border-radius: 12px;
        padding: 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    
    .search-box {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .search-box:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    .filter-chip {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        background: #f3f4f6;
        border: 1px solid #d1d5db;
        border-radius: 20px;
        font-size: 0.875rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .filter-chip.active {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }
    
    .completion-badge {
        position: absolute;
        top: 1rem;
        right: 1rem;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #22c55e;
    }
    
    .completion-badge.pending {
        background: #f97316;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .section-header h3 {
        margin: 0;
        color: #374151;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Veri yapıları
@st.cache_data
def get_initial_data():
    # Yasin dönemleri
    yasin_donemleri = [
        {"id": 1, "tarih": "16 Mayıs 2025", "haftalik_sayi": 36, "toplam_sayi": 226, "aciklama": "Ramazan sonrası özel program"},
        {"id": 2, "tarih": "9 Mayıs 2025", "haftalik_sayi": 35, "toplam_sayi": 190, "aciklama": "Bahar dönemi programı"},
        {"id": 3, "tarih": "2 Mayıs 2025", "haftalik_sayi": 34, "toplam_sayi": 155, "aciklama": "İlkbahar bereket programı"}
    ]
    
    # Hatim dönemleri
    hatim_donemleri = [
        {"id": 1, "ay": "Mayıs 2025", "aciklama": "Ramazan sonrası hatim", "baslangic": "2025-05-01"},
        {"id": 2, "ay": "Nisan 2025", "aciklama": "Ramazan hatimi", "baslangic": "2025-04-01"},
        {"id": 3, "ay": "Mart 2025", "aciklama": "İlkbahar hatimi", "baslangic": "2025-03-01"}
    ]
    
    # Hatim verileri (30 cüz) - daha detaylı
    hatim_okuyanlar = ["Tamer Bey", "Emre Abi", "Gülnhal Hanım", "Fatma Teyze", "Mehmet Abi", "Ayşe Hanım"]
    hatim_verileri = [
        {
            "cuz_no": i+1, 
            "okuyan": hatim_okuyanlar[i % len(hatim_okuyanlar)], 
            "okunma": i % 3 == 0,
            "tamamlanma_tarihi": (datetime.now() - timedelta(days=30-i)).strftime("%Y-%m-%d") if i % 3 == 0 else None,
            "sure_araligi": f"{i*10+1}-{(i+1)*10}" if i < 29 else "281-286"
        }
        for i in range(30)
    ]
    
    # Yasin verileri (40 kişi) - daha detaylı
    yasin_isimleri = [
        "Yunus Emre", "Tamer Bey", "Sabahat Hanım", "Emre Abi", "Hacer Teyze", "Fatih Abi", 
        "Özgür Yaşam", "Dural Abi", "Esra Hanım", "Merve", "Serap Abla", "Rümeysa", 
        "Nursel Teyze", "Zekeriya Abi", "Mustafa Amca", "Ünzile Hanım", "Hikmet Dede", 
        "Esra Gelin", "Ahmet Abi", "Ayşegül", "Sevgi Hanım", "Talha", "Büşra", "Osman Abi",
        "Zeynep", "Tuğba Abla", "Esin Hanım", "Fikret Amca", "Yusuf", "Şeyma", 
        "Burak Enes", "Dürnev Abi", "İsmail", "Havva Hanım", "Eren", "Ayşe Teyze", 
        "Melih", "Yiğit", "Saniye Nene", "Elfize Hanım"
    ]
    
    yasin_verileri = [
        {
            "sira_no": i+1, 
            "okuyan": yasin_isimleri[i], 
            "okunma": i % 4 == 0,
            "tamamlanma_tarihi": (datetime.now() - timedelta(days=7-i//6)).strftime("%Y-%m-%d") if i % 4 == 0 else None,
            "niyetler": ["Şifa", "Bereket", "Rahmet", "Mağfiret"][i % 4]
        }
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
    st.session_state.hatim_filter = "Tümü"
    st.session_state.yasin_filter = "Tümü"
    st.session_state.search_term = ""

# Header
st.markdown("""
<div class="main-header">
    <h1>🌧️ Hatim Yağmuru</h1>
    <p>Bereket ve rahmet dolu okumalar - Birlikte tamamlayalım</p>
</div>
""", unsafe_allow_html=True)

# Genel İstatistikler Dashboard
st.markdown('<div class="section-header"><h3>📊 Genel Durum</h3></div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    tamamlanan_hatim = sum(1 for item in st.session_state.hatim_verileri if item["okunma"])
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="color: #059669; margin: 0;">📖 {tamamlanan_hatim}/30</h2>
        <p style="margin: 0.5rem 0 0 0; color: #6b7280;">Tamamlanan Hatim</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    tamamlanan_yasin = sum(1 for item in st.session_state.yasin_verileri if item["okunma"])
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="color: #7c3aed; margin: 0;">📿 {tamamlanan_yasin}/40</h2>
        <p style="margin: 0.5rem 0 0 0; color: #6b7280;">Tamamlanan Yasin</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    hatim_yuzde = (tamamlanan_hatim / 30) * 100
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="color: #dc2626; margin: 0;">📈 %{hatim_yuzde:.0f}</h2>
        <p style="margin: 0.5rem 0 0 0; color: #6b7280;">Hatim İlerlemesi</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    yasin_yuzde = (tamamlanan_yasin / 40) * 100
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="color: #0891b2; margin: 0;">📊 %{yasin_yuzde:.0f}</h2>
        <p style="margin: 0.5rem 0 0 0; color: #6b7280;">Yasin İlerlemesi</p>
    </div>
    """, unsafe_allow_html=True)

# Grafik Gösterimleri
st.markdown('<div class="section-header"><h3>📈 İlerleme Grafikleri</h3></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Hatim İlerleme Grafiği
    hatim_data = {
        'Durum': ['Tamamlandı', 'Bekliyor'],
        'Sayı': [tamamlanan_hatim, 30 - tamamlanan_hatim],
        'Yüzde': [hatim_yuzde, 100 - hatim_yuzde]
    }
    
    fig_hatim = px.pie(
        values=hatim_data['Sayı'], 
        names=hatim_data['Durum'],
        title="📖 Hatim Cüz Durumu",
        color_discrete_sequence=['#059669', '#f3f4f6']
    )
    fig_hatim.update_traces(textposition='inside', textinfo='percent+label')
    fig_hatim.update_layout(height=300, showlegend=True)
    st.plotly_chart(fig_hatim, use_container_width=True)

with col2:
    # Yasin İlerleme Grafiği
    yasin_data = {
        'Durum': ['Tamamlandı', 'Bekliyor'],
        'Sayı': [tamamlanan_yasin, 40 - tamamlanan_yasin],
        'Yüzde': [yasin_yuzde, 100 - yasin_yuzde]
    }
    
    fig_yasin = px.pie(
        values=yasin_data['Sayı'], 
        names=yasin_data['Durum'],
        title="📿 Yasin Durumu",
        color_discrete_sequence=['#7c3aed', '#f3f4f6']
    )
    fig_yasin.update_traces(textposition='inside', textinfo='percent+label')
    fig_yasin.update_layout(height=300, showlegend=True)
    st.plotly_chart(fig_yasin, use_container_width=True)

# Tab seçimi
tab1, tab2, tab3 = st.tabs(["📖 Hatim Cüz", "📿 Yasin", "📊 Detaylı Raporlar"])

with tab1:
    st.markdown('<div class="section-header"><h3>📖 Hatim Cüz Takibi</h3></div>', unsafe_allow_html=True)
    
    # Kontroller
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        secili_hatim_index = st.selectbox(
            "Hatim Cüz Dönem:",
            range(len(st.session_state.hatim_donemleri)),
            format_func=lambda x: f"{st.session_state.hatim_donemleri[x]['ay']} - {st.session_state.hatim_donemleri[x]['aciklama']}",
            index=st.session_state.secili_hatim_donem,
            key="hatim_donem_select"
        )
        st.session_state.secili_hatim_donem = secili_hatim_index
    
    with col2:
        unique_readers = list(set(item["okuyan"] for item in st.session_state.hatim_verileri))
        st.session_state.hatim_filter = st.selectbox(
            "Okuyucu Filtresi:",
            ["Tümü"] + unique_readers,
            index=0 if st.session_state.hatim_filter == "Tümü" else unique_readers.index(st.session_state.hatim_filter) + 1,
            key="hatim_filter_select"
        )
    
    with col3:
        durum_filter = st.selectbox(
            "Durum Filtresi:",
            ["Tümü", "Tamamlandı", "Bekliyor"],
            key="hatim_durum_filter"
        )
    
    # Arama kutusu
    search_term = st.text_input("🔍 Arama (İsim veya Cüz No):", key="hatim_search")
    
    # İlerleme durumu
    st.markdown('<div class="progress-card">', unsafe_allow_html=True)
    st.markdown(f"**📖 Hatim İlerleme Durumu:** {tamamlanan_hatim}/30 cüz tamamlandı (%{hatim_yuzde:.1f})")
    st.progress(hatim_yuzde / 100)
    
    if tamamlanan_hatim == 30:
        st.success("🎉 Tebrikler! Hatim tamamlandı! 🎉")
    elif tamamlanan_hatim >= 20:
        st.info(f"💪 Çok yaklaştınız! Sadece {30 - tamamlanan_hatim} cüz kaldı!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filtrelenmiş listeyi hazırla
    filtered_hatim = st.session_state.hatim_verileri
    
    if st.session_state.hatim_filter != "Tümü":
        filtered_hatim = [item for item in filtered_hatim if item["okuyan"] == st.session_state.hatim_filter]
    
    if durum_filter == "Tamamlandı":
        filtered_hatim = [item for item in filtered_hatim if item["okunma"]]
    elif durum_filter == "Bekliyor":
        filtered_hatim = [item for item in filtered_hatim if not item["okunma"]]
    
    if search_term:
        filtered_hatim = [item for item in filtered_hatim 
                         if search_term.lower() in item["okuyan"].lower() or 
                         search_term in str(item["cuz_no"])]
    
    # Hatim listesi
    st.markdown("---")
    for i, item in enumerate(st.session_state.hatim_verileri):
        if item not in filtered_hatim:
            continue
            
        original_index = st.session_state.hatim_verileri.index(item)
        card_class = "completed" if item["okunma"] else "pending"
        
        st.markdown(f'<div class="person-card {card_class}">', unsafe_allow_html=True)
        st.markdown(f'<div class="completion-badge {"" if item["okunma"] else "pending"}"></div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 2])
        
        with col1:
            st.markdown(f"**{item['cuz_no']}**")
        
        with col2:
            st.markdown(f"**{item['okuyan']}**")
        
        with col3:
            st.markdown(f"Sayfa: {item['sure_araligi']}")
        
        with col4:
            if item["tamamlanma_tarihi"]:
                st.markdown(f"📅 {item['tamamlanma_tarihi']}")
            else:
                st.markdown("⏳ Bekliyor")
        
        with col5:
            if item["okunma"]:
                if st.button("✅ TAMAMLANDI", key=f"hatim_{original_index}", type="primary"):
                    st.session_state.hatim_verileri[original_index]["okunma"] = False
                    st.session_state.hatim_verileri[original_index]["tamamlanma_tarihi"] = None
                    st.rerun()
            else:
                if st.button("❌ BEKLİYOR", key=f"hatim_{original_index}", type="secondary"):
                    st.session_state.hatim_verileri[original_index]["okunma"] = True
                    st.session_state.hatim_verileri[original_index]["tamamlanma_tarihi"] = datetime.now().strftime("%Y-%m-%d")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-header"><h3>📿 Yasin Takibi</h3></div>', unsafe_allow_html=True)
    
    # Kontroller
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        secili_yasin_index = st.selectbox(
            "Yasin Dönem:",
            range(len(st.session_state.yasin_donemleri)),
            format_func=lambda x: f"{st.session_state.yasin_donemleri[x]['tarih']} - H:{st.session_state.yasin_donemleri[x]['haftalik_sayi']} T:{st.session_state.yasin_donemleri[x]['toplam_sayi']}",
            index=st.session_state.secili_yasin_donem,
            key="yasin_donem_select"
        )
        st.session_state.secili_yasin_donem = secili_yasin_index
    
    with col2:
        unique_niyetler = list(set(item["niyetler"] for item in st.session_state.yasin_verileri))
        niyet_filter = st.selectbox(
            "Niyet Filtresi:",
            ["Tümü"] + unique_niyetler,
            key="yasin_niyet_filter"
        )
    
    with col3:
        yasin_durum_filter = st.selectbox(
            "Durum Filtresi:",
            ["Tümü", "Tamamlandı", "Bekliyor"],
            key="yasin_durum_filter"
        )
    
    # Arama kutusu
    yasin_search = st.text_input("🔍 Arama (İsim veya Sıra No):", key="yasin_search")
    
    # Seçili dönem bilgileri
    secili_donem = st.session_state.yasin_donemleri[secili_yasin_index]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #059669; margin: 0;">📅</h3>
            <h4 style="margin: 0.5rem 0;">{secili_donem["tarih"]}</h4>
            <p style="margin: 0; color: #6b7280; font-size: 0.875rem;">{secili_donem["aciklama"]}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #7c3aed; margin: 0;">📊</h3>
            <h4 style="margin: 0.5rem 0;">Haftalık: {secili_donem["haftalik_sayi"]}</h4>
            <p style="margin: 0; color: #6b7280; font-size: 0.875rem;">Bu hafta hedefi</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #dc2626; margin: 0;">📈</h3>
            <h4 style="margin: 0.5rem 0;">Toplam: {secili_donem["toplam_sayi"]}</h4>
            <p style="margin: 0; color: #6b7280; font-size: 0.875rem;">Genel toplam</p>
        </div>
        """, unsafe_allow_html=True)
    
    # İlerleme durumu
    st.markdown('<div class="progress-card">', unsafe_allow_html=True)
    st.markdown(f"**📿 Yasin İlerleme Durumu:** {tamamlanan_yasin}/40 kişi tamamladı (%{yasin_yuzde:.1f})")
    st.progress(yasin_yuzde / 100)
    
    if tamamlanan_yasin == 40:
        st.success("🎉 Tebrikler! Tüm Yasin okumaları tamamlandı! 🎉")
    elif tamamlanan_yasin >= 30:
        st.info(f"💪 Çok yaklaştınız! Sadece {40 - tamamlanan_yasin} kişi kaldı!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Her dönem için ayrı yasin verisi tutmak için session_state'i güncelle
    if 'yasin_donem_okuyuculari' not in st.session_state:
        # Her dönem için bir liste oluştur
        st.session_state.yasin_donem_okuyuculari = {}
        for idx, donem in enumerate(st.session_state.yasin_donemleri):
            st.session_state.yasin_donem_okuyuculari[idx] = [
                item for item in st.session_state.yasin_verileri
            ]

    # Dönem seçimi
    secili_yasin_index = st.selectbox(
        "Yasin Dönem:",
        range(len(st.session_state.yasin_donemleri)),
        format_func=lambda x: f"{st.session_state.yasin_donemleri[x]['tarih']} - H:{st.session_state.yasin_donemleri[x]['haftalik_sayi']} T:{st.session_state.yasin_donemleri[x]['toplam_sayi']}",
        index=st.session_state.secili_yasin_donem,
        key="yasin_donem_select"
    )
    st.session_state.secili_yasin_donem = secili_yasin_index

    # Seçili dönemin okuyucu verisi
    if secili_yasin_index not in st.session_state.yasin_donem_okuyuculari:
        st.session_state.yasin_donem_okuyuculari[secili_yasin_index] = []

    donem_yasin_verileri = st.session_state.yasin_donem_okuyuculari[secili_yasin_index]

    # Filtreler
    unique_niyetler = list(set(item["niyetler"] for item in donem_yasin_verileri))
    niyet_filter = st.selectbox(
        "Niyet Filtresi:",
        ["Tümü"] + unique_niyetler,
        key="yasin_niyet_filter"
    )
    yasin_durum_filter = st.selectbox(
        "Durum Filtresi:",
        ["Tümü", "Tamamlandı", "Bekliyor"],
        key="yasin_durum_filter"
    )
    yasin_search = st.text_input("🔍 Arama (İsim veya Sıra No):", key="yasin_search")

    # Filtrelenmiş listeyi hazırla
    filtered_yasin = donem_yasin_verileri
    if niyet_filter != "Tümü":
        filtered_yasin = [item for item in filtered_yasin if item["niyetler"] == niyet_filter]
    if yasin_durum_filter == "Tamamlandı":
        filtered_yasin = [item for item in filtered_yasin if item["okunma"]]
    elif yasin_durum_filter == "Bekliyor":
        filtered_yasin = [item for item in filtered_yasin if not item["okunma"]]
    if yasin_search:
        filtered_yasin = [
            item for item in filtered_yasin
            if yasin_search.lower() in item["okuyan"].lower()
            or yasin_search.lower() in item["niyetler"].lower()
            or yasin_search in str(item["sira_no"])
        ]

    # Listeyi göster
    st.markdown("---")
    for i, item in enumerate(donem_yasin_verileri):
        if item not in filtered_yasin:
            continue
        original_index = donem_yasin_verileri.index(item)
        card_class = "completed" if item["okunma"] else "pending"
        st.markdown(f'<div class="person-card {card_class}">', unsafe_allow_html=True)
        st.markdown(f'<div class="completion-badge {"" if item["okunma"] else "pending"}"></div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
        with col1:
            st.markdown(f"**{item['sira_no']}**")
        with col2:
            st.markdown(f"**{item['okuyan']}**")
        with col3:
            if item["tamamlanma_tarihi"]:
                st.markdown(f"📅 {item['tamamlanma_tarihi']}")
            else:
                st.markdown("⏳ Bekliyor")
        with col4:
            if item["okunma"]:
                if st.button("✅ TAMAMLANDI", key=f"yasin_{secili_yasin_index}_{original_index}", type="primary"):
                    donem_yasin_verileri[original_index]["okunma"] = False
                    donem_yasin_verileri[original_index]["tamamlanma_tarihi"] = None
                    st.rerun()
            else:
                if st.button("❌ BEKLİYOR", key=f"yasin_{secili_yasin_index}_{original_index}", type="secondary"):
                    donem_yasin_verileri[original_index]["okunma"] = True
                    donem_yasin_verileri[original_index]["tamamlanma_tarihi"] = datetime.now().strftime("%Y-%m-%d")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Yeni kişi ekleme
    with st.expander("➕ Yeni Yasin Okuyucusu Ekle"):
        yeni_isim = st.text_input("Yeni okuyucu adı girin:", key=f"yeni_isim_{secili_yasin_index}")
        yeni_niyet = st.selectbox("Niyet:", ["Şifa", "Bereket", "Rahmet", "Mağfiret"], key=f"yeni_niyet_{secili_yasin_index}")
        if st.button("Ekle", key=f"yeni_yasin_ekle_{secili_yasin_index}") and yeni_isim:
            donem_yasin_verileri.append({
                "sira_no": len(donem_yasin_verileri) + 1,
                "okuyan": yeni_isim,
                "okunma": False,
                "tamamlanma_tarihi": None,
                "niyetler": yeni_niyet
            })
            st.success(f"{yeni_isim} eklendi!")
            st.rerun()

    # Kişi silme
    for i, item in enumerate(filtered_yasin):
        col1, col2 = st.columns([8, 1])
        with col1:
            st.markdown(f"**{item['sira_no']}. {item['okuyan']}** - {item['niyetler']}")
        with col2:
            if st.button("🗑️", key=f"delete_yasin_{secili_yasin_index}_{i}"):
                donem_yasin_verileri.remove(item)
                st.success(f"{item['okuyan']} silindi!")
                st.rerun()

    # Dışa/İçe aktar
    with st.expander("⬇️/⬆️ Yasin Verilerini Dışa Aktar / İçe Aktar"):
        st.download_button(
            label="Yasin Verilerini İndir (JSON)",
            data=json.dumps(donem_yasin_verileri, ensure_ascii=False, indent=2),
            file_name=f"yasin_verileri_donem_{secili_yasin_index}.json",
            mime="application/json"
        )
        uploaded_file = st.file_uploader("Yasin verisi yükle (JSON)", type="json", key=f"upload_{secili_yasin_index}")
        if uploaded_file:
            try:
                st.session_state.yasin_donem_okuyuculari[secili_yasin_index] = json.load(uploaded_file)
                st.success("Veriler başarıyla yüklendi!")
                st.rerun()
            except Exception as e:
                st.error(f"Yükleme hatası: {e}")