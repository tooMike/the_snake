from random import choice, randrange

import pygame as pg

# Инициализация pg:
pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)
SNAKE_COLOR_2 = (0, 0, 255)

# Скорость движения змейки:
SPEED = 15

# Начальная позиция (середина экрана)
START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()



class GameObject:
    """Родительский класс"""

    def __init__(self, position=START_POSITION,
                 body_color=APPLE_COLOR, border_color=BORDER_COLOR):
        self.position = position
        self.body_color = body_color
        self.border_color = border_color

    def draw(self):
        """Метод для отрисовки объектов"""
        raise NotImplementedError('Будет реализован в дочерних классах')

    def draw_cell(self, surface, position, body_color=None, border_color=None):
        """Раскрашивание 1 ячейки игрового поля"""
        object_rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, body_color, object_rect)
        pg.draw.rect(surface, border_color, object_rect, 1)


class Snake(GameObject):
    """Класс для описания змейки"""

    def __init__(self, body_color_2=SNAKE_COLOR_2):
        super().__init__(position=START_POSITION, 
                         body_color=SNAKE_COLOR)
        self.reset()
        self.body_color_2 = body_color_2

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для создания движения змейки"""
        head_position = self.get_head_position()
        move_direction = self.direction

        # Вычисляем новые координаты
        dx = (head_position[0] + move_direction[0] * GRID_SIZE) % SCREEN_WIDTH
        dy = (head_position[1] + move_direction[1] * GRID_SIZE) % SCREEN_HEIGHT

        # Добавляем новую координату головы змейки.
        self.positions.insert(0, (dx, dy))

        # Проверяем не укусила ли змея сама себя.
        if (dx, dy) in self.positions[2:]:
            self.reset()

        # Проверяем не съела ли змея яблоко.
        if len(self.positions) > self.length:
            self.last = self.positions.pop(len(self.positions) - 1)

    def get_head_position(self):
        """Метод возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод возвращает характеристики змейки в первоначальным"""
        self.length = 1
        self.positions = [START_POSITION]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self, surface):
        """Метод для отрисовки змейки
        обращаеся к методу draw() родительского класс
        """
        # # Отрисовка ховста змейки.
        # self.draw_cell(surface, self.positions[len(self.positions) - 1],
        #                self.body_color, self.border_color)

        # Отрисовка головы змейки.
        if self.length % 2 == 0:
            self.draw_cell(surface, self.positions[0],
                        self.body_color, self.border_color)
        else:
            self.draw_cell(surface, self.positions[0],
                        self.body_color_2, self.border_color)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Класс для описания яблока"""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self, positions=[START_POSITION]):
        """Генерация рандомной позиции яблока на игровом поле"""
        # определяем допустимый диапозон по ширине и высоте
        position_range_x = SCREEN_WIDTH - GRID_SIZE
        position_range_y = SCREEN_WIDTH - GRID_SIZE
        # Генерируем рандомную позицию
        self.position = (randrange(0, position_range_x, GRID_SIZE),
                         randrange(0, position_range_y, GRID_SIZE))
        # Если она совпала с одной из координат змейки, то генерим новые
        # координаты, пока не попадем мимо змейки
        while self.position in positions:
            self.position = (randrange(0, position_range_x, GRID_SIZE),
                             randrange(0, position_range_y, GRID_SIZE))

    def draw(self, surface):
        """Метод для отрисовки яблока,
        обращаемся к методы draw() родительского класса
        """
        self.draw_cell(surface, (self.position[0], self.position[1]),
                       self.body_color, self.border_color)


def handle_keys(game_object):
    """Функция обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()


def main():
    """Основаня исполнительная функция игры"""
    snake = Snake()
    apple = Apple()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        apple.draw(screen)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw(screen)

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        pg.display.update()


if __name__ == '__main__':
    main()