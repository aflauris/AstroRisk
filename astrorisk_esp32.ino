/*
 * AstroRisk — ESP32 Alert System
 * 
 * Recebe via Serial (USB) ou Wi-Fi o resultado da classificação do modelo ML
 * e acende LED vermelho (PERIGOSO) ou verde (SEGURO) + buzzer de alerta.
 * 
 * Conexões:
 *   LED Vermelho → GPIO 25 (+ resistor 220Ω → GND)
 *   LED Verde    → GPIO 26 (+ resistor 220Ω → GND)
 *   Buzzer       → GPIO 27 (+ GND)
 *   Display OLED → SDA GPIO 21 / SCL GPIO 22 (opcional)
 * 
 * Protocolo Serial: envie "PERIGOSO" ou "SEGURO" (+ newline) pelo Python
 */

#include <Arduino.h>
#include <Wire.h>

// ─── Pinos ────────────────────────────────────────────────────────────────────
const int PIN_LED_VERMELHO = 25;
const int PIN_LED_VERDE    = 26;
const int PIN_BUZZER       = 27;

// ─── Estados ──────────────────────────────────────────────────────────────────
bool modoPerigoso = false;
unsigned long ultimaAtualizacao = 0;
const unsigned long INTERVALO_PISCA = 500;  // ms

// ─── Setup ────────────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);

  pinMode(PIN_LED_VERMELHO, OUTPUT);
  pinMode(PIN_LED_VERDE,    OUTPUT);
  pinMode(PIN_BUZZER,       OUTPUT);

  // Teste de inicialização
  testeInicializacao();

  // Estado inicial: aguardando
  digitalWrite(PIN_LED_VERDE, HIGH);
  digitalWrite(PIN_LED_VERMELHO, LOW);

  Serial.println("[ASTRORISK] Sistema inicializado. Aguardando classificacao...");
}

// ─── Loop Principal ───────────────────────────────────────────────────────────
void loop() {
  // Recebe comando via Serial
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    comando.toUpperCase();

    Serial.print("[ASTRORISK] Recebido: ");
    Serial.println(comando);

    if (comando == "PERIGOSO") {
      ativarAlertaPerigo();
    } else if (comando == "SEGURO") {
      ativarEstadoSeguro();
    } else if (comando == "RESET") {
      resetEstado();
    }
  }

  // Pisca LED vermelho se em modo perigoso
  if (modoPerigoso) {
    unsigned long agora = millis();
    if (agora - ultimaAtualizacao >= INTERVALO_PISCA) {
      ultimaAtualizacao = agora;
      digitalWrite(PIN_LED_VERMELHO, !digitalRead(PIN_LED_VERMELHO));
    }
  }
}

// ─── Funções ──────────────────────────────────────────────────────────────────

void ativarAlertaPerigo() {
  modoPerigoso = true;

  // LEDs
  digitalWrite(PIN_LED_VERDE,    LOW);
  digitalWrite(PIN_LED_VERMELHO, HIGH);

  // Buzzer: 3 bipes curtos
  for (int i = 0; i < 3; i++) {
    tone(PIN_BUZZER, 1500, 200);
    delay(300);
  }

  Serial.println("[ASTRORISK] ALERTA: Asteroide PERIGOSO detectado!");
}

void ativarEstadoSeguro() {
  modoPerigoso = false;

  // LEDs
  digitalWrite(PIN_LED_VERMELHO, LOW);
  digitalWrite(PIN_LED_VERDE,    HIGH);

  // Buzzer: 1 bipe longo suave
  tone(PIN_BUZZER, 800, 500);
  delay(600);

  Serial.println("[ASTRORISK] Status: Asteroide SEGURO.");
}

void resetEstado() {
  modoPerigoso = false;
  digitalWrite(PIN_LED_VERMELHO, LOW);
  digitalWrite(PIN_LED_VERDE,    LOW);
  noTone(PIN_BUZZER);
  Serial.println("[ASTRORISK] Sistema resetado. Aguardando...");
  delay(500);
  digitalWrite(PIN_LED_VERDE, HIGH);
}

void testeInicializacao() {
  // Sequência de teste visual ao ligar
  digitalWrite(PIN_LED_VERMELHO, HIGH);
  delay(400);
  digitalWrite(PIN_LED_VERMELHO, LOW);
  digitalWrite(PIN_LED_VERDE, HIGH);
  delay(400);
  digitalWrite(PIN_LED_VERDE, LOW);
  tone(PIN_BUZZER, 1000, 150);
  delay(200);
  tone(PIN_BUZZER, 1500, 150);
  delay(300);
}
