import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Administración EMECU - Táchira", layout="wide")

# URL de tu Google Sheet (formato CSV)
SHEET_ID = "1r-U_9tbE4Q1OK0QllaM14yseq1T-eppb9cfrXo0lq3c"
URL_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60)
def cargar_datos():
    try:
        df = pd.read_csv(URL_CSV)
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return None

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    /* Estilo para el logo dinámico (se invierte en modo claro) */
    @media (prefers-color-scheme: light) {
        .logo-img { filter: invert(1) brightness(0.2); }
    }
    .nombre-escuela {
        color: #1E88E5;
        text-align: center;
        font-size: 1.8rem !important;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .titulo-registro {
        color: #5d6d7e;
        text-align: center;
        font-size: 1.4rem !important;
        font-weight: 500;
        margin-top: 0px;
        margin-bottom: 30px;
    }
    [data-testid="stMetricValue"] { color: #1E88E5 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA (Logo y Títulos) ---
col_a, col_b, col_c = st.columns([1, 0.8, 1])
with col_b:
    # Logo centrado y no muy grande
    st.markdown(f'<div style="text-align: center;"><img src="https://i.postimg.cc/NfBWMzGC/Gran14-Napoleon-blanco.png" class="logo-img" style="width: 120px;"></div>', unsafe_allow_html=True)

st.markdown("<p class='nombre-escuela'>Escuela Magnético Espiritual de la Comuna Universal (EMECU)</p>", unsafe_allow_html=True)
st.markdown("<p class='titulo-registro'>Registro Completo de la Comuna del Estado Táchira</p>", unsafe_allow_html=True)

df = cargar_datos()

if df is not None:
    # --- SECCIÓN DE FILTROS ---
    with st.expander("🔍 Herramientas de Búsqueda y Filtros", expanded=True):
        f_col1, f_col2 = st.columns([1, 2])
        with f_col1:
            catedras = ["Todas"] + sorted(df["Catedra"].unique().tolist())
            cat_f = st.selectbox("Filtrar por Cátedra:", catedras)
        with f_col2:
            busqueda = st.text_input("Búsqueda Global (Cédula, nombre, oficio...):")

    # Lógica de filtrado
    df_filtrado = df.copy()
    if cat_f != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Catedra"] == cat_f]
    if busqueda:
        mask = df_filtrado.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        df_filtrado = df_filtrado[mask]

    # --- MÉTRICAS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Registros Filtrados", len(df_filtrado))
    m2.metric("Total General", len(df))
    m3.metric("Cátedras en Táchira", len(df["Catedra"].unique()))

    # --- VISUALIZACIÓN DE DATOS ---
    st.markdown("---")
    st.subheader("Base de Datos Maestra (Todas las columnas)")
    # Mostramos el DataFrame completo con scroll horizontal
    st.dataframe(df_filtrado, use_container_width=True)

    # Botón de descarga
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Base de Datos Actualizada (CSV)",
        data=csv,
        file_name='registro_completo_emecu_tachira.csv',
        mime='text/csv',
    )
else:
    st.error("No se pudo cargar la información desde el servidor.")
