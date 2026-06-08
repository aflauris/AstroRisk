# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# ☄️ AstroRisk — Sistema de Monitoramento e Classificação de Asteroides

## 👨‍🎓 Integrantes

- Ana Flora Lauris (RM572202)
- Clarice Oliveira Barreto (RM571269)
- Kevin de Freitas Minervino (RM570667)
- Lucas Henrique Aparecido Gomes de Mello (RM569583)
- Renan Chaves Bezerra (RM573532)

## 👩‍🏫 Professores

### Tutor(a)

- Sabrina Otoni — Turma B

### Coordenador(a)

- André Godoi Chiovato

---

## 📜 Descrição

O **AstroRisk** é uma plataforma de monitoramento e classificação de risco de asteroides que utiliza dados reais e atualizados da **NASA NeoWs API** (Near Earth Object Web Service). O sistema coleta, analisa e classifica automaticamente asteroides próximos da Terra como **PERIGOSOS** ou **SEGUROS**, exibindo os resultados em um dashboard interativo e acionando alertas físicos via **ESP32**.

O projeto foi desenvolvido na **Global Solution 2026.1 — FIAP**, com tema **Economia Espacial**.

> 📽️ **Vídeo de Apresentação:** [a ser inserido após gravação]

---

## 📁 Estrutura de Pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- **.github**: arquivos de configuração específicos do GitHub.
- **assets**: imagens, logotipos e prints do dashboard utilizados na documentação.
- **dashboard**: interface web interativa desenvolvida com Streamlit (`app.py`).
- **document**: documentos do projeto solicitados pela atividade, incluindo o PDF de entrega.
- **esp32**: firmware do ESP32 (`astrorisk_esp32.ino`) e script de comunicação serial Python.
- **src**: código-fonte principal — coleta de dados NASA (`coletor_nasa.py`), análise exploratória (`analise_eda.py`) e modelo de Machine Learning (`modelo_ml.py`).
- **README.md**: arquivo que serve como guia e explicação geral sobre o projeto.

---

## 🔧 Como Executar o Código

### Pré-requisitos

- Python 3.10+
- Conta gratuita em [api.nasa.gov](https://api.nasa.gov) para obter sua chave de API

### Instalação

**Fase 1 — Configuração:**

```bash
git clone https://github.com/SEU_USUARIO/AstroRisk
cd AstroRisk
pip install -r requirements.txt
```

**Fase 2 — Configurar variáveis de ambiente:**

```bash
cp .env.example .env
# Edite o .env e insira sua chave NASA_API_KEY
```

**Fase 3 — Coletar dados da NASA:**

```bash
python src/coletor_nasa.py
```

**Fase 4 — Análise exploratória:**

```bash
python src/analise_eda.py
```

**Fase 5 — Treinar o modelo de ML:**

```bash
python src/modelo_ml.py
```

**Fase 6 — Dashboard:**

```bash
streamlit run dashboard/app.py
```

**Fase 7 — ESP32 (opcional):**

1. Abrir `esp32/astrorisk_esp32.ino` na Arduino IDE
2. Selecionar placa: **ESP32 Dev Module**
3. Fazer upload do firmware
4. Executar `python esp32/comunicacao_serial.py`

---

## 🔴 Problema

Todos os dias, a NASA monitora centenas de **Objetos Próximos da Terra (NEOs)**. Dentre eles, alguns são classificados como potencialmente perigosos — aqueles com tamanho e trajetória capazes de representar risco de impacto. A classificação manual desses objetos é um processo lento e dependente de especialistas.

**Consequências da falta de automação:**

- Demora na triagem de novos objetos detectados
- Dificuldade de acesso público a informações de risco em tempo real
- Ausência de sistemas integrados que combinem análise de dados, ML e alertas físicos

---

## 💡 Solução

O AstroRisk automatiza a triagem de asteroides com Machine Learning, entregando:

| Saída | Descrição |
|-------|-----------|
| 📊 Classificação de risco | PERIGOSO ou SEGURO |
| 🔢 Probabilidade | Score entre 0 e 1 |
| 📈 Visualizações | Gráficos de velocidade, distância e diâmetro |
| 🚨 Alerta físico | LED e buzzer via ESP32 |
| 🌐 Dashboard interativo | Interface Streamlit com filtros e predição |

**Exemplo de saída do sistema:**

```
Asteroide  : (2026 XK42)
Diâmetro   : 480 m
Velocidade : 112.000 km/h
Distância  : 720.000 km da Terra

Classificação : 🔴 PERIGOSO
Probabilidade : 87.3%
→ ESP32: LED VERMELHO piscando + 3 bipes de alerta
```

---

## 🤖 Modelo de Machine Learning

**Objetivo:** classificar automaticamente um asteroide como perigoso ou seguro com base em dados orbitais e físicos.

| Componente | Definição |
|------------|-----------|
| Variável alvo | `potencialmente_perigoso` — 0 (seguro) ou 1 (perigoso) |
| Modelo principal | **Random Forest** |
| Features | diâmetro médio, velocidade relativa, distância da Terra, distância lunar, magnitude absoluta |
| Métricas de avaliação | AUC-ROC, F1-score, Recall, Matriz de Confusão |
| Validação | Cross-validation com 5 folds |

---

## 🏗️ Arquitetura da Solução

```
NASA NeoWs API
      │
      ▼
src/coletor_nasa.py     ← Coleta e tratamento de dados (Pandas)
      │
      ▼
src/analise_eda.py      ← Análise exploratória + gráficos (Matplotlib/Seaborn)
      │
      ▼
src/modelo_ml.py        ← Treinamento e avaliação (Random Forest / sklearn)
      │
      ├──► dashboard/app.py       ← Dashboard Streamlit interativo
      │
      └──► esp32/                 ← Alerta físico via ESP32
```

| Componente | Tecnologia |
|------------|-----------|
| Coleta de dados | Python, Requests, NASA NeoWs API |
| Análise de dados | Pandas, NumPy |
| Visualização | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn (Random Forest) |
| Dashboard | Streamlit |
| IoT / Hardware | ESP32, C++ (Arduino Framework) |
| Comunicação serial | PySerial |
| Segurança | python-dotenv |

---

## 🔌 Esquema de Conexão ESP32

```
ESP32           Componente
GPIO 25    →    LED Vermelho (+) → 220Ω → GND
GPIO 26    →    LED Verde (+) → 220Ω → GND
GPIO 27    →    Buzzer (+) → GND
3.3V       →    VCC dos componentes
GND        →    GND comum
```

---

## 📊 Fonte dos Dados

| Fonte | Dado fornecido |
|-------|----------------|
| [NASA NeoWs API](https://api.nasa.gov) | Asteroides próximos da Terra (diâmetro, velocidade, distância, risco) |

- Dados atualizados diariamente
- Chave gratuita disponível em [api.nasa.gov](https://api.nasa.gov)

---

## 🗃 Histórico de Lançamentos

- **1.0.0** — Global Solution 2026.1: MVP completo com coleta NASA, EDA, ML, dashboard Streamlit e integração ESP32

---

## 💻 Tecnologias

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-000000?style=for-the-badge&logo=espressif&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

---

## 📋 Licença

<a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"></a>

[MODELO GIT FIAP](https://github.com/agodoi/template) por [FIAP](https://fiap.com.br) está licenciado sob [Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1).
