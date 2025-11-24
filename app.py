import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Dashboard de Autos", layout="wide")

st.title('🏎️ Análisis de Mercado de Vehículos')
st.markdown("Esta aplicación permite explorar las tendencias en el mercado de venta de coches.")

# --- CARGA DE DATOS ---
try:
    df = pd.read_csv('car_price_prediction_.csv')
except FileNotFoundError:
    st.error("Error: No se encuentra el archivo 'car_price_prediction_.csv'.")
    st.stop()

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header('⚙️ Configuración')

# Filtro 1: Seleccionar Marcas
marcas_disponibles = df['Brand'].unique()
marcas_seleccionadas = st.sidebar.multiselect(
    'Selecciona las marcas a analizar:',
    marcas_disponibles,
    default=marcas_disponibles[:5] # Por defecto selecciona las 5 primeras
)

# Filtro 2: Rango de precios
precio_min = int(df['Price'].min())
precio_max = int(df['Price'].max())
rango_precio = st.sidebar.slider(
    'Rango de Precio ($)',
    precio_min, precio_max, (precio_min, precio_max)
)

# --- APLICAR FILTROS ---
# Filtramos la tabla base usando las selecciones del usuario
df_filtrado = df[
    (df['Brand'].isin(marcas_seleccionadas)) &
    (df['Price'] >= rango_precio[0]) &
    (df['Price'] <= rango_precio[1])
]

# Si no hay datos, mostrar aviso
if df_filtrado.empty:
    st.warning("No hay autos que coincidan con los filtros seleccionados.")
    st.stop()

# --- MOSTRAR DATOS CRUDOS (Opcional) ---
if st.checkbox('Mostrar tabla de datos filtrados'):
    st.dataframe(df_filtrado)

st.divider() # Línea separadora

# --- GRÁFICOS ---
col1, col2 = st.columns(2) # Dividimos la pantalla en 2 columnas

# GRÁFICO 1: Histograma de Precios
with col1:
    st.subheader("1. Distribución de Precios")
    st.write("¿Son caros o baratos la mayoría de los autos?")
    
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.hist(df_filtrado['Price'], bins=20, color='skyblue', edgecolor='black')
    ax1.set_xlabel('Precio')
    ax1.set_ylabel('Cantidad de Autos')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig1)

# GRÁFICO 2: Dispersión (Precio vs Kilometraje)
with col2:
    st.subheader("2. Precio vs. Kilometraje")
    st.write("¿A mayor kilometraje, menor precio?")
    
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.scatter(df_filtrado['Mileage'], df_filtrado['Price'], alpha=0.5, c='orange')
    ax2.set_xlabel('Kilometraje')
    ax2.set_ylabel('Precio')
    ax2.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig2)

st.divider()

# GRÁFICO 3: Precio Promedio por Marca
st.subheader("3. Comparación de Precios Promedio por Marca")
st.write("¿Qué marca es más cara en promedio según tu selección?")

# Calculamos el promedio agrupando por marca
promedio_marca = df_filtrado.groupby('Brand')['Price'].mean().sort_values()

fig3, ax3 = plt.subplots(figsize=(10, 5))
promedio_marca.plot(kind='barh', color='lightgreen', edgecolor='black', ax=ax3)
ax3.set_xlabel('Precio Promedio')
ax3.set_ylabel('Marca')
st.pyplot(fig3)
