# LIBRERÍAS

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
import base64
import requests
from io import BytesIO
import zipfile
from pathlib import Path
from streamlit_folium import st_folium
from modelos.solar import simular_solar
from modelos.financiero import calcular_finanzas

# -------------------------------------------------------------------------------------------------------------------------------------------------------------

# TÍTULO E ÍCONO

st.set_page_config(
    page_title="Explorador Solar",
    page_icon="☀️",
    layout="wide"
)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------

# DISEÑO INTERFAZ

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #102a43;
    --muted: #5f6f83;
    --sky: #eaf6ff;
    --sun: #fff1c7;
    --coral: #ffe4d6;
    --mint: #e6f8ef;
    --lavender: #eee9ff;
    --rose: #ffe7ef;
    --night: #0f2742;
    --yellow: #ffb703;
    --orange: #fb8500;
    --blue: #4361ee;
    --green: #2a9d8f;
}

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif !important;
}

.stApp {
    background: #f7f9fc !important;
    color: var(--ink) !important;
}

.block-container {
    max-width: 100% !important;
    padding-top: 0rem !important;
    padding-left: 2.8rem !important;
    padding-right: 2.8rem !important;
}

h1, h2, h3, h4, h5 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--ink) !important;
}

p, span, div, label {
    color: inherit;
}

.hero-container {
    position: relative;
    width: calc(100% + 5.6rem);
    margin-left: -2.8rem;
    height: 470px;
    overflow: hidden;
    margin-bottom: 2.4rem;
    border-bottom-left-radius: 44px;
    border-bottom-right-radius: 44px;
    box-shadow: 0 22px 55px rgba(15,40,75,0.18);
}

.hero-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(43%) saturate(118%);
}

.hero-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: 5.4rem;
    padding-right: 2rem;
    background: linear-gradient(90deg, rgba(15,39,66,0.72), rgba(15,39,66,0.23), rgba(15,39,66,0.08));
}

.hero-kicker {
    color: var(--yellow) !important;
    font-size: 0.9rem;
    font-weight: 900;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title-main {
    font-family: 'Space Grotesk', sans-serif !important;
    color: white !important;
    font-size: 5.4rem;
    font-weight: 800;
    line-height: 0.93;
    margin-top: 0.8rem;
    max-width: 820px;
    text-shadow: 0 10px 34px rgba(0,0,0,0.50);
}

.hero-subtitle-main {
    color: #eaf2ff !important;
    font-size: 1.18rem;
    max-width: 780px;
    line-height: 1.65;
    margin-top: 1.2rem;
}

.hero-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1.6rem;
    flex-wrap: wrap;
}

.hero-pill-main {
    background: var(--yellow);
    color: #102a43 !important;
    padding: 0.75rem 1.25rem;
    border-radius: 999px;
    font-weight: 900;
    width: fit-content;
    box-shadow: 0 12px 30px rgba(255,183,3,0.38);
}

.hero-pill-soft {
    background: rgba(255,255,255,0.18);
    color: white !important;
    padding: 0.75rem 1.25rem;
    border-radius: 999px;
    font-weight: 800;
    width: fit-content;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.28);
}

.section-card,
.hero-section {
    border-radius: 36px;
    padding: 2rem 2.1rem;
    margin: 1.6rem 0 1.15rem 0;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.72);
    box-shadow: 0 18px 45px rgba(15,40,75,0.10);
    background: var(--sky);
}

.hero-section:nth-of-type(3n), .section-card:nth-of-type(3n) { background: var(--sun); }
.hero-section:nth-of-type(3n+1), .section-card:nth-of-type(3n+1) { background: var(--coral); }
.hero-section:nth-of-type(3n+2), .section-card:nth-of-type(3n+2) { background: var(--mint); }

.hero-section::after,
.section-card::after {
    content: "";
    position: absolute;
    right: -50px;
    top: -55px;
    width: 170px;
    height: 170px;
    border-radius: 50%;
    background: rgba(255,255,255,0.42);
}

.hero-title,
.section-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2rem;
    font-weight: 800;
    color: var(--ink) !important;
    margin-bottom: 0.35rem;
    text-align: left;
    position: relative;
    z-index: 2;
}

.hero-subtitle,
.section-subtitle {
    color: var(--muted) !important;
    font-size: 1rem;
    line-height: 1.58;
    max-width: 950px;
    margin-bottom: 0;
    text-align: left;
    position: relative;
    z-index: 2;
}

.question-box,
.info-box,
.blue-info-box {
    background: white !important;
    border-radius: 28px !important;
    padding: 1.15rem 1.35rem !important;
    box-shadow: 0 13px 30px rgba(15,40,75,0.08) !important;
    border: 1px solid #e4ebf5 !important;
    border-left: 8px solid var(--yellow) !important;
    margin: 1rem 0 !important;
}

.blue-info-box { border-left-color: var(--blue) !important; }
.info-box { border-left-color: var(--orange) !important; }

[data-testid="stMetric"] {
    background: white !important;
    border-radius: 30px 30px 30px 10px !important;
    padding: 1.15rem 1.25rem !important;
    box-shadow: 0px 14px 34px rgba(15,40,75,0.09) !important;
    border: 1px solid #e1e8f0 !important;
}

[data-testid="stMetric"] label,
[data-testid="stMetric"] div {
    color: var(--ink) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 800 !important;
}

.stTabs [data-baseweb="tab-list"] { gap: 0.7rem; flex-wrap: wrap; }

.stTabs [data-baseweb="tab"] {
    background: white;
    border-radius: 999px;
    padding: 0.85rem 1.3rem;
    border: 1px solid #dce6f2;
    font-weight: 800;
}

.stTabs [aria-selected="true"] {
    background: var(--night) !important;
    color: white !important;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label,
div[data-testid="stRadio"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stToggle"] label {
    font-weight: 800 !important;
    color: var(--ink) !important;
}

.power-tag {
    display: inline-block;
    margin-top: 1rem;
    background: var(--night);
    color: white !important;
    padding: 0.55rem 1rem;
    border-radius: 999px;
    font-size: 0.84rem;
    font-weight: 900;
    letter-spacing: 0.3px;
}

.chart-card {
    background: white;
    border-radius: 34px;
    padding: 1.15rem;
    box-shadow: 0 15px 35px rgba(15,40,75,0.08);
    border: 1px solid #e4ebf5;
    margin-top: 1.2rem;
}

.clima-card {
    background: white;
    border-radius: 34px 34px 34px 10px;
    padding: 1.3rem 1.45rem;
    border: 1px solid #e1e8f0;
    box-shadow: 0 14px 34px rgba(15,40,75,0.09);
    min-height: 150px;
    margin-bottom: 1rem;
}
.clima-card.alt { border-radius: 34px 10px 34px 34px; }
.clima-card.dark { background: var(--night); color: white !important; border: none; }
.clima-card.orange { background: var(--yellow); color: #102a43 !important; border: none; }
.clima-card.green { background: var(--green); color: white !important; border: none; }
.clima-label { font-size: 0.82rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.8px; opacity: 0.75; }
.clima-value { font-family: 'Space Grotesk', sans-serif !important; font-size: 2rem; font-weight: 800; margin-top: 0.2rem; }
.clima-note { font-size: 0.9rem; margin-top: 0.4rem; opacity: 0.82; }

.float-icon {
    display: inline-flex;
    width: 62px;
    height: 62px;
    align-items: center;
    justify-content: center;
    border-radius: 22px;
    background: rgba(255,255,255,0.78);
    box-shadow: 0 10px 24px rgba(15,40,75,0.10);
    font-size: 2rem;
    animation: floatIcon 4.2s ease-in-out infinite;
    margin-right: 0.8rem;
}

@keyframes floatIcon {
    0% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-8px) rotate(-2deg); }
    100% { transform: translateY(0px) rotate(0deg); }
}

@media (max-width: 900px) {
    .hero-title-main { font-size: 3.4rem; }
    .hero-overlay { padding-left: 2rem; }
    .block-container { padding-left: 1.2rem !important; padding-right: 1.2rem !important; }
    .hero-container { width: calc(100% + 2.4rem); margin-left: -1.2rem; }
}


.time-settings-box {
    max-width: 920px;
    margin: 0 auto 1rem auto;
}
.panel-layout-wrap {
    background: linear-gradient(135deg, #f8fbff, #fff7df);
    border: 1px solid #e5ecf6;
    border-radius: 34px;
    padding: 1.4rem;
    box-shadow: 0 14px 36px rgba(15,40,75,0.08);
}
.panel-field {
    background: #d7ecff;
    border: 2px dashed rgba(67,97,238,0.35);
    border-radius: 26px;
    padding: 18px;
    overflow: auto;
}
.panel-row-vis {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
    align-items: center;
}
.solar-panel-vis {
    min-width: 54px;
    width: 54px;
    height: 34px;
    border-radius: 8px;
    background: linear-gradient(135deg, #0f2742, #4361ee);
    border: 2px solid rgba(255,255,255,0.75);
    box-shadow: 0 6px 14px rgba(15,40,75,0.18);
    position: relative;
}
.solar-panel-vis:before {
    content: "";
    position: absolute;
    inset: 6px;
    border-top: 1px solid rgba(255,255,255,0.5);
    border-bottom: 1px solid rgba(255,255,255,0.5);
}
.solar-panel-vis:after {
    content: "";
    position: absolute;
    top: 4px;
    bottom: 4px;
    left: 50%;
    border-left: 1px solid rgba(255,255,255,0.55);
}
.recommendation-box {
    background: white;
    border-radius: 28px;
    padding: 1.2rem 1.4rem;
    border: 1px solid #dfe8f5;
    box-shadow: 0 12px 26px rgba(15,40,75,0.08);
}
.agent-card strong { color: #ffb703; }

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.section-shell {
    border-radius: 34px;
    padding: 1.4rem 1.7rem;
    margin: 1.35rem auto 1.15rem auto;
    width: min(1120px, 96%);
    background: linear-gradient(135deg, #ffe4d6 0%, #fff2e8 100%);
    box-shadow: 0 18px 42px rgba(15,40,75,0.10);
    border: 1px solid rgba(255,255,255,0.82);
    text-align: center;
    position: relative;
    overflow: hidden;
}
.section-shell:after {
    content: "";
    position: absolute;
    right: -52px;
    top: -50px;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: rgba(255,255,255,0.42);
}
.section-shell h2 {
    margin: 0;
    font-size: 2.05rem;
    line-height: 1.1;
    text-align: center !important;
    color: #0f2742 !important;
}
.section-shell p {
    max-width: 900px;
    margin: 0.65rem auto 0 auto;
    color: #5f6f83 !important;
    font-size: 1.02rem;
}
.subsection-title {
    text-align: center;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.45rem;
    font-weight: 800;
    color: #fb8500 !important;
    margin: 1.5rem 0 0.7rem 0;
}
.subsection-title.blue { color: #4361ee !important; }
.subsection-title.yellow { color: #b77900 !important; }
.ask-card {
    background: #ffffff;
    border-radius: 30px 30px 10px 30px;
    padding: 1.25rem 1.5rem;
    border: 1px solid #e8eef8;
    box-shadow: 0 18px 40px rgba(15,40,75,0.10);
    margin: 1.0rem auto 1.2rem auto;
    max-width: 980px;
    text-align: center;
    position: relative;
}
.ask-card b {
    color: #0f2742 !important;
    font-size: 1.08rem;
}
.ask-card .mini {
    color: #5f6f83 !important;
    display:block;
    margin-top:0.35rem;
}
.power-chip {
    display: inline-flex;
    align-items:center;
    gap: .45rem;
    padding: .52rem .9rem;
    background: #0f2742;
    color: #fff !important;
    border-radius: 999px;
    font-weight: 900;
    font-size: .82rem;
    margin-top: .8rem;
    animation: floatIcon 4.2s ease-in-out infinite;
}
.tarifa-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: .75rem;
    margin: .7rem 0 1rem 0;
}
.tarifa-card {
    background: #ffffff;
    border-radius: 22px;
    padding: .9rem 1rem;
    border: 1px solid #e6edf7;
    box-shadow: 0 10px 24px rgba(15,40,75,.07);
    cursor: help;
    min-height: 110px;
}
.tarifa-card strong { color:#0f2742; display:block; margin-bottom:.25rem; }
.tarifa-card span { color:#607187; font-size:.86rem; }
.result-bubble {
    background: white;
    border-radius: 36px 14px 36px 14px;
    padding: 1.1rem 1.25rem;
    box-shadow: 0 16px 34px rgba(15,40,75,0.09);
    border: 1px solid #e4ebf5;
    min-height: 126px;
    margin-bottom: .85rem;
}
.result-bubble .label { color:#607187; font-weight:900; font-size:.78rem; text-transform:uppercase; letter-spacing:.6px; }
.result-bubble .value { color:#0f2742; font-family:'Space Grotesk', sans-serif; font-size:1.75rem; font-weight:900; margin-top:.18rem; }
.result-bubble .note { color:#607187; font-size:.86rem; margin-top:.25rem; }
.dashboard-zone {
    background: linear-gradient(135deg, #0f2742 0%, #153f68 100%);
    border-radius: 36px;
    padding: 1.35rem;
    margin-top: 1rem;
    box-shadow: 0 18px 42px rgba(15,40,75,.17);
}
.dashboard-zone h3, .dashboard-zone p { color:white !important; text-align:center; }


.time-settings-box {
    max-width: 920px;
    margin: 0 auto 1rem auto;
}
.panel-layout-wrap {
    background: linear-gradient(135deg, #f8fbff, #fff7df);
    border: 1px solid #e5ecf6;
    border-radius: 34px;
    padding: 1.4rem;
    box-shadow: 0 14px 36px rgba(15,40,75,0.08);
}
.panel-field {
    background: #d7ecff;
    border: 2px dashed rgba(67,97,238,0.35);
    border-radius: 26px;
    padding: 18px;
    overflow: auto;
}
.panel-row-vis {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
    align-items: center;
}
.solar-panel-vis {
    min-width: 54px;
    width: 54px;
    height: 34px;
    border-radius: 8px;
    background: linear-gradient(135deg, #0f2742, #4361ee);
    border: 2px solid rgba(255,255,255,0.75);
    box-shadow: 0 6px 14px rgba(15,40,75,0.18);
    position: relative;
}
.solar-panel-vis:before {
    content: "";
    position: absolute;
    inset: 6px;
    border-top: 1px solid rgba(255,255,255,0.5);
    border-bottom: 1px solid rgba(255,255,255,0.5);
}
.solar-panel-vis:after {
    content: "";
    position: absolute;
    top: 4px;
    bottom: 4px;
    left: 50%;
    border-left: 1px solid rgba(255,255,255,0.55);
}
.recommendation-box {
    background: white;
    border-radius: 28px;
    padding: 1.2rem 1.4rem;
    border: 1px solid #dfe8f5;
    box-shadow: 0 12px 26px rgba(15,40,75,0.08);
}
.agent-card strong { color: #ffb703; }

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------

# IMAGEN Y CLIMA

def cargar_imagen_base64(ruta):
    ruta = Path(ruta)
    if not ruta.exists():
        return None
    with open(ruta, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def clima_card(label, value, note="", style=""):
    return f"""
    <div class="clima-card {style}">
        <div class="clima-label">{label}</div>
        <div class="clima-value">{value}</div>
        <div class="clima-note">{note}</div>
    </div>
    """


@st.cache_data(ttl=3600)
def obtener_clima_open_meteo(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": float(lat),
        "longitude": float(lon),
        "hourly": (
            "temperature_2m,cloud_cover,precipitation,rain,wind_speed_10m,"
            "shortwave_radiation,direct_radiation,diffuse_radiation"
        ),
        "forecast_days": 7,
        "timezone": "auto"
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    clima_df = pd.DataFrame(data["hourly"])
    clima_df["time"] = pd.to_datetime(clima_df["time"])
    return clima_df


def mostrar_modulo_clima(latitud, longitud):
    st.markdown('<p class="centered-note">Consulta meteorológica automática para la ubicación seleccionada.</p>', unsafe_allow_html=True)

    try:
        clima_df = obtener_clima_open_meteo(latitud, longitud)
        nubosidad_prom = float(clima_df["cloud_cover"].mean())
        lluvia_total = float(clima_df["precipitation"].sum())
        radiacion_max = float(clima_df["shortwave_radiation"].max())
        radiacion_prom_dia = float(clima_df[clima_df["shortwave_radiation"] > 0]["shortwave_radiation"].mean()) if (clima_df["shortwave_radiation"] > 0).any() else 0.0
        viento_prom = float(clima_df["wind_speed_10m"].mean())
        temp_prom = float(clima_df["temperature_2m"].mean())

        if nubosidad_prom < 35:
            condicion, emoji, comentario, estilo = "Alta", "☀️", "Baja nubosidad promedio. El clima favorece la generación solar.", "orange"
            factor_climatico_local = 0.96
        elif nubosidad_prom < 65:
            condicion, emoji, comentario, estilo = "Media", "⛅", "Nubosidad moderada. Puede reducir la producción en ciertos horarios.", "dark"
            factor_climatico_local = 0.88
        else:
            condicion, emoji, comentario, estilo = "Baja", "☁️", "Alta nubosidad. La producción puede reducirse de forma importante.", "dark"
            factor_climatico_local = 0.78

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(clima_card("Condición solar", f"{emoji} {condicion}", comentario, estilo), unsafe_allow_html=True)
        with c2:
            st.markdown(clima_card("Nubosidad promedio", f"{nubosidad_prom:.1f}%", "A mayor nubosidad, menor radiación directa.", "alt"), unsafe_allow_html=True)
        with c3:
            st.markdown(clima_card("Lluvia acumulada", f"{lluvia_total:.1f} mm", "Puede bajar la generación durante el evento.", ""), unsafe_allow_html=True)
        with c4:
            st.markdown(clima_card("Radiación máxima", f"{radiacion_max:.0f} W/m²", "Pico estimado de radiación disponible.", "green"), unsafe_allow_html=True)

        c5, c6, c7 = st.columns(3)
        with c5:
            st.markdown(clima_card("Temperatura promedio", f"{temp_prom:.1f} °C", "Temperaturas altas reducen ligeramente el rendimiento.", ""), unsafe_allow_html=True)
        with c6:
            st.markdown(clima_card("Viento promedio", f"{viento_prom:.1f} km/h", "Puede enfriar paneles; valores altos requieren revisión estructural.", "alt"), unsafe_allow_html=True)
        with c7:
            st.markdown(clima_card("Factor climático sugerido", f"{factor_climatico_local*100:.0f}%", "Referencia visual; no reemplaza la simulación técnica.", "orange"), unsafe_allow_html=True)

        with st.expander("💡 Para saber más: ¿cómo afecta el clima a los paneles?"):
            st.write("""
            La nubosidad afecta principalmente la radiación directa que llega al panel. La lluvia reduce la generación mientras ocurre,
            pero también puede limpiar la superficie. La radiación de onda corta representa la energía solar total disponible estimada.
            Este módulo sirve como lectura climática complementaria para entender mejor la simulación.
            """)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig_clima = go.Figure()
        fig_clima.add_trace(go.Scatter(
            x=clima_df["time"], y=clima_df["cloud_cover"], mode="lines", name="Nubosidad (%)",
            line=dict(width=3, color="#4361ee"),
            hovertemplate="Fecha: %{x}<br>Nubosidad: %{y:.1f}%<extra></extra>"
        ))
        fig_clima.add_trace(go.Bar(
            x=clima_df["time"], y=clima_df["precipitation"], name="Precipitación (mm)", yaxis="y2",
            opacity=0.55, marker_color="#ffb703",
            hovertemplate="Fecha: %{x}<br>Precipitación: %{y:.2f} mm<extra></extra>"
        ))
        fig_clima.update_layout(
            title="Nubosidad y precipitación estimada",
            xaxis_title="Fecha y hora", yaxis=dict(title="Nubosidad (%)"),
            yaxis2=dict(title="Precipitación (mm)", overlaying="y", side="right"),
            hovermode="x unified", height=455, paper_bgcolor="white", plot_bgcolor="white",
            legend=dict(orientation="h", y=-0.25), margin=dict(l=40, r=40, t=70, b=90)
        )
        st.plotly_chart(fig_clima, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig_rad = go.Figure()
        fig_rad.add_trace(go.Scatter(
            x=clima_df["time"], y=clima_df["shortwave_radiation"], mode="lines", name="Radiación total",
            line=dict(width=4, color="#ffb703"),
            hovertemplate="Fecha: %{x}<br>Radiación total: %{y:.1f} W/m²<extra></extra>"
        ))
        fig_rad.add_trace(go.Scatter(
            x=clima_df["time"], y=clima_df["direct_radiation"], mode="lines", name="Radiación directa",
            line=dict(width=3, dash="dot", color="#fb8500"),
            hovertemplate="Fecha: %{x}<br>Radiación directa: %{y:.1f} W/m²<extra></extra>"
        ))
        fig_rad.add_trace(go.Scatter(
            x=clima_df["time"], y=clima_df["diffuse_radiation"], mode="lines", name="Radiación difusa",
            line=dict(width=3, dash="dash", color="#2a9d8f"),
            hovertemplate="Fecha: %{x}<br>Radiación difusa: %{y:.1f} W/m²<extra></extra>"
        ))
        fig_rad.update_layout(
            title="Radiación solar estimada por tipo",
            xaxis_title="Fecha y hora", yaxis_title="Radiación (W/m²)", hovermode="x unified",
            height=455, paper_bgcolor="white", plot_bgcolor="white",
            legend=dict(orientation="h", y=-0.25), margin=dict(l=40, r=40, t=70, b=90)
        )
        st.plotly_chart(fig_rad, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return clima_df, factor_climatico_local

    except Exception as e:
        st.warning(f"No se pudo cargar el análisis climatológico en este momento: {e}")
        return None, 1.0


paneles_df = pd.read_csv("datos/paneles.csv", encoding="latin1", sep="\t")
ubicaciones_df = pd.read_csv("datos/ubicaciones.csv", encoding="latin1", sep="\t")

# -------------------------------------------------------------------------------------------------------------------------------------------------------------

# UBICACIONES

capitales_mexico = pd.DataFrame([
    ["Aguascalientes, Aguascalientes", 21.8853, -102.2916, 1888, "America/Mexico_City"],
    ["Mexicali, Baja California", 32.6245, -115.4523, 8, "America/Tijuana"],
    ["La Paz, Baja California Sur", 24.1426, -110.3128, 27, "America/Mazatlan"],
    ["San Francisco de Campeche, Campeche", 19.8301, -90.5349, 10, "America/Merida"],
    ["Tuxtla Gutiérrez, Chiapas", 16.7516, -93.1161, 522, "America/Mexico_City"],
    ["Chihuahua, Chihuahua", 28.6320, -106.0691, 1415, "America/Chihuahua"],
    ["Ciudad de México", 19.4326, -99.1332, 2240, "America/Mexico_City"],
    ["Saltillo, Coahuila", 25.4380, -100.9737, 1600, "America/Monterrey"],
    ["Colima, Colima", 19.2433, -103.7250, 500, "America/Mexico_City"],
    ["Victoria de Durango, Durango", 24.0277, -104.6532, 1880, "America/Monterrey"],
    ["Guanajuato, Guanajuato", 21.0190, -101.2574, 2045, "America/Mexico_City"],
    ["Chilpancingo, Guerrero", 17.5515, -99.5006, 1260, "America/Mexico_City"],
    ["Pachuca, Hidalgo", 20.1011, -98.7591, 2400, "America/Mexico_City"],
    ["Guadalajara, Jalisco", 20.6597, -103.3496, 1566, "America/Mexico_City"],
    ["Toluca, Estado de México", 19.2826, -99.6557, 2660, "America/Mexico_City"],
    ["Morelia, Michoacán", 19.7008, -101.1844, 1920, "America/Mexico_City"],
    ["Cuernavaca, Morelos", 18.9242, -99.2216, 1510, "America/Mexico_City"],
    ["Tepic, Nayarit", 21.5042, -104.8946, 920, "America/Mazatlan"],
    ["Monterrey, Nuevo León", 25.6866, -100.3161, 512, "America/Monterrey"],
    ["Oaxaca de Juárez, Oaxaca", 17.0732, -96.7266, 1555, "America/Mexico_City"],
    ["Puebla, Puebla", 19.0414, -98.2063, 2135, "America/Mexico_City"],
    ["Santiago de Querétaro, Querétaro", 20.5888, -100.3899, 1820, "America/Mexico_City"],
    ["Chetumal, Quintana Roo", 18.5001, -88.2961, 10, "America/Cancun"],
    ["San Luis Potosí, San Luis Potosí", 22.1565, -100.9855, 1864, "America/Mexico_City"],
    ["Culiacán, Sinaloa", 24.8091, -107.3940, 54, "America/Mazatlan"],
    ["Hermosillo, Sonora", 29.0729, -110.9559, 210, "America/Hermosillo"],
    ["Villahermosa, Tabasco", 17.9892, -92.9475, 10, "America/Mexico_City"],
    ["Ciudad Victoria, Tamaulipas", 23.7369, -99.1411, 316, "America/Monterrey"],
    ["Tlaxcala, Tlaxcala", 19.3182, -98.2375, 2230, "America/Mexico_City"],
    ["Xalapa, Veracruz", 19.5438, -96.9102, 1417, "America/Mexico_City"],
    ["Mérida, Yucatán", 20.9674, -89.5926, 10, "America/Merida"],
    ["Zacatecas, Zacatecas", 22.7709, -102.5832, 2440, "America/Mexico_City"],
], columns=["nombre", "latitud", "longitud", "altitud", "zona_horaria"])

capitales_mexico["tipo_dato"] = "Capital estatal"

if "tipo_dato" not in ubicaciones_df.columns:
    ubicaciones_df["tipo_dato"] = "Predeterminado"

ubicaciones_selector = pd.concat(
    [capitales_mexico, ubicaciones_df[["nombre", "latitud", "longitud", "altitud", "zona_horaria", "tipo_dato"]]],
    ignore_index=True
).drop_duplicates(subset=["nombre"], keep="first")

ubicacion_default = ubicaciones_selector[ubicaciones_selector["nombre"].astype(str).str.contains("Consolapa", case=False, na=False)].iloc[0] if any(ubicaciones_selector["nombre"].astype(str).str.contains("Consolapa", case=False, na=False)) else ubicaciones_selector.iloc[0]

if "Manual" in paneles_df["modelo"].values:
    panel_default = paneles_df[paneles_df["modelo"] == "Manual"].iloc[0]
else:
    panel_default = paneles_df.iloc[0]

if "lat_manual" not in st.session_state:
    st.session_state.lat_manual = float(ubicacion_default["latitud"])

if "lon_manual" not in st.session_state:
    st.session_state.lon_manual = float(ubicacion_default["longitud"])

if "alt_manual" not in st.session_state:
    st.session_state.alt_manual = float(ubicacion_default["altitud"])

# -------------------------------------------------------------------------------------------------------------------------------------------------------------

# TARIFAS

tarifas_estimadas = {
    "Residencial subsidiada - casa": {
        "precio": 1.20,
        "descripcion": "Uso doméstico en casa con consumo moderado. Es una tarifa subsidiada y suele ser más baja."
    },
    "Residencial alto consumo DAC": {
        "precio": 6.00,
        "descripcion": "Casa con consumo alto. La tarifa DAC suele ser mucho más cara porque pierde subsidio."
    },
    "Negocio pequeño baja tensión": {
        "precio": 3.50,
        "descripcion": "Locales, pequeños comercios u oficinas conectados en baja tensión."
    },
    "Industrial / GDMTO": {
        "precio": 2.68,
        "descripcion": "Empresas con demanda media o alta. Es la referencia usada para STREGER según su recibo."
    },
    "No sé / usar promedio general": {
        "precio": 2.80,
        "descripcion": "Promedio aproximado para hacer una estimación rápida cuando no se conoce la tarifa."
    }
}

# -------------------------------------------------------------------------------------------------------------------------------------------------------------

# ENCABEZADO

img_base64 = cargar_imagen_base64("assets/solar_header.jpg")

if img_base64:
    st.markdown(
        f"""
        <div class="hero-container">
            <img src="data:image/jpeg;base64,{img_base64}">
            <div class="hero-overlay">
                <div class="hero-kicker">Herramienta de simulación fotovoltaica</div>
                <div class="hero-title-main">Explorador<br>Solar</div>
                <div class="hero-subtitle-main">
                    Visualiza consumo, generación solar, clima, nubosidad, lluvia, radiación, reducción estimada del recibo
                    y escenarios de respaldo eléctrico.
                </div>
                <div class="hero-actions">
                    <div class="hero-pill-main">☀️ Diagnóstico solar interactivo</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("""
    <div class="hero-section" style="background:#0f2742;">
        <div class="hero-title" style="color:white !important;">☀️ Explorador Solar</div>
        <div class="hero-subtitle" style="color:#eaf2ff !important;">
            Herramienta preliminar para estimar gasto eléctrico, ahorro con paneles solares y escenarios de riesgo energético.
            Para mostrar la imagen superior, guarda tu foto como <b>assets/solar_header.jpg</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------

# FUNCIONES

def section_header(icono, titulo, subtitulo=""):
    st.markdown(f"""
    <div class="section-shell">
        <h2>{icono} {titulo}</h2>
        <p>{subtitulo}</p>
    </div>
    """, unsafe_allow_html=True)


def subsection(titulo, color="orange"):
    clase = "subsection-title" if color == "orange" else f"subsection-title {color}"
    st.markdown(f'<div class="{clase}">{titulo}</div>', unsafe_allow_html=True)


def ask_card(texto, nota="", icono="✨"):
    st.markdown(f"""
    <div class="ask-card">
        <b>{icono} {texto}</b>
        <span class="mini">{nota}</span>
    </div>
    """, unsafe_allow_html=True)


def bubble(label, value, note=""):
    return f"""
    <div class="result-bubble">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        <div class="note">{note}</div>
    </div>
    """


def tarifas_html(tarifas):
    html = '<div class="tarifa-grid">'
    for nombre, datos in tarifas.items():
        html += f'<div class="tarifa-card" title="{datos["descripcion"]}"><strong>{nombre}</strong><span>{datos["descripcion"]}<br><b>Valor usado:</b> ${datos["precio"]:.2f}/kWh</span></div>'
    html += '</div>'
    return html


def limpiar_df_para_excel(df):
    df = df.copy()

    for col in df.columns:
        if pd.api.types.is_datetime64tz_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            try:
                if getattr(df[col].dt, "tz", None) is not None:
                    df[col] = df[col].dt.tz_localize(None)
            except Exception:
                pass

        elif df[col].dtype == "object":
            df[col] = df[col].apply(
                lambda x: str(x) if isinstance(x, (list, dict, tuple, set)) else x
            )

    return df


def dataframe_to_download(sheets: dict):
    from io import BytesIO

    output = BytesIO()

    try:
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for sheet_name, df_sheet in sheets.items():
                safe = str(sheet_name)[:31].replace("/", "-").replace("\\", "-")

                if isinstance(df_sheet, pd.DataFrame):
                    df_clean = limpiar_df_para_excel(df_sheet)
                else:
                    df_clean = limpiar_df_para_excel(pd.DataFrame(df_sheet))

                df_clean.to_excel(writer, sheet_name=safe, index=False)

        return (
            output.getvalue(),
            "datos_explorador_solar.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception:
        first_name = list(sheets.keys())[0]
        first_df = list(sheets.values())[0]

        if not isinstance(first_df, pd.DataFrame):
            first_df = pd.DataFrame(first_df)

        first_df = limpiar_df_para_excel(first_df)

        csv = first_df.to_csv(index=False).encode("utf-8-sig")

        return (
            csv,
            f"{first_name}.csv",
            "text/csv"
        )


def generar_pdf_resumen(resumen: dict):
    """Genera un PDF válido, visible y con estructura ejecutiva."""
    buffer = BytesIO()
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=40)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("TitleSolar", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#0f2742"), fontName="Helvetica-Bold", fontSize=20, leading=24, spaceAfter=4)
        subtitle_style = ParagraphStyle("SubtitleSolar", parent=styles["BodyText"], alignment=TA_CENTER, textColor=colors.HexColor("#5f6f83"), fontSize=8.5, leading=11, spaceAfter=10)
        section_style = ParagraphStyle("SectionSolar", parent=styles["Heading2"], textColor=colors.HexColor("#fb8500"), fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8, spaceAfter=5)
        body_style = ParagraphStyle("BodySolar", parent=styles["BodyText"], alignment=TA_JUSTIFY, fontSize=9.1, leading=13.3, spaceAfter=7, textColor=colors.HexColor("#243b53"))
        lead_style = ParagraphStyle("LeadSolar", parent=body_style, fontName="Helvetica-Bold", textColor=colors.HexColor("#0f2742"), fontSize=9.5, leading=13.8)

        story = []
        story.append(Paragraph("Explorador Solar", title_style))
        story.append(Paragraph("Reporte ejecutivo preliminar · Simulación y análisis fotovoltaico", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.1, color=colors.HexColor("#fb8500")))
        story.append(Spacer(1, 8))

        indicadores = [
            ["Ubicación", str(resumen.get("Ubicación", "-")), "Paneles", str(resumen.get("Número paneles", "-"))],
            ["Tarifa", str(resumen.get("Tarifa", "-")), "Cobertura", f"{float(resumen.get('Cobertura %', 0)):.1f}%"],
            ["Consumo anual", f"{float(resumen.get('Consumo anual kWh', 0)):,.0f} kWh", "Generación anual", f"{float(resumen.get('Generación anual kWh', 0)):,.0f} kWh"],
            ["Área aproximada", f"{float(resumen.get('Área total m2', 0)):,.1f} m²", "Reducción estimada", f"{float(resumen.get('Reducción estimada %', 0)):.1f}%"],
        ]
        t = Table(indicadores, colWidths=[88, 170, 94, 158])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7fbff")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#243b53")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d9e2ec")),
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#d9e2ec")),
            ("FONTSIZE", (0, 0), (-1, -1), 7.8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 10))
        story.append(Paragraph("Resumen ejecutivo", section_style))

        narrativa = str(resumen.get("Resumen ejecutivo", "")).strip()
        parrafos = [p.strip() for p in narrativa.split("\n\n") if p.strip()]
        for i, parrafo in enumerate(parrafos):
            story.append(Paragraph(parrafo, lead_style if i == 0 else body_style))

        story.append(Spacer(1, 5))
        story.append(Paragraph("Nota de alcance", section_style))
        story.append(Paragraph("Este documento es un diagnóstico preliminar generado con supuestos editables dentro de la interfaz. No sustituye levantamiento de sitio, ingeniería eléctrica, análisis estructural, cotización comercial ni dictamen técnico.", body_style))
        doc.build(story)
        data = buffer.getvalue()
        if not data or len(data) < 1000:
            raise ValueError("PDF vacío")
        return data
    except Exception:
        # Fallback mínimo válido.
        text = "Explorador Solar - Reporte ejecutivo\n\n" + str(resumen.get("Resumen ejecutivo", ""))
        lines = []
        for raw in text.splitlines():
            line = ""
            for w in raw.split():
                if len(line) + len(w) + 1 > 88:
                    lines.append(line); line = w
                else:
                    line = (line + " " + w).strip()
            if line: lines.append(line)
            if not raw.strip(): lines.append("")
        ops = ["BT", "/F1 14 Tf", "1 0 0 1 72 760 Tm"]
        y = 760
        for i, line in enumerate(lines[:68]):
            safe = str(line).replace("\\", "/").replace("(", "[").replace(")", "]")[:105]
            size = 14 if i == 0 else 8
            ops.append(f"/F1 {size} Tf")
            ops.append(f"1 0 0 1 72 {y} Tm ({safe}) Tj")
            y -= 11 if i else 18
        ops.append("ET")
        stream = "\n".join(ops).encode("latin-1", errors="ignore")
        objs = [
            b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
            b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
            b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n",
            b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n",
            b"5 0 obj << /Length " + str(len(stream)).encode() + b" >> stream\n" + stream + b"\nendstream endobj\n",
        ]
        pdf = b"%PDF-1.4\n"; offsets = [0]
        for obj in objs:
            offsets.append(len(pdf)); pdf += obj
        xref_pos = len(pdf)
        pdf += f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode()
        for off in offsets[1:]: pdf += f"{off:010d} 00000 n \n".encode()
        pdf += f"trailer << /Root 1 0 R /Size {len(objs)+1} >>\nstartxref\n{xref_pos}\n%%EOF".encode()
        return pdf

tarifas_estimadas = {
    "Tarifa 1 - Doméstica básica": {
        "precio": 1.20,
        "descripcion": "Uso residencial en casas con consumo bajo o medio. Suele tener bloques básico/intermedio/excedente y subsidio."
    },
    "Tarifa DAC - Doméstica alto consumo": {
        "precio": 6.00,
        "descripcion": "Residencial de alto consumo. Pierde subsidio y por eso el costo promedio por kWh es mucho mayor."
    },
    "PDBT - Pequeña Demanda en Baja Tensión": {
        "precio": 3.50,
        "descripcion": "Pequeños negocios, locales, oficinas o servicios conectados en baja tensión con demanda menor."
    },
    "GDMTO - Gran Demanda Media Tensión Ordinaria": {
        "precio": 2.68,
        "descripcion": "Empresas o instalaciones en media tensión con demanda relevante."
    },
    "Promedio exploratorio": {
        "precio": 2.80,
        "descripcion": "Opción rápida cuando no se conoce la tarifa. Promedia escenarios residenciales/comerciales, solo para diagnóstico."
    }
}


paneles_tecnicos = pd.DataFrame([
    {"tipo": "Panel estándar monocristalino", "potencia_kw": 0.450, "area_m2": 2.10, "eficiencia": 0.205, "descripcion": "Opción común. Buen equilibrio entre disponibilidad, potencia y área requerida."},
    {"tipo": "Panel de alta eficiencia", "potencia_kw": 0.550, "area_m2": 2.35, "eficiencia": 0.225, "descripcion": "Genera más por panel y ayuda cuando el área disponible es limitada."},
    {"tipo": "Panel bifacial / alto rendimiento", "potencia_kw": 0.600, "area_m2": 2.55, "eficiencia": 0.235, "descripcion": "Puede aprovechar radiación reflejada si el montaje y el suelo lo permiten."},
])


MESES_ES = {
    1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"
}

# Factor mensual preliminar para climatología anual.
# 1.00 = sin castigo; menor valor = menos generación útil por nubosidad/lluvia/condiciones atmosféricas.
# Se deja editable en el comparativo porque no sustituye una base histórica climatológica local.
FACTORES_CLIMA_MENSUAL_DEFAULT = {
    1: 0.95, 2: 0.96, 3: 0.98, 4: 1.00, 5: 0.97, 6: 0.88,
    7: 0.84, 8: 0.83, 9: 0.82, 10: 0.87, 11: 0.92, 12: 0.94
}



def orientacion_recomendada_por_ubicacion(latitud, longitud):
    """Orientación preliminar dependiente de ubicación.
    En el hemisferio norte mira hacia el sur y en el hemisferio sur hacia el norte.
    Se agrega un ajuste fino por longitud respecto al meridiano horario local para que el valor cambie entre ubicaciones;
    la optimización 3D sigue siendo el método más robusto para afinar el azimut.
    """
    latitud = float(latitud)
    longitud = float(longitud)
    base = 180.0 if latitud >= 0 else 0.0
    meridiano_local = round(longitud / 15.0) * 15.0
    ajuste = max(min((longitud - meridiano_local) * 0.75, 12.0), -12.0)
    if abs(latitud) < 3:
        base = 180.0 if longitud < 0 else 0.0
        ajuste = 0.0
    return (base + ajuste) % 360

def preparar_comparativo_mensual(df_solar, consumo_mensual_kwh, precio_kwh, factores_clima):
    energia_mensual = df_solar[["potencia_solar_kw"]].resample("ME").sum() * 0.25
    energia_mensual = energia_mensual.rename(columns={"potencia_solar_kw": "generacion_solar_kwh"})
    energia_mensual["mes_num"] = energia_mensual.index.month
    energia_mensual["mes"] = energia_mensual["mes_num"].map(MESES_ES)
    energia_mensual["consumo_kwh"] = float(consumo_mensual_kwh)
    energia_mensual["factor_climatologico"] = energia_mensual["mes_num"].map(factores_clima).astype(float)
    energia_mensual["generacion_ajustada_clima_kwh"] = energia_mensual["generacion_solar_kwh"] * energia_mensual["factor_climatologico"]
    energia_mensual["red_kwh_sin_clima"] = (energia_mensual["consumo_kwh"] - energia_mensual["generacion_solar_kwh"]).clip(lower=0)
    energia_mensual["red_kwh_con_clima"] = (energia_mensual["consumo_kwh"] - energia_mensual["generacion_ajustada_clima_kwh"]).clip(lower=0)
    energia_mensual["gasto_sin_paneles_mxn"] = energia_mensual["consumo_kwh"] * precio_kwh
    energia_mensual["gasto_con_paneles_mxn"] = energia_mensual["red_kwh_sin_clima"] * precio_kwh
    energia_mensual["gasto_con_clima_mxn"] = energia_mensual["red_kwh_con_clima"] * precio_kwh
    energia_mensual["castigo_clima_kwh"] = energia_mensual["generacion_solar_kwh"] - energia_mensual["generacion_ajustada_clima_kwh"]
    return energia_mensual.reset_index(names="fecha")


def fig_comparativo_anual(dfm):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dfm["mes"], y=dfm["consumo_kwh"], name="Consumo del usuario",
        marker_color="#2b2d42", opacity=0.30,
        hovertemplate="Mes: %{x}<br>Consumo: %{y:,.0f} kWh<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=dfm["mes"], y=dfm["generacion_solar_kwh"], name="Generación solar sin clima",
        mode="lines+markers", line=dict(color="#2a9d8f", width=4),
        hovertemplate="Mes: %{x}<br>Solar sin clima: %{y:,.0f} kWh<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=dfm["mes"], y=dfm["generacion_ajustada_clima_kwh"], name="Generación solar con clima",
        mode="lines+markers", line=dict(color="#fb8500", width=4),
        fill="tonexty", fillcolor="rgba(251,133,0,0.12)",
        hovertemplate="Mes: %{x}<br>Solar con clima: %{y:,.0f} kWh<extra></extra>"
    ))
    fig.update_layout(
        title="Comparativo anual: consumo vs generación solar",
        xaxis_title="Mes", yaxis=dict(title="Energía (kWh)"),
        hovermode="x unified", barmode="overlay", height=640,
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
    )
    return fig

def fig_cashflow_roi(gasto_anual_actual, gasto_con_paneles, gasto_con_clima, periodo):
    years = np.arange(0, int(periodo) + 1)
    gasto_sin = gasto_anual_actual * years
    gasto_paneles = gasto_con_paneles * years
    gasto_clima = gasto_con_clima * years
    ahorro_clima = np.maximum(gasto_sin - gasto_clima, 0)
    roi_relativo = np.nan_to_num((ahorro_clima / np.where(gasto_sin == 0, np.nan, gasto_sin)) * 100)
    df_cash = pd.DataFrame({
        "Año": years,
        "Gasto acumulado sin paneles": gasto_sin,
        "Gasto acumulado con paneles ideal": gasto_paneles,
        "Gasto acumulado con paneles y clima": gasto_clima,
        "Ahorro acumulado con clima": ahorro_clima,
        "ROI relativo por reducción de tarifa (%)": roi_relativo
    })
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_cash["Año"], y=df_cash["Gasto acumulado sin paneles"], mode="lines", name="Sin paneles", line=dict(color="#e63946", width=4), hovertemplate="Año %{x}<br>$%{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=df_cash["Año"], y=df_cash["Gasto acumulado con paneles y clima"], mode="lines", name="Con paneles + clima", line=dict(color="#2a9d8f", width=4), hovertemplate="Año %{x}<br>$%{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Bar(x=df_cash["Año"], y=df_cash["Ahorro acumulado con clima"], name="Ahorro acumulado", marker_color="#8ac926", opacity=0.45, hovertemplate="Año %{x}<br>Ahorro: $%{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=df_cash["Año"], y=df_cash["ROI relativo por reducción de tarifa (%)"], name="ROI relativo", yaxis="y2", mode="lines+markers", line=dict(color="#ffb703", width=4), hovertemplate="Año %{x}<br>ROI relativo: %{y:.1f}%<extra></extra>"))
    fig.update_layout(title="Cashflow comparativo y ROI relativo por reducción del recibo", xaxis_title="Año", yaxis=dict(title="Costo/acumulado (MXN)"), yaxis2=dict(title="ROI relativo (%)", overlaying="y", side="right"), hovermode="x unified", height=600, plot_bgcolor="white", paper_bgcolor="white", legend=dict(orientation="h", y=1.02))
    return df_cash, fig


def filtrar_df_por_periodo(df, base, prefijo=""):
    """Filtra la serie solar por día, mes o año para gráficas 2D."""
    vista = base.get("vista_inicial", "Año")
    fecha_min, fecha_max = df.index.min().date(), df.index.max().date()
    anio_default = int(base.get("anio_analisis", pd.Timestamp.today().year))
    mes_default = int(base.get("mes_analisis", pd.Timestamp.today().month))
    colp1, colp2, colp3 = st.columns([1, 1, 2])
    with colp1:
        vista_local = st.selectbox("Periodo de visualización", ["Día", "Mes", "Año"], index=["Día", "Mes", "Año"].index(vista) if vista in ["Día", "Mes", "Año"] else 2, key=f"{prefijo}_vista_periodo")
    if vista_local == "Día":
        with colp2:
            fecha_obj = pd.to_datetime(base.get("fecha_referencia", fecha_min)).date()
            if fecha_obj < fecha_min or fecha_obj > fecha_max:
                fecha_obj = fecha_min
            fecha = st.date_input("Día", value=fecha_obj, min_value=fecha_min, max_value=fecha_max, key=f"{prefijo}_dia")
        df_periodo = df.loc[str(fecha)]
        etiqueta = f"día {fecha}"
    elif vista_local == "Mes":
        with colp2:
            mes = st.selectbox("Mes", list(MESES_ES.keys()), format_func=lambda m: MESES_ES[m], index=mes_default-1, key=f"{prefijo}_mes")
        df_periodo = df[df.index.month == mes]
        etiqueta = f"mes de {MESES_ES[mes]}"
    else:
        df_periodo = df.copy()
        etiqueta = "año modelado completo"
    if df_periodo.empty:
        df_periodo = df.copy()
        etiqueta = "año modelado completo"
    return df_periodo, etiqueta, vista_local


def crear_heatmap_generacion_anual(df):
    dfh = df.copy()
    dfh["mes_num"] = dfh.index.month
    dfh["mes"] = dfh["mes_num"].map(MESES_ES)
    dfh["hora"] = dfh.index.hour
    # La simulación base trabaja en pasos de 15 min; kWh del intervalo = kW * 0.25.
    dfh["energia_intervalo_kwh"] = dfh["potencia_solar_kw"] * 0.25
    tabla = dfh.groupby(["hora", "mes_num", "mes"], as_index=False)["energia_intervalo_kwh"].mean()
    pivot = tabla.pivot(index="hora", columns="mes", values="energia_intervalo_kwh")
    columnas = [MESES_ES[m] for m in range(1, 13) if MESES_ES[m] in pivot.columns]
    pivot = pivot.reindex(index=list(range(24)), columns=columnas).fillna(0)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=[f"{h:02d}:00" for h in pivot.index],
        colorscale="YlOrBr",
        colorbar=dict(title="kWh prom."),
        hovertemplate="Mes: %{x}<br>Hora: %{y}<br>Energía prom.: %{z:.3f} kWh<extra></extra>"
    ))
    fig.update_layout(
        title="Heatmap anual de generación solar promedio",
        xaxis_title="Mes", yaxis_title="Hora del día",
        height=650, plot_bgcolor="white", paper_bgcolor="white"
    )
    return pivot.reset_index(names="hora"), fig


def obtener_dia_representativo(df):
    """Usa el día con mayor generación solar como día técnico representativo para las gráficas 2D."""
    if df.empty:
        return df, "día representativo"
    energia_diaria = (df["potencia_solar_kw"].resample("D").sum() * 0.25).dropna()
    if energia_diaria.empty:
        fecha = df.index.min().date()
    else:
        fecha = energia_diaria.idxmax().date()
    df_dia = df.loc[str(fecha)]
    return df_dia, f"día representativo {fecha}"


def render_panel_layout(filas, paneles_por_fila, total_paneles, modo="Distribución normal", espacio_paneles_m=0.10, espacio_filas_m=1.20):
    """Dibujo esquemático. Cambia visualmente según el modo seleccionado."""
    restantes = int(total_paneles)
    if modo == "Optimizar espacio":
        clase = "panel-field panel-field-compact"
        etiqueta = "Modo compacto: paneles juntos"
        gap_px = 2
        row_gap_px = 2
    elif modo == "Manual":
        clase = "panel-field panel-field-manual"
        etiqueta = "Modo manual: separación definida por usuario"
        gap_px = max(2, min(30, int(espacio_paneles_m * 18) + 2))
        row_gap_px = max(2, min(38, int(espacio_filas_m * 10) + 2))
    else:
        clase = "panel-field panel-field-normal"
        etiqueta = "Modo normal: arreglo balanceado"
        gap_px = 10
        row_gap_px = 10
    html = f'<div class="panel-mode-label">{etiqueta}</div><div class="{clase}" style="--panel-gap:{gap_px}px; --row-gap:{row_gap_px}px;">'
    for _ in range(int(filas)):
        cantidad = min(int(paneles_por_fila), restantes)
        if cantidad <= 0:
            break
        html += '<div class="panel-row-vis">' + ''.join(['<div class="solar-panel-vis"></div>' for __ in range(cantidad)]) + '</div>'
        restantes -= cantidad
    html += '</div>'
    return html

# -------------------------------------------------------------------------------------------------------------------------------------------------------------


# PESTAÑAS

st.markdown("""
<style>
.visual-question {
    background: #ffffff;
    border-radius: 34px;
    padding: 2.0rem 1.5rem;
    margin: 1.2rem auto 1.5rem auto;
    max-width: 1050px;
    text-align: center;
    box-shadow: 0 18px 42px rgba(15,40,75,0.10);
    border: 1px solid #e6edf7;
}
.visual-question h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #0f2742 !important;
    margin: 0;
    font-size: 1.65rem;
    text-align: center !important;
}
.visual-question p {
    color: #5f6f83 !important;
    margin: .65rem auto 0 auto;
    max-width: 760px;
    text-align: center !important;
}
.tarifa-choice-card {
    background: #ffffff;
    border-radius: 26px;
    padding: 1rem 1rem 1.1rem 1rem;
    min-height: 190px;
    border: 1px solid #e6edf7;
    box-shadow: 0 16px 34px rgba(15,40,75,0.08);
    margin-bottom: .75rem;
}
.tarifa-choice-card.selected {
    border: 2px solid #fb8500;
    box-shadow: 0 18px 40px rgba(251,133,0,.18);
    background: linear-gradient(135deg, #fff7eb 0%, #ffffff 100%);
}
.tarifa-choice-card strong {
    color: #0f2742 !important;
    display:block;
    font-size: 1.02rem;
    margin-bottom:.5rem;
}
.tarifa-choice-card span {
    color: #5f6f83 !important;
    font-size: .88rem;
    line-height: 1.55;
}
.centered-note {
    text-align:center;
    color:#5f6f83 !important;
    margin: .4rem auto 1rem auto;
}
div.stButton > button {
    border-radius: 999px !important;
    border: 0 !important;
    background: #0f2742 !important;
    color: white !important;
    font-weight: 900 !important;
    padding: .65rem 1.1rem !important;
    box-shadow: 0 12px 26px rgba(15,40,75,.18) !important;
}
div.stButton > button:hover {
    transform: translateY(-1px);
    background: #fb8500 !important;
    color: #102a43 !important;
}
.timeline-card {
    background:#ffffff;
    border-radius: 28px;
    padding: 1rem 1.2rem;
    border: 1px solid #e6edf7;
    box-shadow: 0 12px 28px rgba(15,40,75,.07);
    margin-bottom: 1rem;
}

.executive-card {
    background: linear-gradient(135deg, #ffffff 0%, #f5fbff 100%);
    border: 1px solid #e6edf7;
    border-radius: 28px;
    padding: 1.2rem 1.35rem;
    box-shadow: 0 14px 32px rgba(15,40,75,.08);
    min-height: 155px;
}
.report-download-card {
    background: linear-gradient(135deg, #0f2742 0%, #1f4e79 100%);
    color: white !important;
    border-radius: 30px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 18px 42px rgba(15,40,75,.20);
    margin: 1rem 0;
}
.report-download-card h3, .report-download-card p { color:white !important; }
.executive-card b { color:#0f2742 !important; font-size:1.02rem; }
.executive-card p { color:#5f6f83 !important; font-size:.92rem; line-height:1.55; margin-top:.45rem; }
.agent-card {
    background: linear-gradient(135deg, #0f2742 0%, #183b60 100%);
    border-radius: 30px;
    padding: 1.4rem 1.6rem;
    color: white !important;
    box-shadow: 0 18px 42px rgba(15,40,75,.22);
    margin-top: 1rem;
}
.agent-card h3, .agent-card p, .agent-card li { color: white !important; }


.time-settings-box {
    max-width: 920px;
    margin: 0 auto 1rem auto;
}
.panel-layout-wrap {
    background: linear-gradient(135deg, #f8fbff, #fff7df);
    border: 1px solid #e5ecf6;
    border-radius: 34px;
    padding: 1.4rem;
    box-shadow: 0 14px 36px rgba(15,40,75,0.08);
}
.panel-field {
    background: #d7ecff;
    border: 2px dashed rgba(67,97,238,0.35);
    border-radius: 26px;
    padding: 18px;
    overflow: auto;
}
.panel-row-vis {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
    align-items: center;
}
.solar-panel-vis {
    min-width: 54px;
    width: 54px;
    height: 34px;
    border-radius: 8px;
    background: linear-gradient(135deg, #0f2742, #4361ee);
    border: 2px solid rgba(255,255,255,0.75);
    box-shadow: 0 6px 14px rgba(15,40,75,0.18);
    position: relative;
}
.solar-panel-vis:before {
    content: "";
    position: absolute;
    inset: 6px;
    border-top: 1px solid rgba(255,255,255,0.5);
    border-bottom: 1px solid rgba(255,255,255,0.5);
}
.solar-panel-vis:after {
    content: "";
    position: absolute;
    top: 4px;
    bottom: 4px;
    left: 50%;
    border-left: 1px solid rgba(255,255,255,0.55);
}
.recommendation-box {
    background: white;
    border-radius: 28px;
    padding: 1.2rem 1.4rem;
    border: 1px solid #dfe8f5;
    box-shadow: 0 12px 26px rgba(15,40,75,0.08);
}
.agent-card strong { color: #ffb703; }


.visual-question-open {
    background: linear-gradient(135deg, #fff7eb 0%, #ffffff 100%) !important;
    border: 1px solid rgba(251,133,0,.28) !important;
}
.panel-mode-label {
    text-align:center;
    font-weight:900;
    color:#0f2742;
    background:white;
    border:1px solid #e6edf7;
    border-radius:999px;
    padding:.55rem 1rem;
    width:max-content;
    margin:0 auto .85rem auto;
    box-shadow:0 10px 22px rgba(15,40,75,.08);
}
.panel-field-normal { background: linear-gradient(135deg, #d7ecff, #eef8ff); }
.panel-field-compact { background: linear-gradient(135deg, #e9f8ef, #f6fff8); border-color: rgba(46,125,50,.35); }
.panel-field-manual { background: linear-gradient(135deg, #fff3df, #fffaf0); border-color: rgba(251,133,0,.40); }
.panel-row-vis { gap: var(--panel-gap, 10px) !important; margin-bottom: var(--row-gap, 10px) !important; justify-content:center; }
.panel-field-compact .solar-panel-vis { border-radius:4px; box-shadow:0 4px 9px rgba(15,40,75,.12); }
.panel-field-manual .solar-panel-vis { transform: rotate(-1deg); }
.report-hero {
    background: linear-gradient(135deg, #0f2742 0%, #1f4e79 62%, #fb8500 160%);
    color:white !important;
    padding:2rem 2.2rem;
    border-radius:34px;
    box-shadow:0 22px 52px rgba(15,40,75,.24);
    margin:1rem 0 1.2rem 0;
}
.report-hero h2, .report-hero p { color:white !important; text-align:center !important; }
.report-hero h2 { font-size:2rem; margin:0 0 .4rem 0; }
.report-pill-row { display:flex; gap:.75rem; justify-content:center; flex-wrap:wrap; margin-top:1rem; }
.report-pill { background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.24); padding:.55rem .9rem; border-radius:999px; color:white; font-weight:800; }
.executive-report-paper {
    background:#ffffff;
    border:1px solid #e6edf7;
    border-radius:34px;
    padding:2rem 2.2rem;
    box-shadow:0 18px 46px rgba(15,40,75,.10);
    max-width:1050px;
    margin: 0 auto 1.2rem auto;
}
.executive-report-paper p {
    color:#334e68 !important;
    text-align:justify !important;
    line-height:1.82 !important;
    font-size:1.02rem !important;
    margin:0 0 1rem 0 !important;
}
.executive-report-paper .lead {
    font-size:1.12rem !important;
    color:#0f2742 !important;
    font-weight:650;
}
.report-kpi-strip { display:grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap:.8rem; margin:1rem 0 1.2rem 0; }
.report-kpi { background:#f7fbff; border:1px solid #e6edf7; border-radius:22px; padding:.9rem; text-align:center; }
.report-kpi b { display:block; color:#0f2742; font-size:1.15rem; }
.report-kpi span { color:#5f6f83; font-size:.82rem; }
@media (max-width: 900px) { .report-kpi-strip { grid-template-columns: repeat(2, minmax(0,1fr)); } }

</style>
""", unsafe_allow_html=True)


def visual_question(titulo, nota="", key="visualizar"):
    state_key = key
    button_key = f"{key}_btn"
    abierto = bool(st.session_state.get(state_key, False))
    etiqueta = "Ocultar" if abierto else "Visualizar"
    chip = "🟠 Sección desplegada" if abierto else "✨ Power up interactivo"

    st.markdown(f"""
    <div class="visual-question {'visual-question-open' if abierto else ''}">
        <h3>{titulo}</h3>
        <p>{nota}</p>
        <div class="power-chip">{chip}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.3, 1, 1.3])
    with c2:
        if st.button(etiqueta, key=button_key, use_container_width=True):
            st.session_state[state_key] = not abierto
            abierto = not abierto
            st.rerun()

    return abierto


def seleccionar_tarifa(tarifas, default="GDMTO - Gran Demanda Media Tensión Ordinaria"):
    if "tarifa_elegida" not in st.session_state:
        st.session_state.tarifa_elegida = default if default in tarifas else list(tarifas.keys())[0]
    nombres = list(tarifas.keys())
    cols = st.columns(len(nombres))
    for i, nombre in enumerate(nombres):
        datos = tarifas[nombre]
        selected = nombre == st.session_state.tarifa_elegida
        clase = "tarifa-choice-card selected" if selected else "tarifa-choice-card"
        with cols[i]:
            st.markdown(f"""
            <div class="{clase}" title="{datos['descripcion']}">
                <strong>{nombre}</strong>
                <span>{datos['descripcion']}<br><br><b>Valor usado:</b> ${datos['precio']:.2f}/kWh</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Elegir", key=f"tarifa_btn_{i}", use_container_width=True):
                st.session_state.tarifa_elegida = nombre
                st.rerun()
    return st.session_state.tarifa_elegida


def guardar_base_inputs(tipo_tarifa, precio_kwh, consumo_mensual_kwh, periodo_anios, fecha_referencia, dias_clima, anio_analisis, mes_analisis, vista_inicial):
    consumo_anual_kwh = consumo_mensual_kwh * 12
    gasto_anual_actual = consumo_anual_kwh * precio_kwh
    st.session_state["base_inputs"] = {
        "tipo_tarifa": tipo_tarifa,
        "precio_kwh": precio_kwh,
        "consumo_mensual_kwh": consumo_mensual_kwh,
        "consumo_anual_kwh": consumo_anual_kwh,
        "gasto_anual_actual": gasto_anual_actual,
        "periodo_anios": periodo_anios,
        "fecha_referencia": str(fecha_referencia),
        "dias_clima": dias_clima,
        "anio_analisis": anio_analisis,
        "mes_analisis": mes_analisis,
        "vista_inicial": vista_inicial,
    }
    return consumo_anual_kwh, gasto_anual_actual


tab_principal, tab_paneles, tab_diseno, tab_clima, tab_analisis, tab_apagones, tab_dashboard = st.tabs([
    "🏠 Principal",
    "☀️ Paneles solares",
    "🧩 Diseño de paneles",
    "🌤️ Diagnóstico climático",
    "📊 Gráficas y estadísticas",
    "⚡ Apagones",
    "📄 Reporte ejecutivo"
])
# Compatibilidad interna: se fusionan comparativo visual y gráficas técnicas en una sola pestaña.
tab_comparativo = tab_analisis
tab_tecnico = tab_analisis

with tab_principal:
    section_header("🏠", "Gasto eléctrico inicial", "Estimación de consumo y gasto actual.")

    st.markdown("""
    <div class="visual-question">
        <h3>¿Conoces tu consumo eléctrico?</h3>
        <p>Puedes estimarlo usando tu pago bimestral si no conoces tus kWh. Usa consumo mensual si ya tienes el dato del recibo.</p>
    </div>
    """, unsafe_allow_html=True)

    metodo_consumo = st.radio(
        "Selecciona una forma de captura",
        ["Usar pago bimestral en pesos", "Responder con consumo mensual en kWh"],
        horizontal=True,
        key="metodo_consumo"
    )

    anio_analisis = int(pd.Timestamp.today().year)
    mes_analisis = int(pd.Timestamp.today().month)
    fecha_referencia = pd.Timestamp.today().date()
    dias_clima = 7
    vista_inicial = "Día"
    periodo_anios = 10

    if metodo_consumo == "Usar pago bimestral en pesos":
        pago_bimestral = st.number_input("¿Cuánto pagas aproximadamente cada bimestre? ($ MXN)", min_value=0.0, value=29591.0, key="pago_bimestral")
        subsection("Selecciona tu tarifa CFE aproximada", "blue")
        tipo_tarifa = seleccionar_tarifa(tarifas_estimadas)
        precio_kwh = tarifas_estimadas[tipo_tarifa]["precio"]
        consumo_mensual_kwh = (pago_bimestral / precio_kwh) / 2 if precio_kwh > 0 else 0
    else:
        consumo_mensual_kwh = st.number_input("Consumo mensual aproximado (kWh)", min_value=0.0, value=9520.0, key="consumo_mensual")
        subsection("Selecciona tu tarifa CFE aproximada", "blue")
        st.markdown('<p class="centered-note">Aunque ya conozcas tus kWh, la tarifa permite estimar el gasto anual equivalente.</p>', unsafe_allow_html=True)
        tipo_tarifa = seleccionar_tarifa(tarifas_estimadas)
        precio_kwh = tarifas_estimadas[tipo_tarifa]["precio"]

    consumo_anual_kwh, gasto_anual_actual = guardar_base_inputs(tipo_tarifa, precio_kwh, consumo_mensual_kwh, periodo_anios, fecha_referencia, dias_clima, anio_analisis, mes_analisis, vista_inicial)

    st.caption(tarifas_estimadas[tipo_tarifa]["descripcion"])

    with st.expander("💡 Para saber más: ¿cómo se estimó el consumo y gasto?"):
        if metodo_consumo == "Responder con consumo mensual en kWh":
            st.markdown(f"""
            Se usa el consumo mensual capturado por el usuario: **{consumo_mensual_kwh:,.0f} kWh/mes**.  
            Gasto anual aproximado = consumo mensual × 12 × precio promedio por kWh.  
            **{consumo_mensual_kwh:,.0f} × 12 × ${precio_kwh:.2f} = ${gasto_anual_actual:,.0f} MXN/año**.
            """)
        else:
            st.markdown(f"""
            Como no se conoce el consumo, se estima desde el pago bimestral:  
            **consumo mensual = pago bimestral / precio kWh / 2**  
            **{pago_bimestral:,.0f} / {precio_kwh:.2f} / 2 = {consumo_mensual_kwh:,.0f} kWh/mes**.
            """)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(bubble("Consumo mensual", f"{consumo_mensual_kwh:,.0f} kWh", "Base del escenario"), unsafe_allow_html=True)
    with c2: st.markdown(bubble("Consumo anual", f"{consumo_anual_kwh:,.0f} kWh", "Mensual × 12"), unsafe_allow_html=True)
    with c3: st.markdown(bubble("Gasto anual", f"${gasto_anual_actual:,.0f}", "Estimación sin paneles"), unsafe_allow_html=True)
    with c4: st.markdown(bubble("Tarifa usada", f"${precio_kwh:.2f}/kWh", tipo_tarifa), unsafe_allow_html=True)

with tab_paneles:
    if visual_question("¿Te gustaría ver cómo cambiaría tu consumo con paneles solares?", "Aquí aparecen propiedades del panel, ubicación, cobertura, número de paneles, área requerida y reducción estimada del recibo.", key="ver_paneles"):
        base = st.session_state.get("base_inputs", {})
        consumo_mensual_kwh = base.get("consumo_mensual_kwh", 9520.0)
        consumo_anual_kwh = base.get("consumo_anual_kwh", consumo_mensual_kwh * 12)
        precio_kwh = base.get("precio_kwh", 2.68)
        gasto_anual_actual = base.get("gasto_anual_actual", consumo_anual_kwh * precio_kwh)
        fecha_ref = pd.to_datetime(base.get("fecha_referencia", pd.Timestamp.today().date())).date()

        section_header("☀️", "Consumo con paneles solares", "Explora cuántos paneles serían necesarios para cubrir tu consumo y cómo cambiaría el recibo.")
        subsection("Ubicación del proyecto", "orange")
        metodo_ubicacion = st.radio("¿Cómo quieres elegir la ubicación?", ["Buscar en lista de ciudades", "Coordenadas / mapa"], horizontal=True, key="metodo_ubicacion")

        if metodo_ubicacion == "Buscar en lista de ciudades":
            ubicacion_elegida = st.selectbox("Busca o selecciona una ciudad", ubicaciones_selector["nombre"], key="ubicacion_elegida")
            ubicacion = ubicaciones_selector[ubicaciones_selector["nombre"] == ubicacion_elegida].iloc[0]
            latitud = float(ubicacion["latitud"]); longitud = float(ubicacion["longitud"]); altitud = float(ubicacion["altitud"])
            nombre_ubicacion = ubicacion_elegida; tipo_ubicacion = ubicacion["tipo_dato"]
        else:
            st.info("Puedes escribir coordenadas manualmente o hacer clic en el mapa para actualizar el punto seleccionado.")
            c1, c2, c3 = st.columns(3)
            with c1: st.session_state.lat_manual = st.number_input("Latitud", value=float(st.session_state.lat_manual), format="%.6f")
            with c2: st.session_state.lon_manual = st.number_input("Longitud", value=float(st.session_state.lon_manual), format="%.6f")
            with c3: st.session_state.alt_manual = st.number_input("Altitud aproximada (m)", value=float(st.session_state.alt_manual))
            latitud = st.session_state.lat_manual; longitud = st.session_state.lon_manual; altitud = st.session_state.alt_manual
            nombre_ubicacion = "Ubicación manual"; tipo_ubicacion = "Editable"
            mapa = folium.Map(location=[latitud, longitud], zoom_start=5, tiles="OpenStreetMap")
            folium.Marker([latitud, longitud], tooltip="📍 Ubicación seleccionada", popup=f"Lat: {latitud:.5f}, Lon: {longitud:.5f}", icon=folium.Icon(color="red", icon="map-marker", prefix="fa")).add_to(mapa)
            mapa_resultado = st_folium(mapa, height=450, width=None)
            if mapa_resultado and mapa_resultado.get("last_clicked"):
                st.session_state.lat_manual = mapa_resultado["last_clicked"]["lat"]
                st.session_state.lon_manual = mapa_resultado["last_clicked"]["lng"]
                st.success(f"Punto seleccionado: latitud {st.session_state.lat_manual:.5f}, longitud {st.session_state.lon_manual:.5f}. Recalculando con el nuevo punto...")
                st.rerun()

        inclinacion_recomendada = abs(latitud)
        orientacion_recomendada = orientacion_recomendada_por_ubicacion(latitud, longitud)

        r1, r2, r3, r4 = st.columns(4)
        with r1: st.markdown(bubble("Ubicación", nombre_ubicacion, tipo_ubicacion), unsafe_allow_html=True)
        with r2: st.markdown(bubble("Latitud", f"{latitud:.4f}", "Coordenada base"), unsafe_allow_html=True)
        with r3: st.markdown(bubble("Inclinación sugerida", f"{inclinacion_recomendada:.1f}°", "Se aplica en parámetros"), unsafe_allow_html=True)
        with r4: st.markdown(bubble("Orientación sugerida", f"{orientacion_recomendada:.0f}°", "Ajustada por ubicación"), unsafe_allow_html=True)

        subsection("Propiedades del panel", "yellow")
        tipo_panel = st.selectbox("Tipo técnico de panel", paneles_tecnicos["tipo"], key="tipo_panel")
        panel = paneles_tecnicos[paneles_tecnicos["tipo"] == tipo_panel].iloc[0]
        potencia_panel_kw = float(panel["potencia_kw"]); area_panel_m2 = float(panel["area_m2"]); eficiencia = float(panel["eficiencia"])
        st.info(panel["descripcion"])
        p1, p2, p3 = st.columns(3)
        with p1: st.markdown(bubble("Potencia por panel", f"{potencia_panel_kw:.3f} kW", "Propiedad técnica"), unsafe_allow_html=True)
        with p2: st.markdown(bubble("Área por panel", f"{area_panel_m2:.2f} m²", "Para estimar espacio"), unsafe_allow_html=True)
        with p3: st.markdown(bubble("Eficiencia", f"{eficiencia*100:.1f}%", "Energía respecto al área"), unsafe_allow_html=True)

        with st.expander("⚙️ Configuración avanzada"):
            st.write("Si no conoces estos datos, deja los valores estándar. La inclinación recomendada ya se aplica aquí.")
            t1, t2, t3 = st.columns(3)
            with t1:
                area_panel_m2 = st.number_input("Área por panel (m²)", value=float(area_panel_m2))
                eficiencia = st.number_input("Eficiencia", value=float(eficiencia))
            with t2:
                perdidas = st.number_input("Pérdidas del sistema", value=0.20)
            with t3:
                inclinacion_base = st.number_input("Inclinación recomendada/propuesta (°)", value=float(inclinacion_recomendada))
                orientacion_base = st.number_input("Orientación recomendada/propuesta (°)", value=float(orientacion_recomendada))

        objetivo_cobertura = st.slider("¿Qué porcentaje de tu consumo te gustaría intentar cubrir?", min_value=10, max_value=200, value=80, step=5)

        with st.spinner("Calculando generación solar estimada por panel..."):
            solar_1_panel = simular_solar(latitud=latitud, longitud=longitud, altitud=altitud, numero_paneles=1, potencia_panel_kw=potencia_panel_kw, area_panel_m2=area_panel_m2, eficiencia=eficiencia, perdidas=perdidas, inclinacion=inclinacion_base, orientacion=orientacion_base)
        energia_por_panel = solar_1_panel["energia_generada_anual"]
        energia_objetivo = consumo_anual_kwh * (objetivo_cobertura / 100)
        paneles_recomendados = int(np.ceil(energia_objetivo / energia_por_panel)) if energia_por_panel > 0 else 1
        usar_paneles_recomendados = st.checkbox(f"Usar recomendación automática: {paneles_recomendados} paneles", value=True)
        numero_paneles = paneles_recomendados if usar_paneles_recomendados else st.number_input("Número de paneles a simular", min_value=1, value=paneles_recomendados)

        solar = simular_solar(latitud=latitud, longitud=longitud, altitud=altitud, numero_paneles=numero_paneles, potencia_panel_kw=potencia_panel_kw, area_panel_m2=area_panel_m2, eficiencia=eficiencia, perdidas=perdidas, inclinacion=inclinacion_base, orientacion=orientacion_base)
        energia_aprovechada = min(solar["energia_generada_anual"], consumo_anual_kwh)
        cobertura = (energia_aprovechada / consumo_anual_kwh) * 100 if consumo_anual_kwh > 0 else 0
        ahorro_anual_estimado = energia_aprovechada * precio_kwh
        gasto_con_paneles = max(gasto_anual_actual - ahorro_anual_estimado, 0)
        reduccion_gasto = (ahorro_anual_estimado / gasto_anual_actual) * 100 if gasto_anual_actual > 0 else 0
        area_total_m2 = numero_paneles * area_panel_m2

        section_header("☀️", "Resultado técnico con paneles solares", "Resultados preliminares basados en ubicación, consumo, propiedades del panel y parámetros técnicos.")
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.markdown(bubble("Paneles simulados", f"{numero_paneles}", "Recomendados o manuales"), unsafe_allow_html=True)
        with k2: st.markdown(bubble("Generación anual", f"{solar['energia_generada_anual']:,.0f} kWh", "Producción estimada"), unsafe_allow_html=True)
        with k3: st.markdown(bubble("Reducción anual", f"${ahorro_anual_estimado:,.0f}", "Menor pago estimado"), unsafe_allow_html=True)
        with k4: st.markdown(bubble("Área mínima", f"{area_total_m2:,.1f} m²", "Solo paneles, sin pasillos"), unsafe_allow_html=True)
        st.progress(min(int(reduccion_gasto), 100))
        st.caption(f"Reducción aproximada del recibo: {reduccion_gasto:.1f}% | Cobertura energética usada: {cobertura:.1f}% | Fecha de referencia: {fecha_ref}")

        with st.expander("💡 Para saber más: ¿cómo se sugirió el número de paneles?"):
            st.markdown(f"""
            Generación por panel: **{energia_por_panel:,.1f} kWh/año**.  
            Energía objetivo: **{consumo_anual_kwh:,.0f} kWh × {objetivo_cobertura}% = {energia_objetivo:,.0f} kWh/año**.  
            Paneles recomendados: **{paneles_recomendados}**.
            """)

        st.session_state["solar_results"] = {
            "latitud": latitud, "longitud": longitud, "altitud": altitud, "nombre_ubicacion": nombre_ubicacion,
            "tipo_panel": tipo_panel, "potencia_panel_kw": potencia_panel_kw, "area_panel_m2": area_panel_m2,
            "eficiencia": eficiencia, "perdidas": perdidas, "inclinacion_base": inclinacion_base, "orientacion_base": orientacion_base,
            "numero_paneles": numero_paneles, "objetivo_cobertura": objetivo_cobertura, "energia_por_panel": energia_por_panel, "solar": solar,
            "energia_aprovechada": energia_aprovechada, "cobertura": cobertura, "ahorro_anual_estimado": ahorro_anual_estimado,
            "gasto_con_paneles": gasto_con_paneles, "reduccion_gasto": reduccion_gasto, "area_total_m2": area_total_m2,
            "clima_df": st.session_state.get("clima_df"), "factor_climatico": st.session_state.get("factor_climatico", 1.0)
        }


with tab_diseno:
    if visual_question("¿Te gustaría visualizar cómo se distribuirían los paneles?", "La app propone un acomodo inicial y tú puedes modificar filas, paneles por fila y separación para estimar área requerida.", key="ver_diseno_paneles"):
        res = st.session_state.get("solar_results")
        if not res:
            st.warning("Primero visualiza la pestaña de Paneles solares para conocer el número de paneles recomendado.")
        else:
            section_header("🧩", "Diseño visual de paneles", "Distribución preliminar para comunicar espacio requerido. No sustituye un plano estructural ni un levantamiento de sitio.")
            numero_paneles = int(res.get("numero_paneles", 1))
            area_panel_m2 = float(res.get("area_panel_m2", 2.35))
            ancho_panel_m = st.number_input("Ancho estimado por panel (m)", min_value=0.5, max_value=3.0, value=1.13, step=0.01)
            largo_panel_m = max(area_panel_m2 / ancho_panel_m, 0.1)
            modo_diseno = st.radio(
                "Elige cómo quieres ver la distribución",
                ["Distribución normal", "Optimizar espacio", "Manual"],
                horizontal=True
            )
            paneles_raiz = int(np.ceil(np.sqrt(numero_paneles))) if numero_paneles > 0 else 1
            filas_raiz = int(np.ceil(numero_paneles / paneles_raiz)) if paneles_raiz > 0 else 1
            if modo_diseno == "Distribución normal":
                filas = filas_raiz
                paneles_por_fila = paneles_raiz
                espacio_filas_m = 1.20
                espacio_paneles_m = 0.10
                st.info("Distribución balanceada: busca que el arreglo no quede demasiado largo ni demasiado ancho.")
            elif modo_diseno == "Optimizar espacio":
                # Acomodo compacto: paneles juntos, sin separación lateral ni entre filas.
                # Se busca una geometría cercana a cuadrada para que no quede una fila demasiado larga.
                paneles_por_fila = int(np.ceil(np.sqrt(numero_paneles))) if numero_paneles > 0 else 1
                filas = int(np.ceil(numero_paneles / paneles_por_fila)) if paneles_por_fila > 0 else 1
                espacio_filas_m = 0.0
                espacio_paneles_m = 0.0
                st.info("Optimización de espacio: paneles juntos, sin separación entre paneles. En un diseño real se puede agregar separación mínima por inclinación, mantenimiento o sombras.")
            else:
                c1, c2, c3 = st.columns(3)
                with c1:
                    filas = st.number_input("Número de filas", min_value=1, max_value=max(1, numero_paneles), value=max(1, filas_raiz), step=1)
                with c2:
                    paneles_por_fila = st.number_input("Paneles por fila", min_value=1, max_value=max(1, numero_paneles), value=max(1, paneles_raiz), step=1)
                with c3:
                    espacio_filas_m = st.number_input("Separación entre filas (m)", min_value=0.0, max_value=10.0, value=1.20, step=0.10)
                espacio_paneles_m = st.slider("Separación lateral entre paneles (m)", min_value=0.0, max_value=2.0, value=0.10, step=0.05)
            capacidad_layout = int(filas) * int(paneles_por_fila)
            if capacidad_layout < numero_paneles:
                st.error(f"Este acomodo solo muestra {capacidad_layout} paneles, pero el sistema requiere {numero_paneles}. Aumenta filas o paneles por fila.")
            ancho_total = paneles_por_fila * ancho_panel_m + max(paneles_por_fila - 1, 0) * espacio_paneles_m
            largo_total = filas * largo_panel_m + max(filas - 1, 0) * espacio_filas_m
            area_layout = ancho_total * largo_total
            area_solo_paneles = numero_paneles * area_panel_m2
            area_extra = max(area_layout - area_solo_paneles, 0)
            m1, m2, m3, m4 = st.columns(4)
            with m1: st.markdown(bubble("Paneles", f"{numero_paneles}", "Sistema calculado"), unsafe_allow_html=True)
            with m2: st.markdown(bubble("Área solo paneles", f"{area_solo_paneles:,.1f} m²", "Sin separación"), unsafe_allow_html=True)
            with m3: st.markdown(bubble("Huella estimada", f"{area_layout:,.1f} m²", "Con filas y separación"), unsafe_allow_html=True)
            with m4: st.markdown(bubble("Área adicional", f"{area_extra:,.1f} m²", "Separaciones/pasillos"), unsafe_allow_html=True)
            st.markdown('<div class="panel-layout-wrap centered-panel-layout">', unsafe_allow_html=True)
            st.markdown(render_panel_layout(filas, paneles_por_fila, numero_paneles, modo_diseno, espacio_paneles_m, espacio_filas_m), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption(f"Dimensión visual estimada: {ancho_total:.1f} m de ancho × {largo_total:.1f} m de largo. El dibujo es esquemático.")
            layout_df = pd.DataFrame([{
                "modo_diseno": modo_diseno, "paneles": numero_paneles, "filas": int(filas), "paneles_por_fila": int(paneles_por_fila),
                "separacion_filas_m": espacio_filas_m, "separacion_paneles_m": espacio_paneles_m,
                "ancho_total_m": ancho_total, "largo_total_m": largo_total,
                "area_layout_m2": area_layout, "area_solo_paneles_m2": area_solo_paneles
            }])
            st.session_state["layout_paneles"] = layout_df.iloc[0].to_dict()
            layout_bytes, layout_name, layout_mime = dataframe_to_download({"Diseño paneles": layout_df})
            st.download_button("📊 Descargar diseño de paneles", data=layout_bytes, file_name=layout_name, mime=layout_mime, key="descarga_layout_paneles")

with tab_clima:
    if visual_question("¿Te gustaría ver el diagnóstico climático de la ubicación?", "Nubosidad, lluvia, viento, temperatura y radiación estimada para interpretar el rendimiento solar.", key="ver_clima"):
        res = st.session_state.get("solar_results")
        if not res:
            st.warning("Primero visualiza la pestaña de Paneles solares para elegir una ubicación.")
        else:
            section_header("🌤️", "Diagnóstico climático", "El clima se consulta con Open-Meteo para la ubicación seleccionada. Es una lectura complementaria al modelo solar anual.")
            clima_df, factor_climatico = mostrar_modulo_clima(res["latitud"], res["longitud"])
            if clima_df is not None:
                st.session_state["clima_df"] = clima_df
                st.session_state["factor_climatico"] = factor_climatico
                if "solar_results" in st.session_state:
                    st.session_state["solar_results"]["clima_df"] = clima_df
                    st.session_state["solar_results"]["factor_climatico"] = factor_climatico

with tab_comparativo:
    if visual_question("¿Te gustaría comparar consumo normal, paneles y efecto del clima?", "Comparativo anual por meses: consumo, generación solar ideal y generación ajustada por climatología.", key="ver_comparativo"):
        base = st.session_state.get("base_inputs", {})
        res = st.session_state.get("solar_results")
        if not res:
            st.warning("Primero visualiza la pestaña de Paneles solares para generar resultados.")
        else:
            section_header("📊", "Comparativo visual y gráficas técnicas", "Una sola vista para comparar consumo, generación solar, efecto climático, balance mensual, heatmap anual y optimización 3D.")
            consumo_mensual = base.get("consumo_mensual_kwh", 0)
            precio = base.get("precio_kwh", 0)
            gasto_actual_anual = base.get("gasto_anual_actual", 0)
            df_solar = res["solar"]["df"]
            factores = FACTORES_CLIMA_MENSUAL_DEFAULT.copy()
            dfm = preparar_comparativo_mensual(df_solar, consumo_mensual, precio, factores)
            st.session_state["df_comparativo_mensual"] = dfm

            consumo_anual = dfm["consumo_kwh"].sum()
            solar_ideal = dfm["generacion_solar_kwh"].sum()
            solar_clima = dfm["generacion_ajustada_clima_kwh"].sum()
            castigo = dfm["castigo_clima_kwh"].sum()
            gasto_paneles_anual = dfm["gasto_con_paneles_mxn"].sum()
            gasto_clima_anual = dfm["gasto_con_clima_mxn"].sum()
            reduccion_clima = (1 - gasto_clima_anual / gasto_actual_anual) * 100 if gasto_actual_anual > 0 else 0

            m1, m2, m3, m4 = st.columns(4)
            with m1: st.markdown(bubble("Consumo anual", f"{consumo_anual:,.0f} kWh", "Base del usuario"), unsafe_allow_html=True)
            with m2: st.markdown(bubble("Solar ideal", f"{solar_ideal:,.0f} kWh", "Sin castigo climático"), unsafe_allow_html=True)
            with m3: st.markdown(bubble("Solar con clima", f"{solar_clima:,.0f} kWh", f"Castigo: {castigo:,.0f} kWh"), unsafe_allow_html=True)
            with m4: st.markdown(bubble("Reducción recibo", f"{reduccion_clima:.1f}%", "Con climatología mensual"), unsafe_allow_html=True)

            fig = fig_comparativo_anual(dfm)
            st.plotly_chart(fig, use_container_width=True)
            st.info("Puedes hacer zoom, seleccionar un rango de meses, pasar el cursor para ver cifras y hacer doble clic para regresar a la vista completa.")

            comp_bytes, comp_name, comp_mime = dataframe_to_download({"Comparativo mensual": dfm})
            st.download_button("📊 Descargar datos del comparativo", data=comp_bytes, file_name=comp_name, mime=comp_mime, key="descarga_comparativo")

            subsection("Efecto climático sobre la generación", "blue")
            fig_gasto = go.Figure()
            fig_gasto.add_trace(go.Bar(x=dfm["mes"], y=dfm["generacion_solar_kwh"], name="Solar sin clima", marker_color="#2a9d8f", hovertemplate="Mes: %{x}<br>%{y:,.0f} kWh<extra></extra>"))
            fig_gasto.add_trace(go.Bar(x=dfm["mes"], y=dfm["generacion_ajustada_clima_kwh"], name="Solar con clima", marker_color="#ffb703", hovertemplate="Mes: %{x}<br>%{y:,.0f} kWh<extra></extra>"))
            fig_gasto.add_trace(go.Scatter(x=dfm["mes"], y=dfm["castigo_clima_kwh"], name="Pérdida por clima", mode="lines+markers", line=dict(color="#4361ee", width=3), hovertemplate="Mes: %{x}<br>Pérdida: %{y:,.0f} kWh<extra></extra>"))
            fig_gasto.update_layout(title="La generación con clima siempre debe ser menor o igual a la generación ideal", xaxis_title="Mes", yaxis_title="Energía (kWh)", barmode="group", hovermode="x unified", height=500, plot_bgcolor="white", paper_bgcolor="white", legend=dict(orientation="h", y=1.02))
            st.plotly_chart(fig_gasto, use_container_width=True)

            subsection("Lectura ejecutiva del comparativo", "green")
            ahorro_clima_anual = max(gasto_actual_anual - gasto_clima_anual, 0)
            reduccion_clima_anual = (ahorro_clima_anual / gasto_actual_anual) * 100 if gasto_actual_anual else 0
            peor_mes = dfm.loc[dfm["factor_climatologico"].idxmin(), "mes"] if not dfm.empty else "N/D"
            mejor_mes = dfm.loc[dfm["generacion_ajustada_clima_kwh"].idxmax(), "mes"] if not dfm.empty else "N/D"
            e1, e2, e3 = st.columns(3)
            with e1:
                st.markdown(f'<div class="executive-card"><b>Impacto anual</b><p>Con climatología, el recibo anual estimado baja aproximadamente {reduccion_clima_anual:.1f}% frente al escenario sin paneles.</p></div>', unsafe_allow_html=True)
            with e2:
                st.markdown(f'<div class="executive-card"><b>Mes sensible</b><p>{peor_mes} es el mes con menor factor climatológico del supuesto actual. Conviene revisar nubosidad histórica local.</p></div>', unsafe_allow_html=True)
            with e3:
                st.markdown(f'<div class="executive-card"><b>Mes más favorable</b><p>{mejor_mes} muestra la mayor generación ajustada. Útil para explicar estacionalidad al usuario.</p></div>', unsafe_allow_html=True)

with tab_tecnico:
    if visual_question("¿Te gustaría ver las gráficas técnicas?", "Demanda vs generación, irradiancia, balance mensual y optimización 3D.", key="ver_tecnico"):
        res = st.session_state.get("solar_results")
        if not res:
            st.warning("Primero visualiza la pestaña de Paneles solares para tener datos solares calculados.")
        else:
            section_header("📈", "Gráficas técnicas del sistema", "Las curvas 2D muestran el día representativo; el balance mensual y el heatmap usan el año completo.")
            solar = res["solar"]; df = solar["df"]
            df_periodo, etiqueta_periodo = obtener_dia_representativo(df)
            st.caption(f"Periodo activo para gráficas 2D: {etiqueta_periodo}.")

            sub1, sub2, sub3, sub_heat, sub4 = st.tabs(["Demanda vs generación", "Irradiancia", "Balance mensual", "Heatmap anual", "Optimización 3D"])
            with sub1:
                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(x=df_periodo.index, y=df_periodo["demanda_kw"], mode="lines", name="Demanda", line=dict(color="#e63946", width=3), hovertemplate="Hora: %{x}<br>Demanda: %{y:.2f} kW<extra></extra>"))
                fig1.add_trace(go.Scatter(x=df_periodo.index, y=df_periodo["potencia_solar_kw"], mode="lines", name="Generación solar", fill="tozeroy", line=dict(color="#2a9d8f", width=3), hovertemplate="Hora: %{x}<br>Solar: %{y:.2f} kW<extra></extra>"))
                fig1.update_layout(title=f"Demanda vs generación solar - {etiqueta_periodo}", xaxis_title="Fecha y hora", yaxis_title="Potencia (kW)", hovermode="x unified", height=500, plot_bgcolor="white", paper_bgcolor="white", xaxis=dict(rangeslider=dict(visible=True)))
                st.plotly_chart(fig1, use_container_width=True)
                st.info("Esta gráfica permite ver si la producción solar ocurre cuando existe demanda eléctrica.")
                datos_demanda = df_periodo[["demanda_kw", "potencia_solar_kw", "demanda_restante_kw"]].reset_index().rename(columns={"index":"fecha"})
                b, n, m = dataframe_to_download({"Demanda generación": datos_demanda})
                st.download_button("📊 Descargar datos de esta gráfica", data=b, file_name=n, mime=m, key="descarga_tecnico_demanda")
            with sub2:
                fig2 = go.Figure()
                for col, name, color in [("ghi", "GHI - global horizontal", "#ffb703"), ("dni", "DNI - directa", "#fb8500"), ("dhi", "DHI - difusa", "#4361ee")]:
                    fig2.add_trace(go.Scatter(x=df_periodo.index, y=df_periodo[col], mode="lines", name=name, line=dict(color=color, width=3), hovertemplate=f"Hora: %{{x}}<br>{name}: %{{y:.1f}} W/m²<extra></extra>"))
                fig2.update_layout(title=f"Irradiancia solar disponible - {etiqueta_periodo}", xaxis_title="Fecha y hora", yaxis_title="Radiación (W/m²)", hovermode="x unified", height=500, plot_bgcolor="white", paper_bgcolor="white", xaxis=dict(rangeslider=dict(visible=True)))
                st.plotly_chart(fig2, use_container_width=True)
                st.info("GHI incluye radiación total horizontal; DNI es radiación directa; DHI es radiación difusa por nubes/atmósfera.")
                datos_irr = df_periodo[["ghi", "dni", "dhi"]].reset_index().rename(columns={"index":"fecha"})
                b, n, m = dataframe_to_download({"Irradiancia": datos_irr})
                st.download_button("📊 Descargar datos de esta gráfica", data=b, file_name=n, mime=m, key="descarga_tecnico_irr")
            with sub3:
                energia_mensual = df[["potencia_solar_kw", "demanda_kw", "demanda_restante_kw"]].resample("ME").sum() * 0.25
                energia_mensual["mes"] = energia_mensual.index.strftime("%b")
                fig3 = go.Figure()
                fig3.add_trace(go.Bar(x=energia_mensual["mes"], y=energia_mensual["demanda_kw"], name="Consumo modelado", marker_color="#e63946", hovertemplate="Mes: %{x}<br>Consumo: %{y:,.0f} kWh<extra></extra>"))
                fig3.add_trace(go.Bar(x=energia_mensual["mes"], y=energia_mensual["potencia_solar_kw"], name="Generación solar", marker_color="#2a9d8f", hovertemplate="Mes: %{x}<br>Solar: %{y:,.0f} kWh<extra></extra>"))
                fig3.add_trace(go.Scatter(x=energia_mensual["mes"], y=energia_mensual["demanda_restante_kw"], mode="lines+markers", name="Energía de red", line=dict(color="#0f2742", width=3), hovertemplate="Mes: %{x}<br>Red: %{y:,.0f} kWh<extra></extra>"))
                objetivo_cobertura = float(res.get("objetivo_cobertura", 100))
                energia_mensual["objetivo_cobertura_kwh"] = energia_mensual["demanda_kw"] * (objetivo_cobertura / 100)
                fig3.add_trace(go.Scatter(x=energia_mensual["mes"], y=energia_mensual["objetivo_cobertura_kwh"], mode="lines+markers", name=f"Objetivo de cobertura {objetivo_cobertura:.0f}%", line=dict(color="#fb8500", width=3, dash="dot"), hovertemplate="Mes: %{x}<br>Objetivo: %{y:,.0f} kWh<extra></extra>"))
                fig3.update_layout(title=f"Balance energético mensual - objetivo de cobertura {objetivo_cobertura:.0f}%", xaxis_title="Mes", yaxis_title="Energía (kWh)", barmode="group", hovermode="x unified", height=500, plot_bgcolor="white", paper_bgcolor="white")
                st.plotly_chart(fig3, use_container_width=True)
                st.caption(f"El objetivo de cobertura configurado fue {objetivo_cobertura:.0f}%, por eso se incluye como línea de referencia.")
                b, n, m = dataframe_to_download({"Balance mensual": energia_mensual.reset_index().rename(columns={"index":"fecha"})})
                st.download_button("📊 Descargar balance mensual", data=b, file_name=n, mime=m, key="descarga_balance_mensual")
            with sub_heat:
                heatmap_df, fig_heat = crear_heatmap_generacion_anual(df)
                st.plotly_chart(fig_heat, use_container_width=True)
                st.info("Columnas: enero a diciembre. Filas: 0:00 a 23:00. Color: energía promedio generada por intervalo horario en kWh.")
                st.session_state["heatmap_generacion"] = heatmap_df
                b, n, m = dataframe_to_download({"Heatmap generación": heatmap_df})
                st.download_button("📊 Descargar heatmap", data=b, file_name=n, mime=m, key="descarga_heatmap")
            with sub4:
                st.write("La gráfica 3D tarda más porque evalúa combinaciones de inclinación y orientación.")
                if st.button("Generar gráfica 3D de ángulo óptimo"):
                    paso = 10
                    orientaciones = np.arange(0, 360 + paso, paso); inclinaciones = np.arange(0, 90 + paso, paso)
                    resultados = np.zeros((len(inclinaciones), len(orientaciones)))
                    with st.spinner("Calculando optimización..."):
                        for i, inc in enumerate(inclinaciones):
                            for j, ori in enumerate(orientaciones):
                                sim = simular_solar(latitud=res["latitud"], longitud=res["longitud"], altitud=res["altitud"], numero_paneles=1, potencia_panel_kw=res["potencia_panel_kw"], area_panel_m2=res["area_panel_m2"], eficiencia=res["eficiencia"], perdidas=res["perdidas"], inclinacion=inc, orientacion=ori)
                                resultados[i, j] = sim["energia_generada_anual"]
                    maximo = np.max(resultados); coord = np.unravel_index(np.argmax(resultados), resultados.shape)
                    inc_opt = inclinaciones[coord[0]]; ori_opt = orientaciones[coord[1]]
                    fig4 = go.Figure(data=[go.Surface(x=orientaciones, y=inclinaciones, z=resultados, colorscale="Viridis", hovertemplate="Orientación: %{x}°<br>Inclinación: %{y}°<br>Energía: %{z:,.0f} kWh/año<extra></extra>")])
                    fig4.update_layout(title="Energía generada por inclinación y orientación", scene=dict(xaxis_title="Orientación (°)", yaxis_title="Inclinación (°)", zaxis_title="kWh/año"), height=650, paper_bgcolor="white")
                    st.plotly_chart(fig4, use_container_width=True)
                    o1, o2, o3 = st.columns(3)
                    o1.metric("Inclinación óptima", f"{inc_opt:.1f}°"); o2.metric("Orientación óptima", f"{ori_opt:.1f}°"); o3.metric("Energía máxima/panel", f"{maximo:,.0f} kWh/año")

with tab_dashboard:
    if visual_question("¿Te gustaría generar el reporte ejecutivo?", "Integra la lectura ejecutiva, resultados principales y descargas en PDF/Excel desde esta misma pestaña.", key="ver_dashboard"):
        res = st.session_state.get("solar_results"); base = st.session_state.get("base_inputs", {})
        dfm = st.session_state.get("df_comparativo_mensual")
        if not res:
            st.warning("Primero visualiza Paneles solares y la pestaña Comparativo y gráficas para crear el reporte ejecutivo.")
        else:
            section_header("📄", "Reporte ejecutivo", "Resumen formal de una herramienta exploratoria para evaluar generación fotovoltaica, consumo, climatología y continuidad eléctrica.")
            gasto_anual_actual = float(base.get("gasto_anual_actual", 0))
            consumo_anual = float(base.get("consumo_anual_kwh", 0))
            consumo_mensual = float(base.get("consumo_mensual_kwh", 0))
            tarifa = base.get("tipo_tarifa", "No especificada")
            precio = float(base.get("precio_kwh", 0))
            cobertura = float(res.get("cobertura", 0))
            area = float(res.get("area_total_m2", 0))
            paneles = int(res.get("numero_paneles", 0))
            generacion = float(res.get("solar", {}).get("energia_generada_anual", 0))
            ubicacion = res.get("nombre_ubicacion", "Ubicación no especificada")
            tipo_panel = res.get("tipo_panel", "Panel no especificado")
            if isinstance(dfm, pd.DataFrame) and not dfm.empty:
                castigo = float(dfm["castigo_clima_kwh"].sum())
                peor_mes = str(dfm.loc[dfm["factor_climatologico"].idxmin(), "mes"])
                gasto_clima = float(dfm["gasto_con_clima_mxn"].sum())
                reduccion_clima = (1 - gasto_clima / gasto_anual_actual) * 100 if gasto_anual_actual else 0
            else:
                castigo = 0.0
                peor_mes = "No calculado"
                reduccion_clima = float(res.get("reduccion_gasto", 0))

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Paneles", f"{paneles}")
            c2.metric("Cobertura", f"{cobertura:.1f}%")
            c3.metric("Área aprox.", f"{area:,.1f} m²")
            c4.metric("Reducción estimada", f"{reduccion_clima:.1f}%")

            reporte_texto = f"""
            Explorador Solar es una herramienta digital de diagnóstico preliminar para que usuarios residenciales, comercios e industrias comprendan cómo podría comportarse un sistema fotovoltaico antes de solicitar una ingeniería o cotización formal. En este escenario, el proyecto se evaluó para {ubicacion}, con una tarifa de referencia {tarifa}, un precio promedio usado de ${precio:.2f}/kWh, un consumo mensual estimado de {consumo_mensual:,.0f} kWh y un consumo anual aproximado de {consumo_anual:,.0f} kWh. La propuesta no vende una solución cerrada; ofrece una lectura clara del consumo, generación solar, efecto climatológico, área requerida y riesgos por interrupciones eléctricas para apoyar una primera toma de decisiones.

            El servicio se diferencia porque integra en una misma interfaz estimación de recibo, selección simplificada de tarifa, simulación solar por ubicación, características técnicas de paneles, análisis de climatología, diseño visual del acomodo de paneles, comparación anual y una lectura preliminar de continuidad eléctrica. Su ventaja competitiva es convertir cálculos técnicos en resultados visuales comprensibles para personas sin formación especializada, pero manteniendo suficiente profundidad para empresas que necesitan explorar escenarios de energía, resiliencia y reducción del consumo de red.

            La visión del proyecto es convertirse en una herramienta accesible para explorar escenarios solares y de continuidad energética antes de invertir tiempo en estudios avanzados. Su misión es facilitar que cualquier usuario pueda estimar consumo, generación, cobertura, área necesaria y sensibilidad climática de forma ordenada, visual y transparente. La oportunidad se justifica porque muchas decisiones energéticas se toman sin entender la relación entre consumo real, ubicación, clima, número de paneles, espacio disponible y criticidad operativa ante apagones.

            Con los datos actuales, el sistema simula {paneles} paneles tipo {tipo_panel}, una generación anual aproximada de {generacion:,.0f} kWh y una cobertura útil cercana a {cobertura:.1f}% del consumo. El análisis climático preliminar estima una pérdida anual de {castigo:,.0f} kWh respecto al escenario ideal, con {peor_mes} como mes más sensible bajo los factores utilizados. Esto sugiere que el usuario debe revisar recibos históricos, sombras, área real disponible, orientación, inclinación, perfil horario de consumo y cargas críticas antes de avanzar hacia ingeniería de detalle.

            Como estrategia, la herramienta debe usarse primero para dimensionar un escenario base, después para comparar generación ideal contra generación afectada por clima, posteriormente para revisar distribución física de paneles y finalmente para analizar continuidad eléctrica si existen pérdidas por apagones. El equipo de trabajo requerido para llevar el proyecto a una fase real incluiría perfil técnico fotovoltaico, análisis eléctrico, levantamiento de sitio, revisión estructural y validación financiera externa. En esta versión no se presenta inversión requerida ni rentabilidad por cotización, porque el alcance evita precios de instalación; la rentabilidad se expresa como reducción estimada del recibo y energía de red evitada.

            El impacto ambiental esperado es favorable al reducir consumo eléctrico de red y desplazar parte de la demanda hacia generación solar. Para controlarlo correctamente se recomienda evaluar vida útil de equipos, disposición de paneles al final de vida, selección de baterías cuando aplique y mantenimiento preventivo. En conclusión, Explorador Solar no sustituye una ingeniería profesional, pero sí permite identificar si un escenario fotovoltaico tiene sentido preliminar, qué variables son más sensibles y qué información debe levantarse antes de tomar una decisión técnica o económica.
            """
            st.markdown(f"""
            <div class="report-hero">
                <h2>Reporte ejecutivo · Explorador Solar</h2>
                <p>Lectura ejecutiva preliminar con consumo, generación, climatología, distribución física y continuidad eléctrica.</p>
                <div class="report-pill-row">
                    <div class="report-pill">📍 {ubicacion}</div>
                    <div class="report-pill">☀️ {paneles} paneles</div>
                    <div class="report-pill">⚡ {cobertura:.1f}% cobertura</div>
                    <div class="report-pill">📐 {area:,.1f} m² aprox.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="executive-report-paper">
                <div class="report-kpi-strip">
                    <div class="report-kpi"><b>{consumo_anual:,.0f}</b><span>kWh/año consumidos</span></div>
                    <div class="report-kpi"><b>{generacion:,.0f}</b><span>kWh/año solares</span></div>
                    <div class="report-kpi"><b>{reduccion_clima:.1f}%</b><span>reducción estimada</span></div>
                    <div class="report-kpi"><b>{peor_mes}</b><span>mes climático sensible</span></div>
                </div>
                <p class="lead">{reporte_texto.strip().split(chr(10)+chr(10))[0].strip()}</p>
                <p>{'</p><p>'.join([p.strip() for p in reporte_texto.strip().split(chr(10)+chr(10))[1:] if p.strip()])}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="report-download-card"><h3>Descargas ejecutivas</h3><p>El PDF se genera con este contenido narrativo y una tabla de indicadores. El Excel concentra los datos usados por el reporte.</p></div>', unsafe_allow_html=True)

            resumen = {
                "Ubicación": ubicacion,
                "Tarifa": tarifa,
                "Precio kWh usado": precio,
                "Consumo mensual kWh": consumo_mensual,
                "Consumo anual kWh": consumo_anual,
                "Gasto anual actual": gasto_anual_actual,
                "Tipo panel": tipo_panel,
                "Número paneles": paneles,
                "Generación anual kWh": generacion,
                "Cobertura %": cobertura,
                "Área total m2": area,
                "Castigo clima kWh": castigo,
                "Mes más sensible": peor_mes,
                "Reducción estimada %": reduccion_clima,
            }
            resumen_df = pd.DataFrame([resumen])
            sheets = {"Resumen ejecutivo": resumen_df}
            if isinstance(dfm, pd.DataFrame) and not dfm.empty:
                sheets["Comparativo mensual"] = dfm
            if "layout_paneles" in st.session_state:
                sheets["Diseño paneles"] = pd.DataFrame([st.session_state["layout_paneles"]])
            if "apagones_results" in st.session_state:
                sheets["Apagones"] = pd.DataFrame([st.session_state["apagones_results"]])
            excel_bytes, excel_name, excel_mime = dataframe_to_download(sheets)
            pdf_bytes = generar_pdf_resumen({**resumen, "Resumen ejecutivo": reporte_texto})
            d1, d2 = st.columns(2)
            with d1:
                st.download_button("📊 Descargar datos del reporte", data=excel_bytes, file_name=excel_name, mime=excel_mime, key="descarga_reporte_excel")
            with d2:
                st.download_button("📄 Descargar reporte ejecutivo PDF", data=pdf_bytes, file_name="explorador_solar_reporte_ejecutivo.pdf", mime="application/pdf", key="descarga_reporte_pdf")

with tab_apagones:
    if visual_question("¿Te gustaría estimar el riesgo por interrupciones eléctricas?", "Se calcula energía crítica, pérdidas aproximadas, minutos de riesgo y tiempo de aviso necesario para actuar.", key="ver_apagones"):
        res = st.session_state.get("solar_results"); base = st.session_state.get("base_inputs", {})
        if not res:
            st.warning("Primero visualiza la pestaña de Paneles solares para estimar paneles equivalentes y consumo base.")
        else:
            section_header("⚡", "Riesgo eléctrico y energía de respaldo", "Esta sección no diseña baterías; solo ayuda a dimensionar energía crítica y valor económico de continuidad.")
            consumo_mensual_kwh = base.get("consumo_mensual_kwh", 0); energia_por_panel = res.get("energia_por_panel", 0)
            umbral_riesgo_min = st.number_input("¿A partir de cuántos minutos sin luz ya se vuelve un riesgo?", min_value=0.0, value=5.0)
            aviso_min = st.number_input("¿Con cuántos minutos de antelación necesitarías recibir aviso para actuar a tiempo?", min_value=0.0, value=10.0)
            modo_carga = st.radio("¿Sabes cuánta carga crítica necesitas proteger?", ["Sí, conozco la carga crítica en kW", "No, estimarla como porcentaje de mi consumo"], horizontal=True)
            if modo_carga == "Sí, conozco la carga crítica en kW":
                carga_critica_kw = st.number_input("Carga crítica a proteger (kW)", min_value=0.0, value=20.0)
            else:
                consumo_diario_kwh = consumo_mensual_kwh / 30 if consumo_mensual_kwh else 0
                consumo_promedio_kw = consumo_diario_kwh / 24 if consumo_diario_kwh else 0
                porcentaje_critico = st.slider("¿Qué porcentaje de tu consumo consideras crítico durante un apagón?", min_value=5, max_value=100, value=30, step=5)
                carga_critica_kw = consumo_promedio_kw * (porcentaje_critico / 100)
                st.caption(f"Potencia promedio: {consumo_promedio_kw:.2f} kW | carga crítica estimada: {carga_critica_kw:.2f} kW")

            with st.expander("💡 Para saber más: clasificación usada"):
                st.markdown("""
                - **Corto:** 1 a 5 minutos. Riesgo de reinicio o pérdida momentánea de control.  
                - **Medio:** 5 a 60 minutos. Riesgo de detener procesos o afectar equipos críticos.  
                - **Largo:** más de 60 minutos. Riesgo de continuidad operativa, conservación o producción.
                """)
            c1, c2, c3 = st.columns(3)
            with c1:
                apagones_cortos = st.number_input("Apagones cortos por año", min_value=0, value=24)
                duracion_corto_min = st.number_input("Duración corto (min)", min_value=0.0, value=3.0)
            with c2:
                apagones_medios = st.number_input("Apagones medios por año", min_value=0, value=12)
                duracion_medio_min = st.number_input("Duración medio (min)", min_value=0.0, value=30.0)
            with c3:
                apagones_largos = st.number_input("Apagones largos por año", min_value=0, value=3)
                duracion_largo_min = st.number_input("Duración largo (min)", min_value=0.0, value=120.0)
            horas_respaldo_anual = apagones_cortos*duracion_corto_min/60 + apagones_medios*duracion_medio_min/60 + apagones_largos*duracion_largo_min/60
            energia_respaldo_kwh = carga_critica_kw * horas_respaldo_anual
            paneles_equivalentes_respaldo = int(np.ceil(energia_respaldo_kwh / energia_por_panel)) if energia_por_panel > 0 else 0
            a1, a2, a3, a4 = st.columns(4)
            a1.metric("Minutos de riesgo", f"> {umbral_riesgo_min:.0f} min")
            a2.metric("Aviso deseado", f"{aviso_min:.0f} min antes")
            a3.metric("Energía crítica", f"{energia_respaldo_kwh:,.1f} kWh/año")
            a4.metric("Paneles equivalentes", f"{paneles_equivalentes_respaldo}")
            p1, p2 = st.columns(2)
            st.warning("Para continuidad real se requieren baterías, inversor híbrido y estrategia de respaldo. Los paneles por sí solos no sostienen cargas durante un apagón.")

            with st.expander("🤖 Agente preliminar de continuidad"):
                st.caption("El agente interpreta lo que ya capturaste en la interfaz y genera una lectura preliminar.")
                contexto_agente = "Análisis automático con datos de consumo, paneles, cobertura, apagones, pérdidas y carga crítica capturados en la app."
                autonomia_evento_h = max((umbral_riesgo_min + aviso_min) / 60, duracion_medio_min / 60, duracion_largo_min / 60, 0.25)
                bateria_recomendada_kwh = carga_critica_kw * autonomia_evento_h * 1.20
                baterias_modulo_kwh = 10.0
                modulos_bateria = int(np.ceil(bateria_recomendada_kwh / baterias_modulo_kwh)) if baterias_modulo_kwh > 0 else 0
                objetivo_paneles = res.get("objetivo_cobertura", 100)
                cobertura_actual = res.get("cobertura", 0)
                paneles_actuales = res.get("numero_paneles", 0)
                generacion_anual = res.get("solar", {}).get("energia_generada_anual", 0)
                paneles_extra = 0
                if cobertura_actual < objetivo_paneles and res.get("energia_por_panel", 0) > 0:
                    deficit_kwh = max((base.get("consumo_anual_kwh", 0) * objetivo_paneles / 100) - generacion_anual, 0)
                    paneles_extra = int(np.ceil(deficit_kwh / res.get("energia_por_panel", 1)))
                recomendaciones = []
                recomendaciones.append("La planta debería operar conectada a CFE; ante una interrupción, un inversor híbrido/UPS industrial debe transferir automáticamente las cargas críticas a batería.")
                recomendaciones.append(f"Con los datos actuales, la batería útil preliminar sería de al menos {bateria_recomendada_kwh:,.1f} kWh para cubrir {autonomia_evento_h:.2f} h. Como referencia interna, equivale a {modulos_bateria} módulo(s) de 10 kWh útiles.")
                if paneles_extra > 0:
                    recomendaciones.append(f"La cobertura solar actual ({cobertura_actual:.1f}%) queda por debajo del objetivo ({objetivo_paneles:.0f}%). Antes de sobredimensionar baterías, conviene revisar agregar aproximadamente {paneles_extra} panel(es) y después dimensionar el banco de baterías.")
                else:
                    recomendaciones.append(f"La cobertura solar estimada ({cobertura_actual:.1f}%) está alineada con el objetivo de {objetivo_paneles:.0f}%. La prioridad deja de ser agregar paneles y pasa a ser respaldo: baterías, inversor híbrido, tablero de cargas críticas y transferencia automática.")
                if aviso_min <= umbral_riesgo_min:
                    recomendaciones.append("El tiempo de aviso está muy cerca del umbral de riesgo. La acción humana puede no ser suficiente; conviene automatizar detección, transferencia y paro seguro.")
                else:
                    recomendaciones.append("El aviso declarado puede ayudar a operar protocolos, pero si el proceso pierde producto en pocos minutos, el respaldo debe ser automático, no manual.")
                recomendaciones.append("Siguiente paso técnico: levantar lista de cargas críticas por equipo, corriente de arranque, autonomía requerida por evento, tiempo de transferencia permitido y compatibilidad del inversor.")
                st.markdown('<div class="agent-card"><h3>Lectura del agente con tus datos</h3><ul>' + ''.join([f'<li>{r}</li>' for r in recomendaciones]) + '</ul></div>', unsafe_allow_html=True)
                st.session_state["agente_continuidad"] = {"bateria_recomendada_kwh": bateria_recomendada_kwh, "modulos_bateria": modulos_bateria, "paneles_extra_sugeridos": paneles_extra, "autonomia_evento_h": autonomia_evento_h, "recomendaciones": " | ".join(recomendaciones)}

            st.session_state["apagones_results"] = {"umbral_riesgo_min": umbral_riesgo_min, "aviso_min": aviso_min, "carga_critica_kw": carga_critica_kw, "horas_respaldo_anual": horas_respaldo_anual, "energia_respaldo_kwh": energia_respaldo_kwh, "paneles_equivalentes_respaldo": paneles_equivalentes_respaldo, "contexto_agente": contexto_agente, "bateria_recomendada_kwh": st.session_state.get("agente_continuidad", {}).get("bateria_recomendada_kwh", ""), "modulos_bateria": st.session_state.get("agente_continuidad", {}).get("modulos_bateria", ""), "paneles_extra_sugeridos": st.session_state.get("agente_continuidad", {}).get("paneles_extra_sugeridos", "")}



st.markdown("""
<style>
.centered-panel-layout, .centered-panel-layout .panel-field { display:flex; justify-content:center; align-items:center; flex-direction:column; margin-left:auto; margin-right:auto; }
.executive-card p { text-align: justify; line-height: 1.75; }
</style>
""", unsafe_allow_html=True)
