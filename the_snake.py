"""Игра «Змейка» на Pygame."""

from random import randint

import pygame

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

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Цвет неправильной еды:
BAD_FOOD_COLOR = (255, 165, 0)

# Цвет камня:
STONE_COLOR = (128, 128, 128)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """Инициализирует позицию и цвет игрового объекта."""
        if position is None:
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект. Переопределяется в дочерних классах."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Создаёт яблоко и задаёт ему случайную позицию."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class BadFood(GameObject):
    """Класс неправильной еды."""

    def __init__(self):
        """Создаёт неправильную еду и задаёт ей случайную позицию."""
        super().__init__(body_color=BAD_FOOD_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию еды на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовывает неправильную еду на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    """Класс камня-препятствия."""

    def __init__(self):
        """Создаёт камень и задаёт ему случайную позицию."""
        super().__init__(body_color=STONE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию камня на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовывает камень на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self._trail = []

    def update_direction(self):
        """Применяет следующее направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Передвигает змейку на одну ячейку."""
        head = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)

        self._trail = []
        while len(self.positions) > self.length:
            self._trail.append(self.positions.pop())
        self.last = self._trail[-1] if self._trail else None

    def draw(self):
        """Отрисовывает змейку и затирает её след."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        for pos in self._trail:
            last_rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.__init__()


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
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


def move_to_free_cell(obj, occupied):
    """Перемещает объект в свободную клетку.

    Возвращает True, если свободная клетка найдена, иначе False.
    """
    for _ in range(200):
        obj.randomize_position()
        if obj.position not in occupied:
            return True
    return False


def place_all_objects(snake, apple, bad_food, stone):
    """Размещает яблоко, еду и камень на свободных клетках."""
    occupied = set(snake.positions)
    if not move_to_free_cell(apple, occupied):
        return
    occupied.add(apple.position)
    if not move_to_free_cell(bad_food, occupied):
        return
    occupied.add(bad_food.position)
    move_to_free_cell(stone, occupied)


def handle_collisions(snake, apple, bad_food, stone):
    """Обрабатывает все взаимодействия змейки с объектами.

    Возвращает False, если игровое поле заполнено (победа), иначе True.
    """
    head = snake.get_head_position()

    # Съедание обычного яблока — рост на один сегмент:
    if head == apple.position:
        snake.length += 1
        occupied = set(snake.positions) | {
            bad_food.position, stone.position,
        }
        if not move_to_free_cell(apple, occupied):
            return False  # Победа

    # Съедание неправильной еды — уменьшение на один сегмент:
    if head == bad_food.position:
        if snake.length > 1:
            snake.length -= 1
            while len(snake.positions) > snake.length:
                extra = snake.positions.pop()
                snake._trail.append(extra)
                snake.last = extra
        occupied = set(snake.positions) | {
            apple.position, stone.position,
        }
        move_to_free_cell(bad_food, occupied)

    # Столкновение с камнем или самоукус — сброс игры:
    if head == stone.position or head in snake.positions[1:]:
        snake.reset()
        place_all_objects(snake, apple, bad_food, stone)
        screen.fill(BOARD_BACKGROUND_COLOR)

    return True


def main():
    """Запускает основной игровой цикл."""
    pygame.init()

    snake = Snake()
    apple = Apple()
    bad_food = BadFood()
    stone = Stone()

    place_all_objects(snake, apple, bad_food, stone)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if not handle_collisions(snake, apple, bad_food, stone):
            print('Победа! Змейка заполнила всё поле.')
            break

        snake.draw()
        apple.draw()
        bad_food.draw()
        stone.draw()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
