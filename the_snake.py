from random import randint
from source.game_objects import Apple, Snail, Snake, Obstacle
from source.constants import *

import pygame as pg

# Инициализация pg:
pg.init()

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
rect_game_score = pg.Rect(0, SCREEN_HEIGHT, SCREEN_WIDTH, RESULT_HEIGHT // 2)
rect_speed = pg.Rect(0, SCREEN_HEIGHT + RESULT_HEIGHT // 2,
                     SCREEN_WIDTH, SCREEN_HEIGHT // 2)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Добавляем шрифт
font = pg.font.SysFont('couriernew', 20)

# Загружаем картинку
apple_image = pg.image.load('images/apple.png')
snail_image = pg.image.load('images/snail.png')


class Text():
    """Класс текста"""

    def __init__(self,
                 background_rect,
                 background_color=RESULT_COLOR,
                 color=(0, 0, 0)):
        self.background_rect = background_rect
        self.background_color = background_color
        self.color = color
        screen.fill(self.background_color, self.background_rect)

    def print_text(self, text, text_position):
        """Метод для отрисовки текста"""
        screen.fill(self.background_color, self.background_rect)
        self.text = font.render(text, True, self.color)
        screen.blit(self.text, text_position)

    def print_text_centre(self, text, vert_pos):
        """Метод для отрисовки текста с выравниванием по центру"""
        self.text = font.render(text, True, self.color)
        self.text_rect = self.text.get_rect(center=(SCREEN_WIDTH // 2,
                                            vert_pos))
        screen.blit(self.text, self.text_rect)


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
    # Начальная скорость движения змейки:
    speed = 15
    obstacle_timer = 0
    obstacle_visible = False

    snake = Snake()
    apple = Apple()
    snail = Snail()
    obstacle = Obstacle()
    # Делаем заливку игрового поля
    screen.fill(BOARD_BACKGROUND_COLOR, rect_game)
    # Добавляем счетчики очков
    score_text = Text(background_rect=rect_game_score)
    speed_text = Text(background_rect=rect_speed)
    score_text.print_text(text=f'Съедено яблок: {snake.length - 1}',
                          text_position=(10, SCREEN_HEIGHT))
    speed_text.print_text(text=f'Ваша скорость: {speed}',
                          text_position=(10,
                                         SCREEN_HEIGHT + RESULT_HEIGHT // 2))
    running = True

    while running:
        # Задаем скорость игры
        clock.tick(speed)

        # Время в миллисекундах для появления/исчезновени
        obstacle_duration = randint(5000, 25000)

        # Рисуем яблоко и улитку
        apple.draw()
        snail.draw()

        # Проверяем нажатие клавиш и делаем ход
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Обновление препятствий
        obstacle_timer += speed * 10
        if obstacle_timer >= obstacle_duration:
            obstacle_visible = not obstacle_visible
            obstacle_timer = 0
            if obstacle_visible:
                obstacle.randomize_position(snake_positions=snake.positions,
                                            apple_position=apple.position,
                                            snail_position=snail.position)
                obstacle.draw(screen)
            else:
                obstacle.delete(screen)
                obstacle.position = []

        # Рисуем змею
        snake.draw(screen)

        # Если змея съела яблоко:
        if snake.positions[0] == apple.position:
            # Увеличиваем длину змеи на 1
            snake.length += 1
            # Увеличиваем скорость змеи на 1
            speed += 1
            # Задаем яблоку новые рандомные координаты
            apple.randomize_position(snake.positions)
            # Стираем текущее яблоко
            pg.display.update(apple.apple_rect)
            # Обновляем счет игры
            score_text.print_text(f'Съедено яблок: {snake.length - 1}',
                                  text_position=(10, SCREEN_HEIGHT))
            # Обновляем счетчик скорости
            speed_text.print_text(f'Ваша скорость: {speed}',
                                  text_position=(10, SCREEN_HEIGHT
                                                 + RESULT_HEIGHT // 2))

        # Если змея съела улитку:
        if snake.positions[0] == snail.position:
            # Уменьшаем скорость змеи на 1
            speed -= 1
            # Задаем улитке новые рандомные координаты
            snail.randomize_position(snake.positions)
            # Стираем текущую улитку
            pg.display.update(snail.snail_rect)
            # Обновляем счетчик скорости
            speed_text.print_text(f'Ваша скорость: {speed}',
                                  text_position=(10, SCREEN_HEIGHT
                                                 + RESULT_HEIGHT // 2))

        # Если змея попала на препятствие:
        if snake.positions[0] in obstacle.position:
            # Прерываем игровой цикл и перекидывает на экран выбора действий
            running = False

        pg.display.update()

    show_result = True
    while show_result:
        clock.tick(speed)
        # Добавляем текст на игровое поле
        game_over_text = Text(background_color=BOARD_BACKGROUND_COLOR,
                              background_rect=rect_game,
                              color=(255, 255, 255))
        game_over_text.print_text_centre(text='Game Over',
                                         vert_pos=SCREEN_HEIGHT // 2 - 50)
        game_over_text.print_text_centre(text='Нажмите ESCAPE '
                                         'чтобы выйти из игры',
                                         vert_pos=SCREEN_HEIGHT // 2)
        game_over_text.print_text_centre(text='Нажмите ВВЕРХ '
                                         'чтобы начать новую игру',
                                         vert_pos=SCREEN_HEIGHT // 2 + 50)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    main()
                elif event.key == pg.K_ESCAPE:
                    pg.quit()

        pg.display.update()


if __name__ == '__main__':
    main()
