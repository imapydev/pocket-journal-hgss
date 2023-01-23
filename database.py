import json
from os.path import exists

class Database:

    def __init__(self):

        self.dex = {}
        self.natures = {}
        self.party = {}
        self.routes = {}

        # Init
        self.load_database()

    def load_database(self):
        dex_exists = exists("data/dex.json")
        natures_exists = exists("data/natures.json")
        party_exists = exists("data/party.json")
        routes_exists = exists("data/routes.json")

        if dex_exists:
            with open("data/dex.json", "r") as file:
                self.dex = json.load(file)
        print(f"Dex data loaded: {dex_exists}.")

        if natures_exists:
            with open("data/natures.json", "r") as file:
                self.natures = json.load(file)
        print(f"Natures data loaded: {natures_exists}")

        if party_exists:
            with open("data/party.json", "r") as file:
                self.party = json.load(file)
        print(f"Party data loaded: {party_exists}")

        if routes_exists:
            with open("data/routes.json", "r") as file:
                self.routes = json.load(file)
        print(f"Routes data loaded: {routes_exists}")

    # Dex related functions
    def find_dex_number(self, poke_name):
        number = [item for item in self.dex if self.dex[item]["name"] == poke_name]
        try:
            return number[0]
        except IndexError:
            return None

    def find_dex_name(self, dex_number):
        try:
            return self.dex[dex_number]["name"]
        except KeyError:
            return None

    def get_base_stats(self, poke_name):
        try:
            poke_name = self.get_real_name(poke_name)
            return self.dex[self.find_dex_number(poke_name)]["base_stats"]
        except KeyError:
            return None

    def get_dex_names(self):
        names = [self.dex[item]["name"] for item in self.dex]
        return names

    def get_evolution(self, nick):
        name = self.get_real_name(nick)
        dex = self.find_dex_number(name)
        return self.dex[dex]["evolution"]

    def get_ev_yields(self, name):
        try:
            return self.dex[self.find_dex_number(name)]["ev_yields"]
        except KeyError:
            return None

    # Natures related functions
    def get_natures_names(self):
        return list(self.natures.keys())


    # Party related functions
    def get_party_names(self):
        return list(self.party.keys())
    
    def get_real_name(self, nick):
        return self.party[nick]["real_name"]
    
    def get_party_data(self, nickname):
        return self.party[nickname]
    
    def rename_party(self, nick, new_nick):
        self.party[new_nick] = self.party.pop(nick)
        return new_nick

    def add_to_party(self, nick, name):
        basic_evs = [0, 0, 0, 0, 0, 0]
        level = 1
        nature = None
        basic_stats = [0, 0, 0, 0,0 ,0]
        self.party[nick] = {
            "real_name": name,
            "stats": basic_stats,
            "evs": basic_evs,
            "level": level,
            "nature": nature
        }

    def update_party(self, nick, stats=None, evs=None, level=None, nature=None):
        try:
            self.party[nick]["stats"] = stats
            self.party[nick]["evs"] = evs
            self.party[nick]["level"] = level
            self.party[nick]["nature"] = nature
        except KeyError:
            return
        finally:
            self.save_party()

    def save_party(self):
        with open("data/party.json", "w") as file:
            json.dump(self.party, file, indent=4) 
    
    def remove_from_party(self, name):
        try:
            del self.party[name]
            # print(self.party)
        except KeyError:
            print(f"Party database does not contain '{name}'")

    def evolve(self, nick, new_nick):
        evolution = self.get_evolution(nick)
        if evolution != "":
            exists = evolution in self.get_dex_names()
            # print(exists)
            if not exists:
                print("Doesnt exist")
                return False

            self.party[new_nick] = self.party.pop(nick)
            self.party[new_nick]["real_name"] = evolution
            self.save_party()
            return True
        else:
            return False

    def get_evs(self, nick):
        return self.party[nick]["evs"]
    
    def get_stats(self, nick):
        return self.party[nick]["stats"]
    
    def get_nature(self, nick):
        return self.party[nick]["nature"]

    def get_level(self, nick):
        return self.party[nick]["level"]

    # Routes related functions
    def get_routes_names(self):
        return list(self.routes.keys())

    def get_route_wilds(self, location):
        return self.routes[location]
