#CONFIGURAÇÃO

import pandas as pd
import requests
import datetime as dt
import getpass


# Base URL da API
BASE_URL = "https://api.football-data.org/v4"
COMPETITION_CODE = "PL"  # Premier League

# Capturar API Key (não aparece no output)
API_KEY = getpass.getpass("DIGITE SUA API KEY")
HEADERS = {"X-Auth-Token": API_KEY}

#EXTRAÇÃO

def get_matches(date_from, date_to, status="FINISHED"):
    url = f"{BASE_URL}/competitions/{COMPETITION_CODE}/matches"
    params = {
        "dateFrom": date_from,
        "dateTo": date_to,
        "status": status
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()
    return data["matches"]



today = dt.date.today()
date_to = today.strftime("%Y-%m-%d")
date_from = (today - dt.timedelta(days=30)).strftime("%Y-%m-%d")

matches = get_matches(date_from, date_to)
print(f"Total de partidas encontradas: {len(matches)}")


#TRANSFORM

# Criar lista de dicionários com colunas úteis
rows = []
for m in matches:
    home = m["homeTeam"]["name"]
    away = m["awayTeam"]["name"]
    goals_home = m["score"]["fullTime"]["home"]
    goals_away = m["score"]["fullTime"]["away"]
    rows.append({
        "matchday": m["matchday"],
        "date": m["utcDate"],
        "home_team": home,
        "away_team": away,
        "goals_home": goals_home,
        "goals_away": goals_away,
        "total_goals": (goals_home or 0) + (goals_away or 0)
    })


df = pd.DataFrame(rows)
df["date"] = pd.to_datetime(df["date"])
print(df.head())


#LOAD

df.to_csv("matches.csv", index=False)
print("Arquivo 'matches.csv' salvo com sucesso!")


#ANALISE SIMPLES COM PANDAS

# Média de gols por partida
print("Média de gols por jogo:", df["total_goals"].mean())

# Top 5 jogos com mais gols
print("\nTop 5 jogos com mais gols:")
print(df.sort_values("total_goals", ascending=False).head(5))

# Quantidade de jogos por rodada
print("\nJogos por rodada:")
print(df["matchday"].value_counts().sort_index())
