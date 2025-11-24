import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Título
st.header('Análisis de Vehículos (con Matplotlib)')

# Leer archivo
try:
    # Asegúrate de que el nombre coincida EXACTAMENTE con tu archivo en GitHub
    df = pd.read_csv('car_price_prediction_.csv')

    # Botón 1: Histograma
    if st.button('Construir Histograma'):
        st.write('Mostrando distribución de kilometraje...')
        
        # 1. Crear el espacio para el gráfico
        fig, ax = plt.subplots()
        
        # 2. Dibujar el histograma
        ax.hist(df['Mileage'], bins=20, color='skyblue', edgecolor='black')
        
        # 3. Poner títulos y etiquetas
        ax.set_title('Distribución del Kilometraje')
        ax.set_xlabel('Kilometraje')
        ax.set_ylabel('Cantidad de Autos')
        
        # 4. Mostrar el gráfico en Streamlit
        st.pyplot(fig)

    # Botón 2: Dispersión
    if st.button('Construir Gráfico de Dispersión'):
        st.write('Mostrando relación Precio vs. Kilometraje...')
        
        # 1. Crear el espacio para el gráfico
        fig, ax = plt.subplots()
        
        # 2. Dibujar los puntos (scatter)
        ax.scatter(df['Mileage'], df['Price'], alpha=0.5, color='orange')
        
        # 3. Poner títulos y etiquetas
        ax.set_title('Precio vs. Kilometraje')
        ax.set_xlabel('Kilometraje')
        ax.set_ylabel('Precio')
        
        # 4. Mostrar el gráfico en Streamlit
        st.pyplot(fig)

except FileNotFoundError:
    st.error("Error: No encuentro el archivo 'car_price_prediction_.csv'. Revisa el nombre en GitHub.")
