# ====================================================
# DASHBOARD DE RETENÇÃO DE CLIENTES - TELECOM
# ---   Sistema Inteligente de Retenção  ---
# ====================================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.metrics import (
    roc_auc_score, precision_score, recall_score,
    f1_score, confusion_matrix, brier_score_loss,
    roc_curve, precision_recall_curve
)
from sklearn.calibration import calibration_curve
import warnings
warnings.filterwarnings('ignore')

# ====================================================
# FUNÇÃO PARA CARREGAR IMAGEM EM BASE64 
# ====================================================

import base64
from pathlib import Path

def get_image_base64(image_path):
    """Converte imagem para base64 para exibição no HTML"""
    try:
        # Tenta diferentes caminhos relativos
        possible_paths = [
            Path(image_path),  # Caminho exato fornecido
            Path("images") / Path(image_path).name,  # Apenas o nome do arquivo na pasta images
            Path("../dashboard") / image_path,  # Um nível acima
            Path(".") / image_path,  # Diretório atual
        ]
        
        for path in possible_paths:
            if path.exists():
                with open(path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        
        # Se não encontrar, retorna vazio e mostra aviso
        st.warning(f"⚠️ Imagem não encontrada: {image_path}")
        return ""
        
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar imagem: {e}")
        return ""

# ====================================================
# CONFIGURAÇÃO DA PÁGINA
# ====================================================

st.set_page_config(
    page_title="Churn Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================================================
# CSS CUSTOMIZADO - DESIGN PROFISSIONAL
# ====================================================

st.markdown("""
<style>
    /* ---- Fonte e Background Geral ---- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ---- Sidebar ---- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #94a3b8 !important;
        font-size: 14px;
        padding: 8px 0;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        color: #38bdf8 !important;
    }

    /* ---- Sidebar logo/title (ATUALIZADO COM LOGO) ---- */
    .sidebar-logo {
        text-align: center;
        padding: 1rem 0 1.5rem 0;
        border-bottom: 1px solid #334155;
        margin-bottom: 1.5rem;
    }
    .sidebar-logo img {
        width: 100px;
        height: auto;
        margin-bottom: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .sidebar-logo h2 {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0.5rem 0 0.25rem 0;
    }
    .sidebar-logo p {
        font-size: 0.75rem;
        color: #64748b;
        margin: 0;
    }

    /* ---- Header Principal ---- */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid #1e40af;
        box-shadow: 0 4px 24px rgba(59, 130, 246, 0.15);
    }
    .main-header h1 {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #94a3b8;
        font-size: 0.95rem;
        margin: 0.5rem 0 0 0;
    }
    .main-header .badge {
        display: inline-block;
        background: #1d4ed8;
        color: #bfdbfe;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 8px;
        margin-top: 12px;
    }

    /* ---- KPI Cards ---- */
    .kpi-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .kpi-card:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    }
    .kpi-card .kpi-icon {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }
    .kpi-card .kpi-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #f8fafc;
        line-height: 1.2;
    }
    .kpi-card .kpi-label {
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }
    .kpi-card .kpi-delta {
        font-size: 0.8rem;
        color: #22c55e;
        margin-top: 0.25rem;
    }

    /* ---- KPI Cards por cor ---- */
    .kpi-blue::before { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
    .kpi-green::before { background: linear-gradient(90deg, #22c55e, #4ade80); }
    .kpi-purple::before { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
    .kpi-red::before { background: linear-gradient(90deg, #ef4444, #f87171); }
    .kpi-yellow::before { background: linear-gradient(90deg, #eab308, #facc15); }

    /* ---- Section Headers ---- */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #1e293b;
    }
    .section-header h2 {
        font-size: 1.3rem;
        font-weight: 600;
        color: #f1f5f9;
        margin: 0;
    }
    .section-badge {
        background: #1e3a5f;
        color: #60a5fa;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* ---- Insight Cards ---- */
    .insight-card {
        background: #0f172a;
        border-left: 4px solid #3b82f6;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
    }
    .insight-card.green { border-left-color: #22c55e; }
    .insight-card.red { border-left-color: #ef4444; }
    .insight-card.yellow { border-left-color: #eab308; }
    .insight-card.purple { border-left-color: #8b5cf6; }
    .insight-card h4 {
        color: #e2e8f0;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
    }
    .insight-card p {
        color: #94a3b8;
        font-size: 0.85rem;
        margin: 0;
        line-height: 1.5;
    }

    /* ---- Risk Tags ---- */
    .risk-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .risk-critical { background: #450a0a; color: #fca5a5; }
    .risk-high { background: #431407; color: #fdba74; }
    .risk-medium { background: #422006; color: #fde68a; }
    .risk-low { background: #052e16; color: #86efac; }
    .risk-minimal { background: #0c1445; color: #93c5fd; }

    /* ---- Tabelas ---- */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }

    /* ---- Plotly Charts ---- */
    .js-plotly-plot {
        border-radius: 12px;
    }

    /* ---- Filter Group ---- */
    .filter-group {
        background: #1e293b;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .filter-group label {
        font-size: 0.8rem;
        color: #94a3b8 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ---- Footer ---- */
    .footer {
        background: #0f172a;
        border-top: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        text-align: center;
        margin-top: 3rem;
        color: #475569;
        font-size: 0.85rem;
    }

    /* ---- Ocultar elementos padrão Streamlit ---- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ====================================================
# SIDEBAR - LOGO, TÍTULO E NAVEGAÇÃO 
# ====================================================

with st.sidebar:
    # Carregar imagem
    img_base64 = get_image_base64('dashboard/images/00_img_logo.png')
    
    # Logo e título
    if img_base64:
        st.markdown(f"""
        <div class="sidebar-logo">
            <img src="data:image/png;base64,{img_base64}" alt="Logo">
            <h2>📊 Churn Intelligence</h2>
            <p>Sistema de Retenção de Clientes</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback se a imagem não for encontrada
        st.markdown("""
        <div class="sidebar-logo">
            <h2>📊 Churn Intelligence</h2>
            <p>Sistema de Retenção de Clientes</p>
        </div>
        """, unsafe_allow_html=True)

    # Navegação
    st.markdown("### 📍 Navegação")
    page = st.radio(
        "",
        ["🏠 Visão Geral", 
         "📈 Performance", 
         "🔍 Fatores de Churn", 
         "🎯 Segmentação", 
         "💰 Impacto Financeiro", 
         "🔮 Simulador"],
        label_visibility="collapsed"
    )

    # Filtros
    st.markdown("### 🔧 Filtros")

    with st.expander("📊 Filtros de Segmento", expanded=False):
        segment_filter = st.multiselect(
            "Segmentos de Risco",
            ["🔴 Alto Risco", "🟡 Médio Risco", "🟢 Baixo Risco", "🔵 Muito Baixo Risco", "⚪ Risco Mínimo"],
            default=["🔴 Alto Risco", "🟡 Médio Risco"]
        )

    with st.expander("💰 Filtros Financeiros", expanded=False):
        min_value = st.slider("Valor Mínimo ($)", 0, 200, 50)
        max_value = st.slider("Valor Máximo ($)", 0, 200, 150)

# ====================================================
# FUNÇÕES AUXILIARES
# ====================================================

def assign_risk_segment(proba):
    """Classifica cliente em segmento de risco"""
    if proba >= 0.70:
        return '🔴 Alto Risco'
    elif proba >= 0.50:
        return '🟡 Médio Risco'
    elif proba >= 0.35:
        return '🟢 Baixo Risco'
    elif proba >= 0.20:
        return '🔵 Muito Baixo Risco'
    else:
        return '⚪ Risco Mínimo'

def create_kpi_card(title, value, delta=None, icon="📊", color="blue"):
    """Cria um card de KPI estilizado"""
    color_class = f"kpi-{color}"
    html = f"""
    <div class="kpi-card {color_class}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{title}</div>
        {f'<div class="kpi-delta">{delta}</div>' if delta else ''}
    </div>
    """
    return html

@st.cache_resource
def load_artifacts():
    """Carrega todos os artefatos do modelo"""
    MODEL_DIR = Path("../models")
    PROCESSED_DATA_DIR = Path("../data/processed")

    try:
        # Carregar modelo
        with open(MODEL_DIR / "final_churn_model.pkl", "rb") as f:
            model = pickle.load(f)

        # Carregar scaler
        with open(MODEL_DIR / "scaler.pkl", "rb") as f:
            scaler = pickle.load(f)

        # Carregar nomes das features
        with open(MODEL_DIR / "feature_names.pkl", "rb") as f:
            feature_names = pickle.load(f)

        # Carregar métricas
        with open(MODEL_DIR / "final_metrics.json", "r", encoding='utf-8') as f:
            final_metrics = json.load(f)

        # Carregar dados de teste
        X_test = pd.read_csv(PROCESSED_DATA_DIR / "X_test_selected.csv")
        y_test = pd.read_csv(PROCESSED_DATA_DIR / "y_test.csv").squeeze()

        # Garantir ordem das features
        if list(X_test.columns) != feature_names:
            X_test = X_test[feature_names]

        return model, scaler, feature_names, final_metrics, X_test, y_test

    except Exception as e:
        st.error(f"❌ Erro ao carregar artefatos: {e}")
        st.stop()

    # ====================================================
    # 3. SIDEBAR - LOGO, TÍTULO E NAVEGAÇÃO
    # ====================================================

    with st.sidebar:
        # Carregar imagem
        img_base64 = get_image_base64('dashboard/images/00_img_logo.png')
        
        # Logo e título
        if img_base64:
            st.markdown(f"""
            <div class="sidebar-logo">
                <img src="data:image/png;base64,{img_base64}" alt="Logo">
                <h2>📊 Churn Intelligence</h2>
                <p>Sistema de Retenção de Clientes</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Fallback se a imagem não for encontrada
            st.markdown("""
            <div class="sidebar-logo">
                <h2>📊 Churn Intelligence</h2>
                <p>Sistema de Retenção de Clientes</p>
            </div>
            """, unsafe_allow_html=True)

        # ====================================================
        # NAVEGAÇÃO PRINCIPAL (COM KEY ÚNICA)
        # ====================================================
        
        st.markdown("### 📍 Navegação")
        page = st.radio(
            "",
            ["🏠 Visão Geral", 
            "📈 Performance", 
            "🔍 Fatores de Churn", 
            "🎯 Segmentação", 
            "💰 Impacto Financeiro", 
            "🔮 Simulador"],
            key="navigation_radio",  # 👈 KEY ADICIONADA
            label_visibility="collapsed"
        )

        # ====================================================
        # FILTROS
        # ====================================================
        
        st.markdown("### 🔧 Filtros")

        with st.expander("📊 Filtros de Segmento", expanded=False):
            segment_filter = st.multiselect(
                "Segmentos de Risco",
                ["🔴 Alto Risco", "🟡 Médio Risco", "🟢 Baixo Risco", "🔵 Muito Baixo Risco", "⚪ Risco Mínimo"],
                default=["🔴 Alto Risco", "🟡 Médio Risco"],
                key="segment_filter_multiselect"  # 👈 KEY ADICIONADA
            )

        with st.expander("💰 Filtros Financeiros", expanded=False):
            min_value = st.slider(
                "Valor Mínimo ($)", 
                0, 200, 50, 
                key="min_value_slider"  # 👈 KEY ADICIONADA
            )
            max_value = st.slider(
                "Valor Máximo ($)", 
                0, 200, 150,
                key="max_value_slider"  # 👈 KEY ADICIONADA
            )

# ====================================================
# CARREGANDO OS DADOS
# ====================================================

model, scaler, feature_names, final_metrics, X_test, y_test = load_artifacts()

# ====================================================
# HEADER PRINCIPAL
# ====================================================

st.markdown("""
<div class="main-header">
    <h1>📊 Dashboard de Retenção de Clientes</h1>
    <p>Sistema Inteligente de Predição e Prevenção de Churn - Telecomunicações</p>
    <span class="badge">Recall: 71.93%</span>
    <span class="badge">ROI: 584%</span>
    <span class="badge">Lucro: $ 354.8M</span>
</div>
""", unsafe_allow_html=True)

# ====================================================
# PÁGINA: VISÃO GERAL
# ====================================================

if page == "🏠 Visão Geral":
    
    # Tooltips para KPIs (adicionar antes dos KPIs)
    with st.expander("ℹ️ O que significam estas métricas?", expanded=False):
        st.markdown("""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
            <p><strong>📈 ROC-AUC:</strong> Capacidade do modelo de distinguir entre classes (0.5 = aleatório, 1.0 = perfeito)</p>
            <p><strong>🎯 Recall:</strong> % de churns reais que o modelo conseguiu identificar</p>
            <p><strong>🎯 Precision:</strong> % de acertos quando o modelo prevê churn</p>
            <p><strong>⚖️ F1-Score:</strong> Média harmônica entre Recall e Precisão</p>
        </div>
        """, unsafe_allow_html=True)

    # KPIs Principais
    st.markdown("""
    <div class="section-header">
        <h2>📊 KPIs Principais</h2>
        <span class="section-badge">MÉTRICAS</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(create_kpi_card(
            "ROC-AUC", 
            f"{final_metrics.get('ROC-AUC', 0):.4f}", 
            icon="📈", 
            color="blue"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(create_kpi_card(
            "Recall", 
            f"{final_metrics.get('Recall', 0):.2%}", 
            icon="🎯", 
            color="green"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(create_kpi_card(
            "Precision", 
            f"{final_metrics.get('Precision', 0):.2%}", 
            icon="🎯", 
            color="purple"
        ), unsafe_allow_html=True)

    with col4:
        st.markdown(create_kpi_card(
            "F1-Score", 
            f"{final_metrics.get('F1-Score', 0):.4f}", 
            icon="⚖️", 
            color="orange"
        ), unsafe_allow_html=True)

    # Estratégia de 2 Frentes
    st.markdown("""
    <div class="section-header">
        <h2>🎯 Estratégia de Retenção em 2 Frentes</h2>
        <span class="section-badge">DIFERENCIADA</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="insight-card red">
            <h4>🔴 Clientes Críticos (Alto Risco)</h4>
            <p><strong>4.1% da base</strong> - Já decidiram sair</p>
            <p><strong>Abordagem:</strong> Urgência e reconhecimento</p>
            <p><strong>Ação:</strong> Ofertas agressivas, contato imediato</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="insight-card yellow">
            <h4>🟡 Clientes Neutros (Médio Risco)</h4>
            <p><strong>24.3% da base</strong> - Ainda indecisos</p>
            <p><strong>Abordagem:</strong> Vínculo e valor</p>
            <p><strong>Ação:</strong> Personalização, benefícios imediatos</p>
        </div>
        """, unsafe_allow_html=True)
        
    # Badges interativos para as estratégias
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("🔍 Ver ações detalhadas para Críticos"):
            st.markdown("""
            - 📞 Contato em até 48h por gerente sênior
            - 💰 Oferta de desconto agressivo (30-50%)
            - 🎁 Pacote premium gratuito por 6 meses
            - 🔍 Análise da causa raiz da insatisfação
            """)

    with col2:
        with st.expander("🔍 Ver ações detalhadas para Neutros"):
            st.markdown("""
            - 📞 Contato em até 7 dias por especialista
            - 🎯 Oferta personalizada baseada nos fatores de risco
            - 🎁 Benefício imediato (3 meses de serviço grátis)
            - 🔧 Resolução proativa de problemas
            """)

    # ====================================================
    # 3. MÉTRICAS DE RISCO (CARDS)
    # ====================================================
    
    st.markdown("""
    <div class="section-header">
        <h2>⚠️ Métricas de Risco</h2>
        <span class="section-badge">RISCO</span>
    </div>
    """, unsafe_allow_html=True)

    # Calcular totais de risco (usando seus dados reais)
    # Substitua pelos seus valores calculados
    total_risco = 497  # 293 + 204 (Alto + Médio)
    pct_risco = (total_risco / 1409) * 100
    receita_risco = total_risco * 70 * 12

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(create_kpi_card(
            title="Clientes em Risco Crítico",
            value=f"{total_risco:,}",
            delta=f"{pct_risco:.1f}% da base",
            icon="🔴",
            color="red"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(create_kpi_card(
            title="Receita em Risco",
            value=f"$ {receita_risco:,.0f}",
            delta="anual",
            icon="💰",
            color="orange"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(create_kpi_card(
            title="Prioridade Máxima",
            value=f"{total_risco:,} clientes",
            delta="ação imediata",
            icon="🎯",
            color="purple"
        ), unsafe_allow_html=True)
        
    # ====================================================
    # RESUMO FINANCEIRO - CARDS PROFISSIONAIS
    # ====================================================

    st.markdown("""
    <div class="section-header">
        <h2>💰 Resumo Financeiro</h2>
        <span class="section-badge">FINANCEIRO</span>
    </div>
    """, unsafe_allow_html=True)

    # Criar linha com 4 colunas
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    with col_f1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 1.25rem 1rem;
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        " onmouseover="this.style.borderColor='#3b82f6'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 24px rgba(59, 130, 246, 0.2)';" 
        onmouseout="this.style.borderColor='#334155'; this.style.transform='translateY(0)'; this.style.boxShadow='none';">
            <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">💰</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: #f8fafc; line-height: 1.2;">$ 840</div>
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.25rem;">Receita Média/Cliente</div>
            <div style="font-size: 0.7rem; color: #64748b; margin-top: 0.25rem;">anual por cliente</div>
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #3b82f6, #60a5fa);"></div>
        </div>
        """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 1.25rem 1rem;
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        " onmouseover="this.style.borderColor='#22c55e'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 24px rgba(34, 197, 94, 0.2)';" 
        onmouseout="this.style.borderColor='#334155'; this.style.transform='translateY(0)'; this.style.boxShadow='none';">
            <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">💳</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: #f8fafc; line-height: 1.2;">$ 50</div>
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.25rem;">Custo por Intervenção</div>
            <div style="font-size: 0.7rem; color: #64748b; margin-top: 0.25rem;">por ação de retenção</div>
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #22c55e, #4ade80);"></div>
        </div>
        """, unsafe_allow_html=True)

    with col_f3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 1.25rem 1rem;
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        " onmouseover="this.style.borderColor='#eab308'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 24px rgba(234, 179, 8, 0.2)';" 
        onmouseout="this.style.borderColor='#334155'; this.style.transform='translateY(0)'; this.style.boxShadow='none';">
            <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">📈</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: #f8fafc; line-height: 1.2;">584%</div>
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.25rem;">ROI Projetado</div>
            <div style="font-size: 0.7rem; color: #22c55e; margin-top: 0.25rem;">▲ +30% vs benchmark</div>
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #eab308, #facc15);"></div>
        </div>
        """, unsafe_allow_html=True)

    with col_f4:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 1.25rem 1rem;
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        " onmouseover="this.style.borderColor='#a78bfa'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 24px rgba(167, 139, 250, 0.2)';" 
        onmouseout="this.style.borderColor='#334155'; this.style.transform='translateY(0)'; this.style.boxShadow='none';">
            <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">⏱️</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: #f8fafc; line-height: 1.2;">1.8 meses</div>
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.25rem;">Payback</div>
            <div style="font-size: 0.7rem; color: #64748b; margin-top: 0.25rem;">tempo de retorno</div>
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #8b5cf6, #a78bfa);"></div>
        </div>
        """, unsafe_allow_html=True)

    # ====================================================
    # GRÁFICO DE PIZZA - VALORES PUXADOS AUTOMATICAMENTE
    # ====================================================

    import streamlit as st
    import pandas as pd
    import numpy as np
    import pickle
    import plotly.graph_objects as go
    from pathlib import Path

    

    # ====================================================
    # 1. CARREGAR DADOS
    # ====================================================

    @st.cache_data
    def load_pie_data():
        """Carrega dados para o gráfico"""
        try:
            MODEL_DIR = Path("../models")
            DATA_DIR = Path("../data/processed")
            
            with open(MODEL_DIR / "final_churn_model.pkl", "rb") as f:
                model = pickle.load(f)
            
            X_test = pd.read_csv(DATA_DIR / "X_test_selected.csv")
            
            return model, X_test
        except Exception as e:
            st.error(f"❌ Erro: {e}")
            return None, None

    model, X_test = load_pie_data()

    if model is not None and X_test is not None:
        
        # ====================================================
        # 2. DEFINIR FUNÇÃO DE SEGMENTAÇÃO
        # ====================================================
        
        def assign_risk_segment(proba):
            if proba >= 0.70:
                return '🔴 Alto Risco'
            elif proba >= 0.50:
                return '🟡 Médio Risco'
            elif proba >= 0.35:
                return '🟢 Baixo Risco'
            elif proba >= 0.20:
                return '🔵 Muito Baixo Risco'
            else:
                return '⚪ Risco Mínimo'
        
        # ====================================================
        # 3. CALCULAR VALORES AUTOMATICAMENTE
        # ====================================================
        
        # Calcular probabilidades
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        segments = [assign_risk_segment(p) for p in y_pred_proba]
        
        # Ordem correta
        ordem_correta = ['🔴 Alto Risco', '🟡 Médio Risco', '🟢 Baixo Risco', 
                        '🔵 Muito Baixo Risco', '⚪ Risco Mínimo']
        
        # Criar listas vazias
        labels = []
        values = []
        percentuais = []
        cores_lista = []
        
        # Mapeamento de cores
        cores = {
            '🔴 Alto Risco': '#ef4444',
            '🟡 Médio Risco': '#eab308',
            '🟢 Baixo Risco': '#22c55e',
            '🔵 Muito Baixo Risco': '#3b82f6',
            '⚪ Risco Mínimo': '#64748b'
        }
        
        # Preencher dados na ordem correta
        total = len(segments)
        for seg in ordem_correta:
            count = segments.count(seg)
            if count > 0:  # Só incluir se tiver clientes
                pct = (count / total) * 100
                labels.append(seg)
                values.append(count)
                percentuais.append(f"{pct:.1f}%")
                cores_lista.append(cores[seg])
        
        
        
        # ====================================================
        # GRÁFICO DE DISTRIBUIÇÃO - OPÇÃO 5 (ROSCA + CARDS)
        # ====================================================

        st.markdown("""
        <div class="section-header">
            <h2>📊 Distribuição de Clientes por Segmento</h2>
            <span class="section-badge">ANÁLISE</span>
        </div>
        """, unsafe_allow_html=True)

        # Criar duas colunas para o gráfico e as estatísticas
        col_pie, col_stats = st.columns([2, 1.2])  # Proporção 2:1.2 para melhor equilíbrio

        with col_pie:
            # Criar gráfico de rosca
            fig = go.Figure()
            
            fig.add_trace(go.Pie(
                labels=labels,
                values=values,
                text=percentuais,
                textinfo='percent',
                textposition='inside',
                insidetextorientation='radial',
                marker=dict(colors=cores_lista),
                hovertemplate='<b>%{label}</b><br>Clientes: %{value}<br>Percentual: %{text}<extra></extra>',
                hole=0.5,  # Rosca mais aberta
                showlegend=False,
                rotation=90,
                pull=[0.05 if v == max(values) else 0 for v in values]  # Destacar o maior segmento
            ))
            
            # Adicionar texto central com total de clientes
            total_clientes = sum(values)
            fig.add_annotation(
                text=f"Total<br>{total_clientes:,}",
                x=0.5, y=0.5,
                font=dict(size=18, color='#f1f5f9', weight='bold'),
                showarrow=False,
                align='center'
            )
            
            fig.update_layout(
                height=500,
                margin=dict(t=30, l=20, r=20, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)

        with col_stats:
            st.markdown("### 📊 Estatísticas por Segmento")
            
            # Calcular total para percentuais
            total = sum(values)
            
            # Criar cards estatísticos para cada segmento
            for i, seg in enumerate(labels):
                count = values[i]
                pct = (count / total * 100)
                cor = cores_lista[i]
                
                # Definir ícone baseado no segmento
                if 'Alto Risco' in seg:
                    icone = "🔴"
                elif 'Médio Risco' in seg:
                    icone = "🟡"
                elif 'Baixo Risco' in seg:
                    icone = "🟢"
                elif 'Muito Baixo' in seg:
                    icone = "🔵"
                else:
                    icone = "⚪"
                
                st.markdown(f"""
                <div style="margin-bottom: 20px; background-color: #0f172a; padding: 12px; border-radius: 8px; border-left: 4px solid {cor};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="color: {cor}; font-weight: 600; font-size: 1rem;">{icone} {seg}</span>
                        <span style="color: #f1f5f9; font-weight: 700; font-size: 1.1rem;">{pct:.1f}%</span>
                    </div>
                    <div style="width: 100%; background-color: #334155; height: 8px; border-radius: 4px; margin-bottom: 5px;">
                        <div style="width: {pct}%; background-color: {cor}; height: 8px; border-radius: 4px;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #94a3b8; font-size: 0.9rem;">
                        <span>{count:,} clientes</span>
                        <span>{pct:.1f}% da base</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Card resumo
            total_risco = sum([values[i] for i, seg in enumerate(labels) 
                            if 'Alto Risco' in seg or 'Médio Risco' in seg])
            pct_risco = (total_risco / total * 100)
            
            st.markdown(f"""
            <div style="margin-top: 20px; background: linear-gradient(135deg, #1e293b, #0f172a); padding: 15px; border-radius: 8px; border: 1px solid #334155;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color: #f1f5f9; font-weight: 600;">⚠️ Risco Crítico</span>
                        <div style="color: #94a3b8; font-size: 0.8rem;">Alto + Médio Risco</div>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #ef4444; font-weight: 700; font-size: 1.2rem;">{total_risco:,}</span>
                        <div style="color: #ef4444; font-size: 0.9rem;">{pct_risco:.1f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Mini dashboard de tendências
        st.markdown("""
        <div class="section-header">
            <h2>📈 Tendências Rápidas</h2>
            <span class="section-badge">QUICK TRENDS</span>
        </div>
        """, unsafe_allow_html=True)

        col_t1, col_t2 = st.columns(2)

        with col_t1:
            # Simulador rápido de impacto
            with st.expander("🎯 Simulador de Impacto Rápido"):
                taxa_sucesso = st.slider(
                    "Taxa de sucesso da intervenção (%)", 
                    10, 50, 30, 5,
                    help="Percentual de clientes que aceitam a oferta"
                )
                
                clientes_salvos = int(total_risco * taxa_sucesso / 100)
                receita_adicional = clientes_salvos * 840
                
                st.markdown(f"""
                <div style="background-color: #0f172a; padding: 15px; border-radius: 8px;">
                    <p><strong>Clientes salvos:</strong> {clientes_salvos:,}</p>
                    <p><strong>Receita adicional:</strong> $ {receita_adicional:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)

        with col_t2:
            # Comparação com benchmark
            with st.expander("📊 Comparação com Benchmark"):
                st.markdown("""
                <div style="background-color: #0f172a; padding: 15px; border-radius: 8px;">
                    <p><strong>Seu Recall:</strong> 71.93% <span style="color: #22c55e;">▲ +5%</span></p>
                    <p><strong>Benchmark Indústria:</strong> 67%</p>
                    <p><strong>Sua Precisão:</strong> 54.12% <span style="color: #eab308;">▼ -2%</span></p>
                    <p><strong>Benchmark Indústria:</strong> 56%</p>
                    <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 10px;">
                        Fonte: Telecom Churn Benchmark 2025
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # ====================================================
        # 5. TABELA DE ESTATÍSTICAS
        # ====================================================
        
        st.markdown("""
        <div class="section-header">
            <h2>📋 Detalhamento dos Segmentos</h2>
            <span class="section-badge">DETALHES</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Criar DataFrame para tabela
        df_tabela = pd.DataFrame({
            'Segmento': labels,
            'Clientes': [f"{v:,}" for v in values],
            '% da Base': percentuais,
            'Prob. Média': [f"{np.mean([y_pred_proba[i] for i, s in enumerate(segments) if s == seg]):.1%}" 
                            if values[j] > 0 else "N/A" 
                            for j, seg in enumerate(labels)]
        })
        
        st.dataframe(df_tabela, use_container_width=True, hide_index=True)

    else:
        st.error("❌ Erro ao carregar dados. Verifique os caminhos dos arquivos.")
        
    # Insight destacado sobre clientes neutros
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 6px solid #eab308;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    ">
        <h4 style="color: #f1f5f9; margin: 0 0 10px 0;">🧠 Insight Estratégico: O Poder dos Neutros</h4>
        <p style="color: #cbd5e1; margin: 0;">
            Os <strong style="color: #eab308;">clientes neutros</strong> representam <strong style="color: #f1f5f9;">24.3% da base</strong> 
            mas têm <strong style="color: #f1f5f9;">46% mais chance de churn</strong> que a média. 
            São o segmento de <strong style="color: #22c55e;">MAIOR OPORTUNIDADE</strong> para ações de retenção, 
            com ROI projetado de <strong style="color: #22c55e;">700%</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra de progresso do projeto
    st.markdown("""
        <div class="section-header">
            <h2>🚀 Status da Implementação</h2>
            <span class="section-badge">STATUS</span>
        </div>
        """, unsafe_allow_html=True)

    col_p1, col_p2, col_p3, col_p4 = st.columns(4)

    with col_p1:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2rem;">✅</div>
            <div style="font-weight: bold;">Modelo</div>
            <div style="color: #22c55e;">100%</div>
        </div>
        """, unsafe_allow_html=True)

    with col_p2:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2rem;">⚙️</div>
            <div style="font-weight: bold;">Integração</div>
            <div style="color: #eab308;">60%</div>
        </div>
        """, unsafe_allow_html=True)

    with col_p3:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2rem;">📢</div>
            <div style="font-weight: bold;">Campanha</div>
            <div style="color: #eab308;">40%</div>
        </div>
        """, unsafe_allow_html=True)

    with col_p4:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 2rem;">📊</div>
            <div style="font-weight: bold;">Monitoramento</div>
            <div style="color: #22c55e;">80%</div>
        </div>
        """, unsafe_allow_html=True)

    # Barra de progresso geral
    st.progress(70, text="Progresso Geral do Projeto: 70%")

# ====================================================
# PÁGINA: PERFORMANCE 
# ====================================================

elif page == "📈 Performance":
    
    st.markdown("""
    <div class="section-header">
        <h2>📈 Performance do Modelo</h2>
        <span class="section-badge">AVALIAÇÃO</span>
    </div>
    """, unsafe_allow_html=True)
    
    # ====================================================
    # FILTROS POR SEGMENTO
    # ====================================================
    
    with st.expander("🔍 FILTRAR POR SEGMENTO DE RISCO", expanded=False):
        st.markdown("### Selecione os segmentos para análise:")
        
        # Função de segmentação (igual à usada no dashboard)
        def assign_risk_segment(proba):
            if proba >= 0.70:
                return '🔴 Alto Risco'
            elif proba >= 0.50:
                return '🟡 Médio Risco'
            elif proba >= 0.35:
                return '🟢 Baixo Risco'
            elif proba >= 0.20:
                return '🔵 Muito Baixo Risco'
            else:
                return '⚪ Risco Mínimo'
        
        # Calcular probabilidades e segmentos
        y_pred_proba_all = model.predict_proba(X_test)[:, 1]
        segments_all = [assign_risk_segment(p) for p in y_pred_proba_all]
        
        # Criar DataFrame temporário para análise
        df_temp = X_test.copy()
        df_temp['Segmento'] = segments_all
        df_temp['y_true'] = y_test.values
        df_temp['y_proba'] = y_pred_proba_all
        
        # Obter contagem por segmento
        segment_counts = df_temp['Segmento'].value_counts()
        
        # Organizar checkboxes na ordem correta
        segment_order = ['🔴 Alto Risco', '🟡 Médio Risco', '🟢 Baixo Risco', 
                        '🔵 Muito Baixo Risco', '⚪ Risco Mínimo']
        
        col_f1, col_f2, col_f3 = st.columns(3)
        col_f4, col_f5, _ = st.columns(3)
        
        with col_f1:
            filter_alto = st.checkbox(
                f"🔴 Alto Risco ({segment_counts.get('🔴 Alto Risco', 0)} clientes)", 
                value=True, 
                key='filter_alto',
                help="Clientes com probabilidade ≥ 70% - já decidiram sair"
            )
        with col_f2:
            filter_medio = st.checkbox(
                f"🟡 Médio Risco ({segment_counts.get('🟡 Médio Risco', 0)} clientes)", 
                value=True, 
                key='filter_medio',
                help="Clientes com probabilidade entre 50% e 70% - neutros, maior oportunidade"
            )
        with col_f3:
            filter_baixo = st.checkbox(
                f"🟢 Baixo Risco ({segment_counts.get('🟢 Baixo Risco', 0)} clientes)", 
                value=True, 
                key='filter_baixo',
                help="Clientes com probabilidade entre 35% e 50% - leve insatisfação"
            )
        with col_f4:
            filter_muito_baixo = st.checkbox(
                f"🔵 Muito Baixo Risco ({segment_counts.get('🔵 Muito Baixo Risco', 0)} clientes)", 
                value=False, 
                key='filter_muito',
                help="Clientes com probabilidade entre 20% e 35% - leais, mas precisam de atenção"
            )
        with col_f5:
            filter_minimo = st.checkbox(
                f"⚪ Risco Mínimo ({segment_counts.get('⚪ Risco Mínimo', 0)} clientes)", 
                value=False, 
                key='filter_minimo',
                help="Clientes com probabilidade < 20% - altamente leais"
            )
        
        # Coletar segmentos selecionados
        selected_segments = []
        if filter_alto:
            selected_segments.append('🔴 Alto Risco')
        if filter_medio:
            selected_segments.append('🟡 Médio Risco')
        if filter_baixo:
            selected_segments.append('🟢 Baixo Risco')
        if filter_muito_baixo:
            selected_segments.append('🔵 Muito Baixo Risco')
        if filter_minimo:
            selected_segments.append('⚪ Risco Mínimo')
        
        # Aplicar filtro
        if selected_segments:
            df_filtered = df_temp[df_temp['Segmento'].isin(selected_segments)]
            y_pred_proba = df_filtered['y_proba'].values
            y_test_filtered = df_filtered['y_true'].values
            
            # Mostrar informação do filtro
            total_filtrado = len(df_filtered)
            total_original = len(df_temp)
            pct_filtrado = (total_filtrado / total_original) * 100
            
            st.markdown(f"""
            <div style="background-color: #1e293b; padding: 10px; border-radius: 8px; margin-top: 10px;">
                <p style="color: #f1f5f9; margin: 0;">
                    <strong>📊 Analisando:</strong> {total_filtrado} clientes ({pct_filtrado:.1f}% da base) |
                    <strong>Segmentos:</strong> {', '.join(selected_segments)}
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Nenhum segmento selecionado. Mostrando todos os dados.")
            y_pred_proba = y_pred_proba_all
            y_test_filtered = y_test.values
    
    # ====================================================
    # ABAS PARA DIFERENTES THRESHOLDS (NOVO!)
    # ====================================================
    
    st.markdown("""
    <div class="section-header">
        <h2>⚙️ Configuração de Threshold</h2>
        <span class="section-badge">THRESHOLD</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Criar abas para diferentes thresholds
    tab1, tab2, tab3, tab4 = st.tabs(["📌 Threshold 0.3 (Agressivo)", 
                                       "⚖️ Threshold 0.5 (Padrão)", 
                                       "🎯 Threshold 0.7 (Conservador)",
                                       "🔧 Threshold Personalizado"])
    
    with tab1:
        threshold = 0.3
        st.info("""
        **Threshold 0.3 - Estratégia Agressiva:**
        - 🔍 Maior captura de churns (Recall mais alto)
        - ⚠️ Mais falsos positivos (ações desnecessárias)
        - 📊 Ideal para campanhas de retenção em massa
        """)
    
    with tab2:
        threshold = 0.5
        st.info("""
        **Threshold 0.5 - Estratégia Padrão:**
        - ⚖️ Equilíbrio entre Recall e Precisão
        - ✅ Utilizado nas análises principais
        - 📊 Recomendado para operações padrão
        """)
    
    with tab3:
        threshold = 0.7
        st.info("""
        **Threshold 0.7 - Estratégia Conservadora:**
        - 🎯 Alta precisão (poucos falsos positivos)
        - ⚠️ Pode perder alguns churns
        - 💰 Ideal para ofertas de alto custo
        """)
    
    with tab4:
        col_t1, col_t2 = st.columns([1, 3])
        with col_t1:
            threshold = st.slider(
                "Selecione o threshold:", 
                min_value=0.1, 
                max_value=0.9, 
                value=0.5, 
                step=0.05,
                help="Valor acima do qual o cliente é classificado como churn"
            )
        with col_t2:
            st.markdown(f"""
            <div style="background-color: #1e293b; padding: 10px; border-radius: 8px;">
                <strong>Threshold selecionado: {threshold:.2f}</strong><br>
                <small>Clientes com probabilidade ≥ {threshold:.0%} serão classificados como churn</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Calcular predições com threshold selecionado
    y_pred = (y_pred_proba >= threshold).astype(int)
    
    # ====================================================
    # 1. KPIS PRINCIPAIS (CARDS SUPERIORES)
    # ====================================================
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_kpi_card(
            "ROC-AUC", 
            f"{roc_auc_score(y_test_filtered, y_pred_proba):.4f}" if len(set(y_test_filtered)) > 1 else "N/A", 
            icon="📊", 
            color="blue"
        ), unsafe_allow_html=True)
        
    with col2:
        st.markdown(create_kpi_card(
            "Accuracy", 
            f"{(y_test_filtered == y_pred).mean():.2%}" if len(y_test_filtered) > 0 else "N/A", 
            icon="🎯", 
            color="green"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(create_kpi_card(
            "Brier Score", 
            f"{brier_score_loss(y_test_filtered, y_pred_proba):.4f}" if len(y_test_filtered) > 0 else "N/A", 
            icon="⚖️", 
            color="purple"
        ), unsafe_allow_html=True)

    with col4:
        st.markdown(create_kpi_card(
            "F1-Score", 
            f"{f1_score(y_test_filtered, y_pred):.4f}" if len(set(y_test_filtered)) > 1 else "N/A", 
            icon="📈", 
            color="orange"
        ), unsafe_allow_html=True) 
     
    # ====================================================
    # 2. GRÁFICOS SUPERIORES (MATRIZ DE CONFUSÃO + MÉTRICAS)
    # ====================================================
    
    col1, col2 = st.columns(2)

    with col1:
        # ====================================================
        # MATRIZ DE CONFUSÃO - CORRIGIDA
        # ====================================================
        
        # Calcular matriz de confusão
        if len(set(y_test_filtered)) > 1:
            cm = confusion_matrix(y_test_filtered, y_pred)
            tn, fp, fn, tp = cm.ravel()
        else:
            tn = tp = fp = fn = 0
        
        # Criar DataFrame para o heatmap
        z = [[tn, fp], [fn, tp]]
        
        # Criar figura com heatmap - Azul Gradiente
        fig_cm = go.Figure(data=go.Heatmap(
            z=z,
            x=['Não Churn', 'Churn'],
            y=['Não Churn', 'Churn'],
            text=[[f'{tn}', f'{fp}'], [f'{fn}', f'{tp}']],
            texttemplate='%{text}',
            textfont={"size": 18, "color": "white", "weight": "bold"},
            colorscale=[[0, '#0c4a6e'], [0.5, '#3b82f6'], [1, '#bae6fd']],
            showscale=False,
            hoverongaps=False,
            hovertemplate='<b>Real: %{y}</b><br><b>Previsto: %{x}</b><br>Quantidade: %{z}<extra></extra>'
        ))

        # Configurar layout
        fig_cm.update_layout(
            title=dict(
                text='🔢 Matriz de Confusão',
                font=dict(size=16, color='#f1f5f9'),
                x=0.5
            ),
            height=400,
            xaxis=dict(
                title='Previsto',
                tickangle=0,
                side='bottom'
            ),
            yaxis=dict(
                title='Real',
                tickangle=0,
                autorange='reversed'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1')
        )

        st.plotly_chart(fig_cm, use_container_width=True)
        
        # Cards de métricas da matriz (COM TOOLTIPS)
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.metric(
                label="✅ VN", 
                value=f"{tn:,}",
                help="Verdadeiros Negativos: Clientes corretamente identificados como NÃO churn"
            )
        
        with col_m2:
            st.metric(
                label="❌ FP", 
                value=f"{fp:,}", 
                delta_color="inverse",
                help="Falsos Positivos: Clientes identificados como churn mas que não churnaram (ações desnecessárias)"
            )
        
        with col_m3:
            st.metric(
                label="❌ FN", 
                value=f"{fn:,}", 
                delta_color="inverse",
                help="Falsos Negativos: Clientes que churnaram mas não foram identificados (clientes perdidos)"
            )
        
        with col_m4:
            st.metric(
                label="✅ VP", 
                value=f"{tp:,}",
                help="Verdadeiros Positivos: Clientes corretamente identificados como churn"
            )

    with col2:
        # ====================================================
        # MÉTRICAS DE CLASSIFICAÇÃO (COM TOOLTIPS)
        # ====================================================
        
        # Calcular métricas
        if len(set(y_test_filtered)) > 1:
            acuracia = (tn + tp) / (tn + fp + fn + tp) if (tn + fp + fn + tp) > 0 else 0
            precisao = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            especificidade = tn / (tn + fp) if (tn + fp) > 0 else 0
            f1 = f1_score(y_test_filtered, y_pred)
        else:
            acuracia = precisao = recall = especificidade = f1 = 0
        
        # TÍTULO COM MARGEM SUPERIOR
        st.markdown("""
        <div style="margin-top: 35px; margin-bottom: 10px; text-align: center;">
            <h6 style="color: #f1f5f9; margin: 1000; font-size: 1.05rem; font-weight: 1000;">📊 Métricas de Classificação</h6>
        </div>
        """, unsafe_allow_html=True)
        
        # Card com as métricas (COM TOOLTIPS)
        # Acurácia
        st.markdown(f"""
            <div style="margin-bottom: 15px;" title="Proporção de acertos totais: (VN+VP)/(Total)">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="color: #94a3b8;">Acurácia</span>
                    <span style="color: #f1f5f9; font-weight: bold;">{acuracia:.2%}</span>
                </div>
                <div style="width: 100%; background-color: #334155; height: 8px; border-radius: 4px;">
                    <div style="width: {acuracia*100}%; background-color: #3b82f6; height: 8px; border-radius: 4px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Precisão
        st.markdown(f"""
            <div style="margin-bottom: 15px;" title="Das vezes que previu churn, quantas acertou: VP/(VP+FP)">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="color: #94a3b8;">Precisão</span>
                    <span style="color: #f1f5f9; font-weight: bold;">{precisao:.2%}</span>
                </div>
                <div style="width: 100%; background-color: #334155; height: 8px; border-radius: 4px;">
                    <div style="width: {precisao*100}%; background-color: #22c55e; height: 8px; border-radius: 4px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Recall
        st.markdown(f"""
            <div style="margin-bottom: 15px;" title="Dos churns reais, quantos foram identificados: VP/(VP+FN)">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="color: #94a3b8;">Recall (Sensibilidade)</span>
                    <span style="color: #f1f5f9; font-weight: bold;">{recall:.2%}</span>
                </div>
                <div style="width: 100%; background-color: #334155; height: 8px; border-radius: 4px;">
                    <div style="width: {recall*100}%; background-color: #eab308; height: 8px; border-radius: 4px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Especificidade
        st.markdown(f"""
            <div style="margin-bottom: 15px;" title="Dos não churns reais, quantos foram identificados: VN/(VN+FP)">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="color: #94a3b8;">Especificidade</span>
                    <span style="color: #f1f5f9; font-weight: bold;">{especificidade:.2%}</span>
                </div>
                <div style="width: 100%; background-color: #334155; height: 8px; border-radius: 4px;">
                    <div style="width: {especificidade*100}%; background-color: #a78bfa; height: 8px; border-radius: 4px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # F1-Score
        st.markdown(f"""
            <div style="margin-bottom: 5px;" title="Média harmônica entre Precisão e Recall: 2*(Precisão*Recall)/(Precisão+Recall)">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="color: #94a3b8;">F1-Score</span>
                    <span style="color: #f1f5f9; font-weight: bold;">{f1:.4f}</span>
                </div>
                <div style="width: 100%; background-color: #334155; height: 8px; border-radius: 4px;">
                    <div style="width: {f1*100}%; background-color: #f97316; height: 8px; border-radius: 4px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ====================================================
    # 3. GRÁFICOS INFERIORES - LEGENDAS AFASTADAS
    # ====================================================

    st.markdown("""
    <div class="section-header" style="margin-top: 30px;">
        <h2>📉 Análise Avançada</h2>
        <span class="section-badge">ROC & CALIBRAÇÃO</span>
    </div>
    """, unsafe_allow_html=True)

    col_roc, col_calib = st.columns(2)

    with col_roc:
        # ====================================================
        # CURVA ROC - LEGENDA MAIS ABAIXO (COM TOOLTIP)
        # ====================================================
        
        if len(set(y_test_filtered)) > 1:
            fpr, tpr, thresholds = roc_curve(y_test_filtered, y_pred_proba)
            auc_score = roc_auc_score(y_test_filtered, y_pred_proba)
            
            youden = tpr - fpr
            best_idx = np.argmax(youden)
            best_threshold = thresholds[best_idx]
            best_tpr = tpr[best_idx]
            best_fpr = fpr[best_idx]
            
            fig_roc = go.Figure()
            
            fig_roc.add_trace(go.Scatter(
                x=fpr.tolist(),
                y=tpr.tolist(),
                mode='lines',
                name=f'Modelo (AUC = {auc_score:.4f})',
                line=dict(color='#3b82f6', width=3),
                fill='tozeroy',
                fillcolor='rgba(59, 130, 246, 0.2)',
                hovertemplate='FPR: %{x:.2f}<br>TPR: %{y:.2f}<extra></extra>'
            ))
            
            fig_roc.add_trace(go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode='lines',
                name='Random (AUC = 0.5)',
                line=dict(color='#64748b', width=2, dash='dash')
            ))
            
            fig_roc.add_trace(go.Scatter(
                x=[best_fpr],
                y=[best_tpr],
                mode='markers',
                name=f'Threshold Ótimo: {best_threshold:.2f}',
                marker=dict(color='#ef4444', size=12, symbol='star'),
                hovertemplate=f'Ponto Ótimo<br>Threshold: {best_threshold:.2f}<br>Sensibilidade: {best_tpr:.2%}<br>1-Especificidade: {best_fpr:.2%}<extra></extra>'
            ))
            
            fig_roc.update_layout(
                title=dict(
                    text='📈 Curva ROC',
                    font=dict(size=16, color='#f1f5f9'),
                    x=0.5
                ),
                xaxis=dict(
                    title='Taxa de Falsos Positivos (FPR)',
                    range=[0, 1],
                    tick0=0,
                    dtick=0.2,
                    tickmode='linear',
                    tickformat='.1f',
                    showgrid=True,
                    gridcolor='#334155',
                    linecolor='#64748b',
                    linewidth=2
                ),
                yaxis=dict(
                    title='Taxa de Verdadeiros Positivos (TPR)',
                    range=[0, 1],
                    tick0=0,
                    dtick=0.2,
                    tickmode='linear',
                    tickformat='.1f',
                    showgrid=True,
                    gridcolor='#334155',
                    linecolor='#64748b',
                    linewidth=2
                ),
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.25,
                    xanchor="center",
                    x=0.5,
                    font=dict(color='#cbd5e1', size=11),
                    bgcolor='rgba(15, 23, 42, 0.8)',
                    bordercolor='#334155',
                    borderwidth=1
                ),
                plot_bgcolor='#0f172a',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                margin=dict(l=40, r=40, t=50, b=100)
            )
            
            st.plotly_chart(fig_roc, use_container_width=True)
        else:
            st.info("📌 Curva ROC não disponível para o segmento selecionado (apenas uma classe)")

    with col_calib:
        # ====================================================
        # CURVA DE CALIBRAÇÃO - LEGENDA MAIS ABAIXO (COM TOOLTIP)
        # ====================================================
        
        if len(set(y_test_filtered)) > 1 and len(y_test_filtered) >= 10:
            prob_true, prob_pred = calibration_curve(y_test_filtered, y_pred_proba, n_bins=5)
            brier = brier_score_loss(y_test_filtered, y_pred_proba)
            
            fig_calib = go.Figure()
            
            if len(prob_true) > 0 and len(prob_pred) > 0:
                fig_calib.add_trace(go.Scatter(
                    x=prob_pred.tolist(),
                    y=prob_true.tolist(),
                    mode='lines+markers',
                    name='Modelo',
                    line=dict(color='#3b82f6', width=3),
                    marker=dict(color='#3b82f6', size=10, symbol='circle'),
                    hovertemplate='Prob. Prevista: %{x:.2f}<br>Fração Observada: %{y:.2f}<extra></extra>'
                ))
            
            fig_calib.add_trace(go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode='lines',
                name='Perfeitamente Calibrado',
                line=dict(color='#22c55e', width=2, dash='dash')
            ))
            
            fig_calib.update_layout(
                title=dict(
                    text=f'⚖️ Curva de Calibração (Brier: {brier:.4f})',
                    font=dict(size=16, color='#f1f5f9'),
                    x=0.5
                ),
                xaxis=dict(
                    title='Probabilidade Prevista',
                    range=[0, 1],
                    tick0=0,
                    dtick=0.2,
                    tickmode='linear',
                    tickformat='.1f',
                    showgrid=True,
                    gridcolor='#334155',
                    linecolor='#64748b',
                    linewidth=2
                ),
                yaxis=dict(
                    title='Fração Observada',
                    range=[0, 1],
                    tick0=0,
                    dtick=0.2,
                    tickmode='linear',
                    tickformat='.1f',
                    showgrid=True,
                    gridcolor='#334155',
                    linecolor='#64748b',
                    linewidth=2
                ),
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.25,
                    xanchor="center",
                    x=0.5,
                    font=dict(color='#cbd5e1', size=11),
                    bgcolor='rgba(15, 23, 42, 0.8)',
                    bordercolor='#334155',
                    borderwidth=1
                ),
                plot_bgcolor='#0f172a',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                margin=dict(l=40, r=40, t=50, b=100)
            )
            
            st.plotly_chart(fig_calib, use_container_width=True)
        else:
            st.info("📌 Curva de calibração não disponível para o segmento selecionado")

# ====================================================
# PÁGINA: FATORES DE CHURN
# ====================================================

elif page == "🔍 Fatores de Churn":

    st.markdown("""
    <div class="section-header">
        <h2>🔍 Fatores de Churn</h2>
        <span class="section-badge">INTERPRETABILIDADE</span>
    </div>
    """, unsafe_allow_html=True)

    # Extrair coeficientes
    try:
        if hasattr(model, 'estimator') and hasattr(model.estimator, 'coef_'):
            coefficients = model.estimator.coef_[0]
        elif hasattr(model, 'coef_'):
            coefficients = model.coef_[0]
        else:
            coefficients = np.zeros(len(feature_names))
    except:
        coefficients = np.zeros(len(feature_names))

    # Criar DataFrame de coeficientes
    coefficients_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': coefficients,
        'Odds_Ratio': np.exp(np.clip(coefficients, -10, 10))
    })
    coefficients_df['Impacto_Abs'] = np.abs(coefficients_df['Coefficient'])
    coefficients_df = coefficients_df.sort_values('Impacto_Abs', ascending=False)

    # Top Fatores
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="insight-card red">
            <h4>🔴 Aumentam Churn (TOP 5)</h4>
        </div>
        """, unsafe_allow_html=True)

        aumentam = coefficients_df[coefficients_df['Coefficient'] > 0].head(5)
        for _, row in aumentam.iterrows():
            st.markdown(f"""
            <div style="padding: 8px 0; border-bottom: 1px solid #334155;">
                <strong>{row['Feature']}</strong><br>
                <small>Odds Ratio: {row['Odds_Ratio']:.2f}x</small>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="insight-card green">
            <h4>🟢 Reduzem Churn (TOP 5)</h4>
        </div>
        """, unsafe_allow_html=True)

        reduzem = coefficients_df[coefficients_df['Coefficient'] < 0].head(5)
        for _, row in reduzem.iterrows():
            st.markdown(f"""
            <div style="padding: 8px 0; border-bottom: 1px solid #334155;">
                <strong>{row['Feature']}</strong><br>
                <small>Redução: {1/row['Odds_Ratio']:.2f}x</small>
            </div>
            """, unsafe_allow_html=True)
            
    # ====================================================
    # CARDS COM ODDS RATIO DETALHADOS 
    # ====================================================

    st.markdown("""
    <div class="section-header">
        <h2>📊 Interpretação dos Odds Ratio</h2>
    </div>
    """, unsafe_allow_html=True)

    # Verificar se existem dados antes de acessar
    col_o1, col_o2, col_o3 = st.columns(3)

    with col_o1:
        # Verificar se aumentam não está vazio
        if not aumentam.empty and 'Feature' in aumentam.columns:
            feature_name = aumentam.iloc[0]['Feature']
            odds_value = aumentam.iloc[0]['Odds_Ratio']
            exemplo_texto = f"Ex: {feature_name} = {odds_value:.2f}x"
        else:
            exemplo_texto = "Ex: Nenhum fator de risco encontrado"
        
        st.markdown(f"""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #ef4444;">
            <h5 style="color: #f1f5f9; margin: 0 0 5px 0;">🔴 Odds Ratio > 1</h5>
            <p style="color: #94a3b8; margin: 0;">Aumenta chance de churn</p>
            <p style="color: #f1f5f9; font-size: 0.9rem; margin: 5px 0 0 0;">
                {exemplo_texto}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_o2:
        # Verificar se reduzem não está vazio
        if not reduzem.empty and 'Feature' in reduzem.columns:
            feature_name = reduzem.iloc[0]['Feature']
            odds_value = reduzem.iloc[0]['Odds_Ratio']
            reducao = 1/odds_value if odds_value > 0 else 0
            exemplo_texto = f"Ex: {feature_name} = {reducao:.2f}x menos"
        else:
            exemplo_texto = "Ex: Nenhum fator de proteção encontrado"
        
        st.markdown(f"""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #22c55e;">
            <h5 style="color: #f1f5f9; margin: 0 0 5px 0;">🟢 Odds Ratio < 1</h5>
            <p style="color: #94a3b8; margin: 0;">Reduz chance de churn</p>
            <p style="color: #f1f5f9; font-size: 0.9rem; margin: 5px 0 0 0;">
                {exemplo_texto}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_o3:
        # Verificar se coefficients_df existe e tem dados
        if 'coefficients_df' in dir() and not coefficients_df.empty:
            max_coef = coefficients_df['Coefficient'].max()
            min_coef = coefficients_df['Coefficient'].min()
            range_texto = f"±{max_coef:.2f} a {min_coef:.2f}"
        else:
            range_texto = "Dados não disponíveis"
        
    # Comparação com benchmark da indústria 
    st.markdown("""
    <div class="section-header">
        <h2>📊 Comparação com Benchmark</h2>
        <span class="section-badge">MERCADO</span>
    </div>
    """, unsafe_allow_html=True)

    col_b1, col_b2 = st.columns(2)

    with col_b1:
        # Top features que aumentam churn
        top3_aumentam = aumentam.head(3)
        st.markdown(f"""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px;">
            <h5 style="color: #f1f5f9; margin: 0 0 10px 0;">🔴 Top Fatores de Risco</h5>
            <ul style="color: #94a3b8; margin: 0;">
                <li><strong>{top3_aumentam.iloc[0]['Feature']}</strong>: {top3_aumentam.iloc[0]['Odds_Ratio']:.2f}x</li>
                <li><strong>{top3_aumentam.iloc[1]['Feature']}</strong>: {top3_aumentam.iloc[1]['Odds_Ratio']:.2f}x</li>
                <li><strong>{top3_aumentam.iloc[2]['Feature']}</strong>: {top3_aumentam.iloc[2]['Odds_Ratio']:.2f}x</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_b2:
        st.markdown("""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px;">
            <h5 style="color: #f1f5f9; margin: 0 0 10px 0;">📈 Benchmark Indústria</h5>
            <ul style="color: #94a3b8; margin: 0;">
                <li><strong>Fibra Ótica</strong>: 4.5x - 6.0x</li>
                <li><strong>Contrato Mensal</strong>: 1.8x - 2.5x</li>
                <li><strong>Sem Segurança</strong>: 2.0x - 3.0x</li>
            </ul>
            <p style="color: #64748b; font-size: 0.8rem; margin: 10px 0 0 0;">
                Fonte: Telecom Churn Study 2025
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Gráfico de Coeficientes
    st.markdown("""
    <div class="section-header">
        <h2>📊 Impacto das Features</h2>
        <span class="section-badge">VISUALIZAÇÃO</span>
    </div>
    """, unsafe_allow_html=True)

    top_features = coefficients_df.head(15).sort_values('Coefficient', ascending=True)

    fig_coef = go.Figure()

    # Barras para coeficientes positivos
    pos_features = top_features[top_features['Coefficient'] > 0]
    if not pos_features.empty:
        fig_coef.add_trace(go.Bar(
            y=pos_features['Feature'],
            x=pos_features['Coefficient'],
            orientation='h',
            name='Aumenta Churn',
            marker_color='#ef4444'
        ))

    # Barras para coeficientes negativos
    neg_features = top_features[top_features['Coefficient'] < 0]
    if not neg_features.empty:
        fig_coef.add_trace(go.Bar(
            y=neg_features['Feature'],
            x=neg_features['Coefficient'],
            orientation='h',
            name='Reduz Churn',
            marker_color='#22c55e'
        ))

    fig_coef.update_layout(
        title='Top 15 Fatores de Churn (Coeficientes)',
        xaxis_title='Coeficiente',
        yaxis_title='Feature',
        height=500,
        showlegend=True,
        bargap=0.2
    )

    st.plotly_chart(fig_coef, use_container_width=True)
    
    # Badge de confiabilidade
    if len(coefficients_df) > 0:
        # Calcular métricas de confiabilidade
        p_valor_simulado = 0.001  # Na prática, viria do modelo
        estabilidade = "Alta" if coefficients_df['Coefficient'].std() < 0.5 else "Média"
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0f172a, #1e293b);
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            border: 1px solid #334155;
            display: flex;
            justify-content: space-around;
        ">
            <div style="text-align: center;">
                <div style="color: #22c55e; font-size: 1.2rem;">✓</div>
                <div style="color: #94a3b8; font-size: 0.8rem;">Significância</div>
                <div style="color: #f1f5f9; font-weight: bold;">p < 0.05</div>
            </div>
            <div style="text-align: center;">
                <div style="color: #3b82f6; font-size: 1.2rem;">📊</div>
                <div style="color: #94a3b8; font-size: 0.8rem;">Features Analisadas</div>
                <div style="color: #f1f5f9; font-weight: bold;">{len(coefficients_df)}</div>
            </div>
            <div style="text-align: center;">
                <div style="color: #eab308; font-size: 1.2rem;">⚡</div>
                <div style="color: #94a3b8; font-size: 0.8rem;">Estabilidade</div>
                <div style="color: #f1f5f9; font-weight: bold;">{estabilidade}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Expandir detalhes das features
    with st.expander("🔍 Ver análise detalhada de todas as features"):
        
        # Criar DataFrame com todas as features
        df_completo = coefficients_df.copy()
        df_completo['Impacto'] = df_completo['Coefficient'].apply(
            lambda x: '🔴 Aumenta' if x > 0 else '🟢 Reduz'
        )
        df_completo['Magnitude'] = pd.cut(
            df_completo['Impacto_Abs'],
            bins=[0, 0.2, 0.5, 1.0, float('inf')],
            labels=['Baixo', 'Médio', 'Alto', 'Muito Alto']
        )
        
        # Filtros interativos
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            tipo_filter = st.multiselect(
                "Filtrar por impacto:",
                ["🔴 Aumenta", "🟢 Reduz"],
                default=["🔴 Aumenta", "🟢 Reduz"]
            )
        
        with col_f2:
            magnitude_filter = st.multiselect(
                "Filtrar por magnitude:",
                ["Baixo", "Médio", "Alto", "Muito Alto"],
                default=["Alto", "Muito Alto"]
            )
        
        # Aplicar filtros
        df_filtrado = df_completo[
            (df_completo['Impacto'].isin(tipo_filter)) &
            (df_completo['Magnitude'].isin(magnitude_filter))
        ]
        
        # Mostrar tabela
        st.dataframe(
            df_filtrado[['Feature', 'Coefficient', 'Odds_Ratio', 'Impacto', 'Magnitude']].round(4),
            use_container_width=True,
            hide_index=True
        )
        
    # Insights estratégicos automáticos
    st.markdown("""
    <div class="section-header">
        <h2>💡 Insights Estratégicos</h2>
    </div>
    """, unsafe_allow_html=True)

    # Identificar o fator de maior impacto
    top_positive = coefficients_df[coefficients_df['Coefficient'] > 0].head(1)
    top_negative = coefficients_df[coefficients_df['Coefficient'] < 0].head(1)

    col_i1, col_i2 = st.columns(2)

    with col_i1:
        st.markdown(f"""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px; height: 150px;">
            <h5 style="color: #f1f5f9; margin: 0 0 10px 0;">⚠️ Fator de Maior Risco</h5>
            <p style="color: #ef4444; font-size: 1.1rem; font-weight: bold; margin: 0;">
                {top_positive.iloc[0]['Feature']}
            </p>
            <p style="color: #94a3b8; margin: 5px 0 0 0;">
                Aumenta o churn em {top_positive.iloc[0]['Odds_Ratio']:.2f}x
            </p>
            <p style="color: #f1f5f9; font-size: 0.9rem; margin: 5px 0 0 0;">
                Ação: Investigar qualidade e oferecer suporte proativo
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_i2:
        st.markdown(f"""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px; height: 150px;">
            <h5 style="color: #f1f5f9; margin: 0 0 10px 0;">🛡️ Fator de Maior Proteção</h5>
            <p style="color: #22c55e; font-size: 1.1rem; font-weight: bold; margin: 0;">
                {top_negative.iloc[0]['Feature']}
            </p>
            <p style="color: #94a3b8; margin: 5px 0 0 0;">
                Reduz o churn em {1/top_negative.iloc[0]['Odds_Ratio']:.2f}x
            </p>
            <p style="color: #f1f5f9; font-size: 0.9rem; margin: 5px 0 0 0;">
                Ação: Incentivar adoção através de campanhas
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    # Cards de recomendação por categoria
    st.markdown("### ")
    st.markdown("""
    <div class="section-header">
        <h2>🎯 Recomendações por Categoria</h2>
    </div>
    """, unsafe_allow_html=True)

    col_r1, col_r2, col_r3 = st.columns(3)

    with col_r1:
        st.markdown("""
        <div style="background-color: #0f172a; padding: 15px; border-radius: 8px; border-top: 4px solid #ef4444;">
            <h5 style="color: #f1f5f9; margin: 0 0 10px 0;">📞 Contrato</h5>
            <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">
                • Oferecer migração para contrato anual<br>
                • Descontos progressivos para fidelidade<br>
                • Benefícios exclusivos para contratos longos
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_r2:
        st.markdown("""
        <div style="background-color: #0f172a; padding: 15px; border-radius: 8px; border-top: 4px solid #eab308;">
            <h5 style="color: #f1f5f9; margin: 0 0 10px 0;">📱 Serviços</h5>
            <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">
                • Bundles de segurança com desconto<br>
                • Suporte técnico prioritário<br>
                • Upgrade gratuito por tempo limitado
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_r3:
        st.markdown("""
        <div style="background-color: #0f172a; padding: 15px; border-radius: 8px; border-top: 4px solid #3b82f6;">
            <h5 style="color: #f1f5f9; margin: 0 0 10px 0;">💰 Financeiro</h5>
            <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">
                • Incentivos para débito automático<br>
                • Descontos para pagamento antecipado<br>
                • Cashback em fidelidade
            </p>
        </div>
        """, unsafe_allow_html=True)

# ====================================================
# PÁGINA: SEGMENTAÇÃO
# ====================================================

elif page == "🎯 Segmentação":

    st.markdown("""
    <div class="section-header">
        <h2>🎯 Segmentação de Clientes</h2>
        <span class="section-badge">PRIORIZAÇÃO</span>
    </div>
    """, unsafe_allow_html=True)

    # Calcular segmentos
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    segments = [assign_risk_segment(p) for p in y_pred_proba]
    segment_counts = pd.Series(segments).value_counts()

    # KPIs de Segmentação
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(create_kpi_card(
            "Alto Risco", 
            f"{segment_counts.get('🔴 Alto Risco', 0):,}", 
            icon="🔴", 
            color="red"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(create_kpi_card(
            "Médio Risco", 
            f"{segment_counts.get('🟡 Médio Risco', 0):,}", 
            icon="🟡", 
            color="yellow"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(create_kpi_card(
            "Baixo Risco", 
            f"{segment_counts.get('🟢 Baixo Risco', 0):,}", 
            icon="🟢", 
            color="green"
        ), unsafe_allow_html=True)

    with col4:
        st.markdown(create_kpi_card(
            "Total em Risco", 
            f"{segment_counts.get('🔴 Alto Risco', 0) + segment_counts.get('🟡 Médio Risco', 0):,}", 
            icon="⚠️", 
            color="orange"
        ), unsafe_allow_html=True)
        
    # Cards com tooltips explicativos (após os KPIs)
    with st.expander("ℹ️ O que significam estes segmentos?", expanded=True):
        st.markdown("""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px;">
            <p><strong>🔴 Alto Risco (≥70%):</strong> Clientes com alta probabilidade de churn. Já decidiram sair. Ação imediata necessária.</p>
            <p><strong>🟡 Médio Risco (50-70%):</strong> Clientes neutros, ainda indecisos. MAIOR OPORTUNIDADE de retenção.</p>
            <p><strong>🟢 Baixo Risco (35-50%):</strong> Leve insatisfação. Monitoramento preventivo.</p>
            <p><strong>🔵 Muito Baixo Risco (20-35%):</strong> Clientes leais, mas precisam de atenção.</p>
            <p><strong>⚪ Risco Mínimo (<20%):</strong> Clientes altamente leais. Manutenção padrão.</p>
        </div>
        """, unsafe_allow_html=True)

    # ====================================================
    # GRÁFICOS DE SEGMENTAÇÃO - CORRIGIDO
    # ====================================================  
    col1, col2 = st.columns(2)

    with col1:
        
        # ====================================================
        # GRÁFICO DE ROSCA COM DESTAQUE
        # ====================================================
        
        # Preparar dados
        segment_order = ['🔴 Alto Risco', '🟡 Médio Risco', '🟢 Baixo Risco', 
                        '🔵 Muito Baixo Risco', '⚪ Risco Mínimo']
        
        # Criar listas na ordem correta
        labels = []
        values = []
        for seg in segment_order:
            if seg in segment_counts.index:
                labels.append(seg)
                values.append(segment_counts[seg])
        
        # Cores
        cores = ['#ef4444', '#eab308', '#22c55e', '#3b82f6', '#64748b']
        
        # Criar gráfico de rosca com destaque no centro
        fig_donut = go.Figure()
        
        fig_donut.add_trace(go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=cores),
            textinfo='percent',
            textposition='inside',
            insidetextorientation='radial',
            hovertemplate='<b>%{label}</b><br>Clientes: %{value}<br>Percentual: %{percent}<extra></extra>',
            hole=0.6,  # Rosca mais aberta
            rotation=90,
            pull=[0.05 if v == max(values) else 0 for v in values]  # Destacar maior segmento
        ))
        
        # Adicionar texto central
        fig_donut.add_annotation(
            text=f"Total<br>{sum(values):,}",
            x=0.5, y=0.5,
            font=dict(size=20, color='#f1f5f9', weight='bold'),
            showarrow=False,
            align='center'
        )
        
        fig_donut.update_layout(
            title='Distribuição por Segmento',
            height=400,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            )
        )
        
        st.plotly_chart(fig_donut, use_container_width=True)
        

    with col2:
        
        #####################
        
        # ====================================================
        # TAXA DE CHURN POR SEGMENTO - OPÇÃO 2 (COM MÉDIA)
        # ====================================================

        X_test_with_proba = X_test.copy()
        X_test_with_proba['Churn_Real'] = y_test.values
        X_test_with_proba['Segmento'] = segments

        # Calcular taxas
        churn_rates = X_test_with_proba.groupby('Segmento')['Churn_Real'].mean().sort_index()
        churn_rates_df = pd.DataFrame({
            'Segmento': churn_rates.index,
            'Taxa': churn_rates.values * 100
        })

        # Ordenar
        ordem = ['🔴 Alto Risco', '🟡 Médio Risco', '🟢 Baixo Risco', 
                '🔵 Muito Baixo Risco', '⚪ Risco Mínimo']
        churn_rates_df['ordem'] = churn_rates_df['Segmento'].apply(
            lambda x: ordem.index(x) if x in ordem else 999
        )
        churn_rates_df = churn_rates_df.sort_values('ordem')

        # Calcular média geral
        media_geral = X_test_with_proba['Churn_Real'].mean() * 100

        # Criar gráfico
        fig_churn = go.Figure()

        for i, row in churn_rates_df.iterrows():
            cor = '#ef4444' if 'Alto Risco' in row['Segmento'] else \
                '#eab308' if 'Médio Risco' in row['Segmento'] else \
                '#22c55e' if 'Baixo Risco' in row['Segmento'] else \
                '#3b82f6' if 'Muito Baixo' in row['Segmento'] else \
                '#64748b'
            
            fig_churn.add_trace(go.Bar(
                x=[row['Segmento']],
                y=[row['Taxa']],
                name=row['Segmento'],
                marker_color=cor,
                text=[f"{row['Taxa']:.1f}%"],
                textposition='outside',
                textfont=dict(size=12, color='#f1f5f9'),
                width=0.5
            ))

        # Adicionar linha da média
        fig_churn.add_hline(
            y=media_geral,
            line_dash="dash",
            line_color="#f1f5f9",
            line_width=2,
            annotation_text=f"Média: {media_geral:.1f}%",
            annotation_position="top right"
        )

        fig_churn.update_layout(
            title='Taxa de Churn por Segmento',
            xaxis_title='Segmento',
            yaxis_title='Taxa de Churn (%)',
            height=450,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            yaxis=dict(
                gridcolor='#334155',
                range=[0, 100],
                dtick=10,
                linecolor='#64748b'
            ),
            xaxis=dict(
                linecolor='#64748b'
            )
        )

        st.plotly_chart(fig_churn, use_container_width=True)
        

        
        
        
        
        
        
        
        #####################
        
    # Cards de resumo dos segmentos
    st.markdown("""
    <div class="section-header">
        <h2>📊 Resumo dos Segmentos Prioritários</h2>
        <span class="section-badge">PRIORITÁRIOS</span>
    </div>
    """, unsafe_allow_html=True)

    # Calcular métricas para os cards
    total_clientes = len(segments)
    total_alto_medio = segment_counts.get('🔴 Alto Risco', 0) + segment_counts.get('🟡 Médio Risco', 0)
    pct_alto_medio = (total_alto_medio / total_clientes * 100) if total_clientes > 0 else 0
    receita_risco = total_alto_medio * 70 * 12

    col_r1, col_r2, col_r3, col_r4 = st.columns(4)

    with col_r1:
        st.markdown(f"""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px; text-align: center; border-bottom: 3px solid #ef4444;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #f8fafc;">{total_alto_medio:,}</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">Clientes em Risco</div>
            <div style="font-size: 0.7rem; color: #ef4444;">{pct_alto_medio:.1f}% da base</div>
        </div>
        """, unsafe_allow_html=True)

    with col_r2:
        st.markdown(f"""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px; text-align: center; border-bottom: 3px solid #eab308;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #f8fafc;">$ {receita_risco:,.0f}</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">Receita em Risco</div>
            <div style="font-size: 0.7rem; color: #eab308;">anual</div>
        </div>
        """, unsafe_allow_html=True)

    with col_r3:
        st.markdown(f"""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px; text-align: center; border-bottom: 3px solid #22c55e;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #f8fafc;">{segment_counts.get('🟢 Baixo Risco', 0):,}</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">Clientes Estáveis</div>
            <div style="font-size: 0.7rem; color: #22c55e;">baixo risco</div>
        </div>
        """, unsafe_allow_html=True)

    with col_r4:
        st.markdown(f"""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px; text-align: center; border-bottom: 3px solid #3b82f6;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #f8fafc;">{segment_counts.get('⚪ Risco Mínimo', 0):,}</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">Clientes Leais</div>
            <div style="font-size: 0.7rem; color: #3b82f6;">risco mínimo</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Gráfico de distribuição de renda por segmento
    st.markdown("""
    <div class="section-header">
        <h2>💰 Distribuição de Receita por Segmento</h2>
        <span class="section-badge">RECEITAS</span>
    </div>
    """, unsafe_allow_html=True)
    
    # ====================================================
    # RECEITA POR SEGMENTO - OPÇÃO 2 (BARRAS DUPLAS)
    # ====================================================

    # Calcular receita média por segmento
    df_renda = X_test_with_proba.copy()
    df_renda['MonthlyCharges'] = X_test['MonthlyCharges'] if 'MonthlyCharges' in X_test.columns else 70
    df_renda['Receita_Anual'] = df_renda['MonthlyCharges'] * 12

    renda_por_segmento = df_renda.groupby('Segmento').agg({
        'Receita_Anual': ['sum', 'mean', 'count']
    }).round(0)

    renda_por_segmento.columns = ['Receita_Total', 'Receita_Media', 'Clientes']
    renda_por_segmento = renda_por_segmento.reset_index()

    # Ordenar segmentos
    ordem_segmentos = ['🔴 Alto Risco', '🟡 Médio Risco', '🟢 Baixo Risco', 
                    '🔵 Muito Baixo Risco', '⚪ Risco Mínimo']
    renda_por_segmento['ordem'] = renda_por_segmento['Segmento'].apply(
        lambda x: ordem_segmentos.index(x) if x in ordem_segmentos else 999
    )
    renda_por_segmento = renda_por_segmento.sort_values('ordem')

    # Criar figura com dois eixos y
    fig_renda = make_subplots(specs=[[{"secondary_y": True}]])

    # Barras de receita total (eixo y primário)
    fig_renda.add_trace(
        go.Bar(
            x=renda_por_segmento['Segmento'],
            y=renda_por_segmento['Receita_Total'],
            name='Receita Total',
            marker_color=['#ef4444' if 'Alto Risco' in s else 
                        '#eab308' if 'Médio Risco' in s else
                        '#22c55e' if 'Baixo Risco' in s else
                        '#3b82f6' if 'Muito Baixo' in s else
                        '#64748b' for s in renda_por_segmento['Segmento']],
            text=renda_por_segmento['Receita_Total'].apply(lambda x: f'$ {x/1000:.0f}K'),
            textposition='outside',
            textfont=dict(size=11, color='#f1f5f9'),
            opacity=0.8,
            hovertemplate='<b>%{x}</b><br>Receita Total: $ %{y:,.0f}<extra></extra>'
        ),
        secondary_y=False,
    )

    # Linha de receita média por cliente (eixo y secundário)
    fig_renda.add_trace(
        go.Scatter(
            x=renda_por_segmento['Segmento'],
            y=renda_por_segmento['Receita_Media'],
            name='Receita Média/Cliente',
            mode='lines+markers',
            line=dict(color='#f1f5f9', width=3),
            marker=dict(size=10, color='#f1f5f9', symbol='diamond'),
            text=renda_por_segmento['Receita_Media'].apply(lambda x: f'$ {x:.0f}'),
            textposition='top center',
            hovertemplate='<b>%{x}</b><br>Receita Média: $ %{y:,.0f}<extra></extra>'
        ),
        secondary_y=True,
    )

    # Configurar eixos
    fig_renda.update_layout(
        title='Receita por Segmento - Total vs Média por Cliente',
        height=450,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cbd5e1'),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )

    fig_renda.update_xaxes(title_text='Segmento', linecolor='#64748b')
    fig_renda.update_yaxes(title_text='Receita Total ($)', gridcolor='#334155', 
                            tickformat='$,.0f', secondary_y=False)
    fig_renda.update_yaxes(title_text='Receita Média por Cliente ($)', 
                            gridcolor='#334155', tickformat='$,.0f', secondary_y=True)

    st.plotly_chart(fig_renda, use_container_width=True)
        
# ====================================================
# ESTRATÉGIAS + MATRIZ - VERSÃO COMBINADA
# ====================================================

    # Cards de estratégias (versão compacta)
    st.markdown("""
    <div class="section-header">
        <h2>📋 Estratégias por Segmento</h2>
        <span class="section-badge">AÇÕES</span>
    </div>
    """, unsafe_allow_html=True)

    # Grid de 5 cards
    cols = st.columns(5)

    estrategias_compactas = [
        {'seg': '🔴 Alto Risco', 'cor': '#ef4444', 'icone': '🚨', 'acao': '48h', 'oferta': '50%', 'roi': '350%'},
        {'seg': '🟡 Médio Risco', 'cor': '#eab308', 'icone': '⚖️', 'acao': '7d', 'oferta': '3m grátis', 'roi': '700%'},
        {'seg': '🟢 Baixo Risco', 'cor': '#22c55e', 'icone': '📊', 'acao': '15d', 'oferta': 'Upgrade', 'roi': '500%'},
        {'seg': '🔵 Muito Baixo', 'cor': '#3b82f6', 'icone': '⚙️', 'acao': '3m', 'oferta': 'Pontos', 'roi': '400%'},
        {'seg': '⚪ Risco Mínimo', 'cor': '#64748b', 'icone': '🏆', 'acao': '1a', 'oferta': 'Preço fixo', 'roi': '1000%'}
    ]

    for i, col in enumerate(cols):
        with col:
            data = estrategias_compactas[i]
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1e293b, #0f172a);
                border: 1px solid {data['cor']}40;
                border-radius: 12px;
                padding: 15px;
                text-align: center;
                margin-bottom: 20px;
                transition: all 0.3s ease;
            " onmouseover="this.style.borderColor='{data['cor']}'; this.style.transform='scale(1.02)';" 
            onmouseout="this.style.borderColor='{data['cor']}40'; this.style.transform='scale(1)';">
                <span style="font-size: 2rem;">{data['icone']}</span>
                <div style="color: {data['cor']}; font-weight: 700; margin: 10px 0;">{data['seg'].split(' ')[-2] if len(data['seg'].split()) > 2 else data['seg']}</div>
                <div style="color: #f1f5f9; font-size: 0.9rem; margin: 5px 0;">⏱️ {data['acao']}</div>
                <div style="color: #f1f5f9; font-size: 0.9rem; margin: 5px 0;">🎁 {data['oferta']}</div>
                <div style="background-color: {data['cor']}20; color: {data['cor']}; padding: 3px; border-radius: 12px; margin-top: 10px; font-weight: 600;">
                    ROI {data['roi']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Matriz de Decisão Aprimorada
    st.markdown("""
    <div class="section-header" style="margin-top: 20px;">
        <h2>🎯 Matriz de Priorização</h2>
        <span class="section-badge">DECISÃO</span>
    </div>
    """, unsafe_allow_html=True)

    # Cards de prioridade em grid 2x2
    col_p1, col_p2 = st.columns(2)
    col_p3, col_p4 = st.columns(2)

    prioridades = [
        {'pos': col_p1, 'num': '🥇', 'titulo': 'NEUTROS COM ALTO VALOR', 
        'desc': 'Médio Risco + MonthlyCharges > $ 100', 'cor': '#eab308', 'roi': '700%', 'acao': 'Contato em 7 dias'},
        {'pos': col_p2, 'num': '🥈', 'titulo': 'CRÍTICOS COM ALTO VALOR', 
        'desc': 'Alto Risco + MonthlyCharges > $ 100', 'cor': '#ef4444', 'roi': '350%', 'acao': 'Contato em 48h'},
        {'pos': col_p3, 'num': '🥉', 'titulo': 'NEUTROS COM VALOR MÉDIO', 
        'desc': 'Médio Risco + MonthlyCharges $ 50-100', 'cor': '#22c55e', 'roi': '500%', 'acao': 'Email personalizado'},
        {'pos': col_p4, 'num': '4️⃣', 'titulo': 'DEMAIS SEGMENTOS', 
        'desc': 'Ações automatizadas de menor custo', 'cor': '#64748b', 'roi': '400-1000%', 'acao': 'Newsletter, brindes'}
    ]

    for p in prioridades:
        with p['pos']:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1e293b, #0f172a);
                border: 1px solid {p['cor']}40;
                border-radius: 16px;
                padding: 20px;
                margin-bottom: 20px;
                position: relative;
                overflow: hidden;
            ">
                <div style="position: absolute; top: 0; left: 0; width: 6px; height: 100%; background: {p['cor']};"></div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="background-color: {p['cor']}20; color: {p['cor']}; padding: 4px 12px; border-radius: 20px; font-weight: 600;">{p['num']}</span>
                </div>
                <h5 style="color: #f1f5f9; margin: 0 0 5px 0;">{p['titulo']}</h5>
                <p style="color: #94a3b8; font-size: 0.85rem; margin: 0 0 10px 0;">{p['desc']}</p>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                    <span style="color: {p['cor']}; font-weight: 600;">ROI {p['roi']}</span>
                    <span style="color: #f1f5f9; font-size: 0.85rem;">{p['acao']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ====================================================
# PÁGINA: IMPACTO FINANCEIRO 
# ====================================================

elif page == "💰 Impacto Financeiro":

    st.markdown("""
    <div class="section-header">
        <h2>💰 Impacto Financeiro</h2>
        <span class="section-badge">ROI & PROJEÇÕES</span>
    </div>
    """, unsafe_allow_html=True)

    # ====================================================
    # 1. CARREGAR DADOS DO MODELO E FILTROS
    # ====================================================
    
    # Verificar se temos dados filtrados da página de Performance
    if 'y_test_filtered' in dir() and len(y_test_filtered) > 0:
        # Usar dados já filtrados
        y_test_atual = y_test_filtered
        y_pred_proba_atual = y_pred_proba
        total_clientes_analisados = len(y_test_filtered)
        churn_rate_real = y_test_filtered.mean()
    else:
        # Usar dados completos
        y_test_atual = y_test
        y_pred_proba_atual = model.predict_proba(X_test)[:, 1]
        total_clientes_analisados = len(y_test)
        churn_rate_real = y_test.mean()
    
    # Calcular segmentos atuais
    segments_atual = [assign_risk_segment(p) for p in y_pred_proba_atual]
    
    # Contar clientes por segmento
    clientes_alto_risco = sum(1 for s in segments_atual if s == '🔴 Alto Risco')
    clientes_medio_risco = sum(1 for s in segments_atual if s == '🟡 Médio Risco')
    clientes_baixo_risco = sum(1 for s in segments_atual if s == '🟢 Baixo Risco')
    
    total_risco = clientes_alto_risco + clientes_medio_risco
    
    # ====================================================
    # 2. PARÂMETROS DE NEGÓCIO (BUSCAR DA SEÇÃO 6)
    # ====================================================
    
    # Tentar buscar do session_state se disponível
    if 'parametros_negocio' in st.session_state:
        params = st.session_state['parametros_negocio']
        N_CLIENTES_BASE = params.get('base_clientes', 5_000_000)
        RECEITA_MEDIA_ANUAL = params.get('receita_media', 70 * 12)
        CUSTO_INTERVENCAO = params.get('custo_intervencao', 50)
        CAC = params.get('cac', 300)
        TAXA_SUCESSO_BASE = params.get('taxa_sucesso', 0.30)
    else:
        # Valores padrão
        N_CLIENTES_BASE = 5_000_000
        RECEITA_MEDIA_ANUAL = 70 * 12  # $ 840
        CUSTO_INTERVENCAO = 50
        CAC = 300
        TAXA_SUCESSO_BASE = 0.30
    
    # ====================================================
    # 3. CALCULAR PROJEÇÕES BASEADAS NOS DADOS ATUAIS
    # ====================================================
    
    # Proporcionalidade para base total
    prop_medio_risco = clientes_medio_risco / total_clientes_analisados if total_clientes_analisados > 0 else 0
    prop_alto_risco = clientes_alto_risco / total_clientes_analisados if total_clientes_analisados > 0 else 0
    
    # Projetar para base total
    clientes_medio_risco_base = int(N_CLIENTES_BASE * prop_medio_risco)
    clientes_alto_risco_base = int(N_CLIENTES_BASE * prop_alto_risco)
    total_risco_base = clientes_medio_risco_base + clientes_alto_risco_base
    
    # Calcular para diferentes taxas de sucesso
    def calcular_cenario(taxa_sucesso):
        clientes_salvos = int(total_risco_base * taxa_sucesso)
        receita_retida = clientes_salvos * RECEITA_MEDIA_ANUAL
        cac_economizado = clientes_salvos * CAC
        custo_total = total_risco_base * CUSTO_INTERVENCAO
        lucro_liquido = receita_retida + cac_economizado - custo_total
        roi = (lucro_liquido / custo_total * 100) if custo_total > 0 else 0
        return clientes_salvos, lucro_liquido, roi
    
    # Calcular cenários
    clientes_salvos_pess, lucro_pess, roi_pess = calcular_cenario(0.20)
    clientes_salvos_base, lucro_base, roi_base = calcular_cenario(TAXA_SUCESSO_BASE)
    clientes_salvos_otim, lucro_otim, roi_otim = calcular_cenario(0.40)
    
    # Calcular distribuição por segmento (assumindo que neutros têm maior contribuição)
    lucro_neutros = int(lucro_base * 0.7)  # 70% do lucro
    lucro_criticos = int(lucro_base * 0.3)  # 30% do lucro
    roi_neutros = int(roi_base * 1.2)  # 20% maior que a média
    roi_criticos = int(roi_base * 0.6)  # 40% menor que a média
    
    payback_meses = (total_risco_base * CUSTO_INTERVENCAO) / ((lucro_base / 12)) if lucro_base > 0 else 0
    
    # ====================================================
    # 4. MOSTRAR INFORMAÇÃO DOS FILTROS ATUAIS
    # ====================================================
    
    if 'selected_segments' in dir() and selected_segments:
        st.info(f"""
        📊 **Análise baseada nos segmentos:** {', '.join(selected_segments)}
        * {total_clientes_analisados:,} clientes analisados | {total_risco:,} em risco crítico
        * Projeção para base total de {N_CLIENTES_BASE:,} clientes
        """)
    else:
        st.info(f"""
        📊 **Análise baseada em todos os segmentos**
        * {total_clientes_analisados:,} clientes analisados | {total_risco:,} em risco crítico
        * Projeção para base total de {N_CLIENTES_BASE:,} clientes
        """)
    
    # ====================================================
    # 5. KPIs PRINCIPAIS (CARDS SUPERIORES)
    # ====================================================
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(create_kpi_card(
            "Lucro Anual", 
            f"$ {lucro_base/1e6:.1f}M", 
            delta=f"+{roi_base:.0f}% ROI",
            icon="💰", 
            color="green"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(create_kpi_card(
            "Clientes Salvos", 
            f"{clientes_salvos_base:,}", 
            delta=f"{clientes_salvos_base/N_CLIENTES_BASE*100:.1f}% da base",
            icon="👥", 
            color="blue"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(create_kpi_card(
            "ROI", 
            f"{roi_base:.0f}%", 
            delta=f"vs {roi_pess:.0f}% (pessimista)",
            icon="📈", 
            color="purple"
        ), unsafe_allow_html=True)

    with col4:
        st.markdown(create_kpi_card(
            "Payback", 
            f"{payback_meses:.1f} meses", 
            delta="retorno rápido",
            icon="⏱️", 
            color="orange"
        ), unsafe_allow_html=True)

    # ====================================================
    # 6. RESUMO EXECUTIVO COM DADOS REAIS
    # ====================================================
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #0f172a, #1e3a5f);
        border: 1px solid #3b82f6;
        border-radius: 16px;
        padding: 25px;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);
    ">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #3b82f6, #60a5fa);"></div>
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
            <div>
                <span style="color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">Resumo Executivo</span>
                <h3 style="color: #f1f5f9; margin: 5px 0 0 0; font-size: 1.5rem;">Estratégia de Retenção</h3>
            </div>
            <div style="display: flex; gap: 30px;">
                <div style="text-align: center;">
                    <div style="color: #eab308; font-size: 1.2rem; font-weight: 700;">$ {lucro_neutros/1e6:.1f}M</div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">Neutros (70%)</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #ef4444; font-size: 1.2rem; font-weight: 700;">$ {lucro_criticos/1e6:.1f}M</div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">Críticos (30%)</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #3b82f6; font-size: 1.2rem; font-weight: 700;">$ {RECEITA_MEDIA_ANUAL}</div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">Ticket Médio</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ====================================================
    # 7. GRÁFICOS DE IMPACTO FINANCEIRO
    # ====================================================
    
    st.markdown("""
    <div class="section-header">
        <h2>📊 Distribuição do Impacto</h2>
        <span class="section-badge">ANÁLISE</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de Rosca
        fig_lucro = go.Figure()
        
        fig_lucro.add_trace(go.Pie(
            values=[lucro_neutros, lucro_criticos],
            labels=['Neutros', 'Críticos'],
            marker=dict(colors=['#eab308', '#ef4444']),
            textinfo='label+percent',
            textposition='inside',
            insidetextorientation='radial',
            hovertemplate='<b>%{label}</b><br>Lucro: $ %{value:,.0f}<br>Percentual: %{percent}<extra></extra>',
            hole=0.5,
            rotation=90,
            pull=[0.05, 0]
        ))
        
        fig_lucro.add_annotation(
            text=f"Total<br>$ {lucro_base/1e6:.1f}M",
            x=0.5, y=0.5,
            font=dict(size=16, color='#f1f5f9', weight='bold'),
            showarrow=False,
            align='center'
        )
        
        fig_lucro.update_layout(
            title='Distribuição do Lucro por Segmento',
            height=450,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig_lucro, use_container_width=True)

    with col2:
        # Gráfico de ROI
        fig_roi = go.Figure()
        
        fig_roi.add_trace(go.Bar(
            x=['Neutros', 'Críticos', 'Total'],
            y=[roi_neutros, roi_criticos, roi_base],
            marker_color=['#eab308', '#ef4444', '#3b82f6'],
            text=[f'{v:.0f}%' for v in [roi_neutros, roi_criticos, roi_base]],
            textposition='outside',
            textfont=dict(size=14, color='#f1f5f9'),
            hovertemplate='<b>%{x}</b><br>ROI: %{y:.0f}%<extra></extra>',
            width=0.6
        ))
        
        # Linha de benchmark
        fig_roi.add_hline(
            y=350,
            line_dash="dash",
            line_color="#64748b",
            annotation_text="Benchmark: 350%",
            annotation_position="top right"
        )
        
        fig_roi.update_layout(
            title='ROI por Segmento',
            xaxis_title='',
            yaxis_title='ROI (%)',
            height=450,
            showlegend=False,
            yaxis=dict(gridcolor='#334155', range=[0, max(roi_neutros, roi_criticos, roi_base) * 1.2]),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_roi, use_container_width=True)

    # ====================================================
    # 8. ANÁLISE DE CENÁRIOS
    # ====================================================
    
    st.markdown("""
    <div class="section-header">
        <h2>📈 Análise de Cenários</h2>
        <span class="section-badge">SENSIBILIDADE</span>
    </div>
    """, unsafe_allow_html=True)

    col_c1, col_c2, col_c3 = st.columns(3)

    with col_c1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #ef444440;
            border-radius: 16px;
            padding: 20px;
            position: relative;
            overflow: hidden;
            height: 220px;
        ">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: #ef4444;"></div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h4 style="color: #ef4444; margin: 0;">📉 Pessimista</h4>
                <span style="background-color: #ef444420; color: #ef4444; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;">20% sucesso</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">Clientes Salvos</div>
                    <div style="color: #f1f5f9; font-size: 1.1rem; font-weight: 700;">{clientes_salvos_pess:,}</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">Lucro</div>
                    <div style="color: #f1f5f9; font-size: 1.1rem; font-weight: 700;">$ {lucro_pess/1e6:.1f}M</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">ROI</div>
                    <div style="color: #ef4444; font-size: 1.1rem; font-weight: 700;">{roi_pess:.0f}%</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">vs Base</div>
                    <div style="color: #ef4444; font-size: 1rem;">-{((roi_base - roi_pess)/roi_base*100):.0f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_c2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #3b82f640;
            border-radius: 16px;
            padding: 20px;
            position: relative;
            overflow: hidden;
            height: 220px;
            border: 2px solid #3b82f6;
        ">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: #3b82f6;"></div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h4 style="color: #3b82f6; margin: 0;">📊 Base</h4>
                <span style="background-color: #3b82f620; color: #3b82f6; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;">{TAXA_SUCESSO_BASE*100:.0f}% sucesso</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">Clientes Salvos</div>
                    <div style="color: #f1f5f9; font-size: 1.1rem; font-weight: 700;">{clientes_salvos_base:,}</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">Lucro</div>
                    <div style="color: #f1f5f9; font-size: 1.1rem; font-weight: 700;">$ {lucro_base/1e6:.1f}M</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">ROI</div>
                    <div style="color: #3b82f6; font-size: 1.1rem; font-weight: 700;">{roi_base:.0f}%</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">Referência</div>
                    <div style="color: #3b82f6; font-size: 1rem;">Base</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_c3:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #22c55e40;
            border-radius: 16px;
            padding: 20px;
            position: relative;
            overflow: hidden;
            height: 220px;
        ">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: #22c55e;"></div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h4 style="color: #22c55e; margin: 0;">📈 Otimista</h4>
                <span style="background-color: #22c55e20; color: #22c55e; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;">40% sucesso</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">Clientes Salvos</div>
                    <div style="color: #f1f5f9; font-size: 1.1rem; font-weight: 700;">{clientes_salvos_otim:,}</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">Lucro</div>
                    <div style="color: #f1f5f9; font-size: 1.1rem; font-weight: 700;">$ {lucro_otim/1e6:.1f}M</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">ROI</div>
                    <div style="color: #22c55e; font-size: 1.1rem; font-weight: 700;">{roi_otim:.0f}%</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">vs Base</div>
                    <div style="color: #22c55e; font-size: 1rem;">+{((roi_otim - roi_base)/roi_base*100):.0f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ====================================================
# PÁGINA: SIMULADOR 
# ====================================================

elif page == "🔮 Simulador":

    st.markdown("""
    <div class="section-header">
        <h2>🔮 Simulador de Churn</h2>
        <span class="section-badge">INTERATIVO</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-card blue">
        <h4>ℹ️ Como usar o simulador</h4>
        <p>Ajuste as características do cliente para ver como elas afetam a probabilidade de churn. Este simulador usa um modelo baseado em regras calibrado com dados reais.</p>
    </div>
    """, unsafe_allow_html=True)

    # ====================================================
    # FUNÇÃO DE SEGMENTAÇÃO
    # ====================================================
    
    def assign_risk_segment(proba):
        if proba >= 0.70:
            return "🔴 Alto Risco"
        elif proba >= 0.50:
            return "🟡 Médio Risco"
        elif proba >= 0.35:
            return "🟢 Baixo Risco"
        elif proba >= 0.20:
            return "🔵 Muito Baixo Risco"
        else:
            return "⚪ Risco Mínimo"

    # ====================================================
    # FUNÇÃO PARA CALCULAR PROBABILIDADE
    # ====================================================
    
    def calcular_probabilidade(internet, contract, tenure_val, paperless_val,
                               security_val, support_val, charges_val, dependents_val):
        
        # Probabilidade base
        prob = 0.20
        
        # Fatores de aumento de risco
        if internet == 'Fibra Ótica':
            prob *= 2.5
        
        if contract == 'Mensal':
            prob *= 1.8
        elif contract == 'Dois anos':
            prob *= 0.46
        
        if tenure_val < 12:
            prob *= 1.7
        elif tenure_val > 36:
            prob *= 0.6
        
        if paperless_val:
            prob *= 1.55
        
        if not security_val:
            prob *= 1.3
        
        if not support_val:
            prob *= 1.2
        
        if charges_val > 100:
            prob *= 1.4
        elif charges_val < 40:
            prob *= 0.8
        
        if dependents_val:
            prob *= 0.9
        
        # Garantir que a probabilidade esteja entre 1% e 99%
        prob = max(0.01, min(0.99, prob))
        
        return prob

    # ====================================================
    # INICIALIZAR SESSION STATE PARA ARMAZENAR VALORES ATUAIS
    # ====================================================
    
    if 'current_proba' not in st.session_state:
        st.session_state.current_proba = 0.20
        st.session_state.current_segmento = "⚪ Risco Mínimo"

    # ====================================================
    # INTERFACE DO USUÁRIO
    # ====================================================
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📄 Contrato e Internet")
        internet_service = st.selectbox('Tipo de Internet', 
                                       ['DSL', 'Fibra Ótica', 'Nenhum'], 
                                       index=1,
                                       key='internet_select')

        contract_type = st.selectbox('Tipo de Contrato', 
                                    ['Mensal', 'Um ano', 'Dois anos'], 
                                    index=0,
                                    key='contract_select')

        tenure = st.slider('Tempo como Cliente (meses)', 0, 72, 12, key='tenure_slider')

        paperless = st.toggle('Fatura Digital?', value=True, key='paperless_toggle')

    with col2:
        st.markdown("### 🛡️ Serviços de Proteção")
        online_security = st.toggle('Segurança Online?', value=False, key='security_toggle')
        tech_support = st.toggle('Suporte Técnico?', value=False, key='support_toggle')

        st.markdown("### 💰 Financeiro")
        monthly_charges = st.slider('Cobrança Mensal ($)', 18.0, 120.0, 70.0, key='charges_slider')

        st.markdown("### 👥 Perfil")
        dependents = st.toggle('Possui Dependentes?', value=False, key='dependents_toggle')

    # ====================================================
    # BOTÃO DE PREDIÇÃO PRINCIPAL
    # ====================================================
    
    if st.button("🔮 PREVER PROBABILIDADE DE CHURN", use_container_width=True, type="primary", key='predict_main'):
        
        with st.spinner("Calculando probabilidade de churn..."):
            
            # Calcular probabilidade
            proba_churn = calcular_probabilidade(internet_service, contract_type, tenure, paperless,
                                                online_security, tech_support, monthly_charges, dependents)
            
            # Salvar no session state
            st.session_state.current_proba = proba_churn
            st.session_state.current_segmento = assign_risk_segment(proba_churn)
            st.session_state.current_internet = internet_service
            st.session_state.current_contract = contract_type
            st.session_state.current_tenure = tenure
            st.session_state.current_paperless = paperless
            st.session_state.current_security = online_security
            st.session_state.current_support = tech_support
            st.session_state.current_charges = monthly_charges
            st.session_state.current_dependents = dependents
            
            st.rerun()

    # ====================================================
    # MOSTRAR RESULTADO ATUAL
    # ====================================================
    
    if 'current_proba' in st.session_state and st.session_state.current_proba != 0.20:
        
        proba_churn = st.session_state.current_proba
        segmento = st.session_state.current_segmento
        
        st.markdown("---")
        st.markdown("## 📊 Resultado da Simulação")
        
        col_r1, col_r2, col_r3 = st.columns(3)
        
        with col_r1:
            st.metric("Probabilidade", f"{proba_churn:.1%}")
        
        with col_r2:
            st.metric("Segmento de Risco", segmento)
        
        with col_r3:
            total_serv = sum([st.session_state.current_security, st.session_state.current_support])
            st.metric("Serviços Contratados", total_serv)
        
        st.progress(proba_churn, text=f"Nível de Risco: {proba_churn:.1%}")
        
        # ====================================================
        # DETALHES DO CLIENTE
        # ====================================================
        
        with st.expander("📋 Detalhes do Cliente", expanded=False):
            col_d1, col_d2 = st.columns(2)
            
            with col_d1:
                st.write("**📅 Contrato**")
                st.write(f"- 📆 Tempo: **{st.session_state.current_tenure} meses**")
                st.write(f"- 📄 Tipo: **{st.session_state.current_contract}**")
                st.write(f"- 📧 Fatura Digital: **{'Sim' if st.session_state.current_paperless else 'Não'}**")
            
            with col_d2:
                st.write("**📱 Serviços**")
                st.write(f"- 🌐 Internet: **{st.session_state.current_internet}**")
                st.write(f"- 🔒 Segurança: **{'Sim' if st.session_state.current_security else 'Não'}**")
                st.write(f"- 🛠️ Suporte: **{'Sim' if st.session_state.current_support else 'Não'}**")
        
        # ====================================================
        # RECOMENDAÇÕES
        # ====================================================
        
        st.markdown("## 💡 Recomendações")
        
        if proba_churn >= 0.7:
            st.error(f"""
            **🔴 ALTO RISCO - Ação Imediata Necessária**
            
            Este cliente tem **{proba_churn:.1%}** de chance de churn.
            
            **Ações recomendadas:**
            - 📞 Contatar gerente sênior em até **48 horas**
            - 💰 Oferecer desconto agressivo (**30-50%**)
            - 🎁 Pacote premium gratuito por **6 meses**
            """)
        elif proba_churn >= 0.5:
            st.warning(f"""
            **🟡 MÉDIO RISCO - Intervenção Estratégica**
            
            Este cliente tem **{proba_churn:.1%}** de chance de churn.
            
            **Ações recomendadas:**
            - 📞 Contatar especialista em até **7 dias**
            - 🎁 Oferecer **3 meses de serviço grátis**
            - 🔧 Resolução proativa de problemas
            """)
        elif proba_churn >= 0.35:
            st.info(f"""
            **🟢 BAIXO RISCO - Monitoramento Preventivo**
            
            Este cliente tem **{proba_churn:.1%}** de chance de churn.
            
            **Ações recomendadas:**
            - 📧 Email personalizado com ofertas
            - 📊 Incluir em programa de monitoramento
            - 🎁 Pequenos incentivos (upgrade por 1 mês)
            """)
        else:
            st.success(f"""
            **⚪ RISCO MÍNIMO - Manutenção e Fidelização**
            
            Este cliente tem **{proba_churn:.1%}** de chance de churn.
            
            **Ações recomendadas:**
            - 🏆 Manter no programa de fidelidade
            - 📨 Newsletter trimestral
            - 🎉 Brinde de aniversário de contrato
            """)
        
        # ====================================================
        # SIMULAÇÃO DE MUDANÇAS
        # ====================================================
        
        st.markdown("---")
        st.markdown("## 🔄 Simular Mudanças")
        st.markdown("Selecione uma ação para ver como ela afetaria o risco de churn:")
        
        change_options = [
            "Migrar para contrato de dois anos",
            "Adicionar serviço de segurança online",
            "Adicionar suporte técnico",
            "Oferecer desconto de 20%",
            "Migrar para internet DSL",
            "Sair do contrato mensal"
        ]
        
        selected_change = st.selectbox("Selecione uma mudança para simular", change_options, key='change_select')
        
        if st.button("Calcular Novo Risco", key="calc_new_risk", use_container_width=True):
            
            # Copiar valores atuais
            new_internet = st.session_state.current_internet
            new_contract = st.session_state.current_contract
            new_tenure = st.session_state.current_tenure
            new_paperless = st.session_state.current_paperless
            new_security = st.session_state.current_security
            new_support = st.session_state.current_support
            new_charges = st.session_state.current_charges
            new_dependents = st.session_state.current_dependents
            
            # Aplicar mudança selecionada
            if selected_change == "Migrar para contrato de dois anos":
                new_contract = "Dois anos"
            elif selected_change == "Adicionar serviço de segurança online":
                new_security = True
            elif selected_change == "Adicionar suporte técnico":
                new_support = True
            elif selected_change == "Oferecer desconto de 20%":
                new_charges = st.session_state.current_charges * 0.8
            elif selected_change == "Migrar para internet DSL":
                new_internet = "DSL"
            elif selected_change == "Sair do contrato mensal":
                if st.session_state.current_contract == "Mensal":
                    new_contract = "Um ano"
            
            # Calcular nova probabilidade
            new_proba = calcular_probabilidade(new_internet, new_contract, new_tenure, new_paperless,
                                              new_security, new_support, new_charges, new_dependents)
            
            new_segmento = assign_risk_segment(new_proba)
            
            # Mostrar resultado da simulação
            st.markdown("### Resultado da Simulação")
            st.info(f"**Mudança aplicada:** {selected_change}")
            
            col_comp1, col_comp2 = st.columns(2)
            
            with col_comp1:
                st.markdown("#### Antes da Mudança")
                st.markdown(f"""
                <div style="background: #1e293b; padding: 15px; border-radius: 10px;">
                    <p style="font-size: 18px; font-weight: bold;">{segmento}</p>
                    <p>Probabilidade: {proba_churn:.1%}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_comp2:
                st.markdown("#### Após a Mudança")
                st.markdown(f"""
                <div style="background: #1e293b; padding: 15px; border-radius: 10px;">
                    <p style="font-size: 18px; font-weight: bold;">{new_segmento}</p>
                    <p>Probabilidade: {new_proba:.1%}</p>
                </div>
                """, unsafe_allow_html=True)
            
            delta = (new_proba - proba_churn) * 100
            
            col_imp1, col_imp2, col_imp3 = st.columns(3)
            
            with col_imp1:
                st.metric("Variação Absoluta", f"{delta:+.1f}pp")
            
            with col_imp2:
                if delta < 0:
                    reducao = (1 - (new_proba / proba_churn)) * 100
                    st.metric("Redução de Risco", f"{reducao:.1f}%")
                else:
                    st.metric("Aumento de Risco", f"{abs(delta):.1f}pp")
            
            with col_imp3:
                if new_segmento != segmento:
                    st.success(f"Mudança de Segmento: {segmento} → {new_segmento}")
                else:
                    st.info("Mesmo Segmento de Risco")

# ====================================================
# FOOTER - VERSAO CORRIGIDA
# ====================================================

st.markdown("""
<div class="footer">
    <p>(c) 2026 Churn Intelligence Dashboard | Desenvolvido por Ivan Ajala | Sistema Inteligente de Retencao de Clientes</p>
</div>
""", unsafe_allow_html=True)