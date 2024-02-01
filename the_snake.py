from random import randint
from source.game_objects import Apple, Snail, Snake, Obstacle, Hammer
from source.constants import (BOARD_BACKGROUND_COLOR as B_B_C, RESULT_COLOR,
                              SCREEN_WIDTH, screen, UP, DOWN, LEFT, RIGHT,
                              SCREEN_HEIGHT, RESULT_HEIGHT, rect_game,
                              rect_game_score, rect_speed, rect_bonus)

import pygame as pg

# Инициализация pg:
pg.init()

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

    hammer_timer = 0
    hammer_vision = False

    snake_bonus_timer = 0
    snake_bonus_duration = 20000

    snake = Snake()
    apple = Apple()
    snail = Snail()
    hammer = Hammer()
    obstacle = Obstacle()
    # Делаем заливку игрового поля
    screen.fill(B_B_C, rect_game)
    # Добавляем счетчики очков и бонусов
    score_text = Text(background_rect=rect_game_score)
    speed_text = Text(background_rect=rect_speed)
    score_text.print_text(text=f'Съедено яблок: {snake.length - 1}',
                          text_position=(10, SCREEN_HEIGHT))
    speed_text.print_text(text=f'Ваша скорость: {speed}',
                          text_position=(10,
                                         SCREEN_HEIGHT + RESULT_HEIGHT // 2))
    bonus_text = Text(background_rect=rect_bonus)
    bonus_text.print_text(text='Ваш бонус:',
                          text_position=(SCREEN_WIDTH // 2,
                                         SCREEN_HEIGHT))

    running = True

    obstacle_duration = randint(5000, 25000)
    hammer_duration = randint(5000, 25000)

    while running:
        # Задаем скорость игры
        clock.tick(speed)

        # Рисуем яблоко и улитку
        apple.draw()
        snail.draw()

        # Проверяем нажатие клавиш и делаем ход
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Создание препятствий
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

        # Создание молота
        hammer_timer += speed * 10
        if hammer_timer >= hammer_duration and snake.bonus is not True:
            hammer_vision = not hammer_vision
            hammer_timer = 0
            if hammer_vision:
                hammer.randomize_position(apple_pos=apple.position,
                                          snake_pos=snake.positions,
                                          snail_pos=snail.position,
                                          obstacle_pos=obstacle.position)
                hammer.draw()
            else:
                # screen.fill(B_B_C, hammer.hammer_rect)
                hammer.draw_cell(screen, hammer.position,
                                 B_B_C, B_B_C)
                hammer.position = ()

        # Делаем бонусную голову змеи временной
        if snake.bonus is True:
            snake_bonus_timer += speed * 10
            if snake_bonus_timer >= snake_bonus_duration:
                snake.bonus = False
                snake_bonus_timer = 0
                snake.delete_bonus_head(screen)
                snake.bonus_positions = []
                bonus_text = Text(background_rect=rect_bonus)
                bonus_text.print_text(text='Ваш бонус:',
                                      text_position=(SCREEN_WIDTH // 2,
                                                     SCREEN_HEIGHT))

        # Рисуем змею
        snake.draw(screen)

        # Проверяем съела ли змея молот
        if snake.positions[0] == hammer.position:
            snake.bonus = True
            hammer.randomize_position(apple_pos=apple.position,
                                      snake_pos=snake.positions,
                                      snail_pos=snail.position,
                                      obstacle_pos=obstacle.position)
            # pg.display.update(hammer.hammer_rect)
            screen.fill(B_B_C, hammer.hammer_rect)
            bonus_text = Text(background_rect=rect_bonus)
            bonus_text.print_text(text='Ваш бонус: Молот Тора',
                                  text_position=(SCREEN_WIDTH // 2,
                                                 SCREEN_HEIGHT))

        # Если змея съела яблоко:
        if (snake.positions[0] == apple.position
                or apple.position in snake.bonus_positions):
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
        if (snake.positions[0] == snail.position
                or snail.position in snake.bonus_positions):
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

        # Если бонусная часть змея попала на препятствие:
        if snake.bonus_positions:
            if (snake.bonus_positions[0] in obstacle.position
               or snake.bonus_positions[1] in obstacle.position):
                running = False

        pg.display.update()

    show_result = True
    while show_result:
        clock.tick(speed)
        # Добавляем текст на игровое поле
        game_over_text = Text(background_color=B_B_C,
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
