import requests
import json
import itertools
from typing import List, Dict, Tuple
import os

def fetch_kd_ratio(gamertag: str) -> float:
    url = f"https://sr-nextjs.vercel.app/api/halodotapi?path=%2Fgames%2Fhalo-infinite%2Fstats%2Fmultiplayer%2Fplayers%2F{gamertag}%2Fservice-record%2Fmatchmade%3Ffilter%3Dall"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        kills = data['data']['stats']['core']['summary']['kills']
        deaths = data['data']['stats']['core']['summary']['deaths']
        return kills / deaths if deaths > 0 else kills  # Avoid division by zero
    else:
        print(f"Failed to fetch data for {gamertag}")
        return 0.0

def fetch_all_players(gamertags: List[str]) -> Dict[str, float]:
    kd_ratios = {}
    for tag in gamertags:
        kd_ratios[tag] = fetch_kd_ratio(tag)
    return kd_ratios

def save_to_json(data: Dict[str, float], filename: str = "player_kd_ratios.json"):
    script_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_path, filename)
    with open(full_path, "w") as f:
        json.dump(data, f, indent=4)

def balance_teams(players: Dict[str, float], team_size: int) -> Tuple[List[str], List[str]]:
    player_list = list(players.items())
    min_diff = float("inf")
    best_teams = ([], [])
    
    for team1 in itertools.combinations(player_list, team_size):
        team1_names, team1_ratios = zip(*team1)
        team2 = [p for p in player_list if p not in team1]
        
        team2_names, team2_ratios = zip(*team2)
        
        diff = abs(sum(team1_ratios) - sum(team2_ratios))
        if diff < min_diff:
            min_diff = diff
            best_teams = (list(team1_names), list(team2_names))
    
    return best_teams

if __name__ == "__main__":
    gamertags = ["deathstartopo", "itsnukanick", "Ereb2464", "megabaldo986739", "ciccy s"]
    kd_ratios = fetch_all_players(gamertags)
    save_to_json(kd_ratios)
    team1, team2 = balance_teams(kd_ratios)
    
    print(f"Team 1: {team1}")
    print(f"Team 2: {team2}")
