import json

# natures = {}

with open("../data/natures.json", "r") as file:
    natures = json.load(file)

while input("Run?: ") != "n":
    nature = input("Nature name: ")
    plus = input("Plus stat: ")
    minus = input("Minus stat: ")

    natures[nature] = {
        "plus_stat": plus,
        "minus_stat": minus
    }

with open("../data/natures.json", "w") as file:
    json.dump(natures, file, indent=4)
