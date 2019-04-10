import time
import curses
from stars import *
from spaceship import *
from fire import *
from settings import *
import space_garbage

# canvas.addstr(4, 2, str(len(coroutines)))

from globalvars import coroutines

def draw(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)
    max_y, max_x = canvas.getmaxyx()

    fire_coroutine = fire(canvas, max_y / 2, max_x / 2, columns_speed=0)
    stars_coroutines = generate_stars(canvas)
    ship_coroutine = generate_spaceship(canvas)
    garbage_coroutines = space_garbage.generate_garbages(canvas)
    fill_orbit_coroutine = space_garbage.fill_orbit_with_garbage(canvas)

    coroutines.extend(stars_coroutines)
    coroutines.append(ship_coroutine)
    coroutines.append(fire_coroutine)
    coroutines.append(fill_orbit_coroutine)
    coroutines.extend(garbage_coroutines)

    while coroutines:
        for coroutine in coroutines:
            canvas.border()
            try:
                coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                coroutines.remove(coroutine)
                break
            except (SystemExit, KeyboardInterrupt):
                exit(0)
        time.sleep(TIC_TIMEOUT)


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)

if __name__ == '__main__':
    main()