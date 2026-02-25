![Notebooks Banner](../src/banners/notebooks_banner.png)

---

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white) ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) ![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white) ![Status](https://img.shields.io/badge/Status-%E2%9C%85%20Conclu%C3%ADdo-success?style=for-the-badge)

## 📋 Visão Geral

Esta pasta contém os notebooks Jupyter que documentam todo o processo de ciência de dados aplicado ao projeto de predição de churn em telecomunicações. Os notebooks estão organizados sequencialmente, seguindo um pipeline completo desde a preparação dos dados até a implementação de insights de negócio.

Cada notebook é autocontido e inclui explicações detalhadas, visualizações e código comentado, permitindo que você acompanhe o raciocínio e as decisões tomadas em cada etapa do projeto.

## 📊 Notebooks Disponíveis

|#|Notebook|Descrição|Complexidade|Status|
|---|---|---|---|---|
|01|[Qualidade dos Dados](01_qualidade_dados.ipynb)|Preparação, limpeza e validação do dataset|⭐⭐⭐|✅|
|02|[Análise Exploratória](02_analise_exploratoria.ipynb)|Investigação de padrões, correlações e insights iniciais|⭐⭐⭐⭐|✅|
|03|[Engenharia de Features](03_engenharia_feature.ipynb)|Criação e seleção de variáveis relevantes para modelagem|⭐⭐⭐⭐|✅|
|04|[Modelagem Preditiva](04_modelagem_preditiva.ipynb)|Desenvolvimento, otimização e avaliação de modelos|⭐⭐⭐⭐⭐|✅|
|05|[Insights de Negócio](05_business_insights.ipynb)|Tradução dos resultados em ações e estratégias|⭐⭐⭐⭐|✅|

## 🔍 Destaques por Notebook

### 01 - Qualidade dos Dados

- **Verificar a estrutura** (dimensões, tipos de dados, valores únicos).
- **Detectar e tratar valores ausentes** de forma estratégica.
- **Eliminar duplicatas** e validar a unicidade dos IDs de cliente.
- **Corrigir tipos de dados incorretos** (ex.: `TotalCharges` de `object` para `numeric`).
- [Leia mais detalhes](README_01_qualidade_dados.md)

### 02 - Análise Exploratória

- **Identificar padrões, outliers e correlações** entre as variáveis.
- **Quantificar a relação** entre variáveis (demográficas, de serviço, financeiras) e a variável alvo **Churn**.
- **Criar perfis de clientes** de alto e baixo risco de churn.
- **Calcular o Customer Lifetime Value (CLV)** para segmentação estratégica.
- [Leia mais detalhes](README_02_analise_exploratoria.md)

### 03 - Engenharia de Features

- **Criação de 17 novas features** baseadas em conhecimento de domínio
- **Transformação de variáveis categóricas** (one-hot encoding, target encoding)
- **Normalização de variáveis numéricas** para melhor performance dos modelos
- **Seleção de features** com técnicas de importância e correlação
- [Leia mais detalhes](README_03_engenharia_feature.md)

### 04 - Modelagem Preditiva

- **Comparação entre os algoritmos** de machine learning
- **Otimização de hiperparâmetros** com GridSearchCV 
- **Validação cruzada** para garantir robustez do modelo
- **Calibração de probabilidades** para uso em contexto de negócio
- **Análise de métricas** (AUC-ROC, F1-Score, Precision, Recall)
- [Leia mais detalhes](README_04_modelagem_preditiva.md)

### 05 - Insights de Negócio

- **Segmentação de clientes** por nível de risco e valor
- **Cálculo de ROI** para diferentes estratégias de retenção
- **Desenvolvimento de playbook** com ações específicas por segmento
- **Análise de sensibilidade** para otimização de threshold de classificação
- **Preparação de artefatos** para o dashboard executivo
- [Leia mais detalhes](README_05_business_insights.md)

## 🚀 Como Utilizar os Notebooks

### Pré-requisitos

- Python 3.9+
- Jupyter Notebook ou JupyterLab
- Bibliotecas listadas em `requirements.txt`

### Instalação e Execução

1. Instale as dependências necessárias:

```shell
pip install -r ../requirements.txt
```

2. Inicie o servidor Jupyter:

```shell
jupyter notebook
```

3. Execute os notebooks na ordem numérica (01 → 05) para seguir o fluxo completo de análise.

## 📈 Principais Resultados

- **Modelo de Regressão Logística Calibrada** com AUC-ROC de 0.85
- **Identificação dos principais fatores de risco**: Fibra Ótica, Contrato Mensal, Cliente Recente
- **Segmentação em 5 níveis de risco** com estratégias específicas para cada um
- **Projeção de ROI de 584%** nas ações de retenção propostas
- **Descoberta do "Paradoxo da Neutralidade"** em clientes sem interações com suporte

## 🔗 Links Relacionados

- [Dashboard Executivo](README_Dashboard.md)
- [Repositório Principal do Projeto](README.md)

------

![Estrelas](https://img.shields.io/github/stars/IvanAjala/telco-churn-prediction?style=social)
![Forks](https://img.shields.io/github/forks/IvanAjala/telco-churn-prediction?style=social)
![Licença](https://img.shields.io/badge/Licença-MIT-green)

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**

---
## 🔗 Navegação Rápida

**⬅️ [Anterior](../README.md)** | **[🔝 Voltar ao topo](#-visão-geral)** | **➡️ [Próximo](README_01_qualidade_dados)**

---

