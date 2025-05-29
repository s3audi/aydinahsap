import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(layout="wide")

DATA_FILE = "data.json"

# JSON dosyasını oku veya boş bir yapı oluştur
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "hatim_yasin_donemleri": [],
            "hatim_cuz_donemleri": []
        }

# JSON dosyasına veriyi kaydet
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Veriyi yükle
all_data = load_data()

# --- Verileri DataFrame'e dönüştürme fonksiyonları ---
def get_yasin_df(yasin_data):
    records = []
    for donem in yasin_data:
        for cuz in donem["Cüzler"]:
            records.append({
                "Yasin No": donem["Yasin No"],
                "Hatim Dönem": donem["Hatim Dönem"],
                "Cüz No": cuz["Cüz No"],
                "Okuyan": cuz["Okuyan"],
                "DURUM": cuz["DURUM"]
            })
    return pd.DataFrame(records)

def get_cuz_df(cuz_data):
    records = []
    for donem in cuz_data:
        for cuz in donem["Cüzler"]:
            records.append({
                "Hatim No": donem["Hatim No"],
                "Hatim Dönem": donem["Hatim Dönem"],
                "Cüz No": cuz["Cüz No"],
                "Okuyan": cuz["Okuyan"],
                "DURUM": cuz["DURUM"]
            })
    return pd.DataFrame(records)

df_hatim_yasin = get_yasin_df(all_data["hatim_yasin_donemleri"])
df_hatim_cuz = get_cuz_df(all_data["hatim_cuz_donemleri"])

# --- Streamlit Uygulaması ---

st.title("🌧️ Hatim Yağmuru")
st.markdown("---")

# --- Yasin Dönemleri Bölümü ---
st.subheader("Yasin Dönemleri")

yasin_donemleri_list = df_hatim_yasin["Hatim Dönem"].unique().tolist()
selected_yasin_donem = st.selectbox("Yasin Dönemi Seçin:", yasin_donemleri_list, key="yasin_select")

if selected_yasin_donem:
    df_current_yasin = df_hatim_yasin[df_hatim_yasin["Hatim Dönem"] == selected_yasin_donem].copy()
    df_current_yasin.rename(columns={"DURUM": "Okunma Durumu"}, inplace=True)
    df_display_yasin = df_current_yasin[["Cüz No", "Okuyan", "Okunma Durumu"]]

    st.write(f"**Toplam Cüz Sayısı:** {df_display_yasin.shape[0]}")
    st.write(f"**Okunan Cüz Sayısı:** {df_display_yasin[df_display_yasin['Okunma Durumu']=='Evet'].shape[0]}")
    st.write(f"**Okunmayan Cüz Sayısı:** {df_display_yasin[df_display_yasin['Okunma Durumu']=='Hayır'].shape[0]}")

    st.markdown("### Cüz Okunma Durumları")
    for idx, row in df_display_yasin.iterrows():
        col1, col2, col3 = st.columns([1, 3, 2])
        col1.write(row["Cüz No"])
        col2.write(row["Okuyan"])
        durum = row["Okunma Durumu"]
        btn_label = "Evet" if durum == "Evet" else "Hayır"
        btn_style = f"background-color: {'#22c55e' if durum == 'Evet' else '#fca5a5'}; color: white; border: none; padding: 0.5em 1em; border-radius: 5px; width:100%;"
        if col3.button(btn_label, key=f"yasin_{selected_yasin_donem}_{row['Cüz No']}"):
            # JSON verisinde güncelle
            for i, donem in enumerate(all_data["hatim_yasin_donemleri"]):
                if donem["Hatim Dönem"] == selected_yasin_donem:
                    for j, cuz in enumerate(donem["Cüzler"]):
                        if cuz["Cüz No"] == row["Cüz No"]:
                            yeni_durum = "Hayır" if durum == "Evet" else "Evet"
                            all_data["hatim_yasin_donemleri"][i]["Cüzler"][j]["DURUM"] = yeni_durum
                            save_data(all_data)
                            st.rerun()
        else:
            col3.markdown(f"<div style='{btn_style};text-align:center'>{btn_label}</div>", unsafe_allow_html=True)

st.markdown("---")

# --- Hatim Cüz Dönemleri Bölümü ---
st.subheader("Hatim Cüz Dönemleri")

cuz_donemleri_list = df_hatim_cuz["Hatim Dönem"].unique().tolist()
selected_cuz_donem = st.selectbox("Hatim Cüz Dönemi Seçin:", cuz_donemleri_list, key="cuz_select")

if selected_cuz_donem:
    df_current_cuz = df_hatim_cuz[df_hatim_cuz["Hatim Dönem"] == selected_cuz_donem].copy()
    df_current_cuz.rename(columns={"DURUM": "Okunma Durumu"}, inplace=True)
    df_display_cuz = df_current_cuz[["Cüz No", "Okuyan", "Okunma Durumu"]]

    st.write(f"**Toplam Cüz Sayısı:** {df_display_cuz.shape[0]}")
    st.write(f"**Okunan Cüz Sayısı:** {df_display_cuz[df_display_cuz['Okunma Durumu']=='Evet'].shape[0]}")
    st.write(f"**Okunmayan Cüz Sayısı:** {df_display_cuz[df_display_cuz['Okunma Durumu']=='Hayır'].shape[0]}")

    st.markdown("### Cüz Okunma Durumları")
    for idx, row in df_display_cuz.iterrows():
        col1, col2, col3 = st.columns([1, 3, 2])
        col1.write(row["Cüz No"])
        col2.write(row["Okuyan"])
        durum = row["Okunma Durumu"]
        btn_label = "Evet" if durum == "Evet" else "Hayır"
        btn_style = f"background-color: {'#22c55e' if durum == 'Evet' else '#fca5a5'}; color: white; border: none; padding: 0.5em 1em; border-radius: 5px; width:100%;"
        if col3.button(btn_label, key=f"cuz_{selected_cuz_donem}_{row['Cüz No']}"):
            for i, donem in enumerate(all_data["hatim_cuz_donemleri"]):
                if donem["Hatim Dönem"] == selected_cuz_donem:
                    for j, cuz in enumerate(donem["Cüzler"]):
                        if cuz["Cüz No"] == row["Cüz No"]:
                            yeni_durum = "Hayır" if durum == "Evet" else "Evet"
                            all_data["hatim_cuz_donemleri"][i]["Cüzler"][j]["DURUM"] = yeni_durum
                            save_data(all_data)
                            st.rerun()
        else:
            col3.markdown(f"<div style='{btn_style};text-align:center'>{btn_label}</div>", unsafe_allow_html=True)