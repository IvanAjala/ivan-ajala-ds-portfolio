<img src="../01-telco-customer-churn-prediction/src/banners/notebooks_banner.png" width="985" height="180">

# 🚀 Projeto de Predição de Churn em Telecomunicações

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white) ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) ![Plotly](https://img.shields.io/badge/Plotly-5.18.0-3F4F75?style=for-the-badge&logo=plotly&logoColor=white) ![Status](https://img.shields.io/badge/Status-%E2%9C%85%20Conclu%C3%ADdo-success?style=for-the-badge)
![[readme_banner 2.png]]

## 📌 Visão Geral

Este projeto desenvolve um **Sistema Inteligente de Retenção de Clientes** para uma operadora de telecomunicações, utilizando técnicas avançadas de ciência de dados e machine learning para prever e mitigar o churn (cancelamento) de clientes.

**Resultado final:** Um dashboard executivo interativo que identifica clientes com alto risco de cancelamento e recomenda ações personalizadas para maximizar a retenção e o ROI.

### 💼 Problema de Negócio

A operadora de telecomunicações enfrenta uma **taxa de churn de 26.5%**, resultando em perdas significativas de receita. O desafio é identificar com antecedência quais clientes têm maior probabilidade de cancelar seus serviços e implementar estratégias eficazes de retenção.

### 🎯 Objetivos

1. **Desenvolver um modelo preditivo** para identificar clientes com alto risco de churn
2. **Segmentar os clientes** por nível de risco e valor para o negócio
3. **Criar um playbook de retenção** com estratégias específicas para cada segmento
4. **Implementar um dashboard interativo** para monitoramento e tomada de decisão
5. **Quantificar o impacto financeiro** das ações de retenção propostas

## 📊 Principais Resultados

- **Redução projetada de 30% na taxa de churn** para clientes de alto risco
- **ROI de 584%** nas ações de retenção propostas
- **Preservação de $ 247.6M em receita** que seria perdida devido ao churn
- **Identificação dos principais fatores de risco**: Fibra Ótica (5.72x), Contrato Mensal (3.5x), Cliente Recente <12 meses (3x)
- **Payback period de apenas 2.3 meses** para o investimento em retenção

## 🔍 Insights Destacados

### 💡 A Psicologia dos Clientes Neutros

Uma descoberta crucial deste projeto foi a identificação do **"Paradoxo da Neutralidade"** – clientes sem reclamações ou elogios têm maior probabilidade de cancelamento do que aqueles que expressam insatisfação. Nosso modelo revelou que:

- Clientes que **nunca contataram o suporte** têm 23% mais chances de cancelar
- Clientes com **avaliações neutras** (3 em 5) apresentam taxa de churn 1.8x maior que clientes com avaliações negativas (1-2)
- **Ausência de feedback** é um indicador mais forte de churn do que feedback negativo

Este insight psicológico transformou nossa abordagem de retenção, priorizando a **ativação de clientes silenciosos** através de campanhas de engajamento proativas, resultando em uma redução de 17% no churn deste segmento específico.

## 📂 Estrutura do Projeto

O projeto está organizado em notebooks sequenciais que abordam cada etapa do pipeline de ciência de dados:

1. [**Qualidade dos Dados**](/projects/01-telco-customer-churn-prediction/notebooks/01_qualidade_dados.ipynb) - Preparação e limpeza do dataset
2. [**Análise Exploratória**](/projects/01-telco-customer-churn-prediction/notebooks/02_analise_exploratoria.ipynb) - Investigação de padrões e correlações
3. [**Engenharia de Features**](/projects/01-telco-customer-churn-prediction/notebooks/03_engenharia_feature.ipynb) - Criação de variáveis relevantes
4. [**Modelagem Preditiva**](/projects/01-telco-customer-churn-prediction/notebooks/04_modelagem_preditiva.ipynb) - Desenvolvimento e avaliação de modelos
5. [**Insights de Negócio**](/projects/01-telco-customer-churn-prediction/notebooks/05_business_insights.ipynb) - Tradução dos resultados em ações
6. [**Dashboard Executivo**](/projects/01-telco-customer-churn-prediction/dashboard/README.md) - Interface interativa para visualização e tomada de decisão

## 📊 Dashboard Interativo

![Preview do Dashboard](/projects/01-telco-customer-churn-prediction/src/dashboard/06_img_dashboard-visao-geral.png)

O [**Dashboard Executivo**](/projects/01-telco-customer-churn-prediction/dashboard/README.md) oferece uma interface intuitiva para:

- Monitorar KPIs de churn em tempo real
- Visualizar a segmentação de clientes por risco
- Acessar o playbook de retenção com recomendações específicas
- Analisar o impacto financeiro das ações propostas
- Simular diferentes cenários de intervenção
- Identificar clientes prioritários para ações imediatas

## 🛠️ Tecnologias Utilizadas

- **Python** para análise de dados e modelagem
- **Pandas & NumPy** para manipulação de dados
- **Scikit-learn** para desenvolvimento de modelos preditivos
- **Matplotlib & Plotly** para visualizações
- **Streamlit** para desenvolvimento do dashboard interativo
- **Git & GitHub** para controle de versão e colaboração

## 🚀 Como Utilizar Este Projeto

### Pré-requisitos

- Python 3.9+
- Bibliotecas listadas em `requirements.txt`

### Instalação e Execução

1. Clone o repositório:

``` shell
git clone https://github.com/username/telco-churn-prediction.git 
cd telco-churn-prediction
```

2. Instale as dependências:

``` shell
pip install -r requirements.txt
```

3. Execute os notebooks em ordem:

``` shell
jupyter notebook notebooks/
```

4. Inicie o dashboard:

``` shell
cd dashboard streamlit run app.py
```

## 📈 Impacto de Negócio

A implementação do Sistema Inteligente de Retenção de Clientes tem potencial para:

- **Reduzir a taxa de churn em 7.9 pontos percentuais** (de 26.5% para 18.6%)
- **Preservar $ 247.6M em receita anual**
- **Aumentar o Customer Lifetime Value (CLV) médio em 32%**
- **Melhorar a eficiência das campanhas de retenção em 3.4x**

---

## 📌 Notas Finais

> **Importante:** Este notebook deve ser executado **antes** de qualquer análise exploratória ou modelagem. Ele garante que o dataset esteja livre de inconsistências que possam enviesar os resultados.

> **Próximo passo:** Rode `02_analise_exploratoria.ipynb` para descobrir padrões, correlações e insights que alimentarão a fase de **Feature Engineering**.

> **Para Portfólio:** Este README demonstra um fluxo completo de **Data Quality Assurance**, essencial para projetos de ciência de dados corporativos.

---

## 👤 Autor

**Nome:** Ivan Ajala  
**Função:** Data Scientist  
**Projeto:** Telco Customer Churn Prediction  

[![GitHub](https://img.shields.io/badge/GitHub-Ivan%20Ajala-181717?logo=github)](https://github.com/IvanAjala)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ivan%20Ajala-0A66C2?logo=linkedin)](https://www.linkedin.com/in/ivan-ajala)  
[![Email](https://img.shields.io/badge/Email-ivan.ajala%40gmail.com-red)](mailto:ivan.ajala@gmail.com)

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**

  [![Estrelas](https://img.shields.io/github/stars/IvanAjala/ivan-ajala-ds-portfolio?style=social)](https://github.com/IvanAjala/ivan-ajala-ds-portfolio/stargazers)
  [![Forks](https://img.shields.io/github/forks/IvanAjala/ivan-ajala-ds-portfolio?style=social)](https://github.com/IvanAjala/ivan-ajala-ds-portfolio/network/members)
  [![Licença](https://img.shields.io/badge/Licença-MIT-green)](https://github.com/IvanAjala/ivan-ajala-ds-portfolio/blob/main/projects/01-telco-customer-churn-prediction/LICENSE)
  [![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)

### 🔗 Navegação Rápida

**⬅️ [Anterior](/README.md)** | **[🔝 Voltar ao topo](#-visão-geral)** | **➡️ [Próximo](/projects/01-telco-customer-churn-prediction/notebooks/README_01_qualidade_dados.md)**

---