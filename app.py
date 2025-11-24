import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Venta de Coches", layout="wide")

# Título principal y descripción
st.title('🏎️ Dashboard de Venta de Coches')
st.markdown("""
Esta aplicación permite visualizar y analizar datos de venta de coches.
Utiliza los filtros a la izquierda para interactuar con los datos.
""")

# --- CARGAR DATOS ---
try:
    # Leemos el archivo CSV
    df = pd.read_csv('car_price_prediction_.csv')
    
    # --- BARRA LATERAL (SIDEBAR) PARA FILTROS ---
    st.sidebar.header("Filtros de Búsqueda")
    
    # 1. Filtro por Marca
    marcas_disponibles = df['Brand'].unique()
    marcas_seleccionadas = st.sidebar.multiselect(
        "Selecciona la(s) Marca(s):",
        options=marcas_disponibles,
        default=marcas_disponibles # Por defecto selecciona todas
    )
    
    # 2. Filt
