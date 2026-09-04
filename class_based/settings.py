# Constant
WIN_WIDTH: int = 800
WIN_HEIGHT: int = int(0.8 * WIN_WIDTH)
# gravity
GRAVITY: float = 0.75
# Define number of rows and columns
ROWS: int = 16
COLS: int = 150
# Tile Size
TILE_SIZE: int = WIN_HEIGHT // ROWS
# Tile types
TILE_TYPES: int = 21
# Frames per second
FPS: int = 60
# Define color (Strict Tuple Hinting)
BG: tuple[int, int, int] = (144, 201, 120)
RED: tuple[int, int, int] = (255, 0, 0)
GREEN: tuple[int, int, int] = (0, 255, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0)
