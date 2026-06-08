"""
AstroRisk — Análise Exploratória de Dados (EDA)
Gera gráficos e estatísticas sobre os asteroides coletados da NASA.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os

# Paleta temática espacial
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


def carregar(caminho: str = "data/asteroides.csv") -> pd.DataFrame:
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}. Rode coletor_nasa.py primeiro.")
    return pd.read_csv(caminho)


def resumo_estatistico(df: pd.DataFrame) -> None:
    """Imprime resumo estatístico no terminal."""
    print("=" * 55)
    print("         ASTRORISK — RESUMO ESTATÍSTICO")
    print("=" * 55)
    print(f"  Total de asteroides analisados : {len(df)}")
    print(f"  Potencialmente perigosos       : {df['potencialmente_perigoso'].sum()}")
    print(f"  Seguros                        : {(df['potencialmente_perigoso'] == 0).sum()}")
    print(f"  Velocidade média (km/h)        : {df['velocidade_km_h'].mean():,.0f}")
    print(f"  Distância mínima Terra (km)    : {df['distancia_km'].min():,.0f}")
    print(f"  Diâmetro médio (m)             : {df['diametro_medio_m'].mean():.1f}")
    print("=" * 55)


def grafico_distribuicao_perigo(df: pd.DataFrame, salvar: bool = True) -> None:
    """Gráfico de pizza: proporção perigosos vs seguros."""
    fig, ax = plt.subplots(figsize=(7, 7))
    contagem = df["potencialmente_perigoso"].value_counts()
    labels = ["Seguro", "Perigoso"] if 0 in contagem.index else ["Perigoso"]
    cores = [CORES["seguro"], CORES["perigoso"]]

    wedges, texts, autotexts = ax.pie(
        contagem.values,
        labels=None,
        autopct="%1.1f%%",
        colors=cores[:len(contagem)],
        startangle=90,
        wedgeprops={"edgecolor": CORES["fundo"], "linewidth": 3},
        pctdistance=0.75,
    )
    for at in autotexts:
        at.set_color(CORES["fundo"])
        at.set_fontsize(14)
        at.set_fontweight("bold")

    patches = [
        mpatches.Patch(color=CORES["seguro"], label="Seguro"),
        mpatches.Patch(color=CORES["perigoso"], label="Perigoso"),
    ]
    ax.legend(handles=patches, loc="lower center", frameon=False, fontsize=12)
    ax.set_title("Classificação de Risco", fontsize=16, fontweight="bold", pad=20)

    plt.tight_layout()
    if salvar:
        os.makedirs("data/graficos", exist_ok=True)
        plt.savefig("data/graficos/distribuicao_risco.png", dpi=150, bbox_inches="tight")
        print("[OK] Gráfico salvo: data/graficos/distribuicao_risco.png")
    plt.close()


def grafico_velocidade_vs_distancia(df: pd.DataFrame, salvar: bool = True) -> None:
    """Scatter: velocidade x distância, colorido por perigo."""
    fig, ax = plt.subplots(figsize=(10, 6))

    cores_ponto = df["potencialmente_perigoso"].map({1: CORES["perigoso"], 0: CORES["seguro"]})
    scatter = ax.scatter(
        df["distancia_km"] / 1_000_000,
        df["velocidade_km_h"] / 1_000,
        c=cores_ponto,
        alpha=0.8,
        s=df["diametro_medio_m"] / 3 + 20,
        edgecolors="white",
        linewidths=0.3,
    )

    ax.set_xlabel("Distância da Terra (milhões de km)", fontsize=12)
    ax.set_ylabel("Velocidade (mil km/h)", fontsize=12)
    ax.set_title("Velocidade × Distância da Terra\n(tamanho do ponto = diâmetro do asteroide)", fontsize=14)
    ax.grid(True)

    patches = [
        mpatches.Patch(color=CORES["seguro"], label="Seguro"),
        mpatches.Patch(color=CORES["perigoso"], label="Perigoso"),
    ]
    ax.legend(handles=patches, frameon=False, fontsize=11)

    plt.tight_layout()
    if salvar:
        os.makedirs("data/graficos", exist_ok=True)
        plt.savefig("data/graficos/velocidade_distancia.png", dpi=150, bbox_inches="tight")
        print("[OK] Gráfico salvo: data/graficos/velocidade_distancia.png")
    plt.close()


def grafico_diametros(df: pd.DataFrame, salvar: bool = True) -> None:
    """Histograma dos diâmetros com separação por perigo."""
    fig, ax = plt.subplots(figsize=(10, 5))

    for label, grupo, cor in [
        ("Seguro", df[df["potencialmente_perigoso"] == 0], CORES["seguro"]),
        ("Perigoso", df[df["potencialmente_perigoso"] == 1], CORES["perigoso"]),
    ]:
        ax.hist(
            grupo["diametro_medio_m"],
            bins=30,
            color=cor,
            alpha=0.7,
            label=label,
            edgecolor=CORES["fundo"],
        )

    ax.set_xlabel("Diâmetro médio estimado (metros)", fontsize=12)
    ax.set_ylabel("Quantidade de asteroides", fontsize=12)
    ax.set_title("Distribuição de Diâmetros por Classificação de Risco", fontsize=14)
    ax.legend(frameon=False, fontsize=11)
    ax.grid(True, axis="y")

    plt.tight_layout()
    if salvar:
        os.makedirs("data/graficos", exist_ok=True)
        plt.savefig("data/graficos/distribuicao_diametros.png", dpi=150, bbox_inches="tight")
        print("[OK] Gráfico salvo: data/graficos/distribuicao_diametros.png")
    plt.close()


def grafico_heatmap_correlacao(df: pd.DataFrame, salvar: bool = True) -> None:
    """Heatmap de correlação entre variáveis numéricas."""
    colunas = ["diametro_medio_m", "velocidade_km_h", "distancia_km",
               "distancia_lunar", "magnitude_absoluta", "potencialmente_perigoso"]
    corr = df[colunas].corr()

    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        center=0,
        ax=ax,
        linewidths=0.5,
        linecolor=CORES["grade"],
        annot_kws={"size": 10},
    )
    ax.set_title("Mapa de Correlação entre Variáveis", fontsize=14, pad=15)
    plt.tight_layout()

    if salvar:
        os.makedirs("data/graficos", exist_ok=True)
        plt.savefig("data/graficos/heatmap_correlacao.png", dpi=150, bbox_inches="tight")
        print("[OK] Gráfico salvo: data/graficos/heatmap_correlacao.png")
    plt.close()


def rodar_eda_completa(caminho: str = "data/asteroides.csv") -> None:
    df = carregar(caminho)
    resumo_estatistico(df)
    grafico_distribuicao_perigo(df)
    grafico_velocidade_vs_distancia(df)
    grafico_diametros(df)
    grafico_heatmap_correlacao(df)
    print("\n[OK] Análise exploratória concluída. Gráficos em data/graficos/")


if __name__ == "__main__":
    rodar_eda_completa()
