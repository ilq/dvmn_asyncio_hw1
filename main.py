import time
import asyncio
import curses
import random

TIC_TIMEOUT = 0.01
COUNT_STARS = 100

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258

ROCKET_FRAME_FILES = [
    'frames/rocket_frame_1.txt',
    'frames/rocket_frame_2.txt',
    ] 

def get_frames_from_files(filenames):
    frames = []
    for filename in filenames:
        with open(filename) as f:
            frames.append(''.join(f.readlines()))
    return frames


async def animate_spaceship(canvas, row, column, frames):
    last_frame = ''
    canvas.nodelay(True)
    last_row, last_column = (row, column)
    rows_number, columns_number = canvas.getmaxyx()

    while True:
        for frame in frames:
            draw_frame(canvas, last_row, last_column, last_frame, negative=True)
            draw_frame(canvas, row, column, frame)
            
            last_frame = frame
            last_row, last_column = (row, column)
            frame_rows, frame_columns = get_frame_size(last_frame)
            
            rows_direction, columns_direction, space_pressed = read_controls(canvas)
            
            row += rows_direction
            column += columns_direction

            if  row < 0 or \
                row + frame_rows > rows_number or \
                column < 0 or \
                column + frame_columns > columns_number:
                row, column = (last_row, last_column)
            await asyncio.sleep(0)


def get_frame_size(text):
    """Calculate size of multiline text fragment. Returns pair (rows number, colums number)"""
    
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""
    
    rows_direction = columns_direction = 0
    space_pressed = False
    key_code_to_direction = {
        UP_KEY_CODE: (-1, 0),
        DOWN_KEY_CODE: (1, 0),
        RIGHT_KEY_CODE: (0, 1),
        LEFT_KEY_CODE: (0, -1),
    }

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            break

        if pressed_key_code in key_code_to_direction:
            rows_direction, columns_direction = key_code_to_direction[pressed_key_code]

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True
    
    return rows_direction, columns_direction, space_pressed


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas. Erase text instead of drawing if negative=True is specified."""

    rows_number, columns_number = canvas.getmaxyx()
    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue
        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue
            if column >= columns_number:
                break
            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def blink(canvas, row, column, symbol='*'):
    tic_per_second = round(1/(TIC_TIMEOUT*10))*10
    blink_attr_times = [
        {'attr': curses.A_DIM, 'time': 2},
        {'attr': curses.A_NORMAL, 'time': 0.3},
        {'attr': curses.A_BOLD, 'time': 0.5},
        {'attr': curses.A_NORMAL, 'time': 0.3},
    ]

    while True:
        for n in range(random.randint(0, 1*tic_per_second)):
            await asyncio.sleep(0)

        for state in blink_attr_times:
            canvas.addstr(row, column, symbol, state['attr'])
            tics = int(state['time']*tic_per_second)
            for n in range(tics):
                await asyncio.sleep(0)


def draw_fire(canvas):
    max_y, max_x = canvas.getmaxyx()
    coroutine_fire = fire(canvas, max_y/2, max_x/2, columns_speed=0)
    while True:
        try:
            coroutine_fire.send(None)
            canvas.refresh()
        except StopIteration:
            break
        time.sleep(TIC_TIMEOUT*0.1)


def generation_stars(canvas):
    coroutines_stars = []
    max_y, max_x = canvas.getmaxyx()
    rand_yx_original = []
    for n in range(COUNT_STARS):
        while True:
            rand_y = random.randint(1, max_y-1)
            rand_x = random.randint(1, max_x-1)
            if (rand_y, rand_x) not in rand_yx_original:
                rand_yx_original.append((rand_y, rand_x))
                break
        symbol = random.choice('+*.:')
        coroutines_stars.append(blink(canvas, rand_y, rand_x, symbol))
    return coroutines_stars


def draw(canvas):
    curses.curs_set(False)
    max_y, max_x = canvas.getmaxyx()
    coroutines = []
    

    rocket_frames = get_frames_from_files(ROCKET_FRAME_FILES)
    
    draw_fire(canvas)

    coroutines_stars = generation_stars(canvas)
    coroutine_ship = animate_spaceship(canvas, 20, 20, rocket_frames)
    
    coroutines.extend(coroutines_stars)
    coroutines.append(coroutine_ship)

    while True:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                coroutines.remove(couroutine)
        time.sleep(TIC_TIMEOUT)
        if len(coroutines) == 0:
            break

if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
