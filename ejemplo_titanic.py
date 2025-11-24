import pandas as pd
import plotly.express as px
import streamlit as st

# Título
st.header('Análisis de Vehículos')

# Leer archivo
# Como están en la misma carpeta de GitHub, solo ponemos el nombre
df = pd.read_csv('car_price_prediction_.csv')

# Botón 1
if st.button('Construir Histograma'):
    st.write('Mostrando distribución de kilometraje...')
    fig = px.histogram(df, x='Mileage')
    st.plotly_chart(fig, use_container_width=True)

# Botón 2
if st.button('Construir Gráfico de Dispersión'):
    st.write('Mostrando relación Precio vs. Kilometraje...')
    fig = px.scatter(df, x='Mileage', y='Price')
    st.plotly_chart(fig, use_container_width=True)
