import streamlit as st
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

st.title("📊 Dashboard Pokémon")
st.markdown("""
Bem-vindo ao meu dashboard!

Este projeto usa a **PokeAPI** e cria um dashboard interativo com **Streamlit**.
É uma mistura das minhas habilidades de análise de dados e consumo de APIs (vistas no curso Web Academy).

**Use o menu na barra lateral esquerda para navegar entre os dashboards:**

1.  **Pokedex:** Uma Pokédex simples para ver os stats de cada Pokémon.
2.  **Dashboard:** Gráficos e métricas sobre o conjunto de dados dos Pokémon.

Este projeto foi construído usando:
* `Python` como linguagem de programação
* `PokeApi` para obter os dados dos Pokémon
* `Streamlit` para o dashboard
* `Requests` para acessar a PokeAPI
* `Pandas` para manipulação de dados
* `Plotly Express` para plotar os gráficos
""")