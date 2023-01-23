import math


def calculate_hp_iv(base_hp, hp_evs, level, stat):
    iv = 0
    iv_range = []

    for item in range(32):
        hp = math.floor((2 * base_hp + iv + math.floor(hp_evs/4)) * level / 100 + level + 10)

        if hp == stat:
            iv_range.append(iv)

        iv += 1
    try:
        return [iv_range[0], iv_range[-1]]
    except IndexError:
        return None
# print(calculate_hp_iv(45, 0, 10, 30))

def calculate_stat_iv(base_stat, evs, level, nature, stat):
    iv = 0
    iv_range = []

    for item in range(32):
        stat_formula = math.floor(math.floor((2 * base_stat + iv + math.floor(evs/4)) * level / 100 + 5) * nature)
        print(f"IV: {stat_formula}")
        if stat_formula == stat:
            iv_range.append(iv)

        iv += 1
    try:
        return [iv_range[0], iv_range[-1]]
    except IndexError:
        return None


# print(calculate_stat_iv(100, 0, 3, 1.0, 12))