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
    
    fire_coroutine = fire(canvas, max_y / 2, max_x / 2, columns_speed=0)
    stars_coroutines = generate_stars(canvas)

    rocket_frames = get_frames_from_files(ROCKET_FRAME_FILES)
    ship_coroutine = animate_spaceship(canvas, 20, 20, rocket_frames)
    
    coroutines.extend(stars_coroutines)
    coroutines.append(ship_coroutine)
    coroutines.append(fire_coroutine)

    while coroutines:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                coroutines.remove(coroutine)
        time.sleep(TIC_TIMEOUT)


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)

if __name__ == '__main__':
    main()