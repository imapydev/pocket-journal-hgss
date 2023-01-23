import json

routes = {}

with open("../data/routes.json", "r") as file:
    routes = json.load(file)

run = True
while run:
    route = input("Location name: ")
    if route == "exit":
        run = False
    else:
        routes[route] = []
        while input("Add poke? ") != "n":
            poke = input("Pokemon: ")
            routes[route].append(poke)




with open("../data/routes.json", "w") as file:
    json.dump(routes, file, indent=4)