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

    # 'DURUM' sütununu 'Okunma Durumu' olarak yeniden adlandır
    df_current_yasin.rename(columns={"DURUM": "Okunma Durumu"}, inplace=True)

    # İlgili sütunları seç ve düzenle
    df_display_yasin = df_current_yasin[["Cüz No", "Okuyan", "Okunma Durumu"]]

    # Okunan ve okunmayan cüz sayılarını hesapla
    okunan_yasin_cuz = df_display_yasin[df_display_yasin["Okunma Durumu"] == "Evet"].shape[0]
    okunmayan_yasin_cuz = df_display_yasin[df_display_yasin["Okunma Durumu"] == "Hayır"].shape[0]
    total_yasin_cuz = df_display_yasin.shape[0]

    st.write(f"**Sayı:** {total_yasin_cuz} (Haftalık Okuma)")
    st.write(f"Okunan Cüz Sayısı: {okunan_yasin_cuz}")
    st.write(f"Okunmayan Cüz Sayısı: {okunmayan_yasin_cuz}")

    # Tabloyu iki sütuna ayırarak gösterme
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{selected_yasin_donem} Okunan Cüzler")
        st.dataframe(df_display_yasin[df_display_yasin["Okunma Durumu"] == "Evet"].reset_index(drop=True))

    with col2:
        st.subheader(f"{selected_yasin_donem} Okunmayan Cüzler")
        st.dataframe(df_display_yasin[df_display_yasin["Okunma Durumu"] == "Hayır"].reset_index(drop=True))

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

    # 'DURUM' sütununu 'Okunma Durumu' olarak yeniden adlandır
    df_current_cuz.rename(columns={"DURUM": "Okunma Durumu"}, inplace=True)

    # İlgili sütunları seç ve düzenle
    df_display_cuz = df_current_cuz[["Cüz No", "Okuyan", "Okunma Durumu"]]

    # Okunan ve okunmayan cüz sayılarını hesapla
    okunan_cuz = df_display_cuz[df_display_cuz["Okunma Durumu"] == "Evet"].shape[0]
    okunmayan_cuz = df_display_cuz[df_display_cuz["Okunma Durumu"] == "Hayır"].shape[0]
    total_cuz = df_display_cuz.shape[0]

    st.write(f"**Sayı:** {total_cuz} (Aylık Okuma)")
    st.write(f"Okunan Cüz Sayısı: {okunan_cuz}")
    st.write(f"Okunmayan Cüz Sayısı: {okunmayan_cuz}")

    # Tabloyu iki sütuna ayırarak gösterme
    col3, col4 = st.columns(2)

    with col3:
        st.subheader(f"{selected_cuz_donem} Okunan Cüzler")
        st.dataframe(df_display_cuz[df_display_cuz["Okunma Durumu"] == "Evet"].reset_index(drop=True))

    with col4:
        st.subheader(f"{selected_cuz_donem} Okunmayan Cüzler")
        st.dataframe(df_display_cuz[df_display_cuz["Okunma Durumu"] == "Hayır"].reset_index(drop=True))