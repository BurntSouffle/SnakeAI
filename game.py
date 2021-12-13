import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np


pygame.init()
font = pygame.font.Font('arial.ttf', 25)


# reset game
# reward
# play(action) -> direction
# is_collision

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
BlOCK_SIZE = 20


class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.speed = 10
        self.reset()

    def reset(self):
        # innit display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # innit game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head, Point(self.head.x - BlOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BlOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.fram_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w - BlOCK_SIZE) // BlOCK_SIZE) * BlOCK_SIZE
        y = random.randint(0, (self.h - BlOCK_SIZE) // BlOCK_SIZE) * BlOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.fram_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move(action)  # update head
        self.snake.insert(0, self.head)

        # 3. check if game is over
        reward = -1
        game_over = False
        if self.is_collision() or self.fram_iteration > 100 * len(self.snake):
            game_over = True
            reward = -100
            return reward, game_over, self.score
        # 4. place new food or move
        if self.head == self.food:
            self.score += 1
            reward = 10000
            self._place_food()
            self._increase_speed()
        else:
            self.snake.pop()

        # 5. update UI and clock
        self._update_ui()
        self.clock.tick(self.speed)

        # 6. return game over and score
        return reward, game_over, self.score

    def _increase_speed(self):
        self.speed = self.speed * 1.01

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BlOCK_SIZE or pt.x < 0 or pt.y > self.h - BlOCK_SIZE or pt.y < 0:
            print("Boundary hit!")
            return True

        # Boundryless game
        # if self.head.x > self.w:
        #     self.head = Point(0, self.head.y)
        # elif self.head.x < 0:
        #     self.head = Point(self.w, self.head.y)
        # elif self.head.y > self.h:
        #     self.head = Point(self.head.x, 0)
        # elif self.head.y < 0:
        #     self.head = Point(self.head.x, self.h)

        # hits itself
        if pt in self.snake[1:]:
            print("You ate yourself")
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BlOCK_SIZE, BlOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BlOCK_SIZE, BlOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # [straight, right turn, left turn]
        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockwise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clockwise[idx] #straight
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clockwise[next_idx] #turn right
        else: #[0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clockwise[next_idx]  # turn left

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BlOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BlOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BlOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BlOCK_SIZE

        self.head = Point(x, y)
        print(self.head)
        print(self.snake)

