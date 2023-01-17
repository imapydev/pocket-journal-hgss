# Utilities regarding natures
import json


def assert_nature_modifier(nature_name, stat_evaluated):
    """ Returns the modifier for a given stat, considering the nature.

            Parameters:
                nature_name (str): the nature of the Pokémon
                stat_evaluated (str): the stat being evaluated

            Returns:
                stat_mod (float): the modifier needed to calculate Ivs with precision
    """

    nature_name = nature_name.title()
    stat_evaluated = stat_evaluated.title()
    with open("data/natures.json", "r") as file:
        data = json.load(file)

    stat_mod = 1.0

    if data[nature_name]["plus_stat"] == stat_evaluated:
        stat_mod = 1.1
    elif data[nature_name]["minus_stat"] == stat_evaluated:
        stat_mod = 0.9
    else:
        stat_mod = 1.0

    return stat_mod

