# 📓 Notebooks de Análise
---
## 🎯 **Ordem de Execução Recomendada**

Execute os notebooks na seguinte ordem para garantir reprodutibilidade:

```graph LR

    A[📥 01_qualidade_dados] --> B[🧹 02_analise_exploratoria]
    B --> C[⚙️ 03_engenharia_feature]
    C --> D[🤖 04_modelagem_preditiva]
    D --> E[💼 05_business_insights]
```

## 📊 **Detalhamento dos Notebooks**
---
### 1. 📥 **`01_qualidade_dados.ipynb`**

#### _Análise Exploratória de Dados (EDA)_

**🎯 Objetivo**: Compreensão inicial dos dados e identificação de padrões

| Seção   | Conteúdo                          | Duração Estimada |
| ------- | --------------------------------- | ---------------- |
| **1.1** | Carregamento e inspeção inicial   | 15 min           |
| **1.2** | Análise descritiva e estatísticas | 20 min           |
| **1.3** | Análise univariada de variáveis   | 25 min           |
| **1.4** | Análise bivariada (vs churn)      | 30 min           |
| **1.5** | Correlações e visualizações       | 20 min           |
| **1.6** | Insights e hipóteses iniciais     | 15 min           |

**🔍 Principais Insights Gerados**:
``` text
┌────────────────────────────────────────────┬──────────────┐
│ Insight                                    │ Impacto      │
├────────────────────────────────────────────┼──────────────┤
│ Taxa de churn geral: 26.5%                 │ ⚠️ Moderado   │
│ Clientes mensais: 3x mais risco            │ 🔴 Crítico   │
│ Sem segurança digital: +45% churn          | 🟠 Alto      │
│ Tenure < 12 meses: +60% churn              │ 🟠 Alto      │
│ PaymentMethod: Eletronic Check (+22%)      │ 🟡 Médio     │
└────────────────────────────────────────────┴──────────────┘
```

**📁 Saídas**:

- `reports/figures/eda/`: Gráficos de análise
- `notebooks/insights/`: Insights documentados
- `data/processed/eda_summary.csv`: Sumário da EDA

---

### 2. 🧹 **`02_analise_exploratoria.ipynb`**

#### _Limpeza e Preparação de Dados_

**🎯 Objetivo**: Garantir qualidade e consistência dos dados

**🛠️ Transformações Aplicadas**:

|Variável|Problema|Solução|Impacto|
|---|---|---|---|
|**TotalCharges**|Tipo incorreto (object)|Conversão numérica|✅ Resolvido|
|**SeniorCitizen**|Codificação binária|Mapeado para categórico|✅ Melhoria|
|**Missing Values**|11 registros|Remoção segura|✅ Tratado|
|**Duplicatas**|0 encontrados|-|✅ OK|
|**Outliers**|Verificação|Limites definidos|✅ Controlado|

**📊 Dataset Final**:

```text
┌─────────────────────┬──────────────┐
│ Métrica             │ Valor        │
├─────────────────────┼──────────────┤
│ Clientes iniciais   │ 7,043        │
│ Clientes pós limpeza│ 7,032        │
│ Features            │ 20           │
│ Registros removidos │ 11 (0.16%)   │
│ Taxa de churn       │ 26.54%       │
└─────────────────────┴──────────────┘
```

**✅ Validações Realizadas**:

- ✅ Consistência de tipos de dados
- ✅ Domínios válidos para categóricas
- ✅ Range apropriado para numéricas
- ✅ Integridade referencial

**📁 Saída**

- `data/processed/churn_data_clean.csv`

---

### 3. ⚙️ **`03_engenharia_feature.ipynb`**

#### _Criação de Features Derivadas_

**🎯 Objetivo**: Criar features preditivas para modelagem

**🧩 Categorias de Features**:

```text
Total de Features: 64
├── 🏦 Financeiras (5)
│   ├── monthly_to_total_ratio
│   ├── avg_monthly_spend
│   └── spending_efficiency
├── 📅 Tenure (5)
│   ├── tenure_months
│   └── customer_segment
├── 🔧 Serviços (7)
│   ├── total_services
│   └── service_density
├── 📝 Contrato (5)
│   ├── contract_type_encoded
│   └── payment_method_risk
├── 👥 Demográficas (4)
│   ├── partner_dependents_score
│   └── demographic_risk
└── ⚠️ Risco (3)
    ├── overall_risk_score
    └── churn_propensity
```

**📈 Transformações**:

```python
# Exemplo de feature criada
data['tenure_risk_segment'] = pd.cut(data['tenure'], 
    bins=[0, 12, 24, 48, 100],
    labels=['Novo', 'Estável', 'Leal', 'Veterano'])

data['service_density'] = data['total_services'] / data['tenure']
```

**🔧 Técnicas Aplicadas**:

- One-Hot Encoding (categóricas)
- StandardScaler (numéricas)
- Binning (criação de categorias)
- Interação entre features

**📁 Saídas**:

- `X_train_full.csv`, `X_test_full.csv`
- `y_train.csv`, `y_test.csv`
- `models/model_features.txt`

---

### 4. 🤖 **`04_modelagem_preditiva.ipynb`**

#### _Modelagem Preditiva_

**🎯 Objetivo**: Desenvolver e otimizar modelo de previsão de churn

**📊 Comparação de Algoritmos**:

|Modelo|ROC-AUC|Recall|Precision|F1-Score|Calibração|
|---|---|---|---|---|---|
|**Random Forest**|0.8431|73.5%|56.5%|0.639|⭐ Melhor|
|XGBoost|0.8402|71.2%|57.1%|0.633|Bom|
|Logistic Regression|0.7954|68.9%|52.3%|0.594|Regular|
|Gradient Boosting|0.8385|70.5%|56.8%|0.629|Bom|
|SVM|0.8021|65.4%|54.9%|0.597|Regular|

**🔧 Otimização**:

```python
# Hiperparâmetros otimizados
best_params = {
    'n_estimators': 300,
    'max_depth': 15,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'max_features': 'sqrt',
    'class_weight': 'balanced'
}
```

**📈 Métricas do Modelo Final**:

```text
┌──────────────────────┬──────────────┬──────────────┐
│ Métrica              │ Valor        │ Status       │
├──────────────────────┼──────────────┼──────────────┤
│ ROC-AUC              │ 0.8431       | ⭐ Excelente │
│ Recall (Sensitiv)    │ 73.5%        | ✅ Bom       │
│ Precision            │ 56.5%        | ⚠️ Moderado   │
│ F1-Score             │ 0.639        | ✅ Bom       │
│ Calibration Error    │ 3.14%        | ⭐ Excelente │
│ Brier Score          │ 0.123        | ✅ Bom       │
└──────────────────────┴──────────────┴──────────────┘
```

**🎯 Calibração**:

- **Técnica**: `CalibratedClassifierCV` com Isotonic Regression
- **Resultado**: Redução de 9.82% no erro de calibração
- **Confiança**: Probabilidades mais confiáveis para decisão
    

**📁 Saídas**:

- `models/random_forest_calibrated_final.pkl`
- `models/model_metrics_calibrated.json
- `models/feature_importance.csv`
- `reports/figures/model_performance/`: Gráficos

---
### 5. 💼 **`05_business_insights.ipynb`**

#### _Análise de Negócio e Recomendações_

**🎯 Objetivo**: Traduzir resultados técnicos em ações de negócio

**🏷️ Segmentação de Clientes**:

|Segmento|Critério|Clientes|Churn Rate|Ação|
|---|---|---|---|---|
|**Crítico**|Prob > 0.8|62|89%|🔴 Intervenção Imediata|
|**Alto Risco**|Prob 0.6-0.8|187|73%|🟠 Contato Direto|
|**Médio Risco**|Prob 0.3-0.6|985|41%|🟡 Campanha Segmentada|
|**Baixo Risco**|Prob < 0.3|5,798|8%|🟢 Manutenção|

**💰 Impacto Financeiro**:

```text
┌────────────────────────┬──────────────┐
│ Métrica                │ Valor        │
├────────────────────────┼──────────────┤
│ Receita em Risco       │ R$ 2,547,820 │
│ Custo Campanha         │ R$ 728,000   │
│ Churn Evitado (est.)   │ 42%          │
│ Receita Preservada     │ R$ 1,070,000 │
│ ROI                    │ 350%         │
│ Lucro Líquido          │ R$ 625,000   │
└────────────────────────┴──────────────┘
```

**🎯 Sistema de Recomendações**:

|Segmento|Ação|Custo|Efetividade|
|---|---|---|---|
|Crítico|Oferta Personalizada + Retenção|Alto|65-80%|
|Alto Risco|Programa Fidelidade + Desconto|Médio|45-60%|
|Médio Risco|Comunicação Proativa|Baixo|25-40%|
|Baixo Risco|Manutenção Relacionamento|Mínimo|5-15%|

**📊 Dashboard de Métricas**:

- CLV (Customer Lifetime Value) por segmento
- LTV/CAC Ratio
- Churn Rate por canal
- ROI por ação de retenção

**📁 Saídas**:

- `data/processed/customers_with_recommendations.csv`
- `data/processed/segment_summary.csv`
- `data/processed/retention_playbook.json`
- `data/processed/business_metrics.json`
- Listas prioritárias *.csv (Top 20, 50, 100, 500)

---
## ⚙️ **Requisitos Técnicos**

### 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/telco-customer-churn-prediction.git

# Instale dependências
pip install -r requirements.txt

# Instale kernelspec para Jupyter
python -m ipykernel install --user --name=churn-prediction

# Execute Jupyter
jupyter notebook
```

### 🐍 Dependências Principais

```text
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0
matplotlib>=3.6.0
seaborn>=0.12.0
jupyter>=1.0.0
notebook>=6.5.0
ipykernel>=6.0.0
```

### 📁 **Estrutura de Dados Necessária**

```text
data/
└── raw/
    └── WA_Fn-UseC_-Telco-Customer-Churn.csv  ← Arquivo essencial
```
---
## 🚀 **Execução Rápida**

### Método 1: Execução Sequencial

```bash
# Execute na ordem
jupyter notebook notebooks/01_qualidade_dados.ipynb
jupyter notebook notebooks/02_analise_exploratoria.ipynb
jupyter notebook notebooks/03_engenharia_feature.ipynb
jupyter notebook notebooks/04_modelagem_preditiva.ipynb
jupyter notebook notebooks/05_business_insights.ipynb
```
### Método 2: Pipeline Automatizado

```bash
# Use o script de execução
python scripts/run_pipeline.py --all
```

### Método 3: Execução Parcial

```bash
#Apenas análise de negócio (após ter dados processados)
python scripts/run_pipeline.py --notebooks 05_business_insights
```
---
## 🔍 **Dicas de Uso**

### Para Análise

1. **Primeira Execução**: Siga a ordem numérica
2. **Reexecução**: Pode pular para notebooks específicos
3. **Customização**: Ajuste parâmetros nas primeiras células
### Para Desenvolvimento

```python
# Configure logging para debug
import logging
logging.basicConfig(level=logging.INFO)

# Ative interatividade
%matplotlib inline
%config InlineBackend.figure_format = 'retina'
```
### Para Produção

```python
# Converta para script Python
jupyter nbconvert --to script notebooks/*.ipynb

# Execute como pipeline
python notebooks/01_data_understanding.py
```

## 🆘 **Solução de Problemas**

### Problemas Comuns

1. **"File not found"**: Verifique se `WA_Fn-UseC_-Telco-Customer-Churn.csv` está em `data/raw/`
    
2. **"Memory error"**: Reduza o tamanho do dataset ou use amostragem
    
3. **"Dependency error"**: Execute `pip install -r requirements.txt --upgrade`

### Suporte

- **Issues**: [GitHub Issues](https://.github/ISSUE_TEMPLATE/bug_report.md)
- **Documentação**: [docs/](https://../docs/)
- **Email**: suporte-ds@empresa.com

---

## 📚 **Links Relacionados**

### Documentação

- [📖 Data Dictionary](https://../docs/data_dictionary.md)
- [🤖 Model Documentation](https://../docs/model_documentation.md)
- [🚀 Deployment Guide](https://../docs/deployment_guide.md)
### Scripts

- [🔄 run_pipeline.py](https://../scripts/run_pipeline.py)
- [📊 generate_reports.py](https://../scripts/generate_reports.py)


### Dashboards

- [📈 Model Performance](https://../reports/figures/model_performance/)
- [💼 Business Dashboard](https://../dashboard/app.py)

---
> **Nota**: Todos os notebooks foram testados com Python 3.9+. Garanta que todas as dependências estão instaladas antes da execução.

---
*Última atualização: 05/02/2026*
_Versão dos notebooks: 1.0.0_  
*Tempo total estimado de execução: 2-3 horas*

