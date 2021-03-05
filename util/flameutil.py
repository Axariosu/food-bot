import time, random
import asyncio
import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker
from PIL import Image
np.set_printoptions(threshold=np.inf)

class OOMFormatter(matplotlib.ticker.ScalarFormatter):
    def __init__(self, order=0, fformat="%1.1f", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter.__init__(self,useOffset=offset,useMathText=mathText)
    def _set_order_of_magnitude(self):
        self.orderOfMagnitude = self.oom
    def _set_format(self, vmin=None, vmax=None):
        self.format = self.fformat
        if self._useMathText:
            self.format = r'$\mathdefault{%s}$' % self.format

async def get_k_random_from_list(l:list, k:int):
    """
    Given a list l and integer k: 
    Returns k elements from l with random.sample.
    """
    return random.sample(l, k=k)

async def get_flame_tiers(flame_type:int, boss_equip:int):
    """
    Given flame_type and boss_equip:
    Returns an array of the possible flame tiers.
    0: red flame
    1: eternal flame
    """
    # red flame
    # cumulative probability
    # [0.2, 0.3, 0.36, 0.14]
    # [0.2, 0.5, 0.86, 1.00]
    # rainbow flame
    # cumulative probability
    # [0.29, 0.45, 0.25, 0.01]
    # [0.29, 0.74, 0.99, 1.00]

    # non-boss equipment probabilities of lines: 
    # [0.33, 0.46, 0.20, 0.01]

    # red flame 
    if flame_type == 0:
        flame_probability = [0.2, 0.5, 0.86, 1.00]
        res = []
        for i in range(4): 
            k = random.random()
            for j in range(len(flame_probability)):
                if k < flame_probability[j]: 
                    res.append(j)
                    break
        return [x + 3 for x in res] if boss_equip else [x for x in res]
    # rainbow flame
    else: 
        flame_probability = [0.29, 0.74, 0.99, 1.00]
        res = []
        for i in range(4): 
            k = random.random()
            for j in range(len(flame_probability)):
                if k < flame_probability[j]: 
                    res.append(j)
                    break
        return [x + 4 for x in res] if boss_equip else [x + 1 for x in res]

async def convert_flames(flame_list:list, tiers:list, l:int): 
    """
    Given flame list and tiers, 
    Returns a dictionary of the item flame. 
    {kSTAT: nVALUE}
    """
    res = {"STR" : 0,
        "DEX": 0,
        "INT": 0,
        "LUK": 0,
        "Weapon Attack": 0,
        "Magic Attack": 0,
        "Defense": 0,
        "MaxHP": 0,
        "MaxMP": 0,
        "Speed": 0,
        "Jump": 0,
        "All Stats": 0,
        "Equip Level Reduction": 0}
    
    for i in range(len(flame_list)):
        # STR, DEX, INT, LUK
        if 0 <= flame_list[i] <= 3: 
            s = (l // 20 + 1) * tiers[i]
            if flame_list[i] == 0: 
                res["STR"] += s
            elif flame_list[i] == 1: 
                res["DEX"] += s
            elif flame_list[i] == 2: 
                res["INT"] += s
            elif flame_list[i] == 3: 
                res["LUK"] += s
        # DSD, DSI, DSL, DDI, DDL, DIL
        elif 4 <= flame_list[i] <= 9: 
            s = (l // 40 + 1) * tiers[i]
            if flame_list[i] == 4: 
                res["STR"] += s
                res["DEX"] += s
            elif flame_list[i] == 5: 
                res["STR"] += s
                res["INT"] += s
            elif flame_list[i] == 6: 
                res["STR"] += s
                res["LUK"] += s
            elif flame_list[i] == 7: 
                res["DEX"] += s
                res["INT"] += s
            elif flame_list[i] == 8: 
                res["DEX"] += s
                res["LUK"] += s
            elif flame_list[i] == 9: 
                res["INT"] += s
                res["LUK"] += s
        # ATK, MATK, Speed, Jump, AS%
        elif 10 <= flame_list[i] <= 11 or 15 <= flame_list[i] <= 17:
            s = tiers[i]
            if flame_list[i] == 10: 
                res["Weapon Attack"] += s
            elif flame_list[i] == 11: 
                res["Magic Attack"] += s
            elif flame_list[i] == 15: 
                res["Speed"] += s
            elif flame_list[i] == 16: 
                res["Jump"] += s
            elif flame_list[i] == 17: 
                res["All Stats"] += s
        # DEF
        elif flame_list[i] == 12: 
            s = (l // 20 + 1) * tiers[i]
            res["Defense"] += s
        # HP, MP
        elif 13 <= flame_list[i] <= 14:
            s = 0
            if 0 <= l <= 9: 
                s = 3 * tiers[i]
            else: 
                s = (l // 10 + 1) * 30 * tiers[i]
            if flame_list[i] == 13: 
                res["MaxHP"] += s
            elif flame_list[i] == 14: 
                res["MaxMP"] += s
        # Equip level reduction
        elif flame_list[i] == 18: 
            s = 5 * tiers[i]
            res["Equip Level Reduction"] += s
    return res

async def calculate_flame_score(flame_dict:dict, all_stat:float, att:float, secondary:float): 
    """
    Given a flame_dictionary, allstat, and att: 
    Returns a dictionary of flame scores based on stat. 
    """
    score = {"STR": 0,
        "DEX": 0, 
        "INT": 0, 
        "LUK": 0}

    score["STR"] += flame_dict["STR"] + all_stat * flame_dict["All Stats"] + att * flame_dict["Weapon Attack"] + secondary * flame_dict["DEX"]
    score["DEX"] += flame_dict["DEX"] + all_stat * flame_dict["All Stats"] + att * flame_dict["Weapon Attack"] + secondary * flame_dict["STR"]
    score["INT"] += flame_dict["INT"] + all_stat * flame_dict["All Stats"] + att * flame_dict["Magic Attack"] + secondary * flame_dict["LUK"]
    score["LUK"] += flame_dict["LUK"] + all_stat * flame_dict["All Stats"] + att * flame_dict["Weapon Attack"] + secondary * flame_dict["DEX"]

    return score

async def generate_confidence_index_from_histogram(hist):
    """
    Given a histogram:
    Returns median (50th percentile) and 75th, 85th, 95th percentiles.
    """
    return np.percentile(hist, [50, 75, 85, 95])

async def generate_image_from_histogram(hist, xlabel, ylabel):
    """
    Given a histogram:
    Returns an image binary of the histogram.
    """
    q25, q75, q85, q95 = np.percentile(hist,[25, 75, 85, 95])
    bin_width = 2*(q75 - q25)*len(hist)**(-1/3)
    bins = int((hist.max() - hist.min())/bin_width)

    plt.clf()
    # style
    plt.style.use('dark_background')
    n, bins, patches = plt.hist(hist, bins=bins)
    n = n.astype('int') 
    for i in range(len(patches)):
        patches[i].set_facecolor(plt.cm.viridis(n[i]/max(n)))
    # plt.title('frequency histogram')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # plt.gcf().axes[0].xaxis.set_major_formatter(OOMFormatter(9, "%1.1f")) # magic billions format? 
    # plt.gcf().axes[0].xaxis.set_xlim()
    # save to image 
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0) # image binary
    return img
    # uncomment below for testing
    # im = Image.open(img)
    # im.show()
    # return img

async def run_simulation(n:int, l:int, threshold:float, flame_type:int, boss_equip:int, all_stat:float, att:float, secondary:float):
    """
    Runs n simulations with the given parameters. 
    """
    armor_stats = dict(enumerate(
        ["STR increase",
        "DEX increase",
        "INT increase",
        "LUK increase",
        "STR and DEX increase",
        "STR and INT increase",
        "STR and LUK increase",
        "DEX and INT increase",
        "DEX and LUK increase",
        "INT and LUK increase",
        "Attack Power increase (Non-weapons)",
        "Magic Attack increase (Non-weapons)",
        "Defense increase",
        "HP increase",
        "MP increase",
        "Speed increase (Non-Weapons)",
        "Jump increase (Non-Weapons)",
        "All Stats % increase",
        "Equip level requirement reduction"]
    ))

    # weapon_stats = dict(enumerate(
    #     ["STR increase",
    #     "DEX increase",
    #     "INT increase",
    #     "LUK increase",
    #     "STR and DEX increase",
    #     "STR and INT increase",
    #     "STR and LUK increase",
    #     "DEX and INT increase",
    #     "DEX and LUK increase",
    #     "INT and LUK increase",
    #     "Attack Power increase (Weapons)",
    #     "Magic Attack increase (Weapons)",
    #     "Defense increase",
    #     "HP increase",
    #     "MP increase",
    #     "All Stats % increase",
    #     "Damage to Boss Monsters % increase (Weapons)",
    #     "Damage % increase (Weapons)",
    #     "Equip level requirement reduction"]
    # ))
    
    flames, min_flames, max_flames, avg_flames = 1, 10 ** 50, 0, 0
    hist, hist_threshold = np.empty(0, int), np.empty(0, int)
    # hist_str, hist_dex, hist_int, hist_luk = np.empty(0, int), np.empty(0, int), np.empty(0, int), np.empty(0, int)
    count = 0
    
    start = time.time()
    
    for i in range(n): 
        list1 = await get_k_random_from_list(list(armor_stats.keys()), 4)
        list2 = await get_flame_tiers(flame_type, boss_equip)
        res = await convert_flames(list1, list2, l)
        res2 = await calculate_flame_score(res, all_stat, att, secondary)
        score = list(res2.values())[0]
        hist = np.append(hist, score)
        if score < threshold: 
            flames += 1
        else: 
            hist_threshold = np.append(hist_threshold, flames)
            min_flames = min(min_flames, flames)
            max_flames = max(max_flames, flames)
            avg_flames = (flames + count * avg_flames) * (count + 1) ** -1
            count += 1
            flames = 1

    unique, counts = np.unique(hist, return_counts=True)

    results = dict()
    for i in range(30):
        lo = i * 10
        hi = (i + 1) * 10 - 1
        entry = str(lo) + "-" + str(hi)
        for j in range(len(unique)): 
            if (lo <= unique[j] < (hi + 1)): 
                if entry not in results:
                    results.setdefault(entry, counts[j])
                else: 
                    results[entry] += counts[j]
    
    stop = time.time()
    time_elapsed = stop - start
    return (results, hist, hist_threshold, max_flames, min_flames, avg_flames, time_elapsed)
    
# async def main():
#     k = await run_simulation(10000, 200, 120, 0, 1, 9, 3, 0.1)
#     await generate_image_from_histogram(k[1], "flame score", "frequency")

# if __name__ == "__main__":
#     asyncio.run(main())
#     pass