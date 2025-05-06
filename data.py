import pandas as pd
import streamlit as st
def load_data():
    df = pd.read_csv("datacuaca_long_lat.csv")
    return df
def filter_data(df, start_date=None, end_date=None, kota=None):
    if start_date and end_date:
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])  
        df = df[(df['Tanggal'] >= pd.to_datetime(start_date)) & (df['Tanggal'] <= pd.to_datetime(end_date))]
    if kota:  
        df = df[df["Kota"].isin(kota)]
    return df
def select_date_range(df):
    min_date = pd.to_datetime(df['Tanggal']).min()
    max_date = pd.to_datetime(df['Tanggal']).max()
    start_date = st.sidebar.date_input("Tanggal Mulai", min_date)
    end_date = st.sidebar.date_input("Tanggal Akhir", max_date)
    return start_date, end_date
def select_kota(df):
    kota_list = df['Kota'].unique().tolist()
    kota = st.sidebar.multiselect("Pilih Kota", kota_list, default=kota_list)  # Multiselect dengan default semua kota
    return kota
def suhu(df):
    Suhu = df['Suhu']
    return Suhu
def curah(df):
    Curah = df['Curah Hujan']
    return Curah
def kondisi(df):
    Kondisi = df['Kondisi Cuaca']
    return Kondisi
if __name__ == 'main':
    df = load_data()
    start_date, end_date = select_date_range(df)
    selected_kota = select_kota(df)
    filtered_df = filter_data(df, start_date, end_date, selected_kota)
    st.write("Data yang Difilter")
    st.dataframe(filtered_df)
    if not filtered_df.empty:
        st.write("Statistik Suhu")
        st.write(filtered_df['Suhu'].describe())
        st.write("Statistik Curah Hujan")
        st.write(filtered_df['Curah Hujan'].describe())
        st.write("Kondisi Cuaca")
        st.write(filtered_df['Kondisi Cuaca'].value_counts())
    else:
        st.info("Tidak ada data yang sesuai dengan filter yang dipilih.")