/*
 * AstroRisk — ESP32 Alert System
 * FIAP Global Solution 2026.1
 *
 * Recebe via Serial o resultado da classificação do modelo ML
 * e responde com LED vermelho (PERIGOSO) ou verde (SEGURO) + buzzer.
 *
 * Conexões:
 *   LED Vermelho → GPIO 25 + resistor 220Ω → GND
 *   LED Verde    → GPIO 26 + resistor 220Ω → GND
 *   Buzzer       → GPIO 27 → GND
 *
 * No Serial Monitor: envie PERIGOSO, SEGURO ou RESET
 */

#define PIN_LED_VERMELHO 25
#define PIN_LED_VERDE    26
#define PIN_BUZZER       27

void setup() {
  Serial.begin(115200);

  pinMode(PIN_LED_VERMELHO, OUTPUT);
  pinMode(PIN_LED_VERDE,    OUTPUT);
  pinMode(PIN_BUZZER,       OUTPUT);

  // Sequência de teste ao inicializar
  testeInicializacao();

  // Estado padrão: aguardando
  digitalWrite(PIN_LED_VERDE, HIGH);
  digitalWrite(PIN_LED_VERMELHO, LOW);

  Serial.println("╔══════════════════════════════╗");
  Serial.println("║     ASTRORISK - ESP32        ║");
  Serial.println("║  Sistema inicializado!       ║");
  Serial.println("╚══════════════════════════════╝");
  Serial.println("Digite: PERIGOSO | SEGURO | RESET");
  Serial.println("-------------------------------");
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    comando.toUpperCase();

    if (comando == "PERIGOSO") {
      ativarAlertaPerigo();
    } else if (comando == "SEGURO") {
      ativarEstadoSeguro();
    } else if (comando == "RESET") {
      resetEstado();
    } else if (comando.length() > 0) {
      Serial.println("[!] Comando invalido. Use: PERIGOSO | SEGURO | RESET");
    }
  }
}

// ─── Funções ──────────────────────────────────────────────────────────────────

void ativarAlertaPerigo() {
  Serial.println(">>> ALERTA: Asteroide PERIGOSO detectado!");

  digitalWrite(PIN_LED_VERDE, LOW);

  // 3 bipes curtos + LED piscando
  for (int i = 0; i < 3; i++) {
    digitalWrite(PIN_LED_VERMELHO, HIGH);
    tone(PIN_BUZZER, 1500);
    delay(200);
    noTone(PIN_BUZZER);
    digitalWrite(PIN_LED_VERMELHO, LOW);
    delay(150);
  }

  // LED vermelho fixo após os bipes
  digitalWrite(PIN_LED_VERMELHO, HIGH);
  Serial.println(">>> LED VERMELHO ligado. Risco ativo.");
}

void ativarEstadoSeguro() {
  Serial.println(">>> Status: Asteroide SEGURO.");

  digitalWrite(PIN_LED_VERMELHO, LOW);

  // 1 bipe suave
  tone(PIN_BUZZER, 800);
  delay(500);
  noTone(PIN_BUZZER);

  // LED verde fixo
  digitalWrite(PIN_LED_VERDE, HIGH);
  Serial.println(">>> LED VERDE ligado. Sem risco.");
}

void resetEstado() {
  digitalWrite(PIN_LED_VERMELHO, LOW);
  digitalWrite(PIN_LED_VERDE,    LOW);
  noTone(PIN_BUZZER);

  delay(300);

  digitalWrite(PIN_LED_VERDE, HIGH);
  Serial.println(">>> Sistema resetado. Aguardando...");
}

void testeInicializacao() {
  Serial.println(">>> Teste de inicializacao...");

  digitalWrite(PIN_LED_VERMELHO, HIGH);
  delay(400);
  digitalWrite(PIN_LED_VERMELHO, LOW);

  digitalWrite(PIN_LED_VERDE, HIGH);
  delay(400);
  digitalWrite(PIN_LED_VERDE, LOW);

  tone(PIN_BUZZER, 1000);
  delay(150);
  noTone(PIN_BUZZER);
  delay(100);
  tone(PIN_BUZZER, 1500);
  delay(150);
  noTone(PIN_BUZZER);
}