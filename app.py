import streamlit as st
import plotly.express as px
import pandas as pd
from data import *  # Pastikan fungsi load_data(), select_date_range(), select_kota(), filter_data() tersedia

def judul():
    st.title("📊 DASHBOARD KONDISI CUACA DI PULAU JAWA")
    st.write("Selamat datang di dashboard interaktif untuk menganalisis data cuaca di Pulau Jawa!")

# Sidebar
st.sidebar.title("📁 Menu")
menu = st.sidebar.radio("Pilih Halaman", ['Home', 'Halaman Data'])

# Halaman Home
if menu == 'Home':
    judul()
    df = load_data()
    start_date, end_date = select_date_range(df)  # Pilih rentang tanggal
    kota = select_kota(df) 
    df_filtered = filter_data(df, start_date, end_date, kota)

    st.subheader("Kondisi Cuaca yang Paling Sering Muncul")
    if not df_filtered.empty:
        value_counts = df_filtered['Kondisi Cuaca'].value_counts()
        kondisi_terbanyak = value_counts.idxmax()
        jumlah_kemunculan = value_counts.max()
        st.write(f"Kondisi cuaca yang paling sering muncul adalah {kondisi_terbanyak} dengan jumlah kemunculan sebanyak {jumlah_kemunculan} kali.")

        # Opsional: tampilkan semua kondisi cuaca beserta jumlahnya
        with st.expander("Lihat semua kondisi cuaca dan jumlahnya"):
            st.dataframe(value_counts.reset_index().rename(columns={"index": "Kondisi Cuaca", "Kondisi Cuaca": "Jumlah"}))
    else:
        st.info("Tidak ada data yang sesuai dengan filter yang dipilih.")

    st.subheader("Grafik Rata-rata Suhu Per Bulan")
    if not df_filtered.empty:
        df_filtered['Bulan'] = pd.to_datetime(df_filtered['Tanggal']).dt.to_period('M').astype(str)
        avg_temp_per_month = df_filtered.groupby(['Bulan', 'Kota'])['Suhu'].mean().reset_index()
        fig_monthly_temp = px.line(
            avg_temp_per_month,
            x='Bulan',
            y='Suhu',
            color='Kota',
            title='Rata-rata Suhu Per Bulan',
            markers=True,
            color_discrete_map={
                "Bandung": "#636EFA",
                "Yogyakarta": "#EF553B",
                "Surabaya": "#00CC96",
                "Jakarta": "#AB63FA",
            }
        )
        fig_monthly_temp.update_layout(xaxis_title="Bulan", yaxis_title="Suhu Rata-rata (°C)")
        st.plotly_chart(fig_monthly_temp)
    else:
        st.info("Tidak ada data yang sesuai dengan filter yang dipilih.")

    st.subheader("Grafik Curah Hujan")
    if not df_filtered.empty:
        total_rainfall = df_filtered.groupby(['Tanggal', 'Kota'])['Curah Hujan'].sum().reset_index()
        fig_rainfall = px.bar(
            total_rainfall,
            x='Tanggal',
            y='Curah Hujan',
            color='Kota',
            title='Curah Hujan Harian',
            color_discrete_map={
                "Bandung": "#636EFA",
                "Yogyakarta": "#EF553B",
                "Surabaya": "#00CC96",
                "Jakarta": "#AB63FA",
            }
        )
        fig_rainfall.update_layout(xaxis_title="Tanggal", yaxis_title="Curah Hujan (mm)")
        st.plotly_chart(fig_rainfall)
    else:
        st.info("Tidak ada data yang sesuai dengan filter yang dipilih.")

    st.subheader("Peta Lokasi Kota dengan Data Cuaca")
    if not df_filtered.empty:
        if 'latitude' in df_filtered.columns and 'longitude' in df_filtered.columns:
            fig_map = px.scatter_mapbox(
                df_filtered,
                lat="latitude",
                lon="longitude",
                color="Kota",
                size="Suhu",  
                hover_name="Kota",
                hover_data={"Suhu": True, "Curah Hujan": True, "latitude": False, "longitude": False, "Kondisi Cuaca": True},
                title="Peta Lokasi Kota dengan Data Cuaca",
                color_discrete_map={
                    "Bandung": "#636EFA",
                    "Yogyakarta": "#EF553B",
                    "Surabaya": "#00CC96",
                    "Jakarta": "#AB63FA",
                },
                zoom=6,  
                height=500
            )
            fig_map.update_layout(mapbox_style="open-street-map")
            fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
            st.plotly_chart(fig_map)
        else:
            st.warning("Dataset tidak memiliki kolom Latitude dan Longitude.")
    else:
        st.info("Tidak ada data yang sesuai dengan filter yang dipilih.")

# Halaman Data
elif menu == 'Halaman Data':
    st.header("📄 Data Lengkap Cuaca")
    df = load_data()
    start_date, end_date = select_date_range(df)  
    kota = select_kota(df) 
    df_filtered = filter_data(df, start_date, end_date, kota) 
    st.dataframe(df_filtered)
    st.download_button(
        label="Unduh Data",
        data=df_filtered.to_csv(index=False).encode('utf-8'),
        file_name='data_cuaca_filtered.csv',
        mime='text/csv',
    )
    st.write("Data ini berisi informasi tentang suhu, curah hujan, dan kondisi cuaca di berbagai kota di Pulau Jawa.")