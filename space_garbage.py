from to_draw import draw_frame, get_frames_from_files
import asyncio
import random
from settings import COUNT_GARBAGE, GARBAGE_FRAMES


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 1

    while row < rows_number-1:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


def generate_garbages(canvas):
    garbage_coroutines = []
    garbage_frames = get_frames_from_files(GARBAGE_FRAMES)
    rows_number, columns_number = canvas.getmaxyx()

    for n in range(COUNT_GARBAGE):
        garbage_frame = random.choice(garbage_frames)
        column = random.randint(1, columns_number-1)
        garbage_coroutines.append(fly_garbage(canvas, column, garbage_frame))

    return garbage_coroutines