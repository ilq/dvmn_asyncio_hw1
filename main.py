import time
import asyncio
import curses
import random
from stars import *
from spaceship import *
from fire import *
from settings import *


def get_frames_from_files(filenames):
    frames = []
    for filename in filenames:
        with open(filename) as f:
            frames.append(f.read())
    return frames


def draw(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.border()
    max_y, max_x = canvas.getmaxyx()
    coroutines = []
    

    rocket_frames = get_frames_from_files(ROCKET_FRAME_FILES)
    
    draw_fire(canvas)

    stars_coroutines = generate_stars(canvas)
    ship_coroutine = animate_spaceship(canvas, 20, 20, rocket_frames)
    
    coroutines.extend(stars_coroutines)
    coroutines.append(ship_coroutine)

    while coroutines:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                coroutines.remove(couroutine)
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)