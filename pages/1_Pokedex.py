import streamlit as st
import requests
import json
import pandas as pd
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
@st.cache_data
def carregar_dados_pokemon(lista_pokemon):
    """
    Busca os dados detalhados de cada Pokémon na PokeAPI.
    """
    dados_detalhados = []
    
    # Amostra com 151 pokémons (Gen 1) 
    # Para carregar tudo, basta remover o "[:151]" (será lento na 1ª vez).
    lista_amostra = lista_pokemon[:151]
    
    barra_progresso = st.progress(0, text="Carregando dados da PokeAPI...")

    for i, pkm_info in enumerate(lista_amostra):
        url = pkm_info['url']
        try:
            # Busca detalhes do Pokémon
            response = requests.get(url)
            if response.status_code == 200:
                detalhes = response.json()
                
                stats = {stat['stat']['name']: stat['base_stat'] for stat in detalhes['stats']}
                tipos = [t['type']['name'] for t in detalhes['types']]
                habilidades = [a['ability']['name'].capitalize() for a in detalhes['abilities']]
                
                # Junta tudo
                dados_detalhados.append({
                    "nome": detalhes['name'].capitalize(),
                    "id": detalhes['id'],
                    "sprite": detalhes['sprites']['front_default'],
                    "tipos": tipos,
                    "altura": detalhes['height'] / 10.0,  # Converte para metros
                    "peso": detalhes['weight'] / 10.0,    # Converte para kg
                    "habilidades": habilidades,          
                    **stats 
                })
            
            # Atualiza progresso
            percentual = (i + 1) / len(lista_amostra)
            barra_progresso.progress(percentual, text=f"Carregando {pkm_info['name']}...")
            
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar dados do Pokémon {pkm_info['name']}: {e}")
    
    barra_progresso.empty() # Limpa a barra
    return pd.DataFrame(dados_detalhados)

# Carrega o JSON local
try:
    with open('data/pokemon_data.json', 'r') as f:
        lista_pokemon_total = json.load(f) 
except FileNotFoundError:
    st.error("Arquivo 'data/pokemon_data.json' não encontrado.")
    st.stop()

# Chama a função principal de carregamento
df_pokemon = carregar_dados_pokemon(lista_pokemon_total)

st.title(str(icon) + "Meu Dashboard Pokédex Interativo")
st.markdown("Use a barra lateral para selecionar um Pokémon e ver seus detalhes.")

# --- Sidebar ---
st.sidebar.header("Filtros")
pokemon_selecionado = st.sidebar.selectbox(
    "Escolha um Pokémon:",
    df_pokemon['nome'] 
)

# --- Página Principal ---
st.header(f"Detalhes de: {pokemon_selecionado}")

# Filtra o Pokémon selecionado
dados_pkm = df_pokemon[df_pokemon['nome'] == pokemon_selecionado].iloc[0]

# Layout: Imagem | Stats
col1, col2 = st.columns([1, 2]) 

with col1:
    st.image(dados_pkm['sprite'], width=200, caption=f"ID: {dados_pkm['id']}")

with col2:
    st.subheader("Informações Básicas")
    # Formata os tipos para exibição
    tipos_str = ", ".join([t.capitalize() for t in dados_pkm['tipos']])
    st.write(f"**Tipo(s):** {tipos_str}")
    
    st.subheader("Stats Base")
    
    # Prepara dados dos stats para o gráfico
    stats_colunas = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']
    stats_nomes = {
        'hp': 'HP', 'attack': 'Ataque', 'defense': 'Defesa',
        'special-attack': 'Atq. Especial', 'special-defense': 'Def. Especial', 'speed': 'Velocidade'
    }
    
    df_stats = pd.DataFrame({
        'Stat': [stats_nomes[stat] for stat in stats_colunas],
        'Valor': [dados_pkm[stat] for stat in stats_colunas]
    }).set_index('Stat')
    
    st.bar_chart(df_stats, height=300)

st.markdown("---")
st.subheader("Dados Brutos Carregados (DataFrame)")
st.dataframe(df_pokemon)