from to_draw import draw_frame, get_frames_from_files
import asyncio
import random
from settings import COUNT_GARBAGE, GARBAGE_FRAMES
from globalvars import coroutines

deleted_garabages = []

async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 1
    offset_start = random.randint(0, 200)
    for n in range(offset_start):
        await asyncio.sleep(0)

    while row < rows_number-1:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
    canvas.addstr(2, 2, 'O000')
    deleted_garabages.append(True)


def get_garbage_coroutine(canvas, columns_number, garbage_frames):
    garbage_frame = random.choice(garbage_frames)
    column = random.randint(1, columns_number - 1)
    return fly_garbage(canvas, column, garbage_frame)


async def fill_orbit_with_garbage(canvas):
    garbage_frames = get_frames_from_files(GARBAGE_FRAMES)
    rows_number, columns_number = canvas.getmaxyx()
    while True:
        await asyncio.sleep(0)
        if deleted_garabages:
            garbage_coroutine = get_garbage_coroutine(canvas, columns_number, garbage_frames)
            coroutines.append(garbage_coroutine)
            deleted_garabages.pop()


def generate_garbages(canvas):
    garbage_coroutines = []
    garbage_frames = get_frames_from_files(GARBAGE_FRAMES)
    rows_number, columns_number = canvas.getmaxyx()
    for n in range(COUNT_GARBAGE):
        garbage_frame = random.choice(garbage_frames)
        garbage_coroutine = get_garbage_coroutine(canvas, columns_number, garbage_frames)
        garbage_coroutines.append(garbage_coroutine)

    return garbage_coroutines