from random import randint
from typing import Optional

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_SCREEN = (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 20)
HIGH_SCORE = 0

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
SNAKE_COLOR = (165, 42, 42)

# # Цвет камня
# STONE_COLOR = (128, 128, 128)

# # Цвет отравы
# POISON_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:

    def __init__(self) -> None:
        self.position = CENTER_SCREEN
        self.body_color: Optional[tuple] = None

    def draw(self):
        pass


class Apple(GameObject):

    def __init__(self, snake) -> None:
        super().__init__()
        self.snake = snake
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        while True:
            x_pos = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_pos = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position = (x_pos, y_pos)
            if position not in self.snake.positions:
                self.position = position
                break

    def draw(self):
        rect = (pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):

    def __init__(self, font) -> None:
        super().__init__()
        self.positions: list[tuple] = [self.position]
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.font = font

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        x_head, y_head = self.get_head_position()
        x_shift, y_shift = tuple(
            [coord * GRID_SIZE for coord in self.direction])

        new_head = ((x_head + x_shift) % SCREEN_WIDTH,
                    (y_head + y_shift) % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)

        if new_head in self.positions[2:]:
            self.reset()

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        self.positions.clear()
        self.positions.append(CENTER_SCREEN)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.update_highscore_text()

    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_highscore_text(self):    
        global HIGH_SCORE
        text = self.font.render(f"Highscore: {HIGH_SCORE}", True, (255, 255, 255))
        screen.blit(text, (5, 5))


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
            elif event.key == pygame.K_ESCAPE:
                return True

def main():
    # Инициализация PyGame:
    pygame.init()
    global HIGH_SCORE 
    font = pygame.font.Font(None, 36)
    # text = font.render(f"Highscore: {HIGH_SCORE}", True, (255, 255, 255))
    # screen.blit(text, (5, 5)) 

    
    # Тут нужно создать экземпляры классов.
    snake = Snake(font)
    apple = Apple(snake)

    while True:
        clock.tick(SPEED)
        if handle_keys(snake):  
            running = False  
            break        

        snake.update_direction()
        snake.move()

        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position()
            if snake.length > HIGH_SCORE:
                HIGH_SCORE = snake.length

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()
        
        text = font.render(f"Highscore: {HIGH_SCORE}", True, (255, 255, 255))
        screen.blit(text, (5, 5)) 

        pygame.display.update()

if __name__ == '__main__':
    main()