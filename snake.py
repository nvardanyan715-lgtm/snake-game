"""Игра Змейка на Pygame."""

import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE  # 32
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE  # 24

# Цвета (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BOARD_BACKGROUND_COLOR = BLACK

# Направления
RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position, color):
        """Инициализирует игровой объект.

        Args:
            position: Кортеж (x, y) с координатами верхнего левого угла
            color: Кортеж (r, g, b) с цветом объекта
        """
        self.position = position
        self.color = color

    def draw(self, screen):
        """Отрисовывает объект на экране.

        Args:
            screen: Поверхность Pygame для отрисовки
        """
        rect = pygame.Rect(
            self.position[0], self.position[1], CELL_SIZE, CELL_SIZE
        )
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)


class Apple(GameObject):
    """Класс яблока, наследуется от GameObject."""

    def __init__(self):
        """Инициализирует яблоко в случайной позиции."""
        super().__init__((0, 0), RED)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайные координаты для яблока."""
        x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        self.position = (x, y)


class Snake(GameObject):
    """Класс змейки, наследуется от GameObject."""

    def __init__(self):
        """Инициализирует змейку в центре поля."""
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE
        super().__init__((start_x, start_y), GREEN)

        self.positions = [self.position]
        self.direction = RIGHT
        self.length = 1
        self.last = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку на одну клетку в текущем направлении."""
        head_x, head_y = self.get_head_position()

        dx, dy = self.direction
        new_x = (head_x + dx * CELL_SIZE) % WINDOW_WIDTH
        new_y = (head_y + dy * CELL_SIZE) % WINDOW_HEIGHT
        new_head = (new_x, new_y)

        if new_head in self.positions[2:]:
            self.reset()
            return

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE
        self.positions = [(start_x, start_y)]
        self.direction = random.choice([RIGHT, LEFT, UP, DOWN])
        self.last = None

    def draw(self, screen):
        """Отрисовывает змейку на экране.

        Args:
            screen: Поверхность Pygame для отрисовки
        """
        if self.last:
            rect = pygame.Rect(
                self.last[0], self.last[1], CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

        for position in self.positions:
            rect = pygame.Rect(
                position[0], position[1], CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)


def main():
    """Главная функция игры."""
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
