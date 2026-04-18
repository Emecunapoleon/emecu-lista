import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Lista Administrativa EMECU", layout="wide")

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

# Estilos para asegurar legibilidad en celular (Fondo Blanco) y PC (Fondo Oscuro)
st.markdown("""
    <style>
    .main-title {
        color: #1E88E5;
        text-align: center;
        font-weight: bold;
    }
    /* Estilo para que las métricas se vean bien en cualquier fondo */
    [data-testid="stMetricValue"] {
        color: #1E88E5 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📋 Registro Administrativo EMECU</h1>", unsafe_allow_html=True)

df = cargar_datos()

if df is not None:
    # --- FILTROS ---
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # CORRECCIÓN: "Catedra" sin tilde para coincidir con el Excel
        catedras = ["Todas"] + sorted(df["Catedra"].unique().tolist())
        cat_f = st.selectbox("Filtrar por Cátedra:", catedras)
    
    with col2:
        ciudades = ["Todas"] + sorted(df["Ciudad"].unique().tolist())
        ciu_f = st.selectbox("Filtrar por Ciudad:", ciudades)
        
    with col3:
        busqueda = st.text_input("🔍 Buscar Nombre o Cédula:")

    # --- LÓGICA DE FILTRADO ---
    df_filtrado = df.copy()
    
    if cat_f != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Catedra"] == cat_f]
    
    if ciu_f != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Ciudad"] == ciu_f]
        
    if busqueda:
        df_filtrado = df_filtrado[
            df_filtrado["Primer_Nombre"].str.contains(busqueda, case=False, na=False) | 
            df_filtrado["Cedula_Identidad"].astype(str).str.contains(busqueda, na=False)
        ]

    # --- INDICADORES ---
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total en Lista", len(df_filtrado))
    m2.metric("Cátedras Activas", len(df["Catedra"].unique()))
    m3.metric("Ciudades", len(df["Ciudad"].unique()))

    # --- TABLA DE DATOS ---
    # Mostramos las columnas más importantes primero
    columnas_visibles = [
        "Catedra", "Cedula_Identidad", "Primer_Nombre", "Primer_Apellido", 
        "Celular", "Ciudad", "Ocupacion_Actual"
    ]
    
    # Verificamos que las columnas existan antes de mostrar
    cols_finales = [c for c in columnas_visibles if c in df_filtrado.columns]
    
    st.dataframe(df_filtrado[cols_finales], use_container_width=True)

    # Botón para descargar los datos filtrados
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Lista Filtrada (CSV)",
        data=csv,
        file_name='lista_emecu_filtrada.csv',
        mime='text/csv',
    )
else:
    st.error("No se pudo cargar la base de datos. Verifica la conexión con Google Sheets.")
