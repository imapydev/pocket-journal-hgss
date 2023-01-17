import json

with open("../data/dex.json", "r") as file:
    dex = json.load(file)

while input("run?: ") != "n":
    name = input("Name: ")
    dex_num = input("Dex number: ")
    type1 = input("Type 1: ")
    type2 = input("Type 2: ")
    types = [item  for item in (type1, type2) if item]
    abilities = []
    hidden_abilities = []
    while input("Add abilities? ") != "n":
        ability = input("Ability: ")
        abilities.append(ability)
    while input("Add hidden ability? ") != "n":
        hidden_ability = input("Hidden ability: ")
        hidden_abilities.append(hidden_ability)
    print("BASE STATS:")
    base_hp = input("Hp:")
    base_attack = input("Attack: ")
    base_defense = input("Defense: ")
    base_sp_attack = input("Special Attack: ")
    base_sp_defense = input("Special Defense: ")
    base_speed = input("Speed: ")
    print("EV YIELDS:")
    hp_yield = input("Hp: ")
    attack_yield = input("Attack: ")
    defense_yield = input("Defense: ")
    sp_attack_yield = input("Special Attack: ")
    sp_defense_yield = input("Special Defense: ")
    speed_yield = input("Speed: ")

    evolution = input("Evolves to: ")

    dex[dex_num] = {
        "name": name,
        "types": types,
        "abilities": abilities,
        "hidden_abilities": hidden_abilities,
        "base_stats": [
            base_hp,
            base_attack,
            base_defense,
            base_sp_attack,
            base_sp_defense,
            base_speed
        ],
        "ev_yields": [
            hp_yield,
            attack_yield,
            defense_yield,
            sp_attack_yield,
            sp_defense_yield,
            speed_yield
        ],
        "evolution": evolution
        
    }

with open("../data/dex.json", "w") as file:
    json.dump(dex, file, indent=4)