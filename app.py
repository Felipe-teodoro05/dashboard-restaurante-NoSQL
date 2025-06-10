import streamlit as st
from pymongo import MongoClient
import pandas as pd
from bson import ObjectId
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import numpy as np

# Configurações da página Streamlit
st.set_page_config(
    layout="wide",
    page_title="Dashboard de Restaurantes",
    page_icon="",
    initial_sidebar_state="expanded"
)

# Paleta de cores profissional focada em restaurantes (inspirada no iFood e tendências gastronômicas)
RESTAURANT_COLORS = {
    'primary': '#EA1D2C',      # Vermelho iFood - estimula apetite
    'secondary': '#FF6B47',    # Laranja vibrante - energia e calor
    'accent': '#FFD700',       # Dourado - qualidade premium
    'success': '#32CD32',      # Verde fresco - saudável
    'warning': '#FF8C42',      # Laranja suave - atenção
    'info': '#4ECDC4',         # Turquesa - modernidade
    'dark': '#2C3E50',         # Azul escuro - profissionalismo
    'light': '#F8F9FA',        # Cinza claro - limpeza
    'background': '#FFFFFF',   # Branco - pureza
    'card_bg': '#FFF8F0',      # Bege suave - aconchego
    'gradient_start': '#FF6B47',
    'gradient_end': '#FFD700'
}

# CSS customizado com paleta profissional de restaurantes
st.markdown(f"""
<style>
    .main > div {{
        padding-top: 1rem;
    }}
    
    /* Cards de métricas personalizados */
    .metric-card {{
        background: linear-gradient(135deg, {RESTAURANT_COLORS['gradient_start']} 0%, {RESTAURANT_COLORS['gradient_end']} 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
    }}
    
    .metric-card h3 {{
        margin: 0;
        font-size: 2.2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    .metric-card p {{
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 500;
    }}
    
    /* Estilização da sidebar */
    .css-1d391kg {{
        background: linear-gradient(180deg, {RESTAURANT_COLORS['card_bg']} 0%, {RESTAURANT_COLORS['light']} 100%);
    }}
    
    /* Títulos principais */
    h1 {{
        color: {RESTAURANT_COLORS['dark']};
        text-align: center;
        font-size: 3rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(45deg, {RESTAURANT_COLORS['primary']}, {RESTAURANT_COLORS['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    h2 {{
        color: {RESTAURANT_COLORS['primary']};
        border-bottom: 3px solid {RESTAURANT_COLORS['primary']};
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-weight: 600;
    }}
    
    h3 {{
        color: {RESTAURANT_COLORS['secondary']};
        margin-top: 1.5rem;
        font-weight: 500;
    }}
    
    /* Estilização dos selectboxes */
    .stSelectbox > div > div {{
        background-color: {RESTAURANT_COLORS['card_bg']};
        border-radius: 10px;
        border: 2px solid {RESTAURANT_COLORS['accent']};
    }}
    
    .stMultiSelect > div > div {{
        background-color: {RESTAURANT_COLORS['card_bg']};
        border-radius: 10px;
        border: 2px solid {RESTAURANT_COLORS['info']};
    }}
    
    /* Cards de informação */
    .info-card {{
        background: {RESTAURANT_COLORS['card_bg']};
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid {RESTAURANT_COLORS['primary']};
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        color: {RESTAURANT_COLORS['dark']};
    }}
    
    .info-card h4 {{
        color: {RESTAURANT_COLORS['dark']};
        margin: 0 0 0.5rem 0;
    }}
    
    .info-card p {{
        color: {RESTAURANT_COLORS['dark']};
        margin: 0;
    }}
    
    /* Métricas do Streamlit */
    .stMetric {{
        background: linear-gradient(135deg, {RESTAURANT_COLORS['info']} 0%, {RESTAURANT_COLORS['success']} 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }}
    
    .stMetric > div {{
        color: white !important;
    }}
    
    .stMetric label {{
        color: white !important;
        font-weight: bold;
    }}
    
    /* Divisores */
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, {RESTAURANT_COLORS['primary']}, {RESTAURANT_COLORS['accent']}, {RESTAURANT_COLORS['primary']});
        margin: 2rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# Função para conectar ao MongoDB
@st.cache_resource
def connect_mongo(uri, db_name):
    client = MongoClient(uri)
    db = client[db_name]
    return db

# Função para converter ObjectId para string e lidar com tipos aninhados
def process_record(record):
    for key, value in record.items():
        if isinstance(value, ObjectId):
            record[key] = str(value)
        elif isinstance(value, dict):
            record[key] = process_record(value)
        elif isinstance(value, list):
            record[key] = [process_record(item) if isinstance(item, dict) else item for item in value]
    return record

# Função para buscar dados de uma coleção
@st.cache_data(ttl=600)
def fetch_data_from_mongo(_db, collection_name):
    collection = _db[collection_name]
    data = list(collection.find({}))
    processed_data = [process_record(record) for record in data]
    return pd.DataFrame(processed_data)

# Função para criar cards de métricas personalizados
def create_metric_card(title, value, icon):
    return f"""
    <div class="metric-card">
        <h3>{icon} {value}</h3>
        <p>{title}</p>
    </div>
    """

# Função para criar gráficos estilizados com paleta consistente
def create_styled_chart(fig, title, height=500):
    fig.update_layout(
        title={
            'text': f"<b>{title}</b>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': RESTAURANT_COLORS['dark']}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': RESTAURANT_COLORS['dark'], 'family': "Arial"},
        margin=dict(l=20, r=20, t=60, b=20),
        height=height,
        hoverlabel=dict(
            bgcolor="rgba(0,0,0,0.85)",
            font_size=14,
            font_family="Arial",
            font_color="white",
            bordercolor="white"
        ),
        xaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
    )
    return fig

# Cores para gráficos baseadas na paleta profissional
CHART_COLORS = [
    RESTAURANT_COLORS['primary'],
    RESTAURANT_COLORS['secondary'],
    RESTAURANT_COLORS['accent'],
    RESTAURANT_COLORS['success'],
    RESTAURANT_COLORS['info'],
    RESTAURANT_COLORS['warning'],
    '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8'
]

# URI de conexão MongoDB
uri = st.secrets["MONGODB_URI"]
db_name = "restaurante_reviews_db"

try:
    db = connect_mongo(uri, db_name)
    st.success("Conectado ao MongoDB com sucesso!")
except Exception as e:
    st.error(f"Erro ao conectar ao MongoDB: {e}")
    st.stop()

# Carregar todos os dados das coleções
@st.cache_data(ttl=600)
def load_all_data(_db):
    data = {}
    collections = ["avaliacoes", "cardapios", "mensagens", "notificacoes", "pedidos", "pratos", "relatorios", "restaurantes", "usuarios"]
    for col_name in collections:
        data[col_name] = fetch_data_from_mongo(_db, col_name)
    return data

all_data = load_all_data(db)

# --- SIDEBAR COM FILTROS INTELIGENTES ---
st.sidebar.markdown("## Filtros Inteligentes")

# Inicializa os DataFrames
df_pedidos = all_data.get('pedidos', pd.DataFrame()).copy()
df_restaurantes = all_data.get('restaurantes', pd.DataFrame()).copy()

# Filtro de categorias (NOVO)
if not df_restaurantes.empty and 'categorias' in df_restaurantes.columns:
    # Extrair todas as categorias únicas
    all_categories = []
    for categorias in df_restaurantes['categorias'].dropna():
        if isinstance(categorias, list):
            all_categories.extend(categorias)
        elif isinstance(categorias, str):
            all_categories.append(categorias)

    unique_categories = sorted(list(set(all_categories)))

    if unique_categories:
        selected_categories = st.sidebar.multiselect(
            "Categorias de Restaurantes",
            unique_categories,
            default=[],
            help="Selecione as categorias de restaurantes para filtrar"
        )

        # Aplicar filtro de categorias
        if selected_categories:
            filtered_restaurant_ids = []
            for idx, row in df_restaurantes.iterrows():
                if isinstance(row['categorias'], list):
                    if any(cat in selected_categories for cat in row['categorias']):
                        filtered_restaurant_ids.append(row['_id'])
                elif isinstance(row['categorias'], str):
                    if row['categorias'] in selected_categories:
                        filtered_restaurant_ids.append(row['_id'])

            if not df_pedidos.empty and filtered_restaurant_ids:
                df_pedidos = df_pedidos[df_pedidos['restaurante_id'].isin(filtered_restaurant_ids)]

# Filtro de período
if not df_pedidos.empty and 'data_hora_pedido' in df_pedidos.columns:
    df_pedidos['data_hora_pedido'] = pd.to_datetime(df_pedidos['data_hora_pedido'])

    min_date = df_pedidos['data_hora_pedido'].min().date()
    max_date = df_pedidos['data_hora_pedido'].max().date()

    date_range = st.sidebar.date_input(
        "Período de Análise",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
        df_pedidos = df_pedidos[
            (df_pedidos['data_hora_pedido'].dt.date >= start_date) &
            (df_pedidos['data_hora_pedido'].dt.date <= end_date)
        ]

# Filtro de restaurantes
if not df_restaurantes.empty:
    restaurantes_list = ['Todos'] + sorted(df_restaurantes['nome'].unique().tolist())
    selected_restaurants = st.sidebar.multiselect(
        "Restaurantes",
        restaurantes_list,
        default=['Todos']
    )

    if 'Todos' not in selected_restaurants and selected_restaurants:
        if not df_pedidos.empty:
            restaurant_ids = df_restaurantes[df_restaurantes['nome'].isin(selected_restaurants)]['_id'].tolist()
            df_pedidos = df_pedidos[df_pedidos['restaurante_id'].isin(restaurant_ids)]

# Filtro de status de pedidos
if not df_pedidos.empty:
    status_list = ['Todos'] + df_pedidos['status_pedido'].unique().tolist()
    selected_status = st.sidebar.multiselect(
        "Status dos Pedidos",
        status_list,
        default=['Todos']
    )

    if 'Todos' not in selected_status and selected_status:
        df_pedidos = df_pedidos[df_pedidos['status_pedido'].isin(selected_status)]

# --- DASHBOARD PRINCIPAL ---
st.markdown("# Dashboard de Análise de Restaurantes")
st.markdown("### Análise Completa e Inteligente dos Dados de Restaurantes")
st.markdown("---")

# --- MÉTRICAS PRINCIPAIS EM CARDS PERSONALIZADOS ---
if not df_pedidos.empty:
    # Calcular métricas
    total_pedidos = len(df_pedidos)
    valor_total = df_pedidos['valor_total'].sum()
    pedidos_entregues = df_pedidos[df_pedidos['status_pedido'] == 'entregue'].shape[0]
    taxa_sucesso = (pedidos_entregues / total_pedidos * 100) if total_pedidos > 0 else 0
    ticket_medio = valor_total / total_pedidos if total_pedidos > 0 else 0

    # Layout em 4 colunas para métricas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(create_metric_card("Total de Pedidos", f"{total_pedidos:,}", ""), unsafe_allow_html=True)

    with col2:
        st.markdown(create_metric_card("Faturamento Total", f"R$ {valor_total:,.2f}", ""), unsafe_allow_html=True)

    with col3:
        st.markdown(create_metric_card("Taxa de Sucesso", f"{taxa_sucesso:.1f}%", ""), unsafe_allow_html=True)

    with col4:
        st.markdown(create_metric_card("Ticket Médio", f"R$ {ticket_medio:.2f}", ""), unsafe_allow_html=True)

    st.markdown("---")
else:
    st.warning("Nenhum dado de pedido encontrado para os filtros selecionados.")

# --- ANÁLISE DE PEDIDOS AVANÇADA ---
if not df_pedidos.empty:
    st.markdown("## Análise Detalhada de Pedidos")

    # Layout em 2 colunas para gráficos
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de pizza para status dos pedidos
        status_counts = df_pedidos['status_pedido'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']

        fig_status = px.pie(
            status_counts,
            names='status',
            values='count',
            title='Distribuição de Status dos Pedidos',
            color_discrete_sequence=CHART_COLORS,
            hole=0.4
        )
        fig_status.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}<extra></extra>',
            hoverlabel=dict(bgcolor="rgba(0,0,0,0.85)", font_color="white", font_size=14, bordercolor="white")
        )
        st.plotly_chart(create_styled_chart(fig_status, 'Status dos Pedidos'), use_container_width=True)

    with col2:
        # Gráfico de barras para pedidos por dia da semana
        df_pedidos['dia_semana'] = df_pedidos['data_hora_pedido'].dt.day_name()
        dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dias_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

        pedidos_dia = df_pedidos['dia_semana'].value_counts().reindex(dias_ordem).reset_index()
        pedidos_dia.columns = ['dia', 'count']
        pedidos_dia['dia_pt'] = dias_pt

        fig_dias = px.bar(
            pedidos_dia,
            x='dia_pt',
            y='count',
            title='Pedidos por Dia da Semana',
            color='count',
            color_continuous_scale=[[0, RESTAURANT_COLORS['info']], [1, RESTAURANT_COLORS['primary']]]
        )
        fig_dias.update_traces(
            hovertemplate='<b>%{x}</b><br>Pedidos: %{y}<extra></extra>',
            hoverlabel=dict(bgcolor="rgba(0,0,0,0.85)", font_color="white", font_size=14, bordercolor="white")
        )
        st.plotly_chart(create_styled_chart(fig_dias, 'Pedidos por Dia da Semana'), use_container_width=True)

    # Gráfico de evolução temporal (largura completa)
    st.markdown("### Evolução Temporal dos Pedidos")
    df_pedidos['data'] = df_pedidos['data_hora_pedido'].dt.date
    pedidos_tempo = df_pedidos.groupby('data').agg({
        'valor_total': 'sum',
        '_id': 'count'
    }).reset_index()
    pedidos_tempo.columns = ['data', 'faturamento', 'quantidade']

    fig_tempo = make_subplots(specs=[[{"secondary_y": True}]])
    fig_tempo.add_trace(
        go.Scatter(
            x=pedidos_tempo['data'],
            y=pedidos_tempo['quantidade'],
            name="Quantidade de Pedidos",
            line=dict(color=RESTAURANT_COLORS['primary'], width=3),
            hovertemplate='<b>Data: %{x}</b><br>Pedidos: %{y}<extra></extra>',
            hoverlabel=dict(bgcolor="rgba(0,0,0,0.85)", font_color="white", font_size=14, bordercolor="white")
        ),
        secondary_y=False
    )
    fig_tempo.add_trace(
        go.Scatter(
            x=pedidos_tempo['data'],
            y=pedidos_tempo['faturamento'],
            name="Faturamento (R$)",
            line=dict(color=RESTAURANT_COLORS['success'], width=3),
            hovertemplate='<b>Data: %{x}</b><br>Faturamento: R$ %{y:,.2f}<extra></extra>',
            hoverlabel=dict(bgcolor="rgba(0,0,0,0.85)", font_color="white", font_size=14, bordercolor="white")
        ),
        secondary_y=True
    )
    fig_tempo.update_xaxes(title_text="Data")
    fig_tempo.update_yaxes(title_text="Quantidade de Pedidos", secondary_y=False)
    fig_tempo.update_yaxes(title_text="Faturamento (R$)", secondary_y=True)
    st.plotly_chart(create_styled_chart(fig_tempo, 'Evolução Temporal: Pedidos vs Faturamento', 400), use_container_width=True)
    st.markdown("---")

# --- ANÁLISE DE RESTAURANTES ---
if not df_pedidos.empty:
    st.markdown("## Performance dos Restaurantes")

    if not df_restaurantes.empty:
        df_rest_pedidos = pd.merge(df_pedidos, df_restaurantes[['_id', 'nome', 'categorias']],
                                 left_on='restaurante_id', right_on='_id', how='left')

        # Layout em 2 colunas
        col1, col2 = st.columns(2)

        with col1:
            # Top restaurantes por faturamento
            top_rest_faturamento = df_rest_pedidos.groupby('nome')['valor_total'].sum().sort_values(ascending=False).head(10).reset_index()
            fig_top_rest = px.bar(
                top_rest_faturamento,
                x='valor_total',
                y='nome',
                orientation='h',
                title='Top 10 Restaurantes por Faturamento',
                color='valor_total',
                color_continuous_scale=[[0, RESTAURANT_COLORS['accent']], [1, RESTAURANT_COLORS['primary']]]
            )
            fig_top_rest.update_layout(yaxis={'categoryorder':'total ascending'})
            fig_top_rest.update_traces(
                hovertemplate='<b>%{y}</b><br>Faturamento: R$ %{x:,.2f}<extra></extra>',
                hoverlabel=dict(bgcolor="rgba(0,0,0,0.85)", font_color="white", font_size=14, bordercolor="white")
            )
            st.plotly_chart(create_styled_chart(fig_top_rest, 'Top Restaurantes - Faturamento'), use_container_width=True)

        with col2:
            # Faturamento por categoria
            if 'categorias' in df_rest_pedidos.columns and not df_rest_pedidos['categorias'].isnull().all():
                df_exploded = df_rest_pedidos.explode('categorias')
                cozinha_faturamento = df_exploded.groupby('categorias')['valor_total'].sum().reset_index()

                fig_cozinha = px.pie(
                    cozinha_faturamento,
                    names='categorias',
                    values='valor_total',
                    title='Faturamento por Tipo de Cozinha',
                    color_discrete_sequence=CHART_COLORS
                )
                fig_cozinha.update_traces(
                    hovertemplate='<b>%{label}</b><br>Faturamento: R$ %{value:,.2f}<br>Percentual: %{percent}<extra></extra>',
                    hoverlabel=dict(bgcolor="rgba(0,0,0,0.85)", font_color="white", font_size=14, bordercolor="white")
                )
                st.plotly_chart(create_styled_chart(fig_cozinha, 'Tipos de Cozinha'), use_container_width=True)
            else:
                st.info("Coluna 'categorias' não disponível ou sem dados para análise.")
    else:
        st.warning("Nenhum dado de restaurantes encontrado para análise de performance.")

# --- ANÁLISE DE AVALIAÇÕES ---
st.markdown("---")
st.markdown("## Análise de Avaliações e Satisfação")
df_avaliacoes = all_data.get('avaliacoes', pd.DataFrame()).copy()

if not df_avaliacoes.empty:
    df_avaliacoes['data_avaliacao'] = pd.to_datetime(df_avaliacoes['data_avaliacao'])

    # Métricas de avaliação em 3 colunas
    col1, col2, col3 = st.columns(3)

    with col1:
        nota_media = df_avaliacoes['nota'].mean()
        st.metric(label="Nota Média Geral", value=f"{nota_media:.2f}")

    with col2:
        total_avaliacoes = len(df_avaliacoes)
        st.metric(label="Total de Avaliações", value=f"{total_avaliacoes:,}")

    with col3:
        avaliacoes_positivas = df_avaliacoes[df_avaliacoes['nota'] >= 4].shape[0]
        taxa_satisfacao = (avaliacoes_positivas / total_avaliacoes * 100) if total_avaliacoes > 0 else 0
        st.metric(label="Taxa de Satisfação", value=f"{taxa_satisfacao:.1f}%")

    # Gráficos de avaliação em 2 colunas
    col1, col2 = st.columns(2)

    with col1:
        # Histograma de notas
        fig_notas = px.histogram(
            df_avaliacoes,
            x='nota',
            nbins=5,
            title='Distribuição das Notas',
            color_discrete_sequence=[RESTAURANT_COLORS['primary']]
        )
        fig_notas.update_traces(
            marker_line_width=2,
            marker_line_color="white",
            hovertemplate='<b>Nota: %{x}</b><br>Quantidade: %{y}<extra></extra>',
            hoverlabel=dict(bgcolor="rgba(0,0,0,0.85)", font_color="white", font_size=14, bordercolor="white")
        )
        st.plotly_chart(create_styled_chart(fig_notas, 'Distribuição de Notas'), use_container_width=True)

    with col2:
        # Evolução temporal das notas
        df_avaliacoes['mes_ano'] = df_avaliacoes['data_avaliacao'].dt.to_period('M').astype(str)
        avaliacoes_tempo = df_avaliacoes.groupby('mes_ano')['nota'].mean().reset_index()

        fig_aval_tempo = px.line(
            avaliacoes_tempo,
            x='mes_ano',
            y='nota',
            title='Evolução da Nota Média',
            markers=True,
            line_shape='spline'
        )
        fig_aval_tempo.update_traces(
            line=dict(color=RESTAURANT_COLORS['success'], width=4),
            marker=dict(size=8, color=RESTAURANT_COLORS['success']),
            hovertemplate='<b>Período: %{x}</b><br>Nota Média: %{y:.2f}<extra></extra>',
            hoverlabel=dict(bgcolor="rgba(0,0,0,0.85)", font_color="white", font_size=14, bordercolor="white")
        )
        st.plotly_chart(create_styled_chart(fig_aval_tempo, 'Evolução das Avaliações'), use_container_width=True)
else:
    st.warning("Nenhum dado de avaliação encontrado.")

# --- ANÁLISE DE PRATOS ---
st.markdown("---")
st.markdown("## Análise do Cardápio e Pratos")
df_pratos = all_data.get('pratos', pd.DataFrame()).copy()

if not df_pratos.empty:
    # Layout em 2 colunas para análise de pratos
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição de preços 
        fig_precos = px.histogram(
            df_pratos, 
            x='preco', 
            nbins=20,
            title='Distribuição de Preços dos Pratos', 
            color_discrete_sequence=['#E3B778'] 
        )
        fig_precos.update_traces(
            hovertemplate='<b>Faixa de Preço: R$ %{x:.2f}</b><br>Quantidade de pratos: %{y}<extra></extra>',
            hoverlabel=dict(bgcolor="rgba(0,0,0,0.85)", font_color="white", font_size=14, bordercolor="white")
        )
        st.plotly_chart(create_styled_chart(fig_precos, 'Distribuição de Preços dos Pratos'), use_container_width=True)
    
    with col2:
        # Top pratos mais caros
        top_pratos_caros = df_pratos.nlargest(10, 'preco')
        fig_caros = px.bar(
            top_pratos_caros, 
            x='preco', 
            y='nome',
            orientation='h', 
            title='Top 10 Pratos Mais Caros',
            color='preco', 
            color_continuous_scale=[[0, RESTAURANT_COLORS['warning']], [1, RESTAURANT_COLORS['primary']]]
        )
        fig_caros.update_layout(yaxis={'categoryorder':'total ascending'})
        fig_caros.update_traces(
            hovertemplate='<b>%{y}</b><br>Preço: R$ %{x:.2f}<extra></extra>',
            hoverlabel=dict(bgcolor="rgba(0,0,0,0.85)", font_color="white", font_size=14, bordercolor="white")
        )
        st.plotly_chart(create_styled_chart(fig_caros, 'Pratos Mais Caros'), use_container_width=True)
else:
    st.warning("Nenhum dado de pratos encontrado.")

# --- RODAPÉ INFORMATIVO ---
st.markdown("---")
st.markdown("### Informações do Sistema")

# Layout em 3 colunas para informações do sistema
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>Atualização</h4>
        <p>Dados atualizados a cada 10 minutos</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>Fonte de Dados</h4>
        <p>MongoDB - Conexão em tempo real</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h4>Dashboard</h4>
        <p>Análise completa e interativa</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-style: italic; margin-top: 2rem;">
    Dashboard desenvolvido para análise inteligente de dados de restaurantes<br>
</div>
""", unsafe_allow_html=True)