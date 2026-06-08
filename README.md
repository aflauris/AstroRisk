# ☄️ AstroRisk — Sistema de Monitoramento e Classificação de Asteroides

> FIAP Global Solution 2026.1 — Economia Espacial  
> **QUERO CONCORRER**

---

## 👥 Integrantes do Grupo

| Nome | RM |
|------|----|
| [Nome 1] | RM000000 |
| [Nome 2] | RM000000 |
| [Nome 3] | RM000000 |
| [Nome 4] | RM000000 |
| [Nome 5] | RM000000 |

---

## 📋 Descrição do Projeto

O **AstroRisk** é uma plataforma de análise e predição de risco de asteroides que utiliza dados reais e atualizados da **NASA NeoWs API** (Near Earth Object Web Service). O sistema coleta, analisa e classifica automaticamente asteroides próximos da Terra como **PERIGOSOS** ou **SEGUROS**, exibindo os resultados em um dashboard interativo e acionando alertas físicos via **ESP32**.

### Problema que resolve
A classificação manual de asteroides como Objetos Próximos da Terra (NEOs) é um processo lento e dependente de especialistas. O AstroRisk automatiza essa triagem com Machine Learning, democratizando o acesso à informação de segurança espacial.

---

## 🏗️ Arquitetura da Solução

```
NASA NeoWs API
      │
      ▼
src/coletor_nasa.py          ← Coleta e tratamento de dados
      │
      ▼
src/analise_eda.py           ← Análise exploratória + gráficos
      │
      ▼
src/modelo_ml.py             ← Treinamento e avaliação (Random Forest)
      │
      ├──► dashboard/app.py  ← Dashboard Streamlit interativo
      │
      └──► esp32/            ← Alerta físico via ESP32
```

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
|--------|-----------|
| Coleta de dados | Python, Requests, NASA NeoWs API |
| Análise de dados | Pandas, NumPy |
| Visualização | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn (Random Forest) |
| Dashboard | Streamlit |
| IoT / Hardware | ESP32, C++ (Arduino) |
| Comunicação | PySerial |

---

## 📁 Estrutura do Repositório

```
astrorisk/
├── src/
│   ├── coletor_nasa.py       # Coleta dados da NASA NeoWs API
│   ├── analise_eda.py        # Análise exploratória de dados
│   └── modelo_ml.py          # Treinamento e predição com ML
├── dashboard/
│   └── app.py                # Dashboard Streamlit
├── esp32/
│   ├── astrorisk_esp32.ino   # Firmware do ESP32 (Arduino)
│   └── comunicacao_serial.py # Integração Python ↔ ESP32
├── data/                     # Dados coletados e modelos salvos
├── notebooks/                # Notebooks de experimentação
├── requirements.txt
└── README.md
```

---

## 🚀 Instruções de Execução

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Coletar dados da NASA
```bash
python src/coletor_nasa.py
```

### 3. Rodar análise exploratória
```bash
python src/analise_eda.py
```

### 4. Treinar modelo de ML
```bash
python src/modelo_ml.py
```

### 5. Iniciar dashboard
```bash
streamlit run dashboard/app.py
```

### 6. ESP32 (opcional)
1. Abrir `esp32/astrorisk_esp32.ino` na Arduino IDE
2. Selecionar placa: **ESP32 Dev Module**
3. Fazer upload do firmware
4. Executar `python esp32/comunicacao_serial.py`

---

## 🔌 Esquema de Conexão ESP32

```
ESP32           Componente
GPIO 25    →    LED Vermelho (+) → 220Ω → GND
GPIO 26    →    LED Verde (+) → 220Ω → GND
GPIO 27    →    Buzzer (+) → GND
GPIO 21    →    OLED SDA (opcional)
GPIO 22    →    OLED SCL (opcional)
3.3V       →    VCC dos componentes
GND        →    GND comum
```

---

## 🤖 Modelo de Machine Learning

- **Algoritmo:** Random Forest Classifier
- **Features:** diâmetro estimado, velocidade relativa, distância da Terra, distância lunar, magnitude absoluta
- **Target:** `potencialmente_perigoso` (0 = Seguro / 1 = Perigoso)
- **Métricas:** AUC-ROC, F1-Score, Matriz de Confusão

---

## 📊 Fonte dos Dados

- **NASA NeoWs API:** https://api.nasa.gov  
- Chave gratuita disponível em api.nasa.gov  
- Dados atualizados diariamente com asteroides dos próximos 7 dias

---

## 🎥 Vídeo Demonstrativo

> Link do vídeo: [inserir link do YouTube]

---

## 📄 Licença

Projeto acadêmico — FIAP 2026.1
