import requests
import time

def fetch_data(endpoint, total_records):
    all_data = []
    offset = 0
    limit = 100
    url = f"https://pokeapi.co/api/v2/{endpoint}"
    
    while offset < total_records:
        response = requests.get(url, params={"offset": offset, "limit": limit})
        if response.status_code == 200:
            data = response.json()['results']
            all_data.extend(data)
            offset += limit
            print(f"Fetched {len(data)} records from {endpoint}. Total fetched: {offset}")
        else:
            print(f"Failed to fetch data: {response.status_code}")
        
        time.sleep(1)  # Atraso para evitar atingir o limite de taxa
        
    return all_data

# Ingestão de dados dos endpoints
pokemon_data = fetch_data("pokemon", 1302)
ability_data = fetch_data("ability", 367)

# Salvar os dados em arquivos JSON (opcional)
import json

with open('data/pokemon_data.json', 'w') as f:
    json.dump(pokemon_data, f, indent=4)

with open('data/ability_data.json', 'w') as f:
    json.dump(ability_data, f, indent=4)
