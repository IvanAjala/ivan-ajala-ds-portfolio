# 🎯 Dashboard Streamlit - Churn Prediction

## 📋 **Visão Geral**

Dashboard executivo interativo para análise preditiva de churn, segmentação de clientes e tomada de decisão baseada em dados.

---

## ✨ **Funcionalidades Principais**

### 🏠 **📊 Visão Geral**

_KPIs em tempo real e métricas consolidadas_

- Dashboard executivo com métricas-chave
- Distribuição de clientes por nível de risco
- Evolução temporal das taxas de churn
- Indicadores financeiros consolidados

### 🎯 **🎯 Segmentação de Clientes**

_Análise detalhada por perfil de risco_

- Distribuição por segmentos (Crítico, Alto, Médio, Baixo)
- Scatter plots interativos com múltiplas dimensões
- Comparações entre segmentos
- Análise demográfica por grupo

### 💡 **💡 Recomendações Personalizadas**

_Sistema inteligente de ações de retenção_

- Playbook de ações específicas por segmento
- Distribuição de recomendações otimizadas
- Listas de clientes por tipo de ação
- Estimativa de efetividade por intervenção

### 💰 **💰 Análise Financeira**

_ROI e impacto econômico das ações_

- Gráfico de cascata (waterfall) de receita
- ROI estimado por segmento
- Análise de custo-benefício
- Simulação de cenários financeiros

### 👥 **👥 Clientes Prioritários**

_Gestão de campanhas de retenção_

- Tabela interativa com filtros avançados
- Download de listas em múltiplos formatos
- Resumo de métricas por prioridade
- Atribuição de agentes/equipes
---

## 🚀 **Como Executar**

### **1. 📦 Instalação Local**

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/telco-customer-churn-prediction.git

# Navegue para a pasta do dashboard
cd telco-customer-churn-prediction/dashboard

# Instale as dependências
pip install -r requirements.txt
```

### **2. ▶️ Execução**

```bash
# Execute o dashboard
streamlit run app.py
```

### **3. 🌐 Acesso**

O dashboard será aberto automaticamente no seu navegador padrão:

- **URL Local**: `http://localhost:8501`
- **Porta alternativa**: `streamlit run app.py --server.port 8502`

---
## 📁 **Estrutura do Projeto**

```text
dashboard/
├── 📄 app.py                      # Aplicação principal
├── 📁 pages/                      # Páginas multi-page
│   ├── 📄 1_Visao_Geral.py        # Página: Visão Geral
│   ├── 📄 2_Segmentacao.py        # Página: Segmentação
│   ├── 📄 3_Recomendacoes.py      # Página: Recomendações
│   ├── 📄 4_Analise_Financeira.py    # Página: Análise Financeira
│   └── 📄 5_Clientes_Prioritarios.py # Página: Clientes Prioritários
├── 📁 utils/                         # Funções auxiliares
│   ├── 📄 __init__.py
│   └── 📄 helpers.py        # Funções de carregamento e processamento
├── 📁 assets/               # Recursos estáticos
│   ├── 🖼️ logo.png          # Logo da aplicação
│   └── 🎨 style.css         # Estilos customizados
├── 📄 requirements.txt      # Dependências específicas do dashboard
└── 📄 README.md             # Esta documentação
```

## 🎛️ **Filtros e Controles**

### **🔍 Filtros Disponíveis**

|Filtro|Tipo|Descrição|
|---|---|---|
|**Nível de Risco**|Multi-select|Crítico, Alto, Médio, Baixo|
|**Probabilidade de Churn**|Range Slider|0% a 100%|
|**Customer Lifetime Value (CLV)**|Range Input|Faixa de valor|
|**Tenure (Meses)**|Range Slider|Tempo como cliente|
|**Método de Pagamento**|Dropdown|Tipos de pagamento|
|**Tipo de Contrato**|Checkbox|Mensal, Anual, Bienal|
|**Serviços Adicionais**|Multi-select|Internet, TV, Streaming, etc.|

### **📊 Visualizações Interativas**

|Gráfico|Tipo|Interatividade|
|---|---|---|
|Distribuição de Risco|Donut Chart|Clique para filtrar|
|Scatter Plot|2D/3D|Zoom e pan|
|Waterfall Chart|Barra|Hover para detalhes|
|Heatmap|Matriz|Clique para detalhar|
|Tabela Clientes|DataFrame|Ordenação e filtro|

---

## 📥 **Downloads e Exportações**

### **📁 Formatos Suportados**

- **CSV**: Para análise em Excel/BI
- **Excel (.xlsx)**: Com formatação
- **JSON**: Para integrações
- **PDF**: Relatórios executivos
- **PNG**: Gráficos em alta resolução

### **📋 Conteúdos Exportáveis**

1. **Dataset Completo** com todas as métricas
2. **Listas de Clientes Prioritários** (Top 20, 50, 100, 500)
3. **Resumos por Segmento** com métricas consolidadas
4. **Recomendações por Cliente** com ações específica

---

## ☁️ **Deploy em Produção**

### **Opção 1: Streamlit Cloud (Recomendado)**

```bash
# 1. Faça push para o GitHub
git add .
git commit -m "Deploy dashboard"
git push origin main

# 2. Acesse https://share.streamlit.io
# 3. Conecte seu repositório
# 4. Configure o caminho: dashboard/app.py
# 5. Clique em Deploy
```

### **Opção 2: Heroku**

```bash
# Crie um Procfile na raiz do projeto
echo "web: streamlit run dashboard/app.py --server.port $PORT --server.enableCORS false" > Procfile

# Crie requirements.txt consolidado
cat requirements.txt dashboard/requirements.txt | sort -u > requirements_prod.txt

# Deploy
heroku create telco-churn-dashboard
git push heroku main
```

### **Opção 3: Docker**

```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "dashboard/app.py"]
```

```bash
# Build e execução
docker build -t churn-dashboard .
docker run -p 8501:8501 churn-dashboard
```

---

## 🔧 **Configuração Avançada**

### **🔄 Variáveis de Ambiente**

```bash
# Crie um arquivo .env na pasta dashboard/
STREAMLIT_SERVER_PORT=8501
STREAMLIT_THEME_BASE="light"
STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
DATA_PATH="../data/processed/"
MODEL_PATH="../models/"
```

### **🎨 Customização de Tema**

```python
# Em app.py, antes de streamlit.run()
import streamlit as st

st.set_page_config(
    page_title="Dashboard Churn Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar CSS customizado
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
```
---
## 🐛 **Solução de Problemas**

### **Problema 1: Erro ao carregar dados**

**Sintoma**: `FileNotFoundError` ou dados não aparecem  
**Solução**:

```bash
# Execute o pipeline completo primeiro
cd ..
python scripts/run_pipeline.py --all

# Ou execute apenas o notebook de business insights
jupyter notebook notebooks/05_business_insights.ipynb
```

### **Problema 2: Dependências faltando**

**Sintoma**: `ModuleNotFoundError`  
**Solução**:

```bash
# Reinstale todas as dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt --upgrade

# Para o dashboard especificamente
cd dashboard
pip install -r requirements.txt --force-reinstall
```
### **Problema 3: Performance lenta**

**Solução**:

```python
# Ative o cache do Streamlit
@st.cache_data
def load_data():
    return pd.read_csv('data/processed/customers_with_recommendations.csv')

# Use sampling para datasets muito grandes
if len(data) > 10000:
    sample_data = data.sample(10000, random_state=42)
```
### **Problema 4: Porta em uso**

**Solução**:

```bash
# Mude a porta
streamlit run app.py --server.port 8502

# Ou mate processos na porta 8501
lsof -ti:8501 | xargs kill -9
```

## 🔐 **Segurança e Autenticação**

### **Autenticação Básica** (opcional)

```python
# Em app.py
import streamlit_authenticator as stauth

# Configurar autenticação
authenticator = stauth.Authenticate(
    credentials,
    "churn_dashboard",
    "abcdef",
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    # Mostrar dashboard
elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
```

---
## 📈 **Monitoramento e Logs**

### **Ativar Logs Detalhados**

```bash
# Execute com verbosidade aumentada
streamlit run app.py --logger.level=debug

# Ou direcione logs para arquivo
streamlit run app.py 2>&1 | tee dashboard.log
```

### **Métricas de Uso**

```python
# Track de uso básico
import datetime

def track_usage(page_name, action):
    timestamp = datetime.datetime.now()
    log_entry = f"{timestamp},{page_name},{action}\n"
    
    with open('usage_log.csv', 'a') as f:
        f.write(log_entry)
```

## 🔗 **Integrações**

### **API do Modelo**

```python
# Exemplo de integração com API do modelo
import requests

def predict_churn_api(customer_data):
    response = requests.post(
        "http://localhost:8000/predict",
        json=customer_data
    )
    return response.json()
```

### **Webhooks para Sistemas Externos**

```python
# Enviar alertas para Slack
def send_slack_alert(high_risk_customers):
    webhook_url = "https://hooks.slack.com/services/..."
    message = {
        "text": f"⚠️ {len(high_risk_customers)} clientes de alto risco identificados"
    }
    requests.post(webhook_url, json=message)
```

---
## 📚 **Recursos Adicionais**

### **Documentação**

- [📖 Streamlit Documentation](https://docs.streamlit.io/)
- [🎨 Streamlit Components](https://streamlit.io/components)
- [🚀 Deployment Guide](https://../docs/deployment_guide.md)

### **Exemplos e Templates**

- [💼 Dashboard Templates](https://github.com/streamlit/example-apps)
- [📊 Chart Examples](https://docs.streamlit.io/library/api-reference/charts)

### **Suporte**

- [💬 Streamlit Community](https://discuss.streamlit.io/)
- [🐛 Report Issues](https://../.github/ISSUE_TEMPLATE/bug_report.md)

---

## 🎯 **Próximos Passos Planejados**

- Integração com CRM (Salesforce, HubSpot)
- Notificações em tempo real
- A/B testing de recomendações
- Dashboard mobile-responsive
- Internacionalização (multi-língua)
- Análise de sentimentos em feedback

---

> **💡 Dica**: Para desenvolvimento, use `streamlit run app.py --server.runOnSave true` para recarregamento automático.

---

*Última atualização: 05/02/2026*  
_Versão do Dashboard: 1.0.0_  
_Desenvolvido com ❤️ usando Streamlit_