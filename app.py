import streamlit as st
import pandas as pd

st.set_page_config(page_title="Listado Oficial EMECU", layout="wide")

SHEET_ID = "1r-U_9tbE4Q1OK0QllaM14yseq1T-eppb9cfrXo0lq3c"
URL_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=300)
def cargar_datos():
    return pd.read_csv(URL_CSV)

df = cargar_datos()

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Gestión de Datos")
    st.image("https://i.postimg.cc/NfBWMzGC/Gran14-Napoleon-blanco.png", width=80)
    
    st.metric("Registros Totales", len(df))
    
    st.subheader("Buscador")
    termino = st.text_input("Nombre, Cédula o Ciudad:")
    
    st.subheader("Filtros")
    cat_f = st.selectbox("Cátedra:", ["Todas"] + list(df["Cátedra"].unique()))

# --- PROCESAMIENTO ---
df_final = df.copy()
if termino:
    df_final = df_final[df_final.apply(lambda row: row.astype(str).str.contains(termino, case=False).any(), axis=1)]
if cat_f != "Todas":
    df_final = df_final[df_final["Cátedra"] == cat_f]

# --- VISTA PRINCIPAL ---
st.title("📋 Base de Datos de Integrantes EMECU Táchira")
st.markdown("### Información Completa del Registro")

st.dataframe(df_final, use_container_width=True, height=600)

# Opción de descarga
csv = df_final.to_csv(index=False).encode('utf-8')
st.download_button("Descargar Tabla en Excel (CSV)", data=csv, file_name="censo_emecu_completo.csv", mime="text/csv")
