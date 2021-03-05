import time, random
import asyncio
import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker
from PIL import Image

# import matplotlib.patches as patches
# import matplotlib.path as path

# data taken from https://strategywiki.org/wiki/MapleStory/Spell_Trace_and_Star_Force
# https://en.wikipedia.org/wiki/Moving_average#Cumulative_moving_average
# https://stackoverflow.com/questions/513882/python-list-vs-dict-for-look-up-table
# https://stackoverflow.com/questions/33203645/how-to-plot-a-histogram-using-matplotlib-in-python-with-a-list-of-data
# https://stackoverflow.com/questions/24809757/how-to-make-a-histogram-from-a-list-of-data
# https://stackoverflow.com/questions/8598673/how-to-save-a-pylab-figure-into-in-memory-file-which-can-be-read-into-pil-image/8598881
# https://www.reddit.com/r/learnpython/comments/el4vbx/how_to_remove_scientific_notation_from_a/
# changing list lookup -> dict lookup wil reduce runtime for large input n
# runtime may be slightly longer with if-statement logic which bypasses fail maintain/decrease logic
# instead, two numbers are generated per iteration: 
#   first to see if the success passes
#   if not, then roll again for destroy chance

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

async def get_success_array(starcatch:bool, event:int):
    """
    Given boolean starcatch and integer event: 
    Returns an array of the success percentages.
    0: off event
    1: 30% off
    2: 5/10/15
    """
    if not starcatch: 
        if event == 0 or event == 1:
            return [0.95, 0.90, 0.85, 0.85, 0.8, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.03, 0.02, 0.01]
        else: 
            return [0.95, 0.90, 0.85, 0.85, 0.8, 1, 0.70, 0.65, 0.60, 0.55, 1, 0.45, 0.40, 0.35, 0.30, 1, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.03, 0.02, 0.01]
    else:
        if event == 0 or event == 1:
            # 1.05 multiplicative
            return [0.9975, 0.945, 0.8925, 0.8925, 0.84, 0.7875, 0.735, 0.6825, 0.63, 0.5775, 0.525, 0.4725, 0.418, 0.3675, 0.315, 0.315, 0.315, 0.315, 0.315, 0.315, 0.315, 0.315, 0.0315, 0.021, 0.0105]
            # 1.045 multiplicative
            # return [0.99275, 0.9405, 0.88825, 0.88825, 0.836, 0.78375, 0.7315, 0.67925, 0.627, 0.57475, 0.5225, 0.47025, 0.418, 0.36575, 0.3135, 0.3135, 0.3135, 0.3135, 0.3135, 0.3135, 0.3135, 0.3135, 0.03135, 0.0209, 0.01045]
        else: 
            # 1.05 multiplicative
            return [0.9975, 0.945, 0.8925, 0.8925, 0.84, 1.05, 0.735, 0.6825, 0.63, 0.5775, 1.05, 0.4725, 0.418, 0.3675, 0.315, 1.05, 0.315, 0.315, 0.315, 0.315, 0.315, 0.315, 0.0315, 0.021, 0.0105]
            # 1.045 multiplicative
            # return [0.99275, 0.9405, 0.88825, 0.88825, 0.836, 1.045, 0.7315, 0.67925, 0.627, 0.57475, 1.045, 0.47025, 0.418, 0.36575, 0.3135, 1.045, 0.3135, 0.3135, 0.3135, 0.3135, 0.3135, 0.3135, 0.03135, 0.0209, 0.01045]

async def get_meso_for_star(meso:int, safeguard:bool, event:int):
    """
    Given the meso value for the current star, safeguard, and event: 
    Returns the meso needed to star. 
    0: off event
    1: 30% off
    2: 5/10/15
    """
    if not safeguard:
        if event == 0 or event == 2:
            return meso
        else: 
            return int(meso * .7)
    else: 
        if event == 0 or event == 2: 
            return meso * 2
        else:
            return int(meso * .7) + meso

async def generate_image_from_histogram(hist):
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
    plt.ylabel('frequency')
    plt.xlabel('meso (in billions)')
    
    plt.gcf().axes[0].xaxis.set_major_formatter(OOMFormatter(9, "%1.1f")) # magic billions format? 
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

async def generate_confidence_index_from_histogram(hist):
    """
    Given a histogram:
    Returns median (50th percentile) and 75th, 85th, 95th percentiles.
    """
    return np.percentile(hist, [50, 75, 85, 95])

async def run_simulation(n:int, l:int, start:int, end:int, safeguard:bool, starcatch:bool, event:int, boomed_to_12:bool, same_item:bool):
    """
    Runs n simulations with the given parameters. 
    """
    start_time = time.time()
    success_arr = await get_success_array(starcatch, event)
    destroy_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.01, 0.02, 0.03, 0.03, 0.03, 0.03, 0.04, 0.04, 0.10, 0.10, 0.20, 0.30, 0.40]
    meso_arr = [1000 + l ** 3 * (0 + 1) / 25, 
    1000 + l ** 3 * (1 + 1) / 25, 
    1000 + l ** 3 * (2 + 1) / 25, 
    1000 + l ** 3 * (3 + 1) / 25, 
    1000 + l ** 3 * (4 + 1) / 25,
    1000 + l ** 3 * (5 + 1) / 25, 
    1000 + l ** 3 * (6 + 1) / 25, 
    1000 + l ** 3 * (7 + 1) / 25, 
    1000 + l ** 3 * (8 + 1) / 25, 
    1000 + l ** 3 * (9 + 1) / 25,
    1000 + l ** 3 * (10 + 1) ** 2.7 / 400, 
    1000 + l ** 3 * (11 + 1) ** 2.7 / 400, 
    1000 + l ** 3 * (12 + 1) ** 2.7 / 400, 
    1000 + l ** 3 * (13 + 1) ** 2.7 / 400, 
    1000 + l ** 3 * (14 + 1) ** 2.7 / 400, 
    1000 + l ** 3 * (15 + 1) ** 2.7 / 120, 
    1000 + l ** 3 * (16 + 1) ** 2.7 / 120, 
    1000 + l ** 3 * (17 + 1) ** 2.7 / 120, 
    1000 + l ** 3 * (18 + 1) ** 2.7 / 110, 
    1000 + l ** 3 * (19 + 1) ** 2.7 / 110, 
    1000 + l ** 3 * (20 + 1) ** 2.7 / 100, 
    1000 + l ** 3 * (21 + 1) ** 2.7 / 100, 
    1000 + l ** 3 * (22 + 1) ** 2.7 / 100, 
    1000 + l ** 3 * (23 + 1) ** 2.7 / 100, 
    1000 + l ** 3 * (24 + 1) ** 2.7 / 100]
    meso_arr = [int(i) for i in meso_arr]

    # instance variables
    destroyed = False
    boom, failstack, count, star = 0, 0, 0, start
    meso, min_meso, max_meso, avg_meso = 0, 10 ** 50, 0, 0
    hist = np.empty(0, int)
    # res
    results = dict()
    for i in range(26):
        results.setdefault(i, 0)

    # run n simulations
    # for i in range(n):
    if not same_item:
        for i in range(n):
            while not destroyed and star != end:
                # print(boom, star)
                # chance time
                if failstack == 2:
                    meso += await get_meso_for_star(meso_arr[star], safeguard, event)
                    star += 1
                    failstack = 0
                # normal starring
                meso += await get_meso_for_star(meso_arr[star], safeguard, event)
                if random.random() < success_arr[star]:
                    star += 1
                    failstack = 0
                # failed logic
                else: 
                    if random.random() < destroy_arr[star]:
                        # 18 and higher cannot safeguard
                        if safeguard and star < 17:
                            star -= 1
                            failstack += 1 
                        else: 
                            destroyed = True
                            boom += 1
                    else: 
                        # checkpoints
                        if star <= 10 or star == 15 or star == 20: 
                            pass
                        else: 
                            star -= 1
                            failstack += 1
            results[star] += 1
            if not destroyed: 
                min_meso = min(meso, min_meso)
                max_meso = max(meso, max_meso)
                avg_meso = (meso + count * avg_meso) * (count + 1) ** -1
                hist = np.append(hist, meso)
            count = count + 1 if not destroyed else count
            if boomed_to_12:
                star = start if not destroyed else 12 # items go back to 12 when destroyed
            else:
                star = start
            meso = 0 if not destroyed else meso
            destroyed = False
    else:
        while count < n:
            while not destroyed and star != end:
                # print(boom, star)
                # chance time
                if failstack == 2:
                    meso += await get_meso_for_star(meso_arr[star], safeguard, event)
                    star += 1
                    failstack = 0
                # normal starring
                meso += await get_meso_for_star(meso_arr[star], safeguard, event)
                if random.random() < success_arr[star]:
                    star += 1
                    failstack = 0
                # failed logic
                else: 
                    if random.random() < destroy_arr[star]:
                        # 18 and higher cannot safeguard
                        if safeguard and star < 17:
                            star -= 1
                            failstack += 1 
                        else: 
                            destroyed = True
                            boom += 1
                    else: 
                        # checkpoints
                        if star <= 10 or star == 15 or star == 20: 
                            pass
                        else: 
                            star -= 1
                            failstack += 1
            results[star] += 1
            if not destroyed: 
                min_meso = min(meso, min_meso)
                max_meso = max(meso, max_meso)
                avg_meso = (meso + count * avg_meso) * (count + 1) ** -1
                hist = np.append(hist, meso)
            count = count + 1 if not destroyed else count
            if boomed_to_12:
                star = start if not destroyed else 12 # items go back to 12 when destroyed
            else:
                star = start
            meso = 0 if not destroyed else meso
            destroyed = False
    stop_time = time.time()
    time_elapsed = stop_time - start_time
    # print("time elapsed for %i simulations: %f" % (n, stop_time - start_time))
    return (results, hist, max_meso, min_meso, avg_meso, boom, time_elapsed)

# async def main():
# n, l, start, end, safeguard, starcatch, event, boomed_to_12, same_item

#     res, hist, max_meso, min_meso, avg_meso, boom, time_elapsed = await run_simulation(10000, 150, 12, 22, False, False, 2, True, False)
#     # generate_image_from_histogram(hist)
#     print("time elapsed: %f\nmax: %i\nmin: %i\navg: %i\nbooms: %i" % (time_elapsed, max_meso, min_meso, meso_avg, boom))
#     for k, v in res.items():
#         print(k, v)
#     return 

# if __name__ == "__main__":
#     asyncio.run(main())
#     pass
    