<img src="/src/banners/readme_banner.png" width="985" height="180">

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
- **Preservação de R$ 247.6M em receita** que seria perdida devido ao churn
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

1. [**Qualidade dos Dados**](../notebooks/README_01_qualidade_dados.md) - Preparação e limpeza do dataset
2. [**Análise Exploratória**](https://app.innerai.com/notebooks/README_02_analise_exploratoria.md) - Investigação de padrões e correlações
3. [**Engenharia de Features**](https://app.innerai.com/notebooks/README_03_engenharia_feature.md) - Criação de variáveis relevantes
4. [**Modelagem Preditiva**](https://app.innerai.com/notebooks/README_04_modelagem_preditiva.md) - Desenvolvimento e avaliação de modelos
5. [**Insights de Negócio**](https://app.innerai.com/notebooks/README_05_business_insights.md) - Tradução dos resultados em ações
6. [**Dashboard Executivo**](https://app.innerai.com/dashboard/README_Dashboard.md) - Interface interativa para visualização e tomada de decisão

## 📊 Dashboard Interativo

![[06_img_dashboard-visao-geral 1.png]]
![Preview do Dashboard](../src/notebooks/06_img_dashboard-visao-geral.png)

O [**Dashboard Executivo**](https://app.innerai.com/dashboard/README_Dashboard.md) oferece uma interface intuitiva para:

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
- **Preservar R$ 247.6M em receita anual**
- **Aumentar o Customer Lifetime Value (CLV) médio em 32%**
- **Melhorar a eficiência das campanhas de retenção em 3.4x**

## 👥 Equipe e Contato

**Desenvolvedor:** Ivan Ajala  
**E-mail:** ivan.ajala@example.com  
**LinkedIn:** [linkedin.com/in/ivanajala](https://linkedin.com/in/ivanajala)  
**GitHub:** [github.com/ivanajala](https://github.com/ivanajala)

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

---

![Estrelas](https://img.shields.io/github/stars/IvanAjala/telco-churn-prediction?style=social)
![Forks](https://img.shields.io/github/forks/IvanAjala/telco-churn-prediction?style=social)
![Licença](https://img.shields.io/badge/Licença-MIT-green)

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**

---
## 🔗 Navegação Rápida

**⬅️ [Anterior](README_01.md)** | **📋 [Índice](README.md)** | **➡️ [Próximo](README)**

---

_Desenvolvido como parte do portfólio de Data Science de Ivan Ajala, 2025_