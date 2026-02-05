"""
Dashboard Executivo - Sistema de Retenção de Clientes
Autor: Ivan
Data: Fevereiro 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
from datetime import datetime
import sys

# Configuração da página
st.set_page_config(
    page_title="Sistema de Retenção de Clientes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Sistema Inteligente de Retenção de Clientes - Desenvolvido por Ivan"
    }
)

# CSS Customizado
st.markdown("""
<style>
    /* Header principal */
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Cards de métricas */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
        padding: 1rem 2rem;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
    }

    /* Botões */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: 600;
    }

    /* Dataframe */
    .dataframe {
        font-size: 0.9rem;
    }

    /* Info boxes */
    .info-box {
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }

    .info-box-success {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }

    .info-box-warning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }

    .info-box-danger {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Funções auxiliares
@st.cache_data
def load_data():
    """Carregar dados processados"""
    try:
        data_dir = Path("../data/processed")

        # Carregar dataset principal
        df = pd.read_csv(data_dir / "customers_with_recommendations.csv")

        # Carregar resumo por segmento
        segment_summary = pd.read_csv(data_dir / "segment_summary.csv", index_col=0)

        # Carregar playbook
        with open(data_dir / "retention_playbook.json", 'r', encoding='utf-8') as f:
            playbook = json.load(f)

        # Carregar métricas de negócio
        with open(data_dir / "business_metrics.json", 'r', encoding='utf-8') as f:
            metrics = json.load(f)

        return df, segment_summary, playbook, metrics

    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        st.info("💡 Certifique-se de que o Notebook 05 foi executado completamente.")
        return None, None, None, None

def format_currency(value):
    """Formatar valor em reais"""
    return f"R$ {value:,.2f}"

def format_percentage(value):
    """Formatar percentual"""
    return f"{value:.1f}%"

# Carregar dados
df, segment_summary, playbook, metrics = load_data()

if df is None:
    st.stop()

# Header
st.markdown('<h1 class="main-header">📊 Sistema Inteligente de Retenção de Clientes</h1>', 
            unsafe_allow_html=True)

st.markdown("**Dashboard Executivo para Análise de Churn e Tomada de Decisão**")
st.markdown("---")

# Sidebar - Informações e Filtros
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103655.png", width=100)

    st.markdown("## ℹ️ Informações do Sistema")

    if metrics:
        st.metric("Data de Geração", 
                  datetime.strptime(metrics['data_geracao'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y'))
        st.metric("Total de Clientes", f"{metrics['total_clientes']:,}")
        st.metric("Taxa Média de Churn", f"{metrics['taxa_churn_media']*100:.1f}%")

    st.markdown("---")
    st.markdown("## ⚙️ Filtros")

    # Filtro por nível de risco
    risk_levels = ['Todos'] + sorted(df['Risk_Level'].unique().tolist())
    selected_risk = st.multiselect(
        "📊 Nível de Risco",
        options=risk_levels,
        default=['Todos']
    )

    # Filtro por probabilidade
    prob_range = st.slider(
        "🎯 Probabilidade de Churn (%)",
        min_value=0,
        max_value=100,
        value=(0, 100),
        step=5
    )

    # Filtro por CLV
    clv_min = float(df['CLV'].min())
    clv_max = float(df['CLV'].max())
    clv_range = st.slider(
        "💰 CLV (R$)",
        min_value=clv_min,
        max_value=clv_max,
        value=(clv_min, clv_max),
        step=100.0,
        format="R$ %.0f"
    )

    st.markdown("---")
    st.markdown("### 📥 Downloads")

    # Botão de download do dataset completo
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Dataset Completo (CSV)",
        data=csv,
        file_name=f"clientes_segmentados_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Aplicar filtros
df_filtered = df.copy()

if 'Todos' not in selected_risk:
    df_filtered = df_filtered[df_filtered['Risk_Level'].isin(selected_risk)]

df_filtered = df_filtered[
    (df_filtered['Churn_Probability'] * 100 >= prob_range[0]) &
    (df_filtered['Churn_Probability'] * 100 <= prob_range[1]) &
    (df_filtered['CLV'] >= clv_range[0]) &
    (df_filtered['CLV'] <= clv_range[1])
]

# KPIs Principais
st.markdown("### 📊 KPIs Principais")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="👥 Total de Clientes",
        value=f"{len(df_filtered):,}",
        delta=f"{len(df_filtered)/len(df)*100:.1f}% da base"
    )

with col2:
    churn_rate = df_filtered['Churn_Probability'].mean() * 100
    st.metric(
        label="📉 Taxa Média de Churn",
        value=f"{churn_rate:.1f}%",
        delta=f"{churn_rate - df['Churn_Probability'].mean()*100:+.1f}%"
    )

with col3:
    revenue_at_risk = df_filtered['Revenue_at_Risk'].sum()
    st.metric(
        label="💸 Receita em Risco",
        value=format_currency(revenue_at_risk),
        delta=f"{revenue_at_risk/df['Revenue_at_Risk'].sum()*100:.1f}% do total"
    )

with col4:
    revenue_recovered = df_filtered['Revenue_Recovered'].sum()
    st.metric(
        label="💰 Receita Recuperável",
        value=format_currency(revenue_recovered),
        delta=f"{revenue_recovered/revenue_at_risk*100:.1f}% do risco"
    )

with col5:
    avg_roi = df_filtered['Expected_ROI'].mean()
    st.metric(
        label="📈 ROI Médio",
        value=f"{avg_roi:.0f}%",
        delta="Estimativa"
    )

st.markdown("---")

# Tabs principais
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Visão Geral", 
    "🎯 Segmentação", 
    "💡 Recomendações", 
    "💰 Análise Financeira",
    "👥 Clientes Prioritários"
])

# ============================================
# TAB 1: VISÃO GERAL
# ============================================

with tab1:
    st.markdown("### 📊 Visão Geral da Base de Clientes")

    col1, col2 = st.columns(2)

    with col1:
        # Distribuição por nível de risco
        st.markdown("#### Distribuição por Nível de Risco")

        risk_counts = df_filtered['Risk_Level'].value_counts()
        colors_map = {
            'CRÍTICO': '#e74c3c',
            'ALTO': '#f39c12',
            'MÉDIO': '#3498db',
            'BAIXO': '#2ecc71'
        }
        colors = [colors_map.get(level, '#95a5a6') for level in risk_counts.index]

        fig_risk = go.Figure(data=[go.Pie(
            labels=risk_counts.index,
            values=risk_counts.values,
            marker=dict(colors=colors),
            hole=0.4,
            textinfo='label+percent',
            textfont_size=12
        )])

        fig_risk.update_layout(
            showlegend=True,
            height=400,
            margin=dict(t=30, b=30, l=30, r=30)
        )

        st.plotly_chart(fig_risk, use_container_width=True)

    with col2:
        # Distribuição de probabilidade
        st.markdown("#### Distribuição de Probabilidade de Churn")

        fig_hist = px.histogram(
            df_filtered,
            x='Churn_Probability',
            nbins=30,
            color='Risk_Level',
            color_discrete_map=colors_map,
            labels={'Churn_Probability': 'Probabilidade de Churn'},
            opacity=0.7
        )

        fig_hist.update_layout(
            showlegend=True,
            height=400,
            xaxis_title="Probabilidade de Churn",
            yaxis_title="Quantidade de Clientes",
            margin=dict(t=30, b=30, l=30, r=30)
        )

        st.plotly_chart(fig_hist, use_container_width=True)

    # Métricas por segmento
    st.markdown("#### 📋 Métricas por Segmento de Risco")

    segment_metrics = df_filtered.groupby('Risk_Level').agg({
        'customerID': 'count',
        'Churn_Probability': 'mean',
        'CLV': 'mean',
        'Revenue_at_Risk': 'sum',
        'Revenue_Recovered': 'sum',
        'Expected_ROI': 'mean'
    }).round(2)

    segment_metrics.columns = [
        'Total Clientes', 
        'Prob. Churn Média', 
        'CLV Médio',
        'Receita em Risco',
        'Receita Recuperável',
        'ROI Médio (%)'
    ]

    # Formatar valores
    segment_metrics_display = segment_metrics.copy()
    segment_metrics_display['Prob. Churn Média'] = segment_metrics_display['Prob. Churn Média'].apply(lambda x: f"{x*100:.1f}%")
    segment_metrics_display['CLV Médio'] = segment_metrics_display['CLV Médio'].apply(format_currency)
    segment_metrics_display['Receita em Risco'] = segment_metrics_display['Receita em Risco'].apply(format_currency)
    segment_metrics_display['Receita Recuperável'] = segment_metrics_display['Receita Recuperável'].apply(format_currency)

    st.dataframe(segment_metrics_display, use_container_width=True)

# ============================================
# TAB 2: SEGMENTAÇÃO
# ============================================

with tab2:
    st.markdown("### 🎯 Análise de Segmentação")

    col1, col2 = st.columns(2)

    with col1:
        # Receita em risco por segmento
        st.markdown("#### 💸 Receita em Risco por Segmento")

        revenue_by_risk = df_filtered.groupby('Risk_Level')['Revenue_at_Risk'].sum().sort_values()

        fig_revenue = go.Figure(data=[go.Bar(
            x=revenue_by_risk.values,
            y=revenue_by_risk.index,
            orientation='h',
            marker=dict(color=[colors_map.get(level, '#95a5a6') for level in revenue_by_risk.index]),
            text=[format_currency(v) for v in revenue_by_risk.values],
            textposition='outside'
        )])

        fig_revenue.update_layout(
            height=400,
            xaxis_title="Receita em Risco (R$)",
            yaxis_title="",
            showlegend=False,
            margin=dict(t=30, b=30, l=30, r=30)
        )

        st.plotly_chart(fig_revenue, use_container_width=True)

    with col2:
        # CLV médio por segmento
        st.markdown("#### 💰 CLV Médio por Segmento")

        clv_by_risk = df_filtered.groupby('Risk_Level')['CLV'].mean().sort_values()

        fig_clv = go.Figure(data=[go.Bar(
            x=clv_by_risk.values,
            y=clv_by_risk.index,
            orientation='h',
            marker=dict(color=[colors_map.get(level, '#95a5a6') for level in clv_by_risk.index]),
            text=[format_currency(v) for v in clv_by_risk.values],
            textposition='outside'
        )])

        fig_clv.update_layout(
            height=400,
            xaxis_title="CLV Médio (R$)",
            yaxis_title="",
            showlegend=False,
            margin=dict(t=30, b=30, l=30, r=30)
        )

        st.plotly_chart(fig_clv, use_container_width=True)

    # Scatter: Probabilidade vs CLV
    st.markdown("#### 📊 Relação entre Probabilidade de Churn e CLV")

    # Amostra para performance
    sample_size = min(1000, len(df_filtered))
    df_sample = df_filtered.sample(sample_size) if len(df_filtered) > sample_size else df_filtered

    fig_scatter = px.scatter(
        df_sample,
        x='Churn_Probability',
        y='CLV',
        color='Risk_Level',
        color_discrete_map=colors_map,
        size='Revenue_at_Risk',
        hover_data=['customerID', 'Recommended_Action'],
        labels={
            'Churn_Probability': 'Probabilidade de Churn',
            'CLV': 'Customer Lifetime Value (R$)',
            'Risk_Level': 'Nível de Risco'
        },
        opacity=0.6
    )

    fig_scatter.update_layout(
        height=500,
        margin=dict(t=30, b=30, l=30, r=30)
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

# ============================================
# TAB 3: RECOMENDAÇÕES
# ============================================

with tab3:
    st.markdown("### 💡 Sistema de Recomendações")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### 📋 Distribuição de Ações Recomendadas")

        action_counts = df_filtered['Recommended_Action'].value_counts()

        fig_actions = go.Figure(data=[go.Bar(
            x=action_counts.index,
            y=action_counts.values,
            marker=dict(color='steelblue'),
            text=action_counts.values,
            textposition='outside'
        )])

        fig_actions.update_layout(
            height=400,
            xaxis_title="",
            yaxis_title="Quantidade de Clientes",
            showlegend=False,
            xaxis_tickangle=-45,
            margin=dict(t=30, b=100, l=30, r=30)
        )

        st.plotly_chart(fig_actions, use_container_width=True)

    with col2:
        st.markdown("#### 🎯 Playbook de Ações")

        selected_risk_level = st.selectbox(
            "Selecione o nível de risco:",
            options=sorted(df_filtered['Risk_Level'].unique())
        )

        if selected_risk_level in playbook:
            info = playbook[selected_risk_level]

            st.markdown(f"**{info['name']}**")
            st.markdown(f"**Prioridade:** {info['priority']}")
            st.markdown(f"**ROI Estimado:** {info['estimated_roi']}")
            st.markdown(f"**Custo Médio:** R$ {info['estimated_cost']}")
            st.markdown(f"**Taxa de Conversão:** {info['conversion_rate']*100:.0f}%")

            st.markdown("**Ações:**")
            for action in info['actions']:
                st.markdown(f"- {action}")

    # Tabela de clientes por ação
    st.markdown("#### 👥 Clientes por Ação Recomendada")

    selected_action = st.selectbox(
        "Selecione uma ação:",
        options=sorted(df_filtered['Recommended_Action'].unique())
    )

    clients_by_action = df_filtered[df_filtered['Recommended_Action'] == selected_action].nlargest(20, 'Revenue_at_Risk')[
        ['customerID', 'Churn_Probability', 'CLV', 'Revenue_at_Risk', 'Risk_Level']
    ].copy()

    clients_by_action['Churn_Probability'] = clients_by_action['Churn_Probability'].apply(lambda x: f"{x*100:.1f}%")
    clients_by_action['CLV'] = clients_by_action['CLV'].apply(format_currency)
    clients_by_action['Revenue_at_Risk'] = clients_by_action['Revenue_at_Risk'].apply(format_currency)

    st.dataframe(clients_by_action, use_container_width=True, height=400)

# ============================================
# TAB 4: ANÁLISE FINANCEIRA
# ============================================

with tab4:
    st.markdown("### 💰 Análise de Impacto Financeiro")

    # Resumo financeiro
    col1, col2, col3 = st.columns(3)

    total_revenue_at_risk = df_filtered['Revenue_at_Risk'].sum()
    total_action_cost = df_filtered['Action_Cost'].sum()
    total_revenue_recovered = df_filtered['Revenue_Recovered'].sum()
    net_profit = df_filtered['Net_Profit'].sum()
    overall_roi = (net_profit / total_action_cost * 100) if total_action_cost > 0 else 0

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Receita em Risco</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_currency(total_revenue_at_risk)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Receita Recuperável</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_currency(total_revenue_recovered)}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">{total_revenue_recovered/total_revenue_at_risk*100:.1f}% do risco</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Lucro Líquido Estimado</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_currency(net_profit)}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">ROI: {overall_roi:.0f}%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Gráfico de cascata
    st.markdown("#### 📊 Análise de Cascata Financeira")

    fig_waterfall = go.Figure(go.Waterfall(
        name="Impacto Financeiro",
        orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=["Receita em Risco", "Custo de Ações", "Receita Recuperada", "Lucro Líquido"],
        y=[total_revenue_at_risk, -total_action_cost, total_revenue_recovered, net_profit],
        text=[
            format_currency(total_revenue_at_risk),
            format_currency(total_action_cost),
            format_currency(total_revenue_recovered),
            format_currency(net_profit)
        ],
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "#e74c3c"}},
        increasing={"marker": {"color": "#2ecc71"}},
        totals={"marker": {"color": "#3498db"}}
    ))

    fig_waterfall.update_layout(
        height=500,
        showlegend=False,
        margin=dict(t=30, b=30, l=30, r=30)
    )

    st.plotly_chart(fig_waterfall, use_container_width=True)

    # ROI por segmento
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 ROI por Segmento")

        roi_by_segment = df_filtered.groupby('Risk_Level').agg({
            'Action_Cost': 'sum',
            'Net_Profit': 'sum'
        })
        roi_by_segment['ROI'] = (roi_by_segment['Net_Profit'] / roi_by_segment['Action_Cost'] * 100).fillna(0)
        roi_by_segment = roi_by_segment.sort_values('ROI')

        fig_roi = go.Figure(data=[go.Bar(
            x=roi_by_segment['ROI'],
            y=roi_by_segment.index,
            orientation='h',
            marker=dict(color=[colors_map.get(level, '#95a5a6') for level in roi_by_segment.index]),
            text=[f"{v:.0f}%" for v in roi_by_segment['ROI']],
            textposition='outside'
        )])

        fig_roi.update_layout(
            height=400,
            xaxis_title="ROI (%)",
            yaxis_title="",
            showlegend=False,
            margin=dict(t=30, b=30, l=30, r=30)
        )

        st.plotly_chart(fig_roi, use_container_width=True)

    with col2:
        st.markdown("#### 💵 Custo vs Retorno por Segmento")

        financial_by_segment = df_filtered.groupby('Risk_Level').agg({
            'Action_Cost': 'sum',
            'Revenue_Recovered': 'sum'
        }).sort_values('Revenue_Recovered')

        fig_cost_return = go.Figure()

        fig_cost_return.add_trace(go.Bar(
            name='Custo',
            x=financial_by_segment.index,
            y=financial_by_segment['Action_Cost'],
            marker_color='#e74c3c'
        ))

        fig_cost_return.add_trace(go.Bar(
            name='Retorno',
            x=financial_by_segment.index,
            y=financial_by_segment['Revenue_Recovered'],
            marker_color='#2ecc71'
        ))

        fig_cost_return.update_layout(
            barmode='group',
            height=400,
            xaxis_title="",
            yaxis_title="Valor (R$)",
            margin=dict(t=30, b=30, l=30, r=30)
        )

        st.plotly_chart(fig_cost_return, use_container_width=True)

# ============================================
# TAB 5: CLIENTES PRIORITÁRIOS
# ============================================

with tab5:
    st.markdown("### 👥 Clientes Prioritários para Ação Imediata")

    # Filtros adicionais
    col1, col2, col3 = st.columns(3)

    with col1:
        top_n = st.number_input(
            "Quantidade de clientes:",
            min_value=10,
            max_value=500,
            value=50,
            step=10
        )

    with col2:
        sort_by = st.selectbox(
            "Ordenar por:",
            options=['Priority_Score_Normalized', 'Revenue_at_Risk', 'Churn_Probability', 'CLV', 'Expected_ROI'],
            format_func=lambda x: {
                'Priority_Score_Normalized': 'Score de Priorização',
                'Revenue_at_Risk': 'Receita em Risco',
                'Churn_Probability': 'Probabilidade de Churn',
                'CLV': 'CLV',
                'Expected_ROI': 'ROI Esperado'
            }[x]
        )

    with col3:
        filter_critical = st.checkbox("Apenas clientes CRÍTICOS", value=False)

    # Aplicar filtros
    priority_df = df_filtered.copy()

    if filter_critical:
        priority_df = priority_df[priority_df['Risk_Level'] == 'CRÍTICO']

    priority_df = priority_df.nlargest(top_n, sort_by)

    # Tabela de clientes prioritários
    st.markdown(f"#### 📋 Top {top_n} Clientes Prioritários")

    display_df = priority_df[[
        'customerID', 'Churn_Probability', 'Risk_Level', 
        'CLV', 'Revenue_at_Risk', 'Recommended_Action', 'Expected_ROI', 'Priority_Score_Normalized'
    ]].copy()

    display_df.columns = [
        'ID Cliente', 'Prob. Churn', 'Nível Risco',
        'CLV', 'Receita em Risco', 'Ação Recomendada', 'ROI Esperado (%)', 'Score Prioridade'
    ]

    display_df['Prob. Churn'] = display_df['Prob. Churn'].apply(lambda x: f"{x*100:.1f}%")
    display_df['CLV'] = display_df['CLV'].apply(format_currency)
    display_df['Receita em Risco'] = display_df['Receita em Risco'].apply(format_currency)
    display_df['Score Prioridade'] = display_df['Score Prioridade'].apply(lambda x: f"{x:.1f}")

    # Aplicar cores por nível de risco
    def highlight_risk(row):
        color_map = {
            'CRÍTICO': 'background-color: #ffcccc',
            'ALTO': 'background-color: #ffe6cc',
            'MÉDIO': 'background-color: #cce6ff',
            'BAIXO': 'background-color: #ccffcc'
        }
        return [color_map.get(row['Nível Risco'], '')] * len(row)

    styled_df = display_df.style.apply(highlight_risk, axis=1)

    st.dataframe(styled_df, use_container_width=True, height=600)

    # Botão de download
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"clientes_prioritarios_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

    # Resumo dos clientes prioritários
    st.markdown("#### 📊 Resumo dos Clientes Prioritários")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total de Clientes",
            f"{len(priority_df):,}"
        )

    with col2:
        st.metric(
            "Receita em Risco",
            format_currency(priority_df['Revenue_at_Risk'].sum())
        )

    with col3:
        st.metric(
            "Receita Recuperável",
            format_currency(priority_df['Revenue_Recovered'].sum())
        )

    with col4:
        st.metric(
            "ROI Médio",
            f"{priority_df['Expected_ROI'].mean():.0f}%"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>Sistema de Retenção de Clientes</strong> | Desenvolvido por Ivan | 2026</p>
    <p>Modelo: Random Forest Calibrado | ROC-AUC: 0.8431 | Calibração: 3.14%</p>
</div>
""", unsafe_allow_html=True)