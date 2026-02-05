# 📚 Dicionário de Dados

## 📋 **Visão Geral**

Este documento descreve todas as variáveis utilizadas no projeto de previsão de churn da operadora de telecomunicações, incluindo as variáveis originais, features criadas durante o processo de engenharia de features e métricas de negócio derivadas.

---

## 🎯 **Variáveis Originais do Dataset**

### 👤 **Informações Demográficas do Cliente**

|Variável|Tipo|Descrição|Valores|Preenchimento|% Ausentes|
|---|---|---|---|---|---|
|**customerID**|String|Identificador único do cliente|Alfa-numérico|100%|0%|
|**gender**|Categórica|Gênero do cliente|Male, Female|100%|0%|
|**SeniorCitizen**|Binária|Cliente é idoso (65+ anos)|0 = Não, 1 = Sim|100%|0%|
|**Partner**|Categórica|Cliente possui parceiro/companheiro|Yes, No|100%|0%|
|**Dependents**|Categórica|Cliente possui dependentes|Yes, No|100%|0%|

### 📞 **Serviços de Telecomunicações**

|Variável|Tipo|Descrição|Valores|Relação com Churn|
|---|---|---|---|---|
|**PhoneService**|Categórica|Possui serviço de telefonia fixa|Yes, No|Baixa|
|**MultipleLines**|Categórica|Possui múltiplas linhas telefônicas|Yes, No, No phone service|Moderada|
|**InternetService**|Categórica|Tipo de serviço de internet|DSL, Fiber optic, No|Alta|
|**OnlineSecurity**|Categórica|Possui segurança online|Yes, No, No internet service|Muito Alta|
|**OnlineBackup**|Categórica|Possui backup online|Yes, No, No internet service|Alta|
|**DeviceProtection**|Categórica|Possui proteção de dispositivo|Yes, No, No internet service|Moderada|
|**TechSupport**|Categórica|Possui suporte técnico|Yes, No, No internet service|Muito Alta|
|**StreamingTV**|Categórica|Possui streaming de TV|Yes, No, No internet service|Moderada|
|**StreamingMovies**|Categórica|Possui streaming de filmes|Yes, No, No internet service|Moderada|

### 💳 **Informações de Conta e Faturamento**

|Variável|Tipo|Descrição|Valores|Range|Estatísticas|
|---|---|---|---|---|---|
|**Contract**|Categórica|Tipo de contrato|Month-to-month, One year, Two year|-|Churn: 43% (mensal)|
|**PaperlessBilling**|Categórica|Fatura digital (sem papel)|Yes, No|-|59% Yes|
|**PaymentMethod**|Categórica|Método de pagamento|Electronic check, Mailed check, Bank transfer, Credit card|-|Churn: 34% (e-check)|
|**MonthlyCharges**|Numérica Contínua|Valor da mensalidade|-|18.25 - 118.75|Média: 64.76|
|**TotalCharges**|Numérica Contínua|Valor total acumulado|-|18.80 - 8684.80|Média: 2283.30|
|**tenure**|Numérica Discreta|Meses de permanência|-|0 - 72|Média: 32.37|

### 🎯 **Variável Target**

|Variável|Tipo|Descrição|Valores|Distribuição|Custo|
|---|---|---|---|---|---|
|**Churn**|Binária|Cliente cancelou o serviço|Yes, No|Yes: 26.5%  <br>No: 73.5%|Perda CLV|

---

## ⚙️ **Features Criadas (Feature Engineering)**

### 💰 **Features Financeiras**

|Feature|Tipo|Descrição|Fórmula|Interpretação|
|---|---|---|---|---|
|**AvgChargesPerMonth**|Contínua|Média histórica mensal|`TotalCharges / tenure`|Baixa → possível desconto inicial|
|**ChargesDifference**|Contínua|Variação da mensalidade|`MonthlyCharges - AvgChargesPerMonth`|Positiva → aumento recente|
|**ChargesRatio**|Contínua|Razão total/mensal|`TotalCharges / MonthlyCharges`|Alta → cliente de longo prazo|
|**EstimatedCLV**|Contínua|Valor estimado do cliente|`MonthlyCharges × 24`|CLV de 2 anos|
|**HighValueCustomer**|Binária|Cliente de alto valor|`MonthlyCharges > P75`|Percentil 75 (>87.86)|

### 📅 **Features de Tempo (Tenure)**

|Feature|Tipo|Descrição|Categorização|Churn Rate|
|---|---|---|---|---|
|**TenureGroup**|Categórica|Segmentação por tempo|Very_New (0-6), New (7-12), Intermediate (13-24), Established (25-48), Veteran (49+)|45%, 35%, 28%, 18%, 9%|
|**IsNewCustomer**|Binária|Cliente recente|`tenure ≤ 12`|38% churn|
|**IsVeteran**|Binária|Cliente veterano|`tenure > 48`|9% churn|
|**TenureYears**|Contínua|Tenure em anos|`tenure / 12`|-|
|**TenureQuartile**|Categórica|Quartis de tenure|Q1 (0-17), Q2 (18-35), Q3 (36-55), Q4 (56+)|-|

### 🔧 **Features de Serviços**

|Feature|Tipo|Descrição|Fórmula/Critério|Insights|
|---|---|---|---|---|
|**TotalServices**|Discreta|Quantidade total de serviços|Soma serviços adicionais|Média: 3.8|
|**HasManyServices**|Binária|Múltiplos serviços|`TotalServices ≥ 4`|Churn: 22%|
|**NoAdditionalServices**|Binária|Apenas serviço básico|`TotalServices = 1`|Churn: 31%|
|**SecurityServicesCount**|Discreta|Serviços de segurança|OnlineSec + Backup + Protect|0: 40% churn|
|**NoSecurityServices**|Binária|Sem serviços de segurança|`SecurityServicesCount = 0`|Churn: 41%|
|**StreamingServicesCount**|Discreta|Serviços de streaming|StreamingTV + Movies|-|
|**InternetWithoutServices**|Binária|Internet sem serviços extras|Internet=Yes ∧ Services=0|Churn: 44%|

### 📝 **Features de Contrato e Pagamento**

|Feature|Tipo|Descrição|Critério|Impacto Churn|
|---|---|---|---|---|
|**IsMonthlyContract**|Binária|Contrato mensal|Contract = Month-to-month|+25% vs anual|
|**IsLongTermContract**|Binária|Contrato longo prazo|Contract ∈ {One year, Two year}|-40% vs mensal|
|**IsElectronicCheck**|Binária|Pagamento por cheque eletrônico|PaymentMethod = Electronic check|+22% vs outros|
|**IsAutomaticPayment**|Binária|Pagamento automático|PaymentMethod ∈ {Bank transfer, Credit card}|-18% vs cheque|
|**HighRiskPaymentContract**|Binária|Alto risco|Monthly + Electronic check|Churn: 55%|

### 👥 **Features Demográficas Compostas**

|Feature|Tipo|Descrição|Pontuação|Peso Churn|
|---|---|---|---|---|
|**IsAlone**|Binária|Vive sozinho|Partner=No ∧ Dependents=No|+15%|
|**HasFamily**|Binária|Com família|Partner=Yes ∧ Dependents=Yes|-12%|
|**SeniorAlone**|Binária|Idoso vivendo só|Senior=Yes ∧ Alone=Yes|+25%|
|**DemographicRiskScore**|Discreta|Score de risco|Senior(1) + Alone(1) + NoFamily(1)|0-3|

### ⚠️ **Features de Risco Composto**

|Feature|Tipo|Descrição|Componentes|Weight|
|---|---|---|---|---|
|**CompositeRiskScore**|Discreta|Score composto|12 indicadores|0-12|
|**CompositeRiskScore_Normalized**|Contínua|Score normalizado|`(Score / 12) × 10`|0-10|
|**RiskLevel**|Categórica|Nível de risco|Low(0-3), Medium(4-6), High(7-9), Critical(10-12)|-|

```text
Fórmula do CompositeRiskScore:
├── Contract Mensal (2 pontos)
├── Electronic Check (2 pontos)
├── Tenure < 12 meses (2 pontos)
├── Sem Security Services (2 pontos)
├── Internet Fiber (1 ponto)
├── Senior Citizen (1 ponto)
├── Sem Partner (1 ponto)
├── MonthlyCharges > P75 (1 ponto)
└── Total: 0-12 pontos
```

---

## 🤖 **Features Geradas pelo Modelo**

### 🎯 **Predições e Probabilidades**

|Feature|Tipo|Range|Interpretação|Ação Recomendada|
|---|---|---|---|---|
|**Churn_Probability**|Contínua|0-1|Probabilidade estimada|0-0.3: Baixa  <br>0.3-0.6: Média  <br>0.6-0.8: Alta  <br>0.8-1: Crítica|
|**Predicted_Churn**|Binária|0,1|Classificação (threshold=0.5)|Base para campanhas|
|**Risk_Level**|Categórica|4 níveis|Classificação de risco|Segmentação de ações|
|**Priority_Score**|Contínua|0-1|Score de priorização|Ordenação de clientes|
|**Priority_Score_Normalized**|Contínua|0-100|Score normalizado|Comparação direta|

### 📊 **Métricas do Modelo**

|Métrica|Valor|Interpretação|Benchmark|
|---|---|---|---|
|**ROC-AUC**|0.8431|Excelente capacidade discriminativa|>0.8: Bom  <br>>0.85: Excelente|
|**Recall**|73.5%|Captura 73.5% dos churns reais|Balance com Precision|
|**Precision**|56.5%|56.5% dos preditos são churn real|Trade-off com Recall|
|**Calibration Error**|3.14%|Probabilidades bem calibradas|<5%: Excelente|

---

## 💼 **Features de Negócio (Business Intelligence)**

### 💰 **Métricas Financeiras**

|Feature|Tipo|Fórmula|Interpretação|Exemplo|
|---|---|---|---|---|
|**CLV**|Contínua|`MonthlyCharges × (1/Churn_Probability) × 12`|Valor do cliente considerando churn|$100/mês × 20 meses = $2000|
|**Revenue_at_Risk**|Contínua|`Churn_Probability × CLV`|Receita em risco de perda|0.8 × $2000 = $1600|
|**Action_Cost**|Contínua|Baseado em Risk_Level|Custo da ação de retenção|Crítico: $150  <br>Alto: $75  <br>Médio: $30|
|**Conversion_Rate**|Contínua|Baseado em Risk_Level|Taxa esperada de sucesso|Crítico: 15%  <br>Alto: 30%  <br>Médio: 50%|
|**Revenue_Recovered**|Contínua|`Revenue_at_Risk × Conversion_Rate`|Receita recuperável|$1600 × 15% = $240|
|**Net_Profit**|Contínua|`Revenue_Recovered - Action_Cost`|Lucro líquido|$240 - $150 = $90|
|**Expected_ROI**|Contínua|`(Net_Profit / Action_Cost) × 100`|Retorno sobre investimento|($90 / $150) × 100 = 60%|

### 🎯 **Sistema de Recomendações**

|Risk_Level|Probabilidade|Clientes|Ação Recomendada|Custo|Efetividade|
|---|---|---|---|---|---|
|**CRÍTICO**|> 80%|62|Oferta Personalizada + Retenção|$150|15-25%|
|**ALTO**|60-80%|187|Programa Fidelidade + Desconto|$75|30-45%|
|**MÉDIO**|30-60%|985|Comunicação Proativa|$30|45-60%|
|**BAIXO**|< 30%|5,798|Manutenção Relacionamento|$5|70-85%|

### 📋 **Listas de Priorização**

|Lista|Critério|Clientes|Receita em Risco|ROI Esperado|
|---|---|---|---|---|
|**Top 20 Críticos**|Prob > 90%|20|$480,000|45%|
|**Top 50 Alta Prioridade**|Prob 80-90%|50|$750,000|60%|
|**Top 100 Prioridade**|Prob 70-80%|100|$1,200,000|75%|
|**Top 500 Monitoramento**|Prob > 60%|500|$3,500,000|85%|

---

## 🔄 **Pipeline de Transformação**

### **Fluxo de Processamento**

```text
Dados Originais (20 features)
    ↓
Data Cleaning (Tratamento de missing, tipos)
    ↓
Feature Engineering (+44 features)
    ↓
Model Training (Seleção de 64 features)
    ↓
Business Features (+8 features)
    ↓
Dashboard e Relatórios
```

### **Resumo de Features**

```text
Total Features: 72
├── Originais: 20
├── Engenharia: 44
├── Modelo: 4
└── Negócio: 4

Features por Tipo:
├── Numéricas: 38 (53%)
├── Categóricas: 22 (30%)
├── Binárias: 12 (17%)
└── Target: 1
```

---
## 📊 **Distribuições Chave**

### **Tenure vs Churn**

``` text
Meses   | Churn Rate
--------|-----------
0-6     | 45.2%Tipo      | Churn Rate
----------|-----------
Mensal    | 42.7%
Anual     | 11.3%
Bienal    | 2.8%
7-12    | 35.1%
13-24   | 27.8%
25-48   | 18.4%
49+     | 9.1%
```

### **Contract Type vs Churn**

``` text
Tipo      | Churn Rate
----------|-----------
Mensal    | 42.7%
Anual     | 11.3%
Bienal    | 2.8%
```

### **Payment Method vs Churn**

``` text
Método          | Churn Rate
----------------|-----------
Electronic check| 33.6%
Mailed check    | 19.3%
Bank transfer   | 16.2%
Credit card     | 15.7%
```

## ⚠️ **Considerações Importantes**

### **Features Mais Importantes (SHAP Values)**

1. **Contract Type** - Maior impacto no modelo
2. **Tenure** - Relação inversa com churn
3. **Monthly Charges** - Relação direta (contrato mensal)
4. **Online Security** - Fator de proteção forte
5. **Tech Support** - Reduz significativamente churn

### **Limitações das Features**

- **TotalCharges**: Tem missing values tratados
- **SeniorCitizen**: Desbalanceada (16% idosos)
- **Internet Services**: Features condicionais

### **Recomendações de Uso**

1. Sempre usar **todas as 64 features** para predição
2. Manter **mesmo pré-processamento** dos dados de treino
3. Atualizar **periódicamente** as features de negócio
4. Monitorar **drift** nas distribuições das features

---

## 🔗 **Relacionamentos Chave**

### **Correlações Fortes (>0.4)**

- `MonthlyCharges` ↔ `InternetService` (Fiber optic)
- `TotalServices` ↔ `MonthlyCharges`
- `Tenure` ↔ `TotalCharges`
- `Contract` ↔ `Churn_Probability`

### **Interações Significativas**

- Internet Fiber + Contract Mensal = Alto Risco
- Tenure Baixo + Many Services = Risco Moderado
- Senior Citizen + Electronic Check = Alto Risco
- Long Contract + Auto Payment = Baixo Risco

---

## 📈 **Monitoramento e Manutenção**

### **Features a Monitorar**

1. **Distribuição de Churn_Probability** (média, desvio)
2. **Calibration do Modelo** (erro < 5%)
3. **CLV Médio** por segmento
4. **ROI Real** vs Esperado

### **Frequência de Atualização**

- **Diário**: Features de risco e priorização
- **Semanal**: Métricas de negócio
- **Mensal**: Retreino do modelo
- **Trimestral**: Reavaliação de features

---

> **Nota**: Este dicionário é dinâmico e será atualizado conforme novas features forem desenvolvidas ou modificadas.

---

*Última atualização: 05/02/2026*  
_Versão do Dicionário: 2.0.0_  
_Total de Features Documentadas: 72_

