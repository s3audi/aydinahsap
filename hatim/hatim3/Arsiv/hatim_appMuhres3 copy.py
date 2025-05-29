import streamlit as st
import pandas as pd
import json
import plotly.express as px
import base64

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

st.title("🌧️ Hatim Yağmuruuu")
st.markdown("---")

# --- Yedekleme ve Geri Yükleme ---
st.subheader("Veri Yedekleme / Geri Yükleme")

# JSON olarak indir
st.download_button(
    label="Veriyi İndir (JSON Yedek)",
    data=json.dumps(all_data, ensure_ascii=False, indent=2),
    file_name="hatim_yagmur_yedek.json",
    mime="application/json"
)

# JSON olarak yükle
uploaded_file = st.file_uploader("Veri Yükle (JSON)", type="json")
if uploaded_file:
    try:
        new_data = json.load(uploaded_file)
        save_data(new_data)
        st.success("Veri başarıyla yüklendi! Sayfa yenileniyor...")
        st.rerun()
    except Exception as e:
        st.error(f"Yükleme hatası: {e}")

st.markdown("---")

# --- İki Sütunlu Ana Uygulama ---
col_yasin, col_cuz = st.columns(2)

# --- Yasin Dönemleri (Sol Sütun) ---
with col_yasin:
    st.subheader("Yasin Dönemleri")
    yasin_donemleri_list = df_hatim_yasin["Hatim Dönem"].unique().tolist()
    selected_yasin_donem = st.selectbox("Yasin Dönemi Seçin:", yasin_donemleri_list, key="yasin_select")

    if selected_yasin_donem:
        # Filtre açılır menüsü
        yasin_filter = st.selectbox(
            "Filtrele:",
            ("Hepsi", "Okunanlar", "Okunmayanlar"),
            key="yasin_filter"
        )

        df_current_yasin = df_hatim_yasin[df_hatim_yasin["Hatim Dönem"] == selected_yasin_donem].copy()
        df_current_yasin.rename(columns={"DURUM": "Okunma Durumu"}, inplace=True)
        df_display_yasin = df_current_yasin[["Cüz No", "Okuyan", "Okunma Durumu"]]

        # Filtre uygula
        if yasin_filter == "Okunanlar":
            df_display_yasin = df_display_yasin[df_display_yasin["Okunma Durumu"] == "Evet"]
        elif yasin_filter == "Okunmayanlar":
            df_display_yasin = df_display_yasin[df_display_yasin["Okunma Durumu"] == "Hayır"]

        st.write(f"**Toplam Cüz Sayısı:** {df_display_yasin.shape[0]}")
        st.write(f"**Okunan Cüz Sayısı:** {df_display_yasin[df_display_yasin['Okunma Durumu']=='Evet'].shape[0]}")
        st.write(f"**Okunmayan Cüz Sayısı:** {df_display_yasin[df_display_yasin['Okunma Durumu']=='Hayır'].shape[0]}")

        st.markdown("### Cüz Okunma Durumları")
        evet_img_url = "https://cdn-icons-png.flaticon.com/512/845/845646.png"
        hayir_img_url = "https://cdn-icons-png.flaticon.com/512/753/753345.png"

        for idx, row in df_display_yasin.iterrows():
            col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
            col1.write(row["Cüz No"])
            col2.write(row["Okuyan"])
            durum = row["Okunma Durumu"]
            btn_text = "Evet" if durum == "Evet" else "Hayır"
            img_url = evet_img_url if durum == "Evet" else hayir_img_url
            btn_key = f"yasin_{selected_yasin_donem}_{row['Cüz No']}"
            if col3.button(btn_text, key=btn_key, help="Durumu değiştir"):
                for i, donem in enumerate(all_data["hatim_yasin_donemleri"]):
                    if donem["Hatim Dönem"] == selected_yasin_donem:
                        for j, cuz in enumerate(donem["Cüzler"]):
                            if cuz["Cüz No"] == row["Cüz No"]:
                                yeni_durum = "Hayır" if durum == "Evet" else "Evet"
                                all_data["hatim_yasin_donemleri"][i]["Cüzler"][j]["DURUM"] = yeni_durum
                                save_data(all_data)
                                st.rerun()
            col4.markdown(f'<img src="{img_url}" width="32"/>', unsafe_allow_html=True)

# --- Hatim Cüz Dönemleri (Sağ Sütun) ---
with col_cuz:
    st.subheader("Hatim Cüz Dönemleri")
    cuz_donemleri_list = df_hatim_cuz["Hatim Dönem"].unique().tolist()
    selected_cuz_donem = st.selectbox("Hatim Cüz Dönemi Seçin:", cuz_donemleri_list, key="cuz_select")

    if selected_cuz_donem:
        # Filtre açılır menüsü
        cuz_filter = st.selectbox(
            "Filtrele:",
            ("Hepsi", "Okunanlar", "Okunmayanlar"),
            key="cuz_filter"
        )

        df_current_cuz = df_hatim_cuz[df_hatim_cuz["Hatim Dönem"] == selected_cuz_donem].copy()
        df_current_cuz.rename(columns={"DURUM": "Okunma Durumu"}, inplace=True)
        df_display_cuz = df_current_cuz[["Cüz No", "Okuyan", "Okunma Durumu"]]

        # Filtre uygula
        if cuz_filter == "Okunanlar":
            df_display_cuz = df_display_cuz[df_display_cuz["Okunma Durumu"] == "Evet"]
        elif cuz_filter == "Okunmayanlar":
            df_display_cuz = df_display_cuz[df_display_cuz["Okunma Durumu"] == "Hayır"]

        st.write(f"**Toplam Cüz Sayısı:** {df_display_cuz.shape[0]}")
        st.write(f"**Okunan Cüz Sayısı:** {df_display_cuz[df_display_cuz['Okunma Durumu']=='Evet'].shape[0]}")
        st.write(f"**Okunmayan Cüz Sayısı:** {df_display_cuz[df_display_cuz['Okunma Durumu']=='Hayır'].shape[0]}")

        st.markdown("### Cüz Okunma Durumları")
        evet_img_url = "https://cdn-icons-png.flaticon.com/512/845/845646.png"
        hayir_img_url = "https://cdn-icons-png.flaticon.com/512/753/753345.png"

        for idx, row in df_display_cuz.iterrows():
            col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
            col1.write(row["Cüz No"])
            col2.write(row["Okuyan"])
            durum = row["Okunma Durumu"]
            btn_text = "Evet" if durum == "Evet" else "Hayır"
            img_url = evet_img_url if durum == "Evet" else hayir_img_url
            btn_key = f"cuz_{selected_cuz_donem}_{row['Cüz No']}"
            if col3.button(btn_text, key=btn_key, help="Durumu değiştir"):
                for i, donem in enumerate(all_data["hatim_cuz_donemleri"]):
                    if donem["Hatim Dönem"] == selected_cuz_donem:
                        for j, cuz in enumerate(donem["Cüzler"]):
                            if cuz["Cüz No"] == row["Cüz No"]:
                                yeni_durum = "Hayır" if durum == "Evet" else "Evet"
                                all_data["hatim_cuz_donemleri"][i]["Cüzler"][j]["DURUM"] = yeni_durum
                                save_data(all_data)
                                st.rerun()
            col4.markdown(f'<img src="{img_url}" width="32"/>', unsafe_allow_html=True)