from to_draw import draw_frame, get_frames_from_files
import asyncio
import random
from settings import COUNT_GARBAGE, GARBAGE_FRAMES
from main import coroutines

async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 1
    offset_start = 20
    for n in range(offset_start):
        await asyncio.sleep(0)

    while row < rows_number-1:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
    canvas.addstr(2, 2, 'O000')
    fill_orbit_with_garbage(canvas)


def get_garbage_coroutine(canvas, columns_number, garbage_frames):
    garbage_frame = random.choice(garbage_frames)
    column = random.randint(1, columns_number - 1)
    return fly_garbage(canvas, column, garbage_frame)

def fill_orbit_with_garbage(canvas):
    garbage_frames = get_frames_from_files(GARBAGE_FRAMES)
    rows_number, columns_number = canvas.getmaxyx()
    garbage_coroutine = get_garbage_coroutine(canvas, columns_number, garbage_frames)
    canvas.addstr(4, 4, str(len(coroutines)))
    coroutines.append(garbage_coroutine)
    canvas.addstr(5, 5, str(len(coroutines)))
    canvas.addstr(3, 3, '0001')


def generate_garbages(canvas):
    garbage_coroutines = []
    garbage_frames = get_frames_from_files(GARBAGE_FRAMES)
    rows_number, columns_number = canvas.getmaxyx()
    for n in range(COUNT_GARBAGE):
        garbage_frame = random.choice(garbage_frames)
        garbage_coroutine = get_garbage_coroutine(canvas, columns_number, garbage_frames)
        garbage_coroutines.append(garbage_coroutine)

    return garbage_coroutines