import json
from os.path import exists

class Database:

    def __init__(self):

        self.dex = {}
        self.natures = {}
        self.party = {}

        # Init
        self.load_database()

    def load_database(self):
        dex_exists = exists("data/dex.json")
        natures_exists = exists("data/natures.json")
        party_exists = exists("data/party.json")

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
            return self.dex[self.find_dex_number(poke_name)]["base_stats"]
        except KeyError:
            return None

    def get_dex_names(self):
        names = [self.dex[item]["name"] for item in self.dex]
        return names

    # Natures related functions


    # Party related functions
    def get_party_names(self):
        return list(self.party.keys())

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

    def save_party(self):
        with open("data/party.json", "w") as file:
            json.dump(self.party, file, indent=4) 

