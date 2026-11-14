import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Page Configuration
st.set_page_config(
    page_title="EcoOrbit | NASA Space Apps",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #00F5D4;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #A0AAB2;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Language Selector in Sidebar
st.sidebar.header("🌐 Language / Idioma / Langue")
lang = st.sidebar.selectbox("Select Language", ["English", "Español", "Français"])

# Language Dictionary
t = {
    "English": {
        "title": "⚡ EcoOrbit: AI Compute & LEO Orbital Sustainability Engine",
        "subtitle": "NASA Space Apps Challenge Submission — Offloading Terrestrial Data Centers to Low Earth Orbit",
        "params": "🎛️ Simulation Parameters",
        "offload_label": "Terrestrial Workload Offloaded to LEO (%)",
        "offload_help": "Percentage of datacenter workload redirected to solar-powered space satellites.",
        "shell_label": "LEO Shell Deployment",
        "shells": ["Low Shell (400-600 km)", "Mid Shell (600-900 km)", "High Shell (900-1200 km)"],
        "energy_label": "Replaced Earth Energy Source",
        "energy_opts": ["Coal Heavy Grid", "Global Average Grid", "Natural Gas Dominant"],
        "metric_co2": "CO₂ Emissions Avoided",
        "metric_water": "Cooling Water Saved",
        "metric_risk": "Kessler Risk Score",
        "metric_shell": "Active Shell",
        "tabs": ["📊 Impact Dashboard", "🌍 Interactive 3D Node Map", "📡 Live Satellite Tracker", "📜 NASA Strategy", "👩‍💻 About Creator"]
    },
    "Español": {
        "title": "⚡ EcoOrbit: Motor de Sostenibilidad Espacial y Cómputo LEO",
        "subtitle": "Proyecto para NASA Space Apps Challenge — Moviendo Centros de Datos Terrestres a la Órbita Baja Terrestre",
        "params": "🎛️ Parámetros de Simulación",
        "offload_label": "Carga de trabajo enviada al espacio (%)",
        "offload_help": "Porcentaje del procesamiento de datos redirigido a satélites solares en el espacio.",
        "shell_label": "Capa de Despliegue LEO",
        "shells": ["Capa Baja (400-600 km)", "Capa Media (600-900 km)", "Capa Alta (900-1200 km)"],
        "energy_label": "Fuente de energía reemplazada en la Tierra",
        "energy_opts": ["Red basada en Carbón", "Promedio Global de la Red", "Predominante Gas Natural"],
        "metric_co2": "Emisiones de CO₂ Evitadas",
        "metric_water": "Agua de Enfriamiento Ahorrada",
        "metric_risk": "Riesgo de Basura Espacial",
        "metric_shell": "Capa Activa",
        "tabs": ["📊 Panel de Impacto", "🌍 Mapa 3D Interactivo", "📡 Satélites en Directo", "📜 Estrategia NASA", "👩‍💻 Sobre la Creadora"]
    },
    "Français": {
        "title": "⚡ EcoOrbit: Moteur de Calcul Réseau & Durabilité LEO",
        "subtitle": "Projet NASA Space Apps Challenge — Déport des centres de données terrestres vers l'orbite basse",
        "params": "🎛️ Paramètres de Simulation",
        "offload_label": "Charge de travail transférée dans l'espace (%)",
        "offload_help": "Pourcentage de charge informatique redirigé vers des satellites solaires.",
        "shell_label": "Couche de Déploiement LEO",
        "shells": ["Basse Couche (400-600 km)", "Moyenne Couche (600-900 km)", "Haute Couche (900-1200 km)"],
        "energy_label": "Source d'énergie remplacée sur Terre",
        "energy_opts": ["Réseau charbonné", "Moyenne mondiale", "Dominante gaz naturel"],
        "metric_co2": "Émissions de CO₂ Évitées",
        "metric_water": "Eau de Refroidissement Économisée",
        "metric_risk": "Score de Risque Kessler",
        "metric_shell": "Couche Active",
        "tabs": ["📊 Tableau d'Impact", "🌍 Carte 3D Interactive", "📡 Satellites en Direct", "📜 Stratégie NASA", "👩‍💻 À Propos de la Créatrice"]
    }
}

curr = t[lang]

# Title Header
st.markdown(f'<div class="main-title">{curr["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">{curr["subtitle"]}</div>', unsafe_allow_html=True)

# 2. Sidebar Controls
st.sidebar.markdown("---")
st.sidebar.header(curr["params"])

offload_pct = st.sidebar.slider(
    curr["offload_label"],
    min_value=0,
    max_value=100,
    value=40,
    help=curr["offload_help"]
)

orbit_altitude = st.sidebar.selectbox(
    curr["shell_label"],
    curr["shells"],
    index=1
)

energy_source = st.sidebar.radio(
    curr["energy_label"],
    curr["energy_opts"]
)

# Impact Calculations
co2_saved = offload_pct * 425
water_saved = offload_pct * 18500
kessler_score = round(offload_pct * 0.05, 2)

# Top Metrics Row
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric(curr["metric_co2"], f"{co2_saved:,} Tons", f"+{offload_pct}%")
col2.metric(curr["metric_water"], f"{water_saved:,} L", f"+{round(offload_pct * 0.9)}%")
col3.metric(curr["metric_risk"], f"{kessler_score} / 10")
col4.metric(curr["metric_shell"], orbit_altitude.split("(")[0])

st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(curr["tabs"][:3])

with tab1:
    st.subheader("Compute Load Distribution")
    dist_df = pd.DataFrame({
        "Location": ["Terrestrial", "Orbital LEO"],
        "Percentage": [100 - offload_pct, offload_pct]
    })
    fig = px.pie(dist_df, values="Percentage", names="Location", hole=0.5, color_discrete_sequence=["#3A506B", "#00F5D4"])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Orbital Node Map")
    fig_globe = go.Figure(go.Scattergeo(
        lon=[-122.08, -0.12, 139.65],
        lat=[37.38, 51.50, 35.67],
        mode="markers",
        marker=dict(size=12, color="#00F5D4")
    ))
    fig_globe.update_geos(projection_type="orthographic", landcolor="#1A202C", oceancolor="#0B0F19", showland=True, showocean=True)
    fig_globe.update_layout(height=400, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_globe, use_container_width=True)

with tab3:
    st.subheader("Satellite Tracker")
    sat_df = pd.DataFrame({
        "Satellite": ["STARLINK-31042", "ISS (ZARYA)", "ONEWEB-0412"],
        "Altitude (km)": [548.2, 418.5, 1198.4],
        "Period (min)": [95.6, 92.9, 109.4]
    })
    st.dataframe(sat_df, use_container_width=True, hide_index=True)
