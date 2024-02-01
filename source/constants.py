import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
RESULT_HEIGHT = 50

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (139, 0, 0)

# Цвет змейки
SNAKE_COLOR = (240, 255, 255)
SNAKE_COLOR_2 = (0, 191, 255)

# Цвет препятствия
OBSTACLE_COLOR = (178, 34, 34)

# Цвет поля для ведения счета
RESULT_COLOR = (240, 255, 255)

# Начальная позиция (середина экрана)
START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + RESULT_HEIGHT),
                             0, 32)

# Определение областей
rect_game = pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
rect_game_score = pg.Rect(0,
                          SCREEN_HEIGHT,
                          SCREEN_WIDTH // 2,
                          RESULT_HEIGHT // 2)
rect_speed = pg.Rect(0,
                     SCREEN_HEIGHT + RESULT_HEIGHT // 2,
                     SCREEN_WIDTH,
                     SCREEN_HEIGHT // 2)
rect_bonus = pg.Rect(SCREEN_WIDTH // 2,
                     SCREEN_HEIGHT,
                     SCREEN_WIDTH // 2,
                     RESULT_HEIGHT // 2)
