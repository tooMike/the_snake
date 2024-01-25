from random import choice, randint, randrange

import pygame

# Инициализация PyGame:
pygame.init()

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

# Скорость движения змейки:
SPEED = 15

# Начальная позиция (середина экрана)
START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, position = START_POSITION, body_color = None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Snake(GameObject):
    def __init__(self):
        super().__init__(position=START_POSITION, body_color=SNAKE_COLOR)
        self.positions = [self.position]
        self.last = None
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    
    # Метод обновления позиции змейки
    def move(self):
        head_position = self.get_head_position()
        move_direction = self.direction

        if move_direction[0]:
            dx = move_direction[0] * GRID_SIZE
            if not 0 <= head_position[0] + dx <= SCREEN_WIDTH - GRID_SIZE:
                dx = abs(SCREEN_WIDTH - abs(head_position[0] + dx))
            else:
                dx = head_position[0] + dx
            dy = head_position[1]
        else:
            dy = move_direction[1] * GRID_SIZE
            if not 0 <= head_position[1] + dy <= SCREEN_HEIGHT - GRID_SIZE:
                dy = abs(SCREEN_HEIGHT - abs(head_position[1] + dy))
            else:
                dy = head_position[1] + dy
            dx = head_position[0]
        
        for position in self.positions[2:]:
            if (dx, dy) == position:
                self.reset()

        self.positions.insert(0, (dx,dy))

        if len(self.positions) > self.length:
            self.last = self.positions.pop(len(self.positions) - 1)

    # Метод возвращает позицию головы змейки (первый элемент в списке positions).
    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length = 1
        self.positions = [START_POSITION]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)

    # Метод draw класса Snake
    def draw(self, surface):
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    def __init__(self):
        super().__init__(position=self.randomize_position(), body_color=APPLE_COLOR)
        self.position = (self.position)

    # Генерация рандомной позиции яблока на игровом поле
    def randomize_position(self):
        position = (randrange(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE),
                    randrange(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE))
        return position

    # Метод draw класса Apple
    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT

def main():
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        apple.draw(screen)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw(screen)

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

        pygame.display.update()

if __name__ == '__main__':
    main()