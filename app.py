import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Administración EMECU - Total", layout="wide")

# URL de tu Google Sheet (formato CSV)
SHEET_ID = "1r-U_9tbE4Q1OK0QllaM14yseq1T-eppb9cfrXo0lq3c"
URL_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60)
def cargar_datos():
    try:
        df = pd.read_csv(URL_CSV)
        # Limpiamos espacios para evitar errores invisibles
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return None

# Estilos de contraste para legibilidad universal
st.markdown("""
    <style>
    .main-title { color: #1E88E5; text-align: center; font-weight: bold; }
    [data-testid="stMetricValue"] { color: #1E88E5 !important; }
    /* Ajuste para que la tabla permita scroll horizontal cómodo */
    .stDataFrame { border: 1px solid #1E88E5; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📋 Registro Completo de la Comuna</h1>", unsafe_allow_html=True)

df = cargar_datos()

if df is not None:
    # --- FILTROS DE BÚSQUEDA ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Filtro por Cátedra (Usando "Catedra" sin tilde)
        catedras = ["Todas"] + sorted(df["Catedra"].unique().tolist())
        cat_f = st.selectbox("Filtrar por Cátedra:", catedras)
        
    with col2:
        busqueda = st.text_input("🔍 Buscar por cualquier campo (Nombre, Cédula, Profesión, etc.):")

    # --- LÓGICA DE FILTRADO ---
    df_filtrado = df.copy()
    
    if cat_f != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Catedra"] == cat_f]
        
    if busqueda:
        # Buscamos en todo el DataFrame convirtiendo todo a texto
        mask = df_filtrado.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        df_filtrado = df_filtrado[mask]

    # --- MÉTRICAS ---
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Registros Visibles", len(df_filtrado))
    m2.metric("Total General", len(df))
    m3.metric("Cátedras", len(df["Catedra"].unique()))

    # --- TABLA DE DATOS TOTAL ---
    st.subheader("Visualización de Datos Maestros")
    st.info("Desliza la barra inferior de la tabla para ver todas las columnas (Salud, Aptitudes, Medios, etc.)")
    
    # Al no pasarle una lista de columnas, Streamlit mostrará las 33 columnas automáticamente
    st.dataframe(df_filtrado, use_container_width=True)

    # --- EXPORTACIÓN ---
    st.markdown("---")
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Base de Datos Completa (CSV)",
        data=csv,
        file_name='censo_emecu_completo.csv',
        mime='text/csv',
    )
else:
    st.error("No se pudo conectar con la base de datos de Google Sheets.")
