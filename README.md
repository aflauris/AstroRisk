# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="https://upload.wikimedia.org/wikipedia/commons/d/d4/Fiap-logo-novo.jpg" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# ☄️ AstroRisk — Sistema de Monitoramento e Classificação de Asteroides

## 🌐 Global Solution 2026.1 — Economia Espacial

---

## 👨‍🎓 Integrantes

- Ana Flora Lauris (RM572202)
- Clarice Oliveira Barreto (RM571269)
- Kevin de Freitas Minervino (RM570667)
- Lucas Henrique Aparecido Gomes de Mello (RM569583)
- Renan Chaves Bezerra (RM573532)

## 👩‍🏫 Professores

### Tutor(a)
- Sabrina Otoni

### Coordenador(a)
- André Godoi Chiovato

---

## 📜 Descrição

O **AstroRisk** é uma plataforma de monitoramento e classificação de risco de asteroides que utiliza dados reais e atualizados da **NASA NeoWs API** (Near Earth Object Web Service). O sistema coleta, analisa e classifica automaticamente asteroides próximos da Terra como **PERIGOSOS** ou **SEGUROS**, exibindo os resultados em um dashboard interativo e acionando alertas físicos via **ESP32**.

O projeto foi desenvolvido na **Global Solution 2026.1 — FIAP**, com tema **Economia Espacial**, respondendo à pergunta: *"Como a tecnologia espacial pode ser utilizada para melhorar a vida das pessoas e criar novas oportunidades?"*

> 📽️ **Vídeo de Apresentação:** [a ser inserido após gravação]

---

## 📁 Estrutura de Pastas

```bash
📂 AstroRisk
│
├── 📂 assets               # Imagens, logo e prints do dashboard
├── 📂 dashboard
│   └── app.py              # Interface web interativa (Streamlit)
├── 📂 document             # PDF de entrega e documentação
├── 📂 esp32
│   ├── astrorisk_esp32.ino # Firmware do ESP32 (Arduino)
│   └── comunicacao_serial.py # Integração Python ↔ ESP32
├── 📂 src
│   ├── coletor_nasa.py     # Coleta de dados via NASA NeoWs API
│   ├── analise_eda.py      # Análise exploratória + visualizações
│   └── modelo_ml.py        # Treinamento e predição (Random Forest)
├── .env.example            # Template de variáveis de ambiente
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔧 Como Executar o Código

### Pré-requisitos

- Python 3.10+
- Chave gratuita da NASA em [api.nasa.gov](https://api.nasa.gov)

### Instalação

**Fase 1 — Clonar e instalar dependências:**

```bash
git clone https://github.com/SEU_USUARIO/AstroRisk
cd AstroRisk
pip install -r requirements.txt
```

**Fase 2 — Configurar variáveis de ambiente:**

```bash
cp .env.example .env
# Edite o .env e insira sua NASA_API_KEY
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

**Fase 6 — Iniciar o dashboard:**

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

Todos os dias, a NASA monitora centenas de **Objetos Próximos da Terra (NEOs)**. Dentre eles, alguns são classificados como potencialmente perigosos — aqueles com tamanho e trajetória capazes de representar risco de impacto. A classificação manual desses objetos é um processo lento, técnico e pouco acessível ao público geral.

**Consequências:**

- Demora na triagem de novos objetos detectados
- Ausência de sistemas acessíveis que combinem dados reais, ML e alertas
- Baixa visibilidade pública sobre riscos astronômicos reais

---

## 💡 Solução

O AstroRisk automatiza a triagem de asteroides com Machine Learning, entregando:

| Saída | Descrição |
|-------|-----------|
| 📊 Classificação de risco | PERIGOSO ou SEGURO |
| 🔢 Probabilidade | Score de 0 a 1 calculado pelo modelo |
| 📈 Visualizações | Gráficos de velocidade, distância, diâmetro e correlações |
| 🚨 Alerta físico | LED vermelho piscando + buzzer via ESP32 |
| 🌐 Dashboard interativo | Interface Streamlit com filtros e predição em tempo real |

---

## 🤖 Modelo de Machine Learning

| Componente | Definição |
|------------|-----------|
| Variável alvo | `potencialmente_perigoso` — 0 (seguro) ou 1 (perigoso) |
| Modelo | **Random Forest** (scikit-learn) |
| Features | diâmetro médio, velocidade relativa, distância da Terra, distância lunar, magnitude absoluta |
| Métricas | AUC-ROC, F1-score, Recall, Matriz de Confusão |
| Validação | Cross-validation com 5 folds |

---

## 🏗️ Arquitetura da Solução

```
NASA NeoWs API
      │
      ▼
src/coletor_nasa.py     ← Coleta e tratamento de dados
      │
      ▼
src/analise_eda.py      ← Análise exploratória + gráficos
      │
      ▼
src/modelo_ml.py        ← Treinamento e avaliação (Random Forest)
      │
      ├──► dashboard/app.py       ← Dashboard Streamlit interativo
      │
      └──► esp32/                 ← Alerta físico via ESP32
```

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

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
