import streamlit as st  
import pandas as pd
import plotly.express as px
import sqlite3

DB_PATH = "historic_temps.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

df = pd.read_sql("SELECT * FROM bogota;", conn)

df['Date'] = pd.to_datetime(df['Date'])

# Title
st.title('Bogota Weather Dashboard')
st.text("Comparing data from Sept 2009 to May 2026") 

# Color mapping
color_map = {'High': '#FF4B4B', 'Average': "#00FF80", 'Low': '#1C83E1'}

# Sidebar filter - this let the user choose a date to see the corresponding data
st.sidebar.header('Data Insights')
selected_types = st.sidebar.multiselect('Select the Insight to Visualize', df['Insight'].unique(), default=['Average'])

# Filter the data based on the user's selection
filtered_df = df[df['Insight'].isin(selected_types)]

# Visualization 1 - Temperature Trends
st.subheader('Temperature Trends')
fig_line = px.line(filtered_df, x='Date', y='Value', color='Insight', color_discrete_map=color_map, markers=True)
fig_line.update_layout(yaxis_title='Temperature (°F)')
st.plotly_chart(fig_line, use_container_width=True)

# Visualization 2 - Histogram
st.subheader("Distribution of Temperatures (Frequency)")
fig_hist = px.histogram(filtered_df, x='Value', color='Insight', nbins=20, color_discrete_map=color_map)
fig_hist.update_layout(xaxis_title='Temperature (°F)')
st.plotly_chart(fig_hist, use_container_width=True)

#Visualization 3 - Heatmap

df['Month'] = df['Date'].dt.month_name()
df['Year'] = df['Date'].dt.year

pivot_df = df.pivot_table(values='Value', index='Month', columns='Year', aggfunc='mean')

st.subheader("Temperature Seasonality Heatmap")
fig_heat = px.imshow(pivot_df, labels=dict(x="Year", y="Month", color="Temp (°F)"), color_continuous_scale="RdBu_r")
st.plotly_chart(fig_heat, use_container_width=True)

# Visualization 4 - Raw data
st.subheader('Raw Data Inspection')
st.dataframe(filtered_df)