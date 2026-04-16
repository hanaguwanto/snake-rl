import random
from collections import deque

GRID_SIZE = 10  # 🔥 diperkecil

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

        # spawn apel
        self.apel = self.generate_random_position()
        while self.apel in self.snake:
            self.apel = self.generate_random_position()

        self.score = 0
        self.done = False

        return self.get_state(None)

    def move(self, direction):
        new_pos = (
            self.head[0] + direction[0],
            self.head[1] + direction[1]
        )

        self.snake.appendleft(new_pos)
        self.head = new_pos
        self.ekor = new_pos

    def makan(self):
        self.UKURANBRO += 1
        self.snake.append(self.ekor)
        self.score += 1

    def nabrak(self, lawan=None):
        x, y = self.head

        # tembok
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return True

        # badan sendiri
        if self.head in list(self.snake)[1:]:
            return True

        if lawan:
            # badan lawan
            if self.head in list(lawan.snake)[1:]:
                return True

            # head vs head
            if self.head == lawan.head:
                return True

        return False

    def step(self, direction, lawan):
        reward = 0

        # ===== JARAK =====
        old_food_dist = abs(self.head[0] - self.apel[0]) + abs(self.head[1] - self.apel[1])
        old_player_dist = abs(self.head[0] - lawan.head[0]) + abs(self.head[1] - lawan.head[1])

        # ===== MOVE =====
        self.move(direction)

        # ===== MATI =====
        if self.nabrak(lawan):
            self.done = True
            return self.get_state(lawan), -1000, True

        # ===== MAKAN =====
        if self.head == self.apel:
            self.makan()
            reward += 10

            while True:
                new = self.generate_random_position()
                if new not in self.snake:
                    self.apel = new
                    break
        else:
            self.snake.pop()

        # ===== JARAK BARU =====
        new_food_dist = abs(self.head[0] - self.apel[0]) + abs(self.head[1] - self.apel[1])
        new_player_dist = abs(self.head[0] - lawan.head[0]) + abs(self.head[1] - lawan.head[1])

        # ke apel
        if new_food_dist < old_food_dist:
            reward += 0.1
        else:
            reward -= 0.1

        # 🔥 ke player (AGRESIF)
        if new_player_dist < old_player_dist:
            reward += 0.2
        else:
            reward -= 0.2

        # 💀 bunuh player
        if lawan.head in list(self.snake)[1:]:
            reward += 50

        return self.get_state(lawan), reward, self.done

    def get_state(self, lawan=None):
        head_x, head_y = self.head

        danger_up = self._cek((head_x, head_y - 1), lawan)
        danger_down = self._cek((head_x, head_y + 1), lawan)
        danger_left = self._cek((head_x - 1, head_y), lawan)
        danger_right = self._cek((head_x + 1, head_y), lawan)

        food_left = self.apel[0] < head_x
        food_right = self.apel[0] > head_x
        food_up = self.apel[1] < head_y
        food_down = self.apel[1] > head_y

        # 🔥 HANDLE LAWAN NONE
        if lawan is None:
            player_left = 0
            player_right = 0
            player_up = 0
            player_down = 0
        else:
            player_left = lawan.head[0] < head_x
            player_right = lawan.head[0] > head_x
            player_up = lawan.head[1] < head_y
            player_down = lawan.head[1] > head_y

        return [
            int(danger_up),
            int(danger_down),
            int(danger_left),
            int(danger_right),

            int(food_left),
            int(food_right),
            int(food_up),
            int(food_down),

            int(player_left),
            int(player_right),
            int(player_up),
            int(player_down),
        ]

    def _cek(self, pos, lawan):
        x, y = pos

        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return True

        if pos in self.snake:
            return True

        if lawan and pos in lawan.snake:
            return True

        return False