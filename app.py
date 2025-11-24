import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# --- 1. CONFIGURACIÓN VISUAL (LO PRIMERO) ---
st.set_page_config(
    page_title="Dashboard Pro de Autos",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed" # La barra lateral empieza cerrada para más limpieza
)

# Estilo "Darkgrid" de Seaborn para gráficos más profesionales
sns.set_theme(style="darkgrid")
# Paleta de colores personalizada
colores_pro = sns.color_palette("rocket", as_cmap=False)

# --- 2. CARGA Y LIMPIEZA ---
@st.cache_data # Esto hace que la app no recargue los datos cada vez que tocas un botón (¡Más rápido!)
def cargar_datos():
    try:
        df = pd.read_csv('car_price_prediction_.csv')
        # Traducción
        df.rename(columns={
            'Brand': 'Marca',
            'Year': 'Año',
            'Engine Size': 'Motor (L)',
            'Fuel Type': 'Combustible',
            'Transmission': 'Transmisión',
            'Mileage': 'Kilometraje',
            'Condition': 'Condición',
            'Price': 'Precio',
            'Model': 'Modelo'
        }, inplace=True)
        return df
    except FileNotFoundError:
        return None

df = cargar_datos()

if df is None:
    st.error("⚠️ Error: Sube el archivo 'car_price_prediction_.csv' a GitHub.")
    st.stop()

# --- 3. BARRA LATERAL (INTERACTIVIDAD TOTAL) ---
with st.sidebar:
    st.header("🎛️ Panel de Control")
    st.write("Filtra los datos del tablero:")
    
    # Filtro 1: Marcas
    todas_marcas = sorted(df['Marca'].unique())
    sel_marcas = st.multiselect("Marca(s):", todas_marcas, default=todas_marcas[:3])
    
    # Filtro 2: Transmisión (Nuevo)
    transmisiones = df['Transmisión'].unique()
    sel_transmision = st.multiselect("Transmisión:", transmisiones, default=transmisiones)
    
    # Filtro 3: Combustible (Nuevo)
    combustibles = df['Combustible'].unique()
    sel_combustible = st.multiselect("Combustible:", combustibles, default=combustibles)
    
    # Filtro 4: Años
    sel_anio = st.slider("Rango de Años:", int(df['Año'].min()), int(df['Año'].max()), (2010, 2023))

    st.info("💡 Consejo: Si quitas todas las marcas, se seleccionarán todas automáticamente.")

# Lógica: Si el usuario borra todas las marcas, seleccionamos todas para que no de error
if not sel_marcas:
    sel_marcas = todas_marcas
if not sel_transmision:
    sel_transmision = transmisiones
if not sel_combustible:
    sel_combustible = combustibles

# Filtrado de datos
df_filtrado = df[
    (df['Marca'].isin(sel_marcas)) &
    (df['Transmisión'].isin(sel_transmision)) &
    (df['Combustible'].isin(sel_combustible)) &
    (df['Año'].between(sel_anio[0], sel_anio[1]))
]

# --- 4. CUERPO PRINCIPAL ---
st.title("🏎️ Análisis de Mercado Automotriz")
st.markdown(f"Analizando **{len(df_filtrado)}** vehículos filtrados.")

# KPIs con estilo
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Precio Promedio", f"${df_filtrado['Precio'].mean():,.0f}")
col2.metric("🚗 Kilometraje Promedio", f"{df_filtrado['Kilometraje'].mean():,.0f} km")
col3.metric("📅 Año Promedio", int(df_filtrado['Año'].mean()))
col4.metric("⛽ Motor Promedio", f"{df_filtrado['Motor (L)'].mean():.1f} L")

st.markdown("---")

# --- 5. PESTAÑAS ORGANIZADAS ---
tab1, tab2, tab3 = st.tabs(["📊 Visión General", "⏳ Tendencias y Tiempo", "🔬 Comparativa Avanzada"])

# === PESTAÑA 1: VISIÓN GENERAL ===
with tab1:
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Distribución de Precios (Histograma)")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df_filtrado['Precio'], kde=True, color="#4c72b0", alpha=0.6, ax=ax)
        ax.set_title("¿Cómo se concentran los precios?")
        ax.set_xlabel("Precio ($)")
        st.pyplot(fig)
        
        with st.expander("ℹ️ ¿Qué significa esto?"):
            st.write("La curva muestra dónde están la mayoría de los autos. Si la curva es alta a la izquierda, hay más autos baratos.")

    with c2:
        st.subheader("Conteo por Transmisión")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(data=df_filtrado, x='Transmisión', palette="viridis", ax=ax)
        ax.set_title("Manual vs. Automático")
        ax.set_ylabel("Cantidad de Autos")
        st.pyplot(fig)

# === PESTAÑA 2: TENDENCIAS (NUEVO) ===
with tab2:
    st.subheader("📈 Evolución del Precio en el Tiempo")
    st.write("Este gráfico muestra cómo ha cambiado el precio promedio según el año del modelo.")
    
    # Agrupamos por Año para ver el promedio
    precio_por_anio = df_filtrado.groupby('Año')['Precio'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=precio_por_anio, x='Año', y='Precio', marker='o', linewidth=2.5, color="coral", ax=ax)
    ax.set_title("Tendencia de Precio por Año de Fabricación")
    ax.set_ylabel("Precio Promedio ($)")
    st.pyplot(fig)

    st.divider()
    
    st.subheader("Relación Año vs. Kilometraje")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=df_filtrado, x='Año', y='Kilometraje', hue='Condición', alpha=0.6, palette="deep", ax=ax)
    ax.set_title("¿Los autos más viejos tienen siempre más kilometraje?")
    st.pyplot(fig)

# === PESTAÑA 3: COMPARATIVA AVANZADA ===
with tab3:
    col_izq, col_der = st.columns([2, 1])
    
    with col_izq:
        st.subheader("Comparación de Precios por Marca (Gráfico de Violín)")
        st.write("El ancho del 'violín' indica dónde hay más autos en ese rango de precio.")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # El gráfico de Violín es la versión "pro" del boxplot
        sns.violinplot(data=df_filtrado, x='Marca', y='Precio', palette="coolwarm", inner="quartile", ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)

    with col_der:
        st.subheader("Correlación (Heatmap)")
        # Solo columnas numéricas
        corr = df_filtrado.select_dtypes(include=['number']).corr()
        fig, ax = plt.subplots(figsize=(6, 8))
        sns.heatmap(corr[['Precio']].sort_values(by='Precio', ascending=False), annot=True, cmap='RdBu_r', vmin=-1, vmax=1, ax=ax)
        ax.set_title("¿Qué influye más en el Precio?")
        st.pyplot(fig)

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown("**Consejo Pro:** Usa la flecha ↖️ arriba a la izquierda para abrir/cerrar los filtros y ver los gráficos en pantalla completa.")
