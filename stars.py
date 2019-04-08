import asyncio
import curses
import random

from settings import *

def generation_stars(canvas):
    coroutines_stars = []
    max_y, max_x = canvas.getmaxyx()
    rand_yx_original = []
    for n in range(COUNT_STARS):
        while True:
            rand_y = random.randint(1, max_y-2)
            rand_x = random.randint(1, max_x-2)
            if (rand_y, rand_x) not in rand_yx_original:
                rand_yx_original.append((rand_y, rand_x))
                break
        symbol = random.choice('+*.:')
        offset_tics = random.randint(0, 10)
        coroutines_stars.append(blink(canvas, rand_y, rand_x, symbol, offset_tics))
    return coroutines_stars


async def blink(canvas, row, column, symbol='*', offset_tics=0):
    tics_per_second = round(1/(TIC_TIMEOUT*10))*10
    blink_attr_times = [
        {'attr': curses.A_DIM, 'time': 2},
        {'attr': curses.A_NORMAL, 'time': 0.3},
        {'attr': curses.A_BOLD, 'time': 0.5},
        {'attr': curses.A_NORMAL, 'time': 0.3},
    ]

    while True:
        for n in range(offset_tics):
            await asyncio.sleep(0)

        for state in blink_attr_times:
            canvas.addstr(row, column, symbol, state['attr'])
            tics = int(state['time']*tics_per_second)
            for n in range(tics):
                await asyncio.sleep(0)