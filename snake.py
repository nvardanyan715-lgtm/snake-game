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
    """Базовый класс для всех игровых объектов.
    
    Содержит общие атрибуты позиции и цвета, а также метод отрисовки.
    """
    
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
        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)  # Обводка для наглядности


class Apple(GameObject):
    """Класс яблока, наследуется от GameObject.
    
    Яблоко появляется в случайной позиции на игровом поле.
    """
    
    def __init__(self):
        """Инициализирует яблоко в случайной позиции."""
        super().__init__((0, 0), RED)
        self.randomize_position()
    
    def randomize_position(self):
        """Устанавливает случайные координаты для яблока.
        
        Координаты генерируются в пределах игрового поля с учётом размера ячейки.
        """
        x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        self.position = (x, y)


class Snake(GameObject):
    """Класс змейки, наследуется от GameObject.
    
    Управляет движением змейки, её ростом, проверкой столкновений и отрисовкой.
    """
    
    def __init__(self):
        """Инициализирует змейку в центре поля с длиной 1 и направлением вправо."""
        # Центр поля
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE
        super().__init__((start_x, start_y), GREEN)
        
        # Тело змейки: список координат всех сегментов
        self.positions = [self.position]
        self.direction = RIGHT  # Начинаем движение вправо
        self.length = 1  # Текущая длина змейки
        self.last = None  # Позиция последнего удалённого сегмента (для затирания)
    
    def get_head_position(self):
        """Возвращает текущую позицию головы змейки.
        
        Returns:
            Кортеж (x, y) с координатами головы
        """
        return self.positions[0]
    
    def move(self):
        """Перемещает змейку на одну клетку в текущем направлении.
        
        Вычисляет новую позицию головы с учётом телепортации через стены.
        Проверяет столкновение с собой и при необходимости сбрасывает змейку.
        Обновляет список позиций и управляет ростом.
        """
        # Получаем текущую голову
        head_x, head_y = self.get_head_position()
        
        # Вычисляем новую позицию головы
        dx, dy = self.direction
        new_x = (head_x + dx * CELL_SIZE) % WINDOW_WIDTH
        new_y = (head_y + dy * CELL_SIZE) % WINDOW_HEIGHT
        new_head = (new_x, new_y)
        
        # Проверка столкновения с собой
        # Пропускаем проверку для первых двух элементов (голова и шея могут временно совпадать)
        if new_head in self.positions[2:]:
            self.reset()
            return
        
        # Вставляем новую голову в начало списка
        self.positions.insert(0, new_head)
        
        # Проверяем, нужно ли удалить последний сегмент
        if len(self.positions) > self.length:
            self.last = self.positions.pop()  # Сохраняем для затирания
        else:
            self.last = None  # Если выросли, последнего сегмента для удаления нет
    
    def reset(self):
        """Сбрасывает змейку в начальное состояние.
        
        Вызывается при столкновении с собой.
        Устанавливает длину 1, начальную позицию и случайное направление.
        """
        self.length = 1
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE
        self.positions = [(start_x, start_y)]
        self.direction = random.choice([RIGHT, LEFT, UP, DOWN])
        self.last = None
    
    def draw(self, screen):
        """Отрисовывает змейку на экране.
        
        Затирает след от последнего удалённого сегмента и рисует все текущие сегменты.
        
        Args:
            screen: Поверхность Pygame для отрисовки
        """
        # Затираем след от удалённого сегмента
        if self.last:
            rect = pygame.Rect(self.last[0], self.last[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        
        # Рисуем все сегменты змейки
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)


def main():
    """Главная функция игры.
    
    Инициализирует окно, создаёт объекты и запускает основной игровой цикл.
    """
    # Настройка окна
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()
    
    # Создание игровых объектов
    snake = Snake()
    apple = Apple()
    
    # Игровой цикл
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Управление с защитой от разворота на 180 градусов
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
        
        # Логика игры
        snake.move()
        
        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1  # Увеличиваем длину
            apple.randomize_position()  # Новое яблоко
            
            # Убедимся, что яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()
        
        # Отрисовка
        # Полностью очищаем экран (для перезапуска или начального состояния)
        # Но чтобы сохранить эффект движения, мы не очищаем полностью каждый кадр,
        # а только затираем след через snake.last
        # Однако при сбросе змейки нужно очистить всё
        if not snake.positions:  # На случай, если нужно
            screen.fill(BOARD_BACKGROUND_COLOR)
        
        apple.draw(screen)
        snake.draw(screen)
        
        # Обновление экрана
        pygame.display.update()
        clock.tick(10)  # 10 FPS для комфортной игры
    
    pygame.quit()


if __name__ == "__main__":
    main()