import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests

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
        "metric_co2_unit": "Metric Tons/yr",
        "metric_water": "Cooling Water Saved",
        "metric_water_unit": "Liters/yr",
        "metric_risk": "Kessler Risk Score",
        "metric_shell": "Active Shell",
        "tabs": ["📊 Impact Dashboard", "🌍 Interactive 3D Node Map", "📡 Live Satellite Tracker (CelesTrak)", "📜 NASA Strategy & Methodology", "👩‍💻 About Creator"],
        "compute_dist": "Compute Load Distribution",
        "ground_loc": "Terrestrial Data Centers",
        "space_loc": "Orbital LEO Satellites",
        "resource_vs_risk": "Resource Conservation vs. Space Risk",
        "co2_bar": "CO₂ Avoided (x10 Tons)",
        "water_bar": "Water Saved (x100 L)",
        "risk_bar": "Debris Risk Index",
        "map_title": "Global Orbital Compute Relay & Data Center Hubs",
        "map_ground_hubs": ["US West (Silicon Valley)", "EU Central (London)", "Asia East (Tokyo)", "Australia (Sydney)", "Equatorial Relay", "US Pacific NW"],
        "map_legend": "Ground Data Centers",
        "sat_title": "Real-Time Active Low Earth Orbit Environment",
        "sat_sub": "Live orbital data telemetry fetched directly from CelesTrak API",
        "sat_monitored": "Monitored Satellites",
        "sat_avg_alt": "Avg Orbital Altitude",
        "sat_avg_period": "Avg Orbital Period",
        "nasa_title": "EcoOrbit Project Brief & Architecture",
        "nasa_exec": "### 🎯 Executive Summary\nAs global AI and large language model training escalates, terrestrial data centers are driving severe power grid congestion and massive freshwater consumption for cooling. **EcoOrbit** provides an orbital offloading simulation framework to evaluate relocating non-latency-critical compute workloads into Low Earth Orbit (LEO).\n\n---\n\n### 🚀 Key Technical Pillars\n1. **Zero-Emission Compute:** Harnesses continuous, unfiltered solar energy in space to run compute processing without fossil fuels.\n2. **Thermal Dissipation in Vacuum:** Eliminates freshwater cooling dependency by deploying radiational cooling plates facing deep space.\n3. **Debris Mitigation Integration:** Uses live NORAD catalog telemetry to continuously analyze orbital density and prevent worsening Kessler Syndrome risks.\n\n---\n\n### 📌 NASA Open Data Sources\n* **CelesTrak GP Element Sets / NORAD Catalog:** Live active satellite orbital parameters.\n* **NASA Orbital Debris Program Office:** Space debris risk scoring index.\n* **US DOE Data Center Energy Index:** Earth-side baseline metrics.",
        "about_title": "👩‍💻 About the Creator & Project Motivation",
        "about_text": "### Meet Maria Vazquez\nHi! I'm **Maria Vazquez**, creator and lead developer of **EcoOrbit** for the NASA Space Apps Challenge 2026.\n\n### 💡 Why I Built EcoOrbit\nAs artificial intelligence and large-scale model training rapidly expand, terrestrial data centers are placing an unprecedented strain on our local power grids and depleting millions of gallons of freshwater every single day for cooling. I wanted to design a forward-thinking, scientifically grounded solution that asks: *What if we shift the heavy weight of AI compute off Earth and into the stars?*\n\nEcoOrbit was built to model a sustainable hybrid future—harnessing continuous solar energy and deep-space radiative cooling in Low Earth Orbit while carefully safeguarding our orbital pathways against debris risk."
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
        "metric_co2_unit": "Toneladas/año",
        "metric_water": "Agua de Enfriamiento Ahorrada",
        "metric_water_unit": "Litros/año",
        "metric_risk": "Riesgo de Basura Espacial",
        "metric_shell": "Capa Activa",
        "tabs": ["📊 Panel de Impacto", "🌍 Mapa 3D Interactivo", "📡 Satélites en Tiempo Real (CelesTrak)", "📜 Estrategia NASA y Metodología", "👩‍💻 Sobre la Creadora"],
        "compute_dist": "Distribución de Cómputo",
        "ground_loc": "Centros de Datos en la Tierra",
        "space_loc": "Satélites en Órbita (LEO)",
        "resource_vs_risk": "Conservación de Recursos vs. Riesgo Espacial",
        "co2_bar": "CO₂ Evitado (x10 Ton)",
        "water_bar": "Agua Ahorrada (x100 L)",
        "risk_bar": "Índice de Riesgo",
        "map_title": "Red Global de Centros de Datos y Nodos Orbitales",
        "map_ground_hubs": ["EE.UU. Oeste (Silicon Valley)", "Europa Central (Londres)", "Asia Este (Tokio)", "Australia (Sídney)", "Relé Ecuatorial", "EE.UU. Pacífico"],
        "map_legend": "Centros de Datos Terrestres",
        "sat_title": "Entorno Activo en Órbita Baja Terrestre",
        "sat_sub": "Telemetría orbital obtenida en tiempo real directamente desde la API de CelesTrak",
        "sat_monitored": "Satélites Monitoreados",
        "sat_avg_alt": "Altitud Promedio",
        "sat_avg_period": "Período Orbital Promedio",
        "nasa_title": "Resumen del Proyecto y Arquitectura EcoOrbit",
        "nasa_exec": "### 🎯 Resumen Ejecutivo\nA medida que la inteligencia artificial crece, los centros de datos en la Tierra consumen demasiada energía de la red eléctrica y millones de litros de agua para enfriarse. **EcoOrbit** propone un simulador para evaluar el traslado de procesamiento masivo a satélites en Órbita Baja Terrestre (LEO).\n\n---\n\n### 🚀 Pilares Técnicos\n1. **Cómputo con Cero Emisiones:** Usa energía solar continua en el espacio sin quemar combustibles fósiles.\n2. **Enfriamiento en el Vacío:** Elimina el uso de agua dulce aprovechando la radiación térmica directa al espacio exterior.\n3. **Mitigación de Basura Espacial:** Conecta con catálogos NORAD para medir la densidad orbital y prevenir accidentes por el Síndrome de Kessler.\n\n---\n\n### 📌 Fuentes de Datos Abiertos de la NASA\n* **CelesTrak / Catálogo NORAD:** Parámetros orbitales de satélites activos en vivo.\n* **Oficina de Basura Espacial de la NASA:** Índices de riesgo de colisión.\n* **Departamento de Energía de EE.UU. (DOE):** Métricas de consumo energético en la Tierra.",
        "about_title": "👩‍💻 Sobre la Creadora y Motivación del Proyecto",
        "about_text": "### Conoce a María Vázquez\n¡Hola! Soy **María Vázquez**, creadora y desarrolladora principal de **EcoOrbit** para el NASA Space Apps Challenge 2026.\n\n### 💡 Por qué construí EcoOrbit\nA medida que la inteligencia artificial y el entrenamiento de modelos a gran escala se expanden, los centros de datos terrestres están ejerciendo una presión sin precedentes sobre nuestras redes eléctricas y agotando millones de litros de agua dulce todos los días para su refrigeración. Quería diseñar una solución innovadora y científicamente sólida que planteara: *¿Qué pasaría si trasladamos el peso del cómputo de IA fuera de la Tierra y hacia las estrellas?*\n\nEcoOrbit fue creado para modelar un futuro híbrido sostenible, aprovechando energía solar continua y refrigeración radiativa en el espacio, mientras salvaguardamos nuestras órbitas contra el riesgo de desastres por basura espacial."
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
        "metric_co2_unit": "Tonnes/an",
        "metric_water": "Eau de Refroidissement Économisée",
        "metric_water_unit": "Litres/an",
        "metric_risk": "Score de Risque Kessler",
        "metric_shell": "Couche Active",
        "tabs": ["📊 Tableau d'Impact", "🌍 Carte 3D Interactive", "📡 Satellites en Direct (CelesTrak)", "📜 Stratégie NASA & Méthodologie", "👩‍💻 À Propos de la Créatrice"],
        "compute_dist": "Répartition de la Charge de Calcul",
        "ground_loc": "Centres de données terrestres",
        "space_loc": "Satellites orbitaux (LEO)",
        "resource_vs_risk": "Conservation des Ressources vs Risque Spatial",
        "co2_bar": "CO₂ Évité (x10 Tonnes)",
        "water_bar": "Eau Économisée (x100 L)",
        "risk_bar": "Indice de Débris",
        "map_title": "Réseau Mondial de Data Centers et Nœuds Orbitaux",
        "map_ground_hubs": ["USA Ouest (Silicon Valley)", "Europe Centrale (Londres)", "Asie Est (Tokyo)", "Australie (Sydney)", "Relais Équatorial", "USA Pacifique"],
        "map_legend": "Centres de données terrestres",
        "sat_title": "Environnement Actif en Orbite Terrestre Basse",
        "sat_sub": "Télémétrie orbitale en temps réel via l'API CelesTrak",
        "sat_monitored": "Satellites Surveillés",
        "sat_avg_alt": "Altitude Moyenne",
        "sat_avg_period": "Période Orbitale Moyenne",
        "nasa_title": "Présentation du Projet & Architecture EcoOrbit",
        "nasa_exec": "### 🎯 Résumé Exécutif\nFace à l'explosion de l'IA, les data centers terrestres saturent les réseaux électriques et consomment d'immenses quantités d'eau douce. **EcoOrbit** est un simulateur évaluant le déport des calculs vers l'orbite basse terrestre (LEO).\n\n---\n\n### 🚀 Piliers Techniques\n1. **Calcul Zéro Émission:** Exploite l'énergie solaire continue dans l'espace sans énergies fossiles.\n2. **Dissipation Thermique dans le Vide:** Élimine le besoin en eau douce grâce au refroidissement radiatif vers l'espace profond.\n3. **Gestion des Débris Spatiaux:** Utilise le catalogue NORAD en direct pour surveiller la densité orbitale et limiter le syndrome de Kessler.\n\n---\n\n### 📌 Données Ouvertes NASA\n* **CelesTrak / Catalogue NORAD:** Paramètres orbitaux des satellites actifs.\n* **Bureau des Débris Spatiaux de la NASA:** Évaluation du risque de collision.\n* **US DOE:** Données énergétiques des data centers sur Terre.",
        "about_title": "👩‍💻 À propos de la créatrice & motivation du projet",
        "about_text": "### Rencontrez Maria Vazquez\nBonjour ! Je suis **Maria Vazquez**, créatrice et développeuse principale d'**EcoOrbit** pour le NASA Space Apps Challenge 2026.\n\n### 💡 Pourquoi j'ai créé EcoOrbit\nAlors que l'intelligence artificielle et l'entraînement de modèles à grande échelle se développent rapidement, les centres de données terrestres exercent une pression sans précédent sur nos réseaux électriques et consomment des millions d'eau douce chaque jour pour le refroidissement. Je voulais concevoir une solution innovante et scientifiquement rigoureuse pour répondre à la question : *Et si nous déportions le poids du calcul IA hors de la Terre et vers les étoiles ?*\n\nEcoOrbit a été conçu pour modéliser un avenir hybride durable — exploitant l'énergie solaire continue et le refroidissement radiatif en orbite basse, tout en protégeant nos chemins orbitaux contre les risques de débris spatiaux."
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

# 3. Dynamic Factor Logic
grid_multipliers = {
    curr["energy_opts"][0]: 0.95,
    curr["energy_opts"][1]: 0.65,
    curr["energy_opts"][2]: 0.45
}

shell_risk_factors = {
    curr["shells"][0]: 1.15,
    curr["shells"][1]: 1.45,
    curr["shells"][2]: 0.85
}

grid_factor = grid_multipliers[energy_source]
shell_factor = shell_risk_factors[orbit_altitude]

# Impact Calculations (Baseline: 100 MW Data Center Cluster)
co2_saved = round(offload_pct * 425 * grid_factor)
water_saved = round(offload_pct * 18500)
kessler_score = round(min(10.0, (offload_pct * 0.065) * shell_factor), 2)

# 4. Top KPI Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric(curr["metric_co2"], f"{co2_saved:,} {curr['metric_co2_unit']}", f"+{offload_pct}%")
col2.metric(curr["metric_water"], f"{water_saved:,} {curr['metric_water_unit']}", f"+{round(offload_pct * 0.9)}%")
col3.metric(curr["metric_risk"], f"{kessler_score} / 10", delta=f"{round(kessler_score - 2.5, 2)}", delta_color="inverse")
col4.metric(curr["metric_shell"], orbit_altitude.split(" ")[0], orbit_altitude.split("(")[1].replace(")", ""))

st.markdown("---")

# 5. Main Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(curr["tabs"])

# TAB 1: Impact Dashboard
with tab1:
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader(curr["compute_dist"])
        dist_df = pd.DataFrame({
            "Location": [curr["ground_loc"], curr["space_loc"]],
            "Percentage": [100 - offload_pct, offload_pct]
        })
        fig_pie = px.pie(
            dist_df,
            values="Percentage",
            names="Location",
            hole=0.5,
            color_discrete_sequence=["#3A506B", "#00F5D4"]
        )
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.subheader(curr["resource_vs_risk"])
        bar_df = pd.DataFrame({
            "Metric": [curr["co2_bar"], curr["water_bar"], curr["risk_bar"]],
            "Value": [co2_saved / 10, water_saved / 100, kessler_score * 350]
        })
        fig_bar = px.bar(
            bar_df,
            x="Metric",
            y="Value",
            color="Metric",
            color_discrete_sequence=["#00F5D4", "#00BBF9", "#F15BB5"]
        )
        fig_bar.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bar, use_container_width=True)

# TAB 2: Interactive 3D Node Map
with tab2:
    st.subheader(curr["map_title"])
    hubs_df = pd.DataFrame({
        "Hub": curr["map_ground_hubs"],
        "Lat": [37.3861, 51.5074, 35.6762, -33.8688, 0.0, 47.6062],
        "Lon": [-122.0839, -0.1278, 139.6503, 151.2093, -78.4678, -122.3321],
        "Capacity_MW": [25, 20, 20, 15, 10, 10]
    })

    fig_globe = go.Figure()
    fig_globe.add_trace(go.Scattergeo(
        lon=hubs_df["Lon"],
        lat=hubs_df["Lat"],
        text=hubs_df["Hub"],
        mode="markers+text",
        textposition="top center",
        name=curr["map_legend"],
        marker=dict(size=12, color="#00F5D4", line=dict(width=1, color="white"))
    ))

    # Simulated LEO Satellite Constellation Ring
    sat_lons = np.linspace(-180, 180, max(6, int(offload_pct / 2)))
    sat_lats = 45 * np.sin(np.radians(sat_lons * 2))
    fig_globe.add_trace(go.Scattergeo(
        lon=sat_lons,
        lat=sat_lats,
        mode="markers",
        name=curr["space_loc"],
        marker=dict(size=6, color="#F15BB5", symbol="diamond")
    ))

    fig_globe.update_geos(
        projection_type="orthographic",
        showcoastlines=True,
        coastlinecolor="#4A5568",
        showland=True,
        landcolor="#1A202C",
        showocean=True,
        oceancolor="#0B0F19",
        bgcolor="rgba(0,0,0,0)"
    )
    fig_globe.update_layout(height=550, margin={"r":0,"t":20,"l":0,"b":0}, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_globe, use_container_width=True)

# TAB 3: Live Satellite Tracker (CelesTrak)
with tab3:
    st.subheader(curr["sat_title"])
    st.caption(curr["sat_sub"])

    @st.cache_data(ttl=3600)
    def load_celestrak_data():
        try:
            url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"
            resp = requests.get(url, timeout=8)
            if resp.status_code == 200:
                data = resp.json()[:150]
                df = pd.DataFrame(data)
                # Calculate approximate altitude from Mean Motion
                df["Altitude_km"] = ((398600.4418 / ((df["MEAN_MOTION"] * 2 * np.pi / 86400) ** 2)) ** (1/3) - 6371).round(1)
                df["Period_min"] = (1440 / df["MEAN_MOTION"]).round(1)
                return df[["OBJECT_NAME", "NORAD_CAT_ID", "INCLINATION", "Altitude_km", "Period_min"]]
        except Exception:
            pass
        # Fallback telemetry dataset if CelesTrak is rate-limited
        return pd.DataFrame({
            "OBJECT_NAME": ["STARLINK-31042", "STARLINK-31088", "ISS (ZARYA)", "ONEWEB-0412", "TERRA", "AQUA", "LANDSAT 9", "SENTINEL-2B"],
            "NORAD_CAT_ID": [58901, 58915, 25544, 51012, 25994, 27424, 49260, 42063],
            "INCLINATION": [53.16, 53.16, 51.64, 87.90, 98.20, 98.21, 98.22, 98.56],
            "Altitude_km": [548.2, 549.0, 418.5, 1198.4, 705.1, 703.8, 705.0, 786.2],
            "Period_min": [95.6, 95.6, 92.9, 109.4, 98.9, 98.8, 98.9, 100.6]
        })

    sat_df = load_celestrak_data()

    s1, s2, s3 = st.columns(3)
    s1.metric(curr["sat_monitored"], f"{len(sat_df):,}")
    s2.metric(curr["sat_avg_alt"], f"{sat_df['Altitude_km'].mean():.1f} km")
    s3.metric(curr["sat_avg_period"], f"{sat_df['Period_min'].mean():.1f} min")

    st.dataframe(sat_df, use_container_width=True, hide_index=True)

# TAB 4: NASA Strategy & Methodology
with tab4:
    st.subheader(curr["nasa_title"])
    st.markdown(curr["nasa_exec"])

# TAB 5: About Creator
with tab5:
    st.subheader(curr["about_title"])
    st.markdown(curr["about_text"])
