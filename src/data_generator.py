from datetime import datetime, timedelta
import random

with open("./data/animals.txt", "r") as file_in:
    animals = file_in.readlines()

animals = [animal.strip() for animal in animals]


def generate_team(team_size: int, num_malicious: int = 1, accidental_exploration: int = .05,
                  intentional_exploration: int = .25
                  , person_base_name: str = "Zoo_Keeper") -> dict:
    team = dict()
    for i in range(team_size):
        team[f'{person_base_name}_{i}'] = {'legitimate': True}
        team[f'{person_base_name}_{i}'] = {'threshold': accidental_exploration * 100}

    for i in range(num_malicious):
        malicious_person = team.keys()[random.randint(0, team_size - 1)]
        team[malicious_person] = {'legitimate': False}
        team[malicious_person] = {'threshold': intentional_exploration * 100}

    return team
