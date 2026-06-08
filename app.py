"""
AstroRisk — Dashboard Interativo
Execute com: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import joblib
import os
import sys
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do arquivo .env

# Adiciona o diretório raiz ao path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ─── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="AstroRisk — NASA Asteroid Monitor",
    page_icon="☄️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS customizado ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

  html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace;
    background-color: #0A0E1A;
    color: #E0E8FF;
  }
  .stApp { background-color: #0A0E1A; }

  h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 2px;
  }

  .metric-card {
    background: linear-gradient(135deg, #0F1729 0%, #1A2340 100%);
    border: 1px solid #2A3A5A;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin: 5px;
  }
  .metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 900;
  }
  .metric-label {
    font-size: 0.8rem;
    color: #8899CC;
    margin-top: 5px;
    letter-spacing: 1px;
  }
  .danger { color: #FF4C4C; }
  .safe   { color: #4CFFB8; }
  .gold   { color: #FFD700; }

  .alert-danger {
    background: rgba(255, 76, 76, 0.15);
    border: 2px solid #FF4C4C;
    border-radius: 10px;
    padding: 15px 20px;
    font-family: 'Orbitron', monospace;
    color: #FF4C4C;
    font-size: 1.1rem;
    text-align: center;
    animation: pulse 1.5s infinite;
  }
  .alert-safe {
    background: rgba(76, 255, 184, 0.1);
    border: 2px solid #4CFFB8;
    border-radius: 10px;
    padding: 15px 20px;
    font-family: 'Orbitron', monospace;
    color: #4CFFB8;
    font-size: 1.1rem;
    text-align: center;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
  }

  .stSlider > div > div { background-color: #1E2A3A !important; }
  .stButton > button {
    background: linear-gradient(135deg, #1A3A6A, #0A1A3A);
    color: #4CFFB8;
    border: 1px solid #4CFFB8;
    border-radius: 8px;
    font-family: 'Orbitron', monospace;
    letter-spacing: 1px;
    padding: 10px 20px;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, #4CFFB8, #1A3A6A);
    color: #0A0E1A;
  }
  div[data-testid="stSidebar"] {
    background-color: #060A14;
    border-right: 1px solid #1E2A3A;
  }
</style>
""", unsafe_allow_html=True)

# ─── Funções auxiliares ───────────────────────────────────────────────────────
CORES = {
    "perigoso": "#FF4C4C",
    "seguro": "#4CFFB8",
    "fundo": "#0A0E1A",
    "grade": "#1E2A3A",
    "texto": "#E0E8FF",
    "destaque": "#FFD700",
}

plt.rcParams.update({
    "figure.facecolor": CORES["fundo"],
    "axes.facecolor": CORES["fundo"],
    "axes.edgecolor": CORES["grade"],
    "axes.labelcolor": CORES["texto"],
    "xtick.color": CORES["texto"],
    "ytick.color": CORES["texto"],
    "text.color": CORES["texto"],
    "grid.color": CORES["grade"],
    "grid.linestyle": "--",
    "grid.alpha": 0.5,
    "font.family": "monospace",
})


@st.cache_data(ttl=3600)
def buscar_dados_nasa(dias: int = 7) -> pd.DataFrame:
    """Busca dados da NASA NeoWs API com cache de 1 hora."""
    NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
    BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"

    data_fim = datetime.today()
    data_inicio = data_fim - timedelta(days=dias)

    params = {
        "start_date": data_inicio.strftime("%Y-%m-%d"),
        "end_date": data_fim.strftime("%Y-%m-%d"),
        "api_key": NASA_API_KEY,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        dados_brutos = response.json()
    except Exception as e:
        st.error(f"Erro ao acessar a API da NASA: {e}")
        return pd.DataFrame()

    asteroides = []
    for data, lista in dados_brutos.get("near_earth_objects", {}).items():
        for neo in lista:
            dm = neo["estimated_diameter"]["meters"]
            ap = neo["close_approach_data"][0] if neo["close_approach_data"] else {}
            asteroides.append({
                "id": neo["id"],
                "nome": neo["name"],
                "data_observacao": data,
                "diametro_min_m": round(dm["estimated_diameter_min"], 2),
                "diametro_max_m": round(dm["estimated_diameter_max"], 2),
                "diametro_medio_m": round((dm["estimated_diameter_min"] + dm["estimated_diameter_max"]) / 2, 2),
                "potencialmente_perigoso": int(neo["is_potentially_hazardous_asteroid"]),
                "velocidade_km_h": round(float(ap.get("relative_velocity", {}).get("kilometers_per_hour", 0)), 2),
                "distancia_km": round(float(ap.get("miss_distance", {}).get("kilometers", 0)), 2),
                "distancia_lunar": round(float(ap.get("miss_distance", {}).get("lunar", 0)), 4),
                "magnitude_absoluta": neo.get("absolute_magnitude_h", None),
                "url_nasa": neo.get("nasa_jpl_url", ""),
            })

    df = pd.DataFrame(asteroides).drop_duplicates(subset="id").reset_index(drop=True)
    return df


@st.cache_resource
def carregar_modelo():
    caminho = "data/modelo_astrorisk.pkl"
    if os.path.exists(caminho):
        return joblib.load(caminho)
    return None


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ☄️ AstroRisk")
    st.markdown("*NASA Asteroid Monitor*")
    st.markdown("---")

    pagina = st.radio(
        "Navegação",
        ["🏠 Visão Geral", "📊 Análise Exploratória", "🤖 Predição ML", "🔬 Dados Brutos"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    dias = st.slider("Janela de coleta (dias)", 1, 7, 7)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#556688;'>
    Dados: NASA NeoWs API<br>
    Modelo: Random Forest<br>
    FIAP Global Solution 2026.1
    </div>
    """, unsafe_allow_html=True)

# ─── Carrega dados ────────────────────────────────────────────────────────────
with st.spinner("Conectando à NASA..."):
    df = buscar_dados_nasa(dias)
modelo = carregar_modelo()

if df.empty:
    st.error("Não foi possível carregar dados da NASA. Verifique sua conexão.")
    st.stop()

# ─── PÁGINA: Visão Geral ──────────────────────────────────────────────────────
if pagina == "🏠 Visão Geral":
    st.markdown("# ☄️ ASTRORISK")
    st.markdown("### Sistema de Monitoramento e Classificação de Asteroides — NASA NeoWs")
    st.markdown("---")

    total = len(df)
    perigosos = int(df["potencialmente_perigoso"].sum())
    seguros = total - perigosos
    vel_max = df["velocidade_km_h"].max()
    dist_min = df["distancia_km"].min()

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, valor, label, cls in [
        (c1, total, "ASTEROIDES", "gold"),
        (c2, perigosos, "PERIGOSOS", "danger"),
        (c3, seguros, "SEGUROS", "safe"),
        (c4, f"{vel_max/1000:,.0f}k", "VEL. MÁX (km/h)", "gold"),
        (c5, f"{dist_min/1_000_000:.1f}M", "DIST. MÍN (km)", "safe"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
          <div class="metric-value {cls}">{valor}</div>
          <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Alerta de maior ameaça
    if perigosos > 0:
        pior = df[df["potencialmente_perigoso"] == 1].sort_values("distancia_km").iloc[0]
        st.markdown(f"""
        <div class="alert-danger">
        ⚠️ ALERTA — Asteroide mais próximo classificado como PERIGOSO:<br>
        <strong>{pior['nome']}</strong> — {pior['distancia_km']:,.0f} km da Terra
        &nbsp;|&nbsp; {pior['velocidade_km_h']:,.0f} km/h
        &nbsp;|&nbsp; ⌀ {pior['diametro_medio_m']:.0f} m
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-safe">✅ Nenhum asteroide perigoso detectado no período selecionado.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Gráfico rápido: scatter velocidade x distância
    col_g1, col_g2 = st.columns([3, 2])

    with col_g1:
        st.markdown("#### Velocidade × Distância da Terra")
        fig, ax = plt.subplots(figsize=(8, 4))
        cores_ponto = df["potencialmente_perigoso"].map({1: CORES["perigoso"], 0: CORES["seguro"]})
        ax.scatter(
            df["distancia_km"] / 1_000_000,
            df["velocidade_km_h"] / 1_000,
            c=cores_ponto, alpha=0.8,
            s=df["diametro_medio_m"] / 3 + 15,
            edgecolors="white", linewidths=0.3,
        )
        ax.set_xlabel("Distância da Terra (milhões km)")
        ax.set_ylabel("Velocidade (mil km/h)")
        ax.grid(True)
        patches = [
            mpatches.Patch(color=CORES["seguro"], label="Seguro"),
            mpatches.Patch(color=CORES["perigoso"], label="Perigoso"),
        ]
        ax.legend(handles=patches, frameon=False)
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with col_g2:
        st.markdown("#### Distribuição de Risco")
        fig, ax = plt.subplots(figsize=(4, 4))
        contagem = df["potencialmente_perigoso"].value_counts()
        ax.pie(
            contagem.values,
            colors=[CORES["seguro"], CORES["perigoso"]] if 0 in contagem.index else [CORES["perigoso"]],
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"edgecolor": CORES["fundo"], "linewidth": 3},
            pctdistance=0.75,
        )
        patches = [
            mpatches.Patch(color=CORES["seguro"], label="Seguro"),
            mpatches.Patch(color=CORES["perigoso"], label="Perigoso"),
        ]
        ax.legend(handles=patches, frameon=False, loc="lower center")
        st.pyplot(fig, use_container_width=True)
        plt.close()

# ─── PÁGINA: Análise Exploratória ────────────────────────────────────────────
elif pagina == "📊 Análise Exploratória":
    st.markdown("# 📊 Análise Exploratória")
    st.markdown("---")

    # Filtros
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filtro_perigo = st.selectbox("Filtrar por risco", ["Todos", "Perigosos", "Seguros"])
    with col_f2:
        max_dist = st.slider(
            "Distância máxima (milhões km)",
            float(df["distancia_km"].min() / 1e6),
            float(df["distancia_km"].max() / 1e6),
            float(df["distancia_km"].max() / 1e6),
        )

    df_filtrado = df[df["distancia_km"] <= max_dist * 1e6].copy()
    if filtro_perigo == "Perigosos":
        df_filtrado = df_filtrado[df_filtrado["potencialmente_perigoso"] == 1]
    elif filtro_perigo == "Seguros":
        df_filtrado = df_filtrado[df_filtrado["potencialmente_perigoso"] == 0]

    st.markdown(f"*{len(df_filtrado)} asteroides exibidos*")

    # Histograma diâmetros
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Distribuição de Diâmetros")
        fig, ax = plt.subplots(figsize=(6, 4))
        for label, grupo, cor in [
            ("Seguro", df_filtrado[df_filtrado["potencialmente_perigoso"] == 0], CORES["seguro"]),
            ("Perigoso", df_filtrado[df_filtrado["potencialmente_perigoso"] == 1], CORES["perigoso"]),
        ]:
            if not grupo.empty:
                ax.hist(grupo["diametro_medio_m"], bins=20, color=cor, alpha=0.7, label=label, edgecolor=CORES["fundo"])
        ax.set_xlabel("Diâmetro médio (m)")
        ax.set_ylabel("Quantidade")
        ax.legend(frameon=False)
        ax.grid(True, axis="y")
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with col2:
        st.markdown("#### Distribuição de Velocidades")
        fig, ax = plt.subplots(figsize=(6, 4))
        for label, grupo, cor in [
            ("Seguro", df_filtrado[df_filtrado["potencialmente_perigoso"] == 0], CORES["seguro"]),
            ("Perigoso", df_filtrado[df_filtrado["potencialmente_perigoso"] == 1], CORES["perigoso"]),
        ]:
            if not grupo.empty:
                ax.hist(grupo["velocidade_km_h"] / 1000, bins=20, color=cor, alpha=0.7, label=label, edgecolor=CORES["fundo"])
        ax.set_xlabel("Velocidade (mil km/h)")
        ax.set_ylabel("Quantidade")
        ax.legend(frameon=False)
        ax.grid(True, axis="y")
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # Heatmap correlação
    st.markdown("#### Mapa de Correlação")
    colunas = ["diametro_medio_m", "velocidade_km_h", "distancia_km",
               "distancia_lunar", "magnitude_absoluta", "potencialmente_perigoso"]
    corr = df_filtrado[colunas].corr()
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn", center=0,
                ax=ax, linewidths=0.5, linecolor=CORES["grade"], annot_kws={"size": 9})
    ax.set_title("Correlação entre variáveis")
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ─── PÁGINA: Predição ML ──────────────────────────────────────────────────────
elif pagina == "🤖 Predição ML":
    st.markdown("# 🤖 Predição de Risco — Machine Learning")
    st.markdown("Insira os dados de um asteroide para classificar o risco de impacto.")
    st.markdown("---")

    if modelo is None:
        st.warning("⚠️ Modelo não treinado. Execute `python src/modelo_ml.py` para treinar e salvar o modelo.")
    else:
        col_in1, col_in2 = st.columns(2)

        with col_in1:
            diametro = st.number_input("Diâmetro médio estimado (metros)", 1.0, 100000.0, 350.0, step=10.0)
            velocidade = st.number_input("Velocidade relativa (km/h)", 1000.0, 300000.0, 85000.0, step=1000.0)
            distancia = st.number_input("Distância da Terra (km)", 100000.0, 100_000_000.0, 1_500_000.0, step=100000.0)

        with col_in2:
            dist_lunar = st.number_input("Distância lunar (LD)", 0.1, 100.0, 3.9, step=0.1)
            magnitude = st.number_input("Magnitude absoluta (H)", 10.0, 35.0, 19.5, step=0.1)

        st.markdown("---")

        if st.button("☄️ CLASSIFICAR ASTEROIDE"):
            entrada = {
                "diametro_medio_m": diametro,
                "velocidade_km_h": velocidade,
                "distancia_km": distancia,
                "distancia_lunar": dist_lunar,
                "magnitude_absoluta": magnitude,
            }

            X_input = pd.DataFrame([entrada])
            prob = modelo.predict_proba(X_input)[0][1]
            classe = "PERIGOSO" if prob >= 0.5 else "SEGURO"

            st.markdown("---")
            if classe == "PERIGOSO":
                st.markdown(f"""
                <div class="alert-danger">
                ⚠️ CLASSIFICAÇÃO: <strong>PERIGOSO</strong><br>
                Probabilidade de risco: <strong>{prob*100:.1f}%</strong>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="alert-safe">
                ✅ CLASSIFICAÇÃO: <strong>SEGURO</strong><br>
                Probabilidade de risco: <strong>{prob*100:.1f}%</strong>
                </div>
                """, unsafe_allow_html=True)

            # Barra de probabilidade
            st.markdown("#### Nível de Ameaça")
            st.progress(float(prob))
            st.markdown(f"*Score de perigo: {prob:.4f}*")

# ─── PÁGINA: Dados Brutos ─────────────────────────────────────────────────────
elif pagina == "🔬 Dados Brutos":
    st.markdown("# 🔬 Dados Brutos — NASA NeoWs")
    st.markdown("---")

    st.markdown(f"**{len(df)} asteroides** coletados nos últimos **{dias} dias**")

    # Tabela interativa
    df_exibir = df.copy()
    df_exibir["risco"] = df_exibir["potencialmente_perigoso"].map({1: "⚠️ PERIGOSO", 0: "✅ SEGURO"})
    df_exibir["velocidade_km_h"] = df_exibir["velocidade_km_h"].apply(lambda x: f"{x:,.0f}")
    df_exibir["distancia_km"] = df_exibir["distancia_km"].apply(lambda x: f"{x:,.0f}")

    colunas_exibir = ["nome", "data_observacao", "risco", "diametro_medio_m",
                      "velocidade_km_h", "distancia_km", "distancia_lunar", "magnitude_absoluta"]
    st.dataframe(df_exibir[colunas_exibir], use_container_width=True, height=500)

    # Download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Baixar CSV completo",
        data=csv,
        file_name=f"astrorisk_asteroides_{datetime.today().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )
