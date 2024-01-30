from random import choice, randrange, randint
from .constants import *
import pygame as pg

# Загружаем картинку
apple_image = pg.image.load('images/apple.png')
snail_image = pg.image.load('images/snail.png')


class GameObject:
    """Родительский класс"""

    def __init__(self, position=START_POSITION):
        self.position = position

    def draw(self, surface):
        """Метод для отрисовки объектов"""
        raise NotImplementedError('Будет реализован в дочерних классах')

    def draw_cell(self, surface, position, body_color=None, border_color=None):
        """Раскрашивание 1 ячейки игрового поля"""
        object_rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, body_color, object_rect)
        pg.draw.rect(surface, border_color, object_rect, 1)


class Snake(GameObject):
    """Класс для описания змейки"""

    def __init__(self,
                 body_color=SNAKE_COLOR,
                 body_color_2=SNAKE_COLOR_2,
                 border_color=BORDER_COLOR):
        super().__init__(position=START_POSITION)
        self.reset()
        self.body_color_2 = body_color_2
        self.body_color = body_color
        self.border_color = border_color

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
        # Делаем питона двухцветным
        for position in self.positions:
            if self.positions.index(position) % 2 == 0:
                self.draw_cell(surface, position,
                               self.body_color, self.border_color)
            else:
                self.draw_cell(surface, position,
                               self.body_color_2, self.border_color)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Obstacle(GameObject):
    """Класс для препятствий"""

    def __init__(self,
                 body_color=OBSTACLE_COLOR,
                 border_color=BORDER_COLOR):
        super().__init__(position=[])
        self.position = []
        self.body_color = body_color
        self.border_color = border_color

    def randomize_position(self, snake_positions=[START_POSITION],
                           apple_position=[START_POSITION],
                           snail_position=[START_POSITION]):
        """Генерация рандомной позиции препятствия на игровом поле"""
        # определяем допустимый диапозон по ширине и высоте
        self.size = randint(5, 15)
        pos_range_x = SCREEN_WIDTH - GRID_SIZE
        pos_range_y = SCREEN_HEIGHT - GRID_SIZE
        # Генерируем рандомную позицию 1 элемента
        self.position = [(randrange(0, pos_range_x, GRID_SIZE),
                          randrange(0, pos_range_y, GRID_SIZE))]
        # Если она совпала с одной из координат змейки, яблока или улитки,
        # то генерим новые координаты, пока не попадем мимо
        while self.position in snake_positions or \
            self.position in apple_position or \
            self.position in snail_position:
            self.position = [(randrange(0, pos_range_x, GRID_SIZE),
                             randrange(0, pos_range_y, GRID_SIZE))]

        # Генерируем рандомно другие позиции препятствия
        index = 0
        generation_active = True
        while index < self.size - 1 and generation_active:
            position_valid = False
            # Вводим количество попыток генерации координат
            attempt = 0
            while not position_valid and generation_active:
                # Генерируем рандомный следующий шаг
                new_position = choice([-20, 20])
                # Генерируем рандомный выбор оси
                obst_pos_index = choice([0, 1])
                # Записываем координаты предыдущей ячейки
                new_x, new_y = self.position[index]
                # В зависимости от оси прибавляем шаг
                if obst_pos_index:
                    new_x += new_position
                else:
                    new_y += new_position
                # Проверяем, не вышли ли координаты за поле
                if 0 <= new_x <= pos_range_x and 0 <= new_y <= pos_range_y:
                    # Проверяем, не совпадают ли координаты с предыдущими
                    if (new_x, new_y) not in self.position[:index] and \
                          (new_x, new_y) not in snake_positions and \
                          (new_x, new_y) not in [apple_position] and \
                          (new_x, new_y) not in [snail_position]:
                        self.position.append((new_x, new_y))
                        position_valid = True
                attempt += 1
                # Если сделано больше 5 попыток сгенировать координату
                # но координата, удовлетворяющая всем условиям не была
                # найдена, то прерываем цикл
                if attempt >= 15:
                    generation_active = False
            index += 1

    def draw(self, surface):
        """Метод для отрисовки препятствия"""
        for position in self.position:
            self.draw_cell(surface, position,
                           self.body_color, self.border_color)

    def delete(self, surface):
        """Метод для удаления препятствия"""
        for position in self.position:
            self.draw_cell(surface, position,
                           BOARD_BACKGROUND_COLOR, BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Класс для описания яблока"""

    def __init__(self):
        super().__init__()
        self.randomize_position()
        self.apple_size = pg.transform.scale(apple_image, (GRID_SIZE,
                                                           GRID_SIZE))
        self.apple_rect = self.apple_size.get_rect(x=self.position[0],
                                                   y=self.position[1])

    def randomize_position(self, positions=[START_POSITION]):
        """Генерация рандомной позиции яблока на игровом поле"""
        # определяем допустимый диапозон по ширине и высоте
        pos_range_x = SCREEN_WIDTH - GRID_SIZE
        pos_range_y = SCREEN_HEIGHT - GRID_SIZE
        # Генерируем рандомную позицию
        self.position = (randrange(0, pos_range_x, GRID_SIZE),
                         randrange(0, pos_range_y, GRID_SIZE))
        # Если она совпала с одной из координат змейки, то генерим новые
        # координаты, пока не попадем мимо змейки
        while self.position in positions:
            self.position = (randrange(0, pos_range_x, GRID_SIZE),
                             randrange(0, pos_range_y, GRID_SIZE))

    def draw(self):
        """Метод для отрисовки яблока"""
        # Получение прямоугольника с размерами нового изображения
        self.apple_rect = self.apple_size.get_rect(x=self.position[0],
                                                   y=self.position[1])
        screen.blit(self.apple_size, self.apple_rect)


class Snail(GameObject):
    """Класс для описания улитки"""

    def __init__(self):
        super().__init__()
        self.randomize_position()
        self.snail_size = pg.transform.scale(snail_image, (GRID_SIZE,
                                                           GRID_SIZE))
        self.snail_rect = self.snail_size.get_rect(x=self.position[0],
                                                   y=self.position[1])

    def randomize_position(self, positions=[START_POSITION]):
        """Генерация рандомной позиции улитка на игровом поле"""
        # определяем допустимый диапозон по ширине и высоте
        pos_range_x = SCREEN_WIDTH - GRID_SIZE
        pos_range_y = SCREEN_HEIGHT - GRID_SIZE
        # Генерируем рандомную позицию
        self.position = (randrange(0, pos_range_x, GRID_SIZE),
                         randrange(0, pos_range_y, GRID_SIZE))
        # Если она совпала с одной из координат змейки, то генерим новые
        # координаты, пока не попадем мимо змейки
        while self.position in positions:
            self.position = (randrange(0, pos_range_x, GRID_SIZE),
                             randrange(0, pos_range_y, GRID_SIZE))

    def draw(self):
        """Рисуем улитку"""
        self.snail_rect = self.snail_size.get_rect(x=self.position[0],
                                                   y=self.position[1])
        screen.blit(self.snail_size, self.snail_rect)