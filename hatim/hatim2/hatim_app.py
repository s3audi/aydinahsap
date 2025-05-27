import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Verileri doğrudan kod içine gömelim (PDF'lerden alınan örnek veriler)
# Hatim Data PDF'den alınan ilk tabloya göre [cite: 1]
hatim_data_16_mayis_2025 = {
    "Yasin No": [1]*40,
    "Hatim Dönem": ["16 Mayıs 2025"]*40,
    "Cüz No": list(range(1, 41)),
    "Okuyan": [
        "Yunus Emre", "Tamer", "Sabahat", "Emine", "Hacer", "Fatih", "Özgür Yaşam", "Durali", "Esra", "Merve",
        "Serap", "Rümeysa", "Nursel", "Zekeriya", "Mustafa", "Unzile", "Hikmet", "Esra Gelin", "Ahmet", "Ayşegül",
        "Sevgi", "Talha", "Büşra", "Osman", "Zeynep", "Tuğba", "Esin", "Fikret", "Yusuf", "Şeyma",
        "Burak Enes", "Dürnev", "Ismail", "Havva", "Eren", "Ayşe", "Melih", "Yiğit", "Saniye", "Elfize"
    ],
    "DURUM": [
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır",
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır",
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır",
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır"
    ]
}
df_hatim_16_mayis_2025 = pd.DataFrame(hatim_data_16_mayis_2025)

# Hatim Data PDF'den alınan ikinci tabloya göre (23 Mayıs 2025) [cite: 1]
hatim_data_23_mayis_2025_part1 = {
    "Yasin No": [2]*36,
    "Hatim Dönem": ["23 Mayıs 2025"]*36,
    "Cüz No": list(range(1, 37)),
    "Okuyan": [
        "Yunus Emre", "Tamer", "Sabahat", "Emine", "Hacer", "Fatih", "Özgür Yaşam", "Durali", "Esra", "Merve",
        "Serap", "Rümeysa", "Nursel", "Zekeriya", "Mustafa", "Ünzile", "Hikmet", "Esra Gelin", "Ahmet", "Ayşegül",
        "Sevgi", "Talha", "Büşra", "Osman", "Zeynep", "Tuğba", "Esin", "Fikret", "Yusuf", "Şeyma",
        "Burak Enes", "Dürnev", "İsmail", "Havva", "Eren", "Ayse"
    ],
    "DURUM": ["Hayır"]*36
}
df_hatim_23_mayis_2025_part1 = pd.DataFrame(hatim_data_23_mayis_2025_part1)

# Hatim Data PDF'den alınan üçüncü tabloya göre (30 Mayıs 2025) [cite: 3]
hatim_data_30_mayis_2025 = {
    "Yasin No": [3]*40,
    "Hatim Dönem": ["30 Mayıs 2025"]*40,
    "Cüz No": list(range(1, 41)),
    "Okuyan": [
        "Yunus Emre", "Tamer", "Sabahat", "Emine", "Hacer", "Fatih", "Özgür Yaşam", "Durali", "Esra", "Merve",
        "Serap", "Rümeysa", "Nursel", "Zekeriya", "Mustafa", "Unzile", "Hikmet", "Esra Gelin", "Ahmet", "Ayşegül",
        "Sevgi", "Talha", "Buşra", "Osman", "Zeynep", "Tuğba", "Esin", "Fikret", "Yusuf", "Şeyma",
        "Burak Enes", "Dürnev", "Ismail", "Havva", "Eren", "Ayşe", "Melih", "Yiğit", "Saniye", "Elfize"
    ],
    "DURUM": [
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır",
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır",
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır",
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır"
    ]
}
df_hatim_30_mayis_2025 = pd.DataFrame(hatim_data_30_mayis_2025)

# Hatim Data PDF'den alınan 2. kaynaktaki ilk tablo (Mayıs 2025) [cite: 2]
hatim_data_mayis_2025_cuz = {
    "Hatim No": [1]*30,
    "Hatim Dönem": ["Mayıs 2025"]*30,
    "Cüz No": list(range(1, 31)),
    "Okuyan": [
        "Emine", "Nursel", "Esra", "Merve", "Serap", "Büşra", "Hacer", "Durali", "Hulusi", "Hikmet",
        "Elfize", "Sevgi", "Osman", "Şerike", "Şeyma", "İsmail", "Zekeriya", "Rumeysa", "Ahmet", "Esin",
        "Mustafa", "Saniye", "Özgür Yaşam", "Elif", "Unzile", "Esra Gelin", "Gülnihal", "Yunus Emre", "Tamer", "Sabahat"
    ],
    "Durum": [
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır",
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır",
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır"
    ]
}
df_hatim_mayis_2025_cuz = pd.DataFrame(hatim_data_mayis_2025_cuz)

# Hatim Data PDF'den alınan 2. kaynaktaki ikinci tablo (Haziran 2025) [cite: 2]
hatim_data_haziran_2025_cuz = {
    "Hatim No": [2]*30,
    "Hatim Dönem": ["Haziran 2025"]*30,
    "Cüz No": list(range(1, 31)),
    "Okuyan": [
        "Sabahat", "Emine", "Nursel", "Esra", "Merve", "Serap", "Büşra", "Hacer", "Durali", "Hulusi",
        "Hikmet", "Elfize", "Sevgi", "Osman", "Şerike", "Şeyma", "Ismail", "Zekeriya", "Rumeysa", "Ahmet",
        "Esin", "Mustafa", "Saniye", "Özgür Yaşam", "Elif", "Ünzile", "Esra Gelin", "Gülnihal", "Yunus Emre", "Tamer"
    ],
    "Durum": [
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır",
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır",
        "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır", "Evet", "Hayır"
    ]
}
df_hatim_haziran_2025_cuz = pd.DataFrame(hatim_data_haziran_2025_cuz)

# Tüm hatim verilerini birleştirelim
df_all_hatim = pd.concat([
    df_hatim_16_mayis_2025,
    df_hatim_23_mayis_2025_part1,
    df_hatim_30_mayis_2025,
    df_hatim_mayis_2025_cuz.rename(columns={"Durum": "DURUM"}), # Sütun adını eşitle [cite: 2]
    df_hatim_haziran_2025_cuz.rename(columns={"Durum": "DURUM"}) # Sütun adını eşitle [cite: 2]
], ignore_index=True)


# UI tasarımına göre Hatim Yağmuru (Yasin Dönemi) bölümü [cite: 5]
st.title("🌧️ Hatim Yağmuru")
st.markdown("---")

st.subheader("Yasin Dönemleri")

# Dönemleri seçmek için selectbox
yasin_donemleri = df_all_hatim[df_all_hatim["Yasin No"].notna()]["Hatim Dönem"].unique()
selected_yasin_donem = st.selectbox("Yasin Dönemi Seçin:", yasin_donemleri)

if selected_yasin_donem:
    df_current_yasin = df_all_hatim[
        (df_all_hatim["Hatim Dönem"] == selected_yasin_donem) & 
        (df_all_hatim["Yasin No"].notna())
    ].copy()
    df_current_yasin.rename(columns={"DURUM": "Okunma Durumu"}, inplace=True)
    df_display_yasin = df_current_yasin[["Cüz No", "Okuyan", "Okunma Durumu"]]

    st.write(f"**Sayı:** {df_display_yasin.shape[0]} (Haftalık Okuma)")

    # Satır satır butonlu gösterim
    for idx, row in df_display_yasin.iterrows():
        col1, col2, col3 = st.columns([1, 3, 2])
        col1.write(row["Cüz No"])
        col2.write(row["Okuyan"])
        durum = row["Okunma Durumu"]
        btn_label = "Evet" if durum == "Evet" else "Hayır"
        btn_style = f"background-color: {'#22c55e' if durum == 'Evet' else '#fca5a5'}; color: white; border: none; padding: 0.5em 1em; border-radius: 5px; width:100%;"
        if col3.button(btn_label, key=f"yasin_{selected_yasin_donem}_{idx}", help="Durumu değiştir"):
            yeni_durum = "Hayır" if durum == "Evet" else "Evet"
            df_all_hatim.at[idx, "DURUM"] = yeni_durum
            st.rerun()
        else:
            col3.markdown(f"<div style='{btn_style};text-align:center'>{btn_label}</div>", unsafe_allow_html=True)

st.markdown("---")

# UI tasarımına göre Hatim Cüz Dönem (Aylık Okuma) bölümü [cite: 6]
st.subheader("Hatim Cüz Dönemleri")

cuz_donemleri = df_all_hatim[df_all_hatim["Hatim No"].notna()]["Hatim Dönem"].unique()
selected_cuz_donem = st.selectbox("Hatim Cüz Dönemi Seçin:", cuz_donemleri)

if selected_cuz_donem:
    df_current_cuz = df_all_hatim[
        (df_all_hatim["Hatim Dönem"] == selected_cuz_donem) & 
        (df_all_hatim["Hatim No"].notna())
    ].copy()
    df_current_cuz.rename(columns={"DURUM": "Okunma Durumu"}, inplace=True)
    df_display_cuz = df_current_cuz[["Cüz No", "Okuyan", "Okunma Durumu"]]

    st.write(f"**Sayı:** {df_display_cuz.shape[0]} (Aylık Okuma)")

    for idx, row in df_display_cuz.iterrows():
        col1, col2, col3 = st.columns([1, 3, 2])
        col1.write(row["Cüz No"])
        col2.write(row["Okuyan"])
        durum = row["Okunma Durumu"]
        btn_label = "Evet" if durum == "Evet" else "Hayır"
        btn_style = f"background-color: {'#22c55e' if durum == 'Evet' else '#fca5a5'}; color: white; border: none; padding: 0.5em 1em; border-radius: 5px; width:100%;"
        # Tek bir buton, rengi HTML ile
        if col3.button(btn_label, key=f"cuz_{selected_cuz_donem}_{idx}", help="Durumu değiştir"):
            yeni_durum = "Hayır" if durum == "Evet" else "Evet"
            df_all_hatim.at[idx, "DURUM"] = yeni_durum
            st.rerun()
        else:
            # Butonun yerine sadece renkli kutu göster
            col3.markdown(f"<div style='{btn_style};text-align:center'>{btn_label}</div>", unsafe_allow_html=True)