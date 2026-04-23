import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE MARCA JDE CARGO
st.set_page_config(page_title="JDE Cargo - Tracking", page_icon="🚢", layout="centered")

# Colores Corporativos: #1A1676 (Azul), #92C02A (Verde), #B0BEC5 (Gris)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #ffffff; }}
    h1, h2, h3 {{ color: #1A1676 !important; }}
    .stButton>button {{
        background-color: #92C02A;
        color: white;
        border-radius: 8px;
        border: none;
        width: 100%;
        font-weight: bold;
    }}
    [data-testid="stMetricValue"] {{ color: #1A1676; }}
    hr {{ border: 0; height: 1px; background: #B0BEC5; }}
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO (Logo y Título)
logo_path = "image_8.png" # Asegúrate de que el archivo se llame así en tu carpeta
if os.path.exists(logo_path):
    st.image(logo_path, width=220)
else:
    st.title("JDE CARGO")

st.subheader("Portal de Rastreo de Embarques")
st.write("Introduzca su número de referencia para conocer el estado de su carga.")
st.markdown("---")

# 3. CONEXIÓN A GOOGLE SHEETS
sheet_url = "https://docs.google.com/spreadsheets/d/1WPjbNJ90IBW6kZW6ifZpVhpXsUNiBdKcri6uE_sxFE8/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=10)
def load_data():
    try:
        data = pd.read_csv(sheet_url)
        data.columns = data.columns.str.strip().str.upper()
        return data
    except:
        return None

df = load_data()

# 4. BUSCADOR Y LÓGICA DE WHATSAPP
if df is not None:
    busqueda = st.text_input("Número de Proyecto / Referencia:", placeholder="Ej: TEST1")

    if busqueda:
        # Buscamos el proyecto
        resultado = df[df['PROYECTO'].astype(str).str.upper() == busqueda.strip().upper()]

        if not resultado.empty:
            st.success(f"✅ Registro encontrado")
            
            # Datos principales
            c1, c2 = st.markdown(f"""
                <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 20px; margin-bottom: 20px;">
                    <div style="flex: 1; min-width: 200px;">
                        <p style="color: #B0BEC5; font-size: 14px; margin-bottom: 5px; font-weight: bold;">ESTATUS ACTUAL</p>
                        <p style="color: #1A1676; font-size: 24px; font-weight: bold; line-height: 1.2;">{str(resultado['ESTATUS'].values[0])}</p>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <p style="color: #B0BEC5; font-size: 14px; margin-bottom: 5px; font-weight: bold;">FECHA ESTIMADA</p>
                        <p style="color: #1A1676; font-size: 24px; font-weight: bold;">{str(resultado['FECHA'].values[0])}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Botón visual de WhatsApp
            st.markdown(f"""
                <a href="{link_wa}" target="_blank" style="text-decoration: none;">
                    <div style="background-color:#92C02A; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:18px;">
                        💬 SOLICITAR AYUDA POR WHATSAPP
                    </div>
                </a>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Referencia no encontrada. Por favor, verifique el número.")
else:
    st.warning("Cargando base de datos...")

st.markdown("---")
st.caption("© 2026 JDE Cargo | Conectando el mundo con eficiencia.")
