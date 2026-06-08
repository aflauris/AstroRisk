"""
AstroRisk — Coletor de Dados da NASA NeoWs API
Coleta asteroides próximos da Terra e salva em CSV para análise.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do arquivo .env

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"


def coletar_asteroides(dias_atras: int = 7) -> pd.DataFrame:
    """
    Coleta dados de asteroides dos últimos N dias via NeoWs API.
    Retorna um DataFrame com os dados tratados.
    """
    data_fim = datetime.today()
    data_inicio = data_fim - timedelta(days=dias_atras)

    params = {
        "start_date": data_inicio.strftime("%Y-%m-%d"),
        "end_date": data_fim.strftime("%Y-%m-%d"),
        "api_key": NASA_API_KEY,
    }

    print(f"[INFO] Buscando asteroides de {params['start_date']} a {params['end_date']}...")

    response = requests.get(BASE_URL, params=params, timeout=30)

    if response.status_code != 200:
        raise ConnectionError(f"Erro na API da NASA: {response.status_code} — {response.text}")

    dados_brutos = response.json()
    asteroides = []

    for data, lista in dados_brutos["near_earth_objects"].items():
        for neo in lista:
            diametro_min = neo["estimated_diameter"]["meters"]["estimated_diameter_min"]
            diametro_max = neo["estimated_diameter"]["meters"]["estimated_diameter_max"]
            diametro_medio = (diametro_min + diametro_max) / 2

            # Pega a aproximação mais próxima registrada
            aproximacao = neo["close_approach_data"][0] if neo["close_approach_data"] else {}

            asteroides.append({
                "id": neo["id"],
                "nome": neo["name"],
                "data_observacao": data,
                "diametro_min_m": round(diametro_min, 2),
                "diametro_max_m": round(diametro_max, 2),
                "diametro_medio_m": round(diametro_medio, 2),
                "potencialmente_perigoso": int(neo["is_potentially_hazardous_asteroid"]),
                "velocidade_km_h": round(
                    float(aproximacao.get("relative_velocity", {}).get("kilometers_per_hour", 0)), 2
                ),
                "distancia_km": round(
                    float(aproximacao.get("miss_distance", {}).get("kilometers", 0)), 2
                ),
                "distancia_lunar": round(
                    float(aproximacao.get("miss_distance", {}).get("lunar", 0)), 4
                ),
                "magnitude_absoluta": neo.get("absolute_magnitude_h", None),
                "url_nasa": neo.get("nasa_jpl_url", ""),
            })

    df = pd.DataFrame(asteroides)

    # Limpeza: remove duplicatas por ID
    df = df.drop_duplicates(subset="id").reset_index(drop=True)

    print(f"[OK] {len(df)} asteroides coletados.")
    return df


def salvar_dados(df: pd.DataFrame, caminho: str = "data/asteroides.csv") -> None:
    """Salva o DataFrame em CSV."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    df.to_csv(caminho, index=False, encoding="utf-8")
    print(f"[OK] Dados salvos em: {caminho}")


def carregar_dados(caminho: str = "data/asteroides.csv") -> pd.DataFrame:
    """Carrega o CSV existente ou coleta novos dados se não existir."""
    if os.path.exists(caminho):
        print(f"[INFO] Carregando dados locais: {caminho}")
        return pd.read_csv(caminho)
    else:
        print("[INFO] Arquivo local não encontrado. Coletando da API...")
        df = coletar_asteroides()
        salvar_dados(df, caminho)
        return df


if __name__ == "__main__":
    df = coletar_asteroides(dias_atras=7)
    salvar_dados(df)
    print("\n--- Amostra dos dados ---")
    print(df.head())
    print(f"\nTotal perigosos: {df['potencialmente_perigoso'].sum()}")
    print(f"Total seguros:   {(df['potencialmente_perigoso'] == 0).sum()}")
