"""
AstroRisk — Modelo de Machine Learning
Classificação de risco de asteroides usando Random Forest.
Treina, avalia e salva o modelo para uso no dashboard.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)
from sklearn.pipeline import Pipeline

# Configuração visual
plt.rcParams.update({
    "figure.facecolor": "#0A0E1A",
    "axes.facecolor": "#0A0E1A",
    "axes.edgecolor": "#1E2A3A",
    "axes.labelcolor": "#E0E8FF",
    "xtick.color": "#E0E8FF",
    "ytick.color": "#E0E8FF",
    "text.color": "#E0E8FF",
    "grid.color": "#1E2A3A",
    "font.family": "monospace",
})

FEATURES = [
    "diametro_medio_m",
    "velocidade_km_h",
    "distancia_km",
    "distancia_lunar",
    "magnitude_absoluta",
]
TARGET = "potencialmente_perigoso"
MODELO_PATH = "data/modelo_astrorisk.pkl"


def preparar_dados(df: pd.DataFrame):
    """Remove NaN e separa features e target."""
    df_clean = df[FEATURES + [TARGET]].dropna()
    X = df_clean[FEATURES]
    y = df_clean[TARGET]
    return X, y


def treinar_modelo(df: pd.DataFrame) -> Pipeline:
    """Treina o pipeline de ML e retorna o modelo treinado."""
    X, y = preparar_dados(df)

    print(f"[INFO] Dataset: {len(X)} amostras | Perigosos: {y.sum()} | Seguros: {(y==0).sum()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        )),
    ])

    pipeline.fit(X_train, y_train)

    # Avaliação
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    print("\n--- Relatório de Classificação ---")
    print(classification_report(y_test, y_pred, target_names=["Seguro", "Perigoso"]))
    print(f"AUC-ROC: {roc_auc_score(y_test, y_prob):.4f}")

    # Cross-validation
    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="roc_auc")
    print(f"CV AUC-ROC (5-fold): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # Gráficos de avaliação
    _grafico_matriz_confusao(y_test, y_pred)
    _grafico_roc(y_test, y_prob)
    _grafico_importancia(pipeline, FEATURES)

    return pipeline, X_test, y_test


def _grafico_matriz_confusao(y_test, y_pred) -> None:
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="YlOrRd",
        xticklabels=["Seguro", "Perigoso"],
        yticklabels=["Seguro", "Perigoso"],
        ax=ax, linewidths=0.5,
    )
    ax.set_xlabel("Predito", fontsize=12)
    ax.set_ylabel("Real", fontsize=12)
    ax.set_title("Matriz de Confusão", fontsize=14)
    plt.tight_layout()
    os.makedirs("data/graficos", exist_ok=True)
    plt.savefig("data/graficos/matriz_confusao.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("[OK] Gráfico salvo: data/graficos/matriz_confusao.png")


def _grafico_roc(y_test, y_prob) -> None:
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(fpr, tpr, color="#FFD700", lw=2, label=f"AUC = {auc:.3f}")
    ax.plot([0, 1], [0, 1], color="#4CFFB8", lw=1, linestyle="--", label="Baseline")
    ax.set_xlabel("Taxa de Falsos Positivos", fontsize=12)
    ax.set_ylabel("Taxa de Verdadeiros Positivos", fontsize=12)
    ax.set_title("Curva ROC — AstroRisk", fontsize=14)
    ax.legend(frameon=False, fontsize=12)
    ax.grid(True)
    plt.tight_layout()
    plt.savefig("data/graficos/curva_roc.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("[OK] Gráfico salvo: data/graficos/curva_roc.png")


def _grafico_importancia(pipeline: Pipeline, features: list) -> None:
    importancias = pipeline.named_steps["clf"].feature_importances_
    idx = np.argsort(importancias)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(
        [features[i] for i in idx],
        importancias[idx],
        color="#4CFFB8",
        edgecolor="#0A0E1A",
    )
    ax.set_xlabel("Importância", fontsize=12)
    ax.set_title("Importância das Features — Random Forest", fontsize=14)
    ax.grid(True, axis="x")
    plt.tight_layout()
    plt.savefig("data/graficos/importancia_features.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("[OK] Gráfico salvo: data/graficos/importancia_features.png")


def salvar_modelo(pipeline: Pipeline, caminho: str = MODELO_PATH) -> None:
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    joblib.dump(pipeline, caminho)
    print(f"[OK] Modelo salvo em: {caminho}")


def carregar_modelo(caminho: str = MODELO_PATH) -> Pipeline:
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Modelo não encontrado: {caminho}. Rode modelo_ml.py primeiro.")
    return joblib.load(caminho)


def predizer(pipeline: Pipeline, dados: dict) -> dict:
    """
    Recebe um dicionário com as features e retorna:
    - classificacao: 'PERIGOSO' ou 'SEGURO'
    - probabilidade: float entre 0 e 1
    """
    X = pd.DataFrame([dados])[FEATURES]
    prob = pipeline.predict_proba(X)[0][1]
    classe = "PERIGOSO" if prob >= 0.5 else "SEGURO"
    return {"classificacao": classe, "probabilidade": round(prob, 4)}


if __name__ == "__main__":
    import sys as _sys
    _sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from coletor_nasa import carregar_dados

    df = carregar_dados()
    pipeline, X_test, y_test = treinar_modelo(df)
    salvar_modelo(pipeline)

    # Teste de predição manual
    exemplo = {
        "diametro_medio_m": 350.0,
        "velocidade_km_h": 85000.0,
        "distancia_km": 1_500_000.0,
        "distancia_lunar": 3.9,
        "magnitude_absoluta": 19.5,
    }
    resultado = predizer(pipeline, exemplo)
    print(f"\n[TESTE] Predição: {resultado['classificacao']} (prob={resultado['probabilidade']})")
