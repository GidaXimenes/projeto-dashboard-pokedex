# 📊 Projeto Dashboard Pokedex (Projeto Pessoal)

Um dashboard de dados interativo construído com Streamlit para visualizar e analisar dados de Pokémon, consumidos diretamente da [PokeAPI](https://pokeapi.co/).

Este é um projeto pessoal desenvolvido para aplicar e demonstrar habilidades em consumo de APIs, análise de dados e criação de gráficos interativos (vistos no curso Web Academy).

## ✨ Visão Geral

Este projeto é uma aplicação web que oferece duas visualizações principais:

1.  **Pokedex**: Uma ferramenta de consulta onde o usuário pode selecionar um Pokémon (da Geração 1) e visualizar seus atributos básicos, estatísticas de combate (como Ataque, Defesa, HP), tipo e habilidades.
2.  **Dashboard**: Uma página analítica que exibe métricas agregadas e gráficos sobre o conjunto de dados dos 151 Pokémon. Inclui:
      * Métricas de KPI (Total de Pokémon, Total de Habilidades, Tipo Mais Comum).
      * Identificação de outliers (Pokémon mais pesado, mais leve, mais alto e mais baixo).
      * Gráficos interativos (Plotly) mostrando a distribuição de tipos, a relação entre Ataque vs. Defesa, e a frequência das habilidades mais comuns.

## ⚙️ Como a Aplicação Funciona

A aplicação utiliza uma arquitetura de dados em duas etapas para otimizar o desempenho:

1.  **Ingestão de Dados (Script `teste.py`)**: Um script Python (`teste.py`) é usado para fazer a primeira varredura na PokeAPI. Ele busca a lista completa de *endpoints* de Pokémon e Habilidades (nome e URL) e salva essas listas localmente em arquivos `data/pokemon_data.json` e `data/ability_data.json`. Isso evita a necessidade de consultar a lista inteira toda vez que o app é carregado.

2.  **Carregamento do Dashboard (Streamlit)**:

      * Quando um usuário acessa as páginas "Pokedex" ou "Dashboard", a aplicação lê o arquivo `pokemon_data.json` local.
      * Ela, então, itera sobre uma amostra desses dados (os primeiros 151 Pokémon, correspondentes à Geração 1) e faz requisições `GET` individuais à PokeAPI para obter os detalhes completos de cada um (stats, tipos, peso, altura, etc.).
      * Para garantir um carregamento rápido após a primeira inicialização, a função que busca e processa esses dados (`carregar_dados_pokemon` e `carregar_dados_analiticos`) utiliza o decorador `@st.cache_data` do Streamlit. Isso armazena em cache o DataFrame do Pandas, fazendo com que as chamadas de API demoradas ocorram apenas uma vez por sessão.
      * Os dados processados são então usados para alimentar os componentes interativos do Streamlit e os gráficos do Plotly.

## 🛠️ Tecnologias Utilizadas

  * **Linguagem**: Python
  * **Framework Web/Dashboard**: Streamlit
  * **Fonte de Dados**: [PokeAPI (v2)](https://pokeapi.co/)
  * **Manipulação de Dados**: Pandas
  * **Requisições HTTP**: Requests
  * **Visualização de Dados**: Plotly Express e componentes nativos do Streamlit

## 🚀 Como Executar o Projeto Localmente

Siga estas etapas para executar a aplicação em sua máquina local.

1.  **Clone o Repositório**

    ```bash
    git clone https://github.com/seu-usuario/projeto-dashboard-pokedex.git
    cd projeto-dashboard-pokedex
    ```

2.  **Crie e Ative um Ambiente Virtual** (Recomendado)

    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as Dependências**
    O projeto possui um arquivo `requirements.txt` com todas as bibliotecas necessárias.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a Aplicação Streamlit**
    O Streamlit será iniciado e abrirá a aplicação no seu navegador padrão.

    ```bash
    streamlit run Home.py
    ```

**Nota sobre os dados:** Os arquivos `data/pokemon_data.json` e `data/ability_data.json` já estão incluídos no projeto. Se desejar atualizá-los (por exemplo, se novos Pokémon forem adicionados à PokeAPI), você pode executar o script `teste.py` manualmente:

```bash
python teste.py
```
