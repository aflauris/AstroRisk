"""
AstroRisk — Comunicação Python ↔ ESP32
Envia o resultado do modelo ML para o ESP32 via porta Serial (USB).
"""

import serial
import serial.tools.list_ports
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def listar_portas():
    """Lista todas as portas seriais disponíveis."""
    portas = serial.tools.list_ports.comports()
    if not portas:
        print("[AVISO] Nenhuma porta serial encontrada.")
        return []
    for p in portas:
        print(f"  {p.device} — {p.description}")
    return [p.device for p in portas]


def conectar_esp32(porta: str = None, baudrate: int = 115200) -> serial.Serial:
    """
    Conecta ao ESP32 via Serial.
    Se porta=None, tenta detectar automaticamente.
    """
    if porta is None:
        portas = listar_portas()
        # Tenta porta USB comum no Linux/macOS/Windows
        for tentativa in ["/dev/ttyUSB0", "/dev/ttyACM0", "COM3", "COM4"]:
            if tentativa in portas:
                porta = tentativa
                break
        if porta is None and portas:
            porta = portas[0]

    if porta is None:
        raise ConnectionError("ESP32 não encontrado. Conecte o cabo USB e tente novamente.")

    print(f"[INFO] Conectando ao ESP32 em {porta} @ {baudrate} baud...")
    conn = serial.Serial(porta, baudrate, timeout=2)
    time.sleep(2)  # Aguarda o ESP32 inicializar
    print("[OK] Conectado!")
    return conn


def enviar_classificacao(conn: serial.Serial, classificacao: str) -> None:
    """
    Envia 'PERIGOSO' ou 'SEGURO' para o ESP32.
    """
    classificacao = classificacao.upper().strip()
    if classificacao not in ("PERIGOSO", "SEGURO", "RESET"):
        raise ValueError(f"Classificação inválida: {classificacao}")

    mensagem = (classificacao + "\n").encode("utf-8")
    conn.write(mensagem)
    time.sleep(0.5)

    # Lê resposta do ESP32
    if conn.in_waiting:
        resposta = conn.readline().decode("utf-8", errors="ignore").strip()
        print(f"[ESP32] {resposta}")


def modo_demo(porta: str = None) -> None:
    """
    Modo de demonstração: alterna entre PERIGOSO e SEGURO a cada 5 segundos.
    Útil para testar o hardware sem o modelo ML.
    """
    conn = conectar_esp32(porta)
    print("\n[DEMO] Iniciando modo demonstração. Ctrl+C para sair.\n")

    try:
        estados = ["PERIGOSO", "SEGURO", "PERIGOSO", "SEGURO"]
        for estado in estados * 3:
            print(f"[DEMO] Enviando: {estado}")
            enviar_classificacao(conn, estado)
            time.sleep(4)
    except KeyboardInterrupt:
        print("\n[DEMO] Encerrado pelo usuário.")
    finally:
        enviar_classificacao(conn, "RESET")
        conn.close()
        print("[OK] Conexão encerrada.")


def integrar_com_modelo(dados_asteroide: dict, porta: str = None) -> dict:
    """
    Pipeline completo:
    1. Carrega modelo
    2. Classifica asteroide
    3. Envia resultado para ESP32
    4. Retorna resultado
    """
    from src.modelo_ml import carregar_modelo, predizer

    modelo = carregar_modelo()
    resultado = predizer(modelo, dados_asteroide)

    print(f"\n[ML] Classificação: {resultado['classificacao']} (prob={resultado['probabilidade']})")

    try:
        conn = conectar_esp32(porta)
        enviar_classificacao(conn, resultado["classificacao"])
        conn.close()
        resultado["esp32_enviado"] = True
    except ConnectionError as e:
        print(f"[AVISO] ESP32 não disponível: {e}")
        resultado["esp32_enviado"] = False

    return resultado


if __name__ == "__main__":
    # Modo demo para testar o hardware
    print("=== AstroRisk — Comunicação ESP32 ===")
    print("Portas disponíveis:")
    listar_portas()

    modo = input("\nModo? [demo/integrar]: ").strip().lower()

    if modo == "demo":
        porta = input("Porta (Enter para auto-detectar): ").strip() or None
        modo_demo(porta)

    elif modo == "integrar":
        exemplo = {
            "diametro_medio_m": 450.0,
            "velocidade_km_h": 120000.0,
            "distancia_km": 800_000.0,
            "distancia_lunar": 2.1,
            "magnitude_absoluta": 18.0,
        }
        resultado = integrar_com_modelo(exemplo)
        print(f"\n[RESULTADO] {resultado}")
