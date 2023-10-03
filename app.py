import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page setting
st.set_page_config(page_title="Bike-Share Dashboard",
                   page_icon="🏍️",
                   layout="wide",
                   initial_sidebar_state="expanded")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Membuka dataset
np.random.seed(0)
df = pd.read_csv('all_data_v1.csv')

# Judul dashboard
html_temp = """ 
    <div style ="background-color:#bd0d21;padding:13px"> 
    <h1 style ="color:white;text-align:center;">Bike-Sharing Dashboard</h1> 
    </div> 
    """

# display the front end aspect
st.markdown(html_temp, unsafe_allow_html=True)
st.write("---")

# Menampilkan data
st.subheader('Data Bike-Sharing')
st.dataframe(df.head(5))

# Statistik sederhana
st.subheader('Ridership Statistics')
col1, col2, col3, col4 = st.columns(4)

def add_border(html_content):
    return f'<div style="border: 2px solid #fd0d24; padding: 10px; border-radius: 10px;">{html_content}</div>'

with col1:
    jumlah = df['count'].sum()
    st.markdown(add_border(f'<h4>Total Ridership</h4><p>{jumlah}</p>'), unsafe_allow_html=True)

with col2:
    rerata = round(df['count'].mean(), 2)
    st.markdown(add_border(f'<h4>Average Ridership</h4><p>{rerata}</p>'), unsafe_allow_html=True)

with col3:
    rmax = df['count'].max()
    st.markdown(add_border(f'<h4>Maximum Ridership</h4><p>{rmax}</p>'), unsafe_allow_html=True)

with col4:
    rmin = df['count'].min()
    st.markdown(add_border(f'<h4>Ridership Minimum</h4><p>{rmin}</p>'), unsafe_allow_html=True)

# Grafik Ridership
# Menampilkan grafik berdasarkan tahun yang dipilih oleh pengguna
st.subheader('Grafik Ridership by Year')

# Menambahkan pilihan tahun ke dalam sidebar
years = df['year'].unique()
selected_year = st.selectbox('Select Years', years)

# Filter data berdasarkan tahun yang dipilih
filtered_df_year = df[df['year'] == selected_year]

# Menampilkan grafik
st.bar_chart(filtered_df_year.set_index('month')['count'])

# Histogram Ridership
st.subheader('Grafik Ridership Seasonal')
st.write("Grafik Best and Worst Performing Distribution by Season")
df_max = df.groupby(by="season").agg({
    "count": "sum"
}).sort_values(by="count", ascending=False).reset_index()

df_min = df.groupby(by="season").agg({
    "count": "sum"
}).sort_values(by="count", ascending=True).reset_index()

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
fig,ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
# st.bar_chart(df.set_index('season')['count'])
sns.barplot(data=df_max[['season',
                    'count']],
              x='season',
              y='count',
              palette=colors,
              ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Season", fontsize=30)
ax[0].set_title("Best Performing Distribution", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(data=df_min[['season',
                    'count']],
              x='season',
              y='count',
              palette=colors,
              ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Season", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Distribution", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Tabel Ridership harian
st.subheader('Daily Ridership Table')
st.dataframe(df.head(5))

# Menampilkan data yang dipilih oleh pengguna
st.sidebar.header('Settings')
months = df['month'].unique()
weekdays = df['week_day'].unique()
season = df['season'].unique()
selected_month = st.sidebar.selectbox('Select Month', months)
selected_weekdays = st.sidebar.selectbox('Select Day', weekdays)
selected_season = st.sidebar.selectbox('Select Season', season)

filtered_df = df[(df['month'] == selected_month) & (df['week_day'] == selected_weekdays) & (df['season'] == selected_season)]
st.write(f'Ridership Data for the month {selected_month} day {selected_weekdays} in season {selected_season}')
st.dataframe(filtered_df.head(5))

# Menampilkan grafik berdasarkan bulan yang dipilih oleh pengguna
st.subheader('Grafik Ridership by Months')

# Filter data berdasarkan tahun yang dipilih
filtered_df = df[df['month'] == selected_month]
st.write(f'Ridership chart for the month {selected_month}')
# Menampilkan grafik
st.bar_chart(filtered_df.set_index('week_day')['count'])


st.caption('Copyright © Arif Munandar 2023')
