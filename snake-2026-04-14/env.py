import random
from collections import deque

GRID_SIZE = 15

RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)


class SnakeEnv:
    def __init__(self):
        self.reset()

    def generate_random_position(self):
        return (
            random.randint(0, GRID_SIZE - 1),
            random.randint(0, GRID_SIZE - 1)
        )

    def reset(self):
        self.head = self.generate_random_position()
        self.ekor = self.head
        self.UKURANBRO = 1
        self.snake = deque([self.head])

        self.apel = self.generate_random_position()
        while self.apel in self.snake:
            self.apel = self.generate_random_position()

        self.score = 0
        self.done = False

        return self.get_state()

    def move(self, direction):
        new_pos = (
            self.head[0] + direction[0],
            self.head[1] + direction[1]
        )

        self.snake.appendleft(new_pos)
        self.head = new_pos
        self.ekor = new_pos  # sama kayak di main

    def makan(self):
        self.UKURANBRO += 1
        self.snake.append(self.ekor)
        self.score += 1

    def nabrak(self):
        x, y = self.head

        # tembok
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return True

        # badan sendiri
        if self.head in list(self.snake)[1:]:
            return True

        return False

    def step(self, direction):
        reward = 0

        # jarak lama ke apel
        old_distance = abs(self.head[0] - self.apel[0]) + abs(self.head[1] - self.apel[1])

        self.move(direction)

        # mati
        if self.nabrak():
            self.done = True
            return self.get_state(), -10, True

        # makan
        if self.head == self.apel:
            self.makan()
            reward = 10

            # generate apel baru (kayak di main)
            while True:
                new = self.generate_random_position()
                if new not in self.snake:
                    self.apel = new
                    break
        else:
            self.snake.pop()

        # jarak baru ke apel
        new_distance = abs(self.head[0] - self.apel[0]) + abs(self.head[1] - self.apel[1])

        if new_distance < old_distance:
            reward += 0.1
        else:
            reward -= 0.1

        return self.get_state(), reward, self.done

    def get_state(self):
        head_x, head_y = self.head

        danger_up = self._cek((head_x, head_y - 1))
        danger_down = self._cek((head_x, head_y + 1))
        danger_left = self._cek((head_x - 1, head_y))
        danger_right = self._cek((head_x + 1, head_y))

        food_left = self.apel[0] < head_x
        food_right = self.apel[0] > head_x
        food_up = self.apel[1] < head_y
        food_down = self.apel[1] > head_y

        return [
            int(danger_up),
            int(danger_down),
            int(danger_left),
            int(danger_right),
            int(food_left),
            int(food_right),
            int(food_up),
            int(food_down)
        ]

    def _cek(self, pos):
        x, y = pos

        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return True

        if pos in self.snake:
            return True

        return False