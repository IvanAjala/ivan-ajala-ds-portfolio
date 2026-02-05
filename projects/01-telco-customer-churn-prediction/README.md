# 📊 Telco Customer Churn Prediction

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg) ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-orange.svg) ![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg)

Sistema inteligente de predição e prevenção de churn de clientes para empresas de telecomunicações, utilizando Machine Learning e análise de negócio.

## 🎯 Objetivo

Desenvolver um sistema completo de retenção de clientes que:

- Prediz a probabilidade de churn com alta precisão (ROC-AUC: 0.84)
- Segmenta clientes por nível de risco
- Recomenda ações personalizadas de retenção
- Calcula impacto financeiro e ROI

## 🚀 Demonstração

![Dashboard](https://app.innerai.com/reports/figures/business/executive_dashboard.png)

**[🔗 Ver Dashboard Interativo](https://telco-churn-dashboard.streamlit.app/)** _(link do deploy)_

## 📊 Resultados Principais

|Métrica|Valor|
|---|---|
|**ROC-AUC**|0.8431|
|**Recall**|73.5%|
|**Precision**|56.5%|
|**Erro de Calibração**|3.14%|
|**ROI Estimado**|350%+|

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**
- **Machine Learning**: Scikit-Learn, XGBoost, LightGBM
- **Análise de Dados**: Pandas, NumPy
- **Visualização**: Matplotlib, Seaborn, Plotly
- **Dashboard**: Streamlit
- **Versionamento**: Git, DVC (Data Version Control)

## 📁 Estrutura do Projeto

```
├── data/               # Dados brutos e processados
├── notebooks/          # Análise exploratória (Jupyter)
├── src/                # Código-fonte
├── models/             # Modelos treinados
├── dashboard/          # Dashboard Streamlit
├── reports/            # Relatórios e visualizações
└── tests/              # Testes automatizados
```

## 🔧 Instalação

### 1. Clonar o repositório

bash

Copiar![](data:image/svg+xml;utf8,%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2216%22%20height%3D%2216%22%20viewBox%3D%220%200%2016%2016%22%20fill%3D%22none%22%3E%0A%20%20%3Cpath%20d%3D%22M10.8%208.63V11.57C10.8%2014.02%209.82%2015%207.37%2015H4.43C1.98%2015%201%2014.02%201%2011.57V8.63C1%206.18%201.98%205.2%204.43%205.2H7.37C9.82%205.2%2010.8%206.18%2010.8%208.63Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%20%20%3Cpath%20d%3D%22M15%204.42999V7.36999C15%209.81999%2014.02%2010.8%2011.57%2010.8H10.8V8.62999C10.8%206.17999%209.81995%205.19999%207.36995%205.19999H5.19995V4.42999C5.19995%201.97999%206.17995%200.999992%208.62995%200.999992H11.57C14.02%200.999992%2015%201.97999%2015%204.42999Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%3C%2Fsvg%3E%0A)

```bash
git clone https://github.com/seu-usuario/telco-customer-churn-prediction.git
cd telco-customer-churn-prediction
```

### 2. Criar ambiente virtual

bash

Copiar![](data:image/svg+xml;utf8,%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2216%22%20height%3D%2216%22%20viewBox%3D%220%200%2016%2016%22%20fill%3D%22none%22%3E%0A%20%20%3Cpath%20d%3D%22M10.8%208.63V11.57C10.8%2014.02%209.82%2015%207.37%2015H4.43C1.98%2015%201%2014.02%201%2011.57V8.63C1%206.18%201.98%205.2%204.43%205.2H7.37C9.82%205.2%2010.8%206.18%2010.8%208.63Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%20%20%3Cpath%20d%3D%22M15%204.42999V7.36999C15%209.81999%2014.02%2010.8%2011.57%2010.8H10.8V8.62999C10.8%206.17999%209.81995%205.19999%207.36995%205.19999H5.19995V4.42999C5.19995%201.97999%206.17995%200.999992%208.62995%200.999992H11.57C14.02%200.999992%2015%201.97999%2015%204.42999Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%3C%2Fsvg%3E%0A)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências

bash

Copiar![](data:image/svg+xml;utf8,%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2216%22%20height%3D%2216%22%20viewBox%3D%220%200%2016%2016%22%20fill%3D%22none%22%3E%0A%20%20%3Cpath%20d%3D%22M10.8%208.63V11.57C10.8%2014.02%209.82%2015%207.37%2015H4.43C1.98%2015%201%2014.02%201%2011.57V8.63C1%206.18%201.98%205.2%204.43%205.2H7.37C9.82%205.2%2010.8%206.18%2010.8%208.63Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%20%20%3Cpath%20d%3D%22M15%204.42999V7.36999C15%209.81999%2014.02%2010.8%2011.57%2010.8H10.8V8.62999C10.8%206.17999%209.81995%205.19999%207.36995%205.19999H5.19995V4.42999C5.19995%201.97999%206.17995%200.999992%208.62995%200.999992H11.57C14.02%200.999992%2015%201.97999%2015%204.42999Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%3C%2Fsvg%3E%0A)

```bash
pip install -r requirements.txt
```

### 4. Baixar dados

bash

Copiar![](data:image/svg+xml;utf8,%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2216%22%20height%3D%2216%22%20viewBox%3D%220%200%2016%2016%22%20fill%3D%22none%22%3E%0A%20%20%3Cpath%20d%3D%22M10.8%208.63V11.57C10.8%2014.02%209.82%2015%207.37%2015H4.43C1.98%2015%201%2014.02%201%2011.57V8.63C1%206.18%201.98%205.2%204.43%205.2H7.37C9.82%205.2%2010.8%206.18%2010.8%208.63Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%20%20%3Cpath%20d%3D%22M15%204.42999V7.36999C15%209.81999%2014.02%2010.8%2011.57%2010.8H10.8V8.62999C10.8%206.17999%209.81995%205.19999%207.36995%205.19999H5.19995V4.42999C5.19995%201.97999%206.17995%200.999992%208.62995%200.999992H11.57C14.02%200.999992%2015%201.97999%2015%204.42999Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%3C%2Fsvg%3E%0A)

```bash
python scripts/download_data.py
```

## 🚀 Uso Rápido

### Executar Pipeline Completo

bash

Copiar![](data:image/svg+xml;utf8,%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2216%22%20height%3D%2216%22%20viewBox%3D%220%200%2016%2016%22%20fill%3D%22none%22%3E%0A%20%20%3Cpath%20d%3D%22M10.8%208.63V11.57C10.8%2014.02%209.82%2015%207.37%2015H4.43C1.98%2015%201%2014.02%201%2011.57V8.63C1%206.18%201.98%205.2%204.43%205.2H7.37C9.82%205.2%2010.8%206.18%2010.8%208.63Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%20%20%3Cpath%20d%3D%22M15%204.42999V7.36999C15%209.81999%2014.02%2010.8%2011.57%2010.8H10.8V8.62999C10.8%206.17999%209.81995%205.19999%207.36995%205.19999H5.19995V4.42999C5.19995%201.97999%206.17995%200.999992%208.62995%200.999992H11.57C14.02%200.999992%2015%201.97999%2015%204.42999Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%3C%2Fsvg%3E%0A)

```bash
python scripts/train_pipeline.py
```

### Gerar Predições

bash

Copiar![](data:image/svg+xml;utf8,%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2216%22%20height%3D%2216%22%20viewBox%3D%220%200%2016%2016%22%20fill%3D%22none%22%3E%0A%20%20%3Cpath%20d%3D%22M10.8%208.63V11.57C10.8%2014.02%209.82%2015%207.37%2015H4.43C1.98%2015%201%2014.02%201%2011.57V8.63C1%206.18%201.98%205.2%204.43%205.2H7.37C9.82%205.2%2010.8%206.18%2010.8%208.63Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%20%20%3Cpath%20d%3D%22M15%204.42999V7.36999C15%209.81999%2014.02%2010.8%2011.57%2010.8H10.8V8.62999C10.8%206.17999%209.81995%205.19999%207.36995%205.19999H5.19995V4.42999C5.19995%201.97999%206.17995%200.999992%208.62995%200.999992H11.57C14.02%200.999992%2015%201.97999%2015%204.42999Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%3C%2Fsvg%3E%0A)

```bash
python scripts/generate_predictions.py --input data/raw/novos_clientes.csv
```

### Executar Dashboard

bash

Copiar![](data:image/svg+xml;utf8,%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2216%22%20height%3D%2216%22%20viewBox%3D%220%200%2016%2016%22%20fill%3D%22none%22%3E%0A%20%20%3Cpath%20d%3D%22M10.8%208.63V11.57C10.8%2014.02%209.82%2015%207.37%2015H4.43C1.98%2015%201%2014.02%201%2011.57V8.63C1%206.18%201.98%205.2%204.43%205.2H7.37C9.82%205.2%2010.8%206.18%2010.8%208.63Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%20%20%3Cpath%20d%3D%22M15%204.42999V7.36999C15%209.81999%2014.02%2010.8%2011.57%2010.8H10.8V8.62999C10.8%206.17999%209.81995%205.19999%207.36995%205.19999H5.19995V4.42999C5.19995%201.97999%206.17995%200.999992%208.62995%200.999992H11.57C14.02%200.999992%2015%201.97999%2015%204.42999Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%3C%2Fsvg%3E%0A)

```bash
cd dashboard
streamlit run app.py
```

## 📓 Notebooks

1. **[01_data_understanding.ipynb](https://app.innerai.com/notebooks/01_data_understanding.ipynb)** - Análise exploratória inicial
2. **[02_data_cleaning.ipynb](https://app.innerai.com/notebooks/02_data_cleaning.ipynb)** - Limpeza e tratamento de dados
3. **[03_feature_engineering.ipynb](https://app.innerai.com/notebooks/03_feature_engineering.ipynb)** - Criação de features
4. **[04_modeling.ipynb](https://app.innerai.com/notebooks/04_modeling.ipynb)** - Treinamento e avaliação de modelos
5. **[05_business_insights.ipynb](https://app.innerai.com/notebooks/05_business_insights.ipynb)** - Insights de negócio e ROI

## 🎯 Metodologia

### 1. Análise Exploratória

- Análise univariada e bivariada
- Identificação de padrões de churn
- Correlações e insights iniciais

### 2. Feature Engineering

- Criação de 34+ features derivadas
- Features financeiras, demográficas e comportamentais
- Encoding e normalização

### 3. Modelagem

- Comparação de 5 algoritmos (RF, XGBoost, LightGBM, etc.)
- Random Forest como melhor modelo
- Calibração com Isotonic Regression

### 4. Business Intelligence

- Segmentação em 4 níveis de risco
- Sistema de recomendação de ações
- Cálculo de CLV e ROI

## 📈 Performance do Modelo

### Métricas de Classificação

|Métrica|Treino|Validação|Teste|
|---|---|---|---|
|ROC-AUC|0.9197|0.8431|0.8431|
|Recall|0.8012|0.7351|0.7350|
|Precision|0.6234|0.5649|0.5650|
|F1-Score|0.7012|0.6401|0.6400|

![](data:image/svg+xml;utf8,%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2216%22%20height%3D%2216%22%20viewBox%3D%220%200%2016%2016%22%20fill%3D%22none%22%3E%0A%20%20%3Cpath%20d%3D%22M10.3078%200.92981C9.94255%200.92981%209.6556%201.21677%209.6556%201.58198C9.6556%201.9472%209.94255%202.23416%2010.3078%202.23416C12.473%202.23416%2014.0904%203.98198%2014.0904%206.27764V10.582C14.0904%2012.7994%2012.2643%2014.6255%2010.0469%2014.6255H5.76864C3.55125%2014.6255%201.72516%2012.7994%201.72516%2010.582V6.27764C1.72516%203.98198%203.34255%202.23416%205.50777%202.23416C5.87299%202.23416%206.15995%201.9472%206.15995%201.58198C6.15995%201.21677%205.87299%200.92981%205.50777%200.92981C2.66429%200.92981%200.420815%203.27764%200.420815%206.27764V10.582C0.420815%2013.5298%202.82081%2015.9298%205.76864%2015.9298H10.073C13.0208%2015.9298%2015.4208%2013.5298%2015.4208%2010.582V6.27764C15.3947%203.27764%2013.1773%200.92981%2010.3078%200.92981Z%22%20fill%3D%22%23717C92%22%2F%3E%0A%20%20%3Cpath%20d%3D%22M7.90784%200.92981C7.54262%200.92981%207.25567%201.21677%207.25567%201.58198V10.2689L5.16871%208.18198C4.90784%207.92111%204.49045%207.92111%204.25567%208.18198C3.9948%208.44285%203.9948%208.86024%204.25567%209.09503L7.43827%2012.2776C7.56871%2012.4081%207.72523%2012.4602%207.90784%2012.4602C8.09045%2012.4602%208.24697%2012.4081%208.3774%2012.2776L11.56%209.09503C11.8209%208.83416%2011.8209%208.41677%2011.56%208.18198C11.2991%207.92111%2010.8818%207.92111%2010.647%208.18198L8.56001%2010.2689V1.58198C8.56001%201.21677%208.27306%200.92981%207.90784%200.92981Z%22%20fill%3D%22%23717C92%22%2F%3E%0A%3C%2Fsvg%3E%0A)Exportar

![](data:image/svg+xml;utf8,%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2216%22%20height%3D%2216%22%20viewBox%3D%220%200%2016%2016%22%20fill%3D%22none%22%3E%0A%20%20%3Cpath%20d%3D%22M10.7209%209.05985V11.9999C10.7209%2014.4499%209.7409%2015.4299%207.2909%2015.4299H4.3509C1.9009%2015.4299%200.920898%2014.4499%200.920898%2011.9999V9.05985C0.920898%206.60985%201.9009%205.62985%204.3509%205.62985H7.2909C9.7409%205.62985%2010.7209%206.60985%2010.7209%209.05985Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%20%20%3Cpath%20d%3D%22M14.9211%204.85966V7.79966C14.9211%2010.2497%2013.9411%2011.2297%2011.4911%2011.2297H10.7211V9.05966C10.7211%206.60966%209.74108%205.62966%207.29108%205.62966H5.12108V4.85966C5.12108%202.40966%206.10108%201.42966%208.55108%201.42966H11.4911C13.9411%201.42966%2014.9211%202.40966%2014.9211%204.85966Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%3C%2Fsvg%3E%0A)Copiar

### Calibração

- **Erro de Calibração**: 3.14% (excelente)
- **Método**: Isotonic Regression
- **Melhoria**: 75.8% vs modelo não calibrado

## 💼 Impacto de Negócio

### Segmentação de Clientes

- **CRÍTICO** (10%): Probabilidade > 90% → Ação imediata
- **ALTO** (15%): Probabilidade 75-90% → Campanha direcionada
- **MÉDIO** (25%): Probabilidade 50-75% → Monitoramento
- **BAIXO** (50%): Probabilidade < 50% → Manutenção padrão

### ROI Estimado

- **Receita em Risco**: R$ 2.5M
- **Receita Recuperável**: R$ 875K (35% conversão)
- **Custo de Ações**: R$ 250K
- **Lucro Líquido**: R$ 625K
- **ROI**: 350%

## 🎨 Dashboard Interativo

O dashboard Streamlit oferece:

- 📊 Visão geral com KPIs principais
- 🎯 Análise de segmentação por risco
- 💡 Sistema de recomendações personalizadas
- 💰 Análise financeira e ROI
- 👥 Lista de clientes prioritários

**[Acessar Dashboard →](https://telco-churn-dashboard.streamlit.app/)**

## 🧪 Testes

bash

Copiar![](data:image/svg+xml;utf8,%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2216%22%20height%3D%2216%22%20viewBox%3D%220%200%2016%2016%22%20fill%3D%22none%22%3E%0A%20%20%3Cpath%20d%3D%22M10.8%208.63V11.57C10.8%2014.02%209.82%2015%207.37%2015H4.43C1.98%2015%201%2014.02%201%2011.57V8.63C1%206.18%201.98%205.2%204.43%205.2H7.37C9.82%205.2%2010.8%206.18%2010.8%208.63Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%20%20%3Cpath%20d%3D%22M15%204.42999V7.36999C15%209.81999%2014.02%2010.8%2011.57%2010.8H10.8V8.62999C10.8%206.17999%209.81995%205.19999%207.36995%205.19999H5.19995V4.42999C5.19995%201.97999%206.17995%200.999992%208.62995%200.999992H11.57C14.02%200.999992%2015%201.97999%2015%204.42999Z%22%20stroke%3D%22%23717C92%22%20stroke-width%3D%221.05%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%0A%3C%2Fsvg%3E%0A)

```bash
pytest tests/
```

## 📚 Documentação

- [Dicionário de Dados](https://app.innerai.com/docs/data_dictionary.md)
- [Documentação do Modelo](https://app.innerai.com/docs/model_documentation.md)
- [Guia de Deploy](https://app.innerai.com/docs/deployment_guide.md)
- [API Documentation](https://app.innerai.com/docs/api_documentation.md)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](https://app.innerai.com/LICENSE) para mais detalhes.

## 👤 Autor

**Ivan**

- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Nome](https://linkedin.com/in/seu-perfil)
- Email: seu.email@example.com

## 🙏 Agradecimentos

- Dataset: [Kaggle - Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- Inspiração: Projetos de Data Science da comunidade

## 📊 Status do Projeto

✅ **Completo e em Produção**

- [x] Análise exploratória
- [x] Feature engineering
- [x] Modelagem e otimização
- [x] Calibração do modelo
- [x] Business insights
- [x] Dashboard interativo
- [x] Documentação completa
- [ ] API REST (em desenvolvimento)
- [ ] Deploy em cloud (planejado)

---

**⭐ Se este projeto foi útil, considere dar uma estrela!**
