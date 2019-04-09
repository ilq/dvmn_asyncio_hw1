import asyncio

from settings import \
    UP_KEY_CODE,\
    DOWN_KEY_CODE,\
    RIGHT_KEY_CODE,\
    LEFT_KEY_CODE,\
    SPACE_KEY_CODE,\
    ROCKET_FRAME_FILES

from to_draw import get_frames_from_files, draw_frame, get_frame_size

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


async def animate_spaceship(canvas, row, column, frames):
    rows_number, columns_number = canvas.getmaxyx()

    while True:
        for frame in frames:
            draw_frame(canvas, row, column, frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, frame, negative=True)
            last_row, last_column = (row, column)
            frame_rows, frame_columns = get_frame_size(frame)

            rows_direction, columns_direction, space_pressed = read_controls(canvas)

            row += rows_direction
            column += columns_direction

            if row < 1 or row + frame_rows > rows_number - 1:
                row = last_row
            if column < 1 or column + frame_columns > columns_number - 1:
                column = last_column


def generate_spaceship(canvas):
    rocket_frames = get_frames_from_files(ROCKET_FRAME_FILES)
    spacehip_soroutine = animate_spaceship(canvas, 20, 20, rocket_frames)
    return spacehip_soroutine