import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from PIL import Image

# Define o caminho do ícone
icon_path = "icon/pokeball.png" 
icon = Image.open(icon_path)

# Configura a página principal
st.set_page_config(
    page_title="Dashboard Pokémon",
    page_icon=icon,
    layout="wide"
)

# @st.cache_data evita chamar a API toda vez que a página recarregar
@st.cache_data(show_spinner=False)
def carregar_dados_analiticos(lista_pokemon):
    """
    Busca os dados detalhados da API para análise.
    """
    dados_detalhados = []
    
    # Amostra com 151 pokémons (Gen 1)  
    # Para carregar tudo, basta remover o "[:151]" (será lento na 1ª vez).
    lista_amostra = lista_pokemon[:151] 
    
    barra_progresso = st.progress(0, text="Carregando dados analíticos da PokeAPI...")
    
    for i, pkm_info in enumerate(lista_amostra):
        url = pkm_info['url']
        try:
            response = requests.get(url)
            if response.status_code == 200:
                detalhes = response.json()
                
                stats = {stat['stat']['name']: stat['base_stat'] for stat in detalhes['stats']}
                tipos = [t['type']['name'] for t in detalhes['types']]
                habilidades = [a['ability']['name'].capitalize() for a in detalhes['abilities']]
                
                # Adiciona dados
                dados_detalhados.append({
                    "nome": detalhes['name'].capitalize(),
                    "id": detalhes['id'],
                    "sprite": detalhes['sprites']['front_default'],
                    "tipo_principal": tipos[0], # Pega o primeiro tipo para análise
                    "tipos": tipos,
                    "altura": detalhes['height'] / 10.0,  
                    "peso": detalhes['weight'] / 10.0,    
                    "habilidades": habilidades,           
                    **stats 
                })
            
            # Atualiza progresso
            percentual = (i + 1) / len(lista_amostra)
            barra_progresso.progress(percentual, text=f"Carregando {pkm_info['name']}...")
            
        except requests.exceptions.RequestException:
            pass # Pula o Pokémon se a API falhar
    
    barra_progresso.empty() # Limpa a barra
    return pd.DataFrame(dados_detalhados)

# Carrega os JSONs
try:
    with open('data/pokemon_data.json', 'r') as f:
        lista_pokemon_total = json.load(f) 
    with open('data/ability_data.json', 'r') as f:
        lista_ability_total = json.load(f) 
except FileNotFoundError as e:
    st.error(f"Erro: Arquivo JSON não encontrado. {e}")
    st.stop()

df_pokemon = carregar_dados_analiticos(lista_pokemon_total)


st.title("📈 Dashboard Geral dos Pokémon")
st.markdown(f"""
Este dashboard analisa os **{len(df_pokemon)}** Pokémon da amostra carregada.
""")

st.header("Métricas Principais")

col1, col2, col3 = st.columns(3)

# Métrica 1: Total Pokémon (Amostra)
total_pokemon_amostra = df_pokemon.shape[0]
col1.metric(label="Total de Pokémon (Amostra)", value=total_pokemon_amostra)

# Métrica 2: Total Habilidades (Global)
total_habilidades = len(lista_ability_total) 
col2.metric(label="Total de Habilidades (Global)", value=total_habilidades)

# Métrica 3: Tipo mais comum (Amostra)
if not df_pokemon.empty:
    tipo_mais_comum = df_pokemon['tipo_principal'].value_counts().idxmax()
else:
    tipo_mais_comum = "N/A"
col3.metric(label="Tipo Principal Mais Comum (Amostra)", value=tipo_mais_comum.capitalize())


st.markdown("---") 

# Encontra os Pokémon com valores máximos/mínimos
idx_pesado = df_pokemon['peso'].idxmax()
nome_pesado = df_pokemon.loc[idx_pesado, 'nome']
valor_pesado = df_pokemon.loc[idx_pesado, 'peso']
    
idx_leve = df_pokemon['peso'].idxmin()
nome_leve = df_pokemon.loc[idx_leve, 'nome']
valor_leve = df_pokemon.loc[idx_leve, 'peso']
    
idx_alto = df_pokemon['altura'].idxmax()
nome_alto = df_pokemon.loc[idx_alto, 'nome']
valor_alto = df_pokemon.loc[idx_alto, 'altura']
    
idx_baixo = df_pokemon['altura'].idxmin()
nome_baixo = df_pokemon.loc[idx_baixo, 'nome']
valor_baixo = df_pokemon.loc[idx_baixo, 'altura']
    
col4, col5, col6, col7 = st.columns(4)
    
col4.metric(label="Pokémon Mais Pesado", value=nome_pesado, delta=f"{valor_pesado} kg")
col5.metric(label="Pokémon Mais Leve", value=nome_leve, delta=f"{valor_leve} kg")
col6.metric(label="Maior Pokémon", value=nome_alto, delta=f"{valor_alto} m")
col7.metric(label="Menor Pokémon", value=nome_baixo, delta=f"{valor_baixo} m")

st.header("Análise Detalhada dos Stats (Amostra)")

col_graf1, col_graf2 = st.columns(2)

if not df_pokemon.empty:
    with col_graf1:
        contagem_tipos = df_pokemon['tipo_principal'].value_counts().sort_values(ascending=False)
        fig_tipos = px.bar(
            contagem_tipos,
            x=contagem_tipos.index,
            y=contagem_tipos.values,
            title="Contagem de Pokémon por Tipo Principal",
            labels={'x': 'Tipo Principal', 'y': 'Quantidade'},
            color=contagem_tipos.values,
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig_tipos.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_tipos, use_container_width=True)

    with col_graf2:
        fig_hist = px.histogram(
            df_pokemon,
            x="attack",
            title="Distribuição de Ataque Base",
            labels={'attack': 'Ataque Base', 'count': 'Contagem'},
            color_discrete_sequence=['orange'] 
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # Gráfico de Dispersão
    st.markdown("---")
    st.header("Relação entre Stats (Ataque vs. Defesa)")
    
    fig_scatter = px.scatter(
        df_pokemon,
        x="attack",
        y="defense",
        color="tipo_principal", 
        hover_name="nome",      
        title="Relação Ataque vs. Defesa (Colorido por Tipo)"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Gráfico de Habilidades
    st.markdown("---")
    st.header("Análise de Habilidades (Amostra)")

    habilidades_df = df_pokemon['habilidades'].explode()
    contagem_habilidades = habilidades_df.value_counts().head(10) # Pega o Top 10

    fig_hab = px.bar(
        contagem_habilidades,
        x=contagem_habilidades.index,
        y=contagem_habilidades.values,
        title="Top 10 Habilidades Mais Comuns (Gen 1)",
        labels={'x': 'Habilidade', 'y': 'Contagem'},
        color=contagem_habilidades.values,
        color_continuous_scale=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig_hab, use_container_width=True)


    # Altura vs Peso
    st.markdown("---")
    st.header("Relação Altura vs. Peso (Amostra)")

    fig_peso_altura = px.scatter(
        df_pokemon,
        x="altura",
        y="peso",
        color="tipo_principal", 
        hover_name="nome",      
        title="Relação Altura vs. Peso (Colorido por Tipo)",
        labels={'altura': 'Altura (m)', 'peso': 'Peso (kg)'}
    )
    st.plotly_chart(fig_peso_altura, use_container_width=True)

    st.markdown("---")
    st.subheader("Dados Brutos Carregados (DataFrame da Amostra)")
    st.dataframe(df_pokemon)

else:
    st.warning("O DataFrame está vazio. Não foi possível carregar dados da API.")