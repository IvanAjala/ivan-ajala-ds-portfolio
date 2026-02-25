# ✨ Notebook 01 - Qualidade de Dados & Limpeza


![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white) ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) ![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Status](https://img.shields.io/badge/Status-✅%20Concluído-success?style=for-the-badge) ![Células](https://img.shields.io/badge/Células-92-yellow?style=for-the-badge) ![Complexidade](https://img.shields.io/badge/Complexidade-⭐⭐⭐-orange?style=for-the-badge)

**Sistema Inteligente de Retenção de Clientes - Telecomunicações**

[📓 Notebook](/projects/01-telco-customer-churn-prediction/notebooks/01_qualidade_dados.ipynb) • [📊 Dataset](/projects/01-telco-customer-churn-prediction/data/raw/) • [📚 Docs](/projects/01-telco-customer-churn-prediction/docs/)

---
## 📋 Visão Geral

| 📊 Métrica | 📈 Valor |
|-----------|---------|
| **Arquivo** | `01_qualidade_dados.ipynb` |
| **Tipo** | ✨ Qualidade de Dados & Limpeza |
| **Total de Células** | 92 |
| **Células de Código** | 48 |
| **Células de Texto** | 44 |
| **Outputs Gerados** | 0 |
| **Visualizações** | 5 |
| **Complexidade** | ⭐⭐⭐ (Intermediário) |
| **Tempo Estimado** | 20-30 minutos |
| **Data de Criação** | 06/02/2026 |
| **Última Atualização** | 06/02/2026 |

---
## 🎯 Objetivo Principal

Este notebook é a **primeira etapa fundamental** do pipeline de Machine Learning para predição de Churn. Seu objetivo é garantir que o dataset esteja **limpo, consistente e pronto** para as fases subsequentes de Análise Exploratória e Modelagem.

**Principais metas:**

1.  **Verificar a estrutura** (dimensões, tipos de dados, valores únicos).
2.  **Detectar e tratar valores ausentes** de forma estratégica.
3.  **Eliminar duplicatas** e validar a unicidade dos IDs de cliente.
4.  **Corrigir tipos de dados incorretos** (ex.: `TotalCharges` de `object` para `numeric`).
5.  **Padronizar categorias** em variáveis categóricas (ex.: "No internet service" para "No").
6.  **Identificar e analisar outliers** e valores ilógicos, decidindo sobre seu tratamento.
7.  **Exportar o dataset limpo** para a pasta `data/processed`, garantindo rastreabilidade.

---
## 🚀 Resultados Alcançados
### 📊 Estatísticas Finais de Qualidade

| 📈 Métrica | 📊 Valor | 🎯 Status |
|-----------|---------|-----------|
| **Total de Registros** | 7,043 | ✅ |
| **Total de Colunas** | 21 | ✅ |
| **Valores Ausentes** | 0 | ✅ |
| **Registros Duplicados** | 0 | ✅ |
| **IDs de Cliente Únicos** | 7,043 | ✅ |
| **`TotalCharges` (Tipo)** | `float64` | ✅ |
| **Checkpoints Aprovados** | 100% | 🎉 |

---
## 🔧 Stack Tecnológico

### 📚 Bibliotecas Principais

```bash
import pandas as pd # Manipulação e análise de dados 
import numpy as np # Operações numéricas 
import matplotlib.pyplot as plt # Visualização de dados 
import seaborn as sns # Visualização estatística aprimorada 
from pathlib import Path # Manipulação de caminhos de arquivo 
import datetime # Para timestamps no log
```
### 🛠️ Técnicas Aplicadas

| Técnica | Aplicação |
|---------|-----------|
| **Data Cleaning** | Conversão de tipos, tratamento de missing, remoção de duplicatas |
| **Exploratory QA** | Análise de outliers, consistência lógica (tenure × charges) |
| **Logging** | Registro de cada transformação para rastreabilidade |
| **Padronização** | Consistência de valores categóricos |
| **Exportação** | Persistência do dataset limpo e log de transformações |

---
## 📁 Estrutura do Notebook

```
📓 01_qualidade_dados.ipynb │ 
├── 1. Configuração Inicial 
├── 2. Carregamento dos Dados
├── 3. Inspeção da Estrutura dos Dados │ 
	├── 3.1 Dimensões do Dataset │ 
	├── 3.2 Tipos de Dados e Valores Não-Nulos │ 
	├── 3.3 Estatísticas Descritivas 
	│ └── 3.4 Contagem de Valores Únicos │ 
├── 4. Detecção de Problemas Críticos │ 
	├── 4.1 Problema 1: Coluna 'TotalCharges' como 'object' │ 
	├── 4.2 Problema 2: Valores Ausentes │ 
	└── 4.3 Problema 3: Registros Duplicados e IDs de Cliente │ 
├── 5. Tratamento de Dados │ 
	├── 5.1 Tratamento de 'TotalCharges' │ 
	├── 5.2 Tratamento de Valores Ausentes │ 
	├── 5.3 Tratamento de Duplicatas │ 
	├── 5.4 Padronização de Categorias │ 
	└── 5.5 Análise e Tratamento de Outliers (Decisão: Manter) │ 
├── 6. Validações & Checkpoints de Qualidade │ 
	├── 6.1 Verificação Final de Valores Ausentes │ 
	├── 6.2 Verificação Final de Duplicatas │ 
	├── 6.3 Verificação Final de Tipos de Dados │ 
	└── 6.4 Verificação de Consistência Lógica │ 
├── 7. Exportação do Dataset Limpo e Log de Transformações │ 
	├── 7.1 Exportar Dataset Limpo │ 
	└── 7.2 Exportar Log de Transformações │ 
└── 8. Resumo Final
```
---
## 🚀 Como Executar

### 1️⃣ Pré-requisitos

Para executar este notebook, você precisará das seguintes bibliotecas. Instale-as usando pip:

```bash
pip install pandas numpy matplotlib seaborn
```

### 2️⃣ Executar Notebook

```bash
cd notebooks
jupyter notebook 01_qualidade_dados.ipynb
```
### 3️⃣ Executar Todas as Células

```
Kernel → Restart & Run All
```

---
## 🔗 Integração com o Pipeline

| Entrada                                         | Saída                                                 |
| ----------------------------------------------- | ----------------------------------------------------- |
| `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv` | `data/processed/churn_data_clean_v1.csv`              |
| Configurações de logging                        | `transformations_log.json` (arquivo JSON)             |
| Métricas de qualidade                           | Variáveis `completude`, `consistência`, `checkpoints` |

➡️ **Próxima etapa:** `02_analise_exploratoria.ipynb` (EDA)

---
## ⚠️ Possíveis Problemas e Soluções

| Problema | Sintoma | Solução |
|----------|---------|---------|
| **`TotalCharges` como `object`** | Erro ao calcular estatísticas numéricas, valores não numéricos. | `pd.to_numeric(..., errors='coerce')` para converter para numérico, seguido de `fillna(0)` para clientes com `tenure = 0` (novos clientes sem cobrança total). |
| **Valores ausentes** | `df.isnull().sum()` > 0 em colunas importantes. | Identificado em `TotalCharges` (11 registros). Preenchido com `0` após conversão de tipo. |
| **IDs duplicados** | `df['customerID'].nunique() < len(df)`. | Nenhuma duplicata encontrada. Caso houvesse, a estratégia seria remover ou manter a primeira ocorrência. |
| **Outliers extremos** | Boxplots mostram pontos muito distantes do IQR. | Identificados em `MonthlyCharges` e `TotalCharges`. Decisão de **manter** por representarem clientes reais e serem importantes para a predição de churn. |
| **Inconsistência entre `tenure`, `MonthlyCharges` e `TotalCharges`** | `TotalCharges` não é `MonthlyCharges * tenure`. | Diferenças esperadas devido a descontos, promoções ou arredondamentos. **Mantido** conforme a lógica de negócio. |

---
## 📈 Métricas de Performance

| Métrica | Valor | Status |
|---------|-------|--------|
| **Tempo de execução** | ~25 min | ⚡ |
| **Uso de memória** | 6.8 MB | 💾 |
| **Total de registros** | 7,043 | ✅ |
| **Colunas** | 21 | ✅ |
| **Valores ausentes** | 0 | ✅ |
| **Duplicatas** | 0 | ✅ |
| **Checkpoints aprovados** | 100% | 🎉 |

---
## 💡 Dicas para Uso

| Cenário             | Recomendações                                                                                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Análise rápida**  | Execute o notebook inteiro; verifique o `transformations_log.json` ao final para confirmar as transformações.                                                        |
| **Desenvolvimento** | Alterar parâmetros de preenchimento (ex.: valor de `TotalCharges`) e testar em um *subset* antes de rodar no dataset completo.                                       |
| **Produção**        | Converta o notebook em script (`nbconvert`) e automatize a execução via CI/CD; persista o `scaler.pkl` (se aplicável) e o `transformations_log.json` para auditoria. |


## 📌 Notas Finais

> **Importante:** Este notebook deve ser executado **antes** de qualquer análise exploratória ou modelagem. Ele garante que o dataset esteja livre de inconsistências que possam enviesar os resultados.

> **Próximo passo:** Execute `02_analise_exploratoria.ipynb` para descobrir padrões, correlações e insights que alimentarão a fase de **Feature Engineering**.

> **Para Portfólio:** Este README demonstra um fluxo completo de **Data Quality Assurance**, essencial para projetos de ciência de dados corporativos.


## 🔄 Notas de Versão

| Versão     | Data       | Alterações                                                                                       |
| ---------- | ---------- | ------------------------------------------------------------------------------------------------ |
| **v1.0.0** | 07/12/2025 | Pipeline de qualidade completo – 92 células, 5 visualizações, exportação de dataset limpo.       |
| **v1.1.0** | 15/01/2026 | Adição de *logging* detalhado, melhoria nos checkpoints e inclusão de visualizações de outliers. |
| **v2.0.0** | 08/02/2026 | Revisão textual e ajustes necessários na escrita para melhor entendimento.                             |
| **v2.1.0** | 25/02/2026 | Atualização e revisão final (código e documentação).              |

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

---

### 🔗 Navegação Rápida

**⬅️ [Anterior](/README.md)** | **[🔝 Voltar ao topo](#-visão-geral)** | **➡️ [Próximo](README_02_analise_exploratoria.md)**

---

