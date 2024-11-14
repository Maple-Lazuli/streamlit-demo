from datetime import datetime, timedelta
import random


def generate_team(team_size: int, num_malicious: int = 1, accidental_exploration: int = .05,
                  intentional_exploration: int = .15,
                  person_base_name: str = "Zoo_Keeper") -> dict:
    team = dict()
    for i in range(team_size):
        team[f'{person_base_name}_{i}'] = {'threshold': accidental_exploration * 100, 'legitimate': True}

    for i in range(num_malicious):
        malicious_person = [_ for _ in team.keys()][random.randint(0, team_size - 1)]
        team[malicious_person] = {'threshold': intentional_exploration * 100, 'legitimate': False}

    return team


def generate_interactions(team: dict, num_team_animals: int = 15, num_days: int = 7, daily_step_size: int = 5) -> list:
    week_start = datetime.strptime("01-01-2024 08:00:00", "%d-%m-%Y %H:%M:%S")
    interactions = []
    interactions_per_step = int(len([_ for _ in team.keys()]) / 4)

    with open("../data/animals.txt", "r") as file_in:
        animals = file_in.readlines()
    animals = [animal.strip() for animal in animals]

    team_animal_idx = set()
    while len(team_animal_idx) < num_team_animals:
        team_animal_idx.add(random.randint(0, len(animals) - 1))
    team_animal_idx = list(team_animal_idx)

    for i in range(num_days):
        current_day_time = week_start + timedelta(days=i)
        current_day_end_time = current_day_time + timedelta(hours=8)

        while current_day_time < current_day_end_time:
            interactions_step = random.randint(0, interactions_per_step)
            for _ in range(interactions_step):
                zoo_keeper = [_ for _ in team.keys()][random.randint(0, len(team.keys()) - 1)]
                selected_zoo_keeper = team[zoo_keeper]
                event = random.randint(0, 100)

                if event < selected_zoo_keeper['threshold']:
                    random_animal = animals[random.randint(0, len(animals) - 1)]
                else:
                    random_idx = random.randint(0, len(team_animal_idx) - 1)
                    random_animal = animals[random_idx]

                interactions.append((zoo_keeper, random_animal, current_day_time, selected_zoo_keeper['legitimate']))
            current_day_time = current_day_time + timedelta(minutes=1)
    return interactions  # maybe make this a generator instead


def prune_interactions(interactions):
    seen_interactions = set()
    pruned_interactions = []
    for interaction in interactions:
        event = f'{interaction[0]}-{interaction[1]}'
        if event in seen_interactions:
            continue
        seen_interactions.add(event)
        pruned_interactions.append(interaction)
    return interactions
