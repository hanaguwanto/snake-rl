# Example file showing a basic pygame "game loop"
import pygame
import random
from collections import deque
import torch
import torch.nn as nn

GRID_SIZE = 15
CELL_SIZE = 32
WINDOW_SIZE = 480
MOVE_DELAY = 1000

RIGHT = [1 * CELL_SIZE, 0]
LEFT = [-1 * CELL_SIZE, 0]
UP = [0, -1 * CELL_SIZE]
DOWN = [0, 1 * CELL_SIZE]


class Trail:
    def __init__(self, timeout):
        self.timeout = timeout
        self.img = pygame.image.load("graphics/player.png")

    # def update()

class Player:
    def __init__(self, img="player.png"):
        self.img = pygame.image.load(f"{img}")
        self.rect = self.img.get_rect()
        self.head = self.generate_random_position()
        self.ekor = self.head
        self.UKURANBRO = 1
        self.snake = deque(
            [self.head]
            )
        self.rectimg = pygame.Rect(self.head[0]+1, self.head[1]+1, CELL_SIZE-2, CELL_SIZE-2)

    def generate_random_position(self):
        return (random.randint(3, GRID_SIZE - 3) * CELL_SIZE, random.randint(3, GRID_SIZE - 3) * CELL_SIZE)

    def update(self, screen):
        pygame.draw.rect(screen, "purple", self.rectimg)
        for pos in self.snake:
            screen.blit(self.img, pos)

    def move(self, dir):
        new_pos = (self.head[0] + dir[0], self.head[1] + dir[1])
        self.snake.appendleft(new_pos)
        self.snake.pop()
        self.head = new_pos
        self.ekor = new_pos
        self.rectimg = pygame.Rect(self.head[0]+1, self.head[1]+1, CELL_SIZE-2, CELL_SIZE-2)

    def makan(self):
        self.UKURANBRO += 1
        self.snake.append(self.ekor)

    def nabrak(self):
        x, y = self.head
        if x < 0 or x >= WINDOW_SIZE or y < 0 or y >= WINDOW_SIZE:
            return True
        if self.head in list(self.snake)[1:]:
            return True
        return False

    def reset(self):
        self.head = self.generate_random_position()
        self.snake = deque([self.head])
        self.ekor = self.head
        self.UKURANBRO = 1
        self.rectimg = pygame.Rect(self.head[0]+1, self.head[1]+1, CELL_SIZE-2, CELL_SIZE-2)


class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(8, 128),
            nn.ReLU(),
            nn.Linear(128, 4)
        )

    def forward(self, x):
        return self.net(x)
    

# ================= HELPER AI =================
def pixel_to_grid(pos):
    return (pos[0] // CELL_SIZE, pos[1] // CELL_SIZE)


def get_state(player, apel):
    head_x, head_y = pixel_to_grid(player.head)
    apple_x, apple_y = pixel_to_grid(apel)

    def cek(pos):
        x, y = pos
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return True

        for s in player.snake:
            if pixel_to_grid(s) == pos:
                return True

        return False

    danger_up = cek((head_x, head_y - 1))
    danger_down = cek((head_x, head_y + 1))
    danger_left = cek((head_x - 1, head_y))
    danger_right = cek((head_x + 1, head_y))

    food_left = apple_x < head_x
    food_right = apple_x > head_x
    food_up = apple_y < head_y
    food_down = apple_y > head_y

    return torch.tensor([
        int(danger_up),
        int(danger_down),
        int(danger_left),
        int(danger_right),
        int(food_left),
        int(food_right),
        int(food_up),
        int(food_down)
    ], dtype=torch.float)


def action_to_direction(action):
    if action == 0:
        return UP
    elif action == 1:
        return DOWN
    elif action == 2:
        return LEFT
    elif action == 3:
        return RIGHT

# ================= FUNGSINYA CLARAAAA =================
def FASTERRRRR():
    global MOVE_DELAY
    MOVE_DELAY = MOVE_DELAY * 0.95


def generate_random_position():
    return (random.randint(0, GRID_SIZE - 1) * CELL_SIZE,
            random.randint(0, GRID_SIZE - 1) * CELL_SIZE)

# main
def main():
    last_move_time = 0
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    clock = pygame.time.Clock()
    running = True

    bg = pygame.image.load("graphics/background.png")
    apel_img = pygame.image.load("graphics/apel.png")

    # load AI
    model = DQN()
    model.load_state_dict(torch.load("model.pth"))
    model.eval()

    player = Player("graphics/player.png")
    ai = Player("graphics/ai.png")

    apel_pos = generate_random_position()

    last_movement = RIGHT
    movement_now = last_movement

    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if keys := pygame.key.get_pressed():
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and last_movement != DOWN:
                movement_now = UP
            elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and last_movement != UP:
                movement_now = DOWN
            elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and last_movement != LEFT:
                movement_now = RIGHT
            elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and last_movement != RIGHT:
                movement_now = LEFT
        else:
            pass

        screen.fill("purple")
        if current_time - last_move_time >= MOVE_DELAY:
            last_movement = movement_now

            # PLAYER MOVE
            player.move(movement_now)
            if player.nabrak():
                print("PLAYER GAME OVER")
                break

            # AI MOVE
            state = get_state(ai, apel_pos)
            with torch.no_grad():
                action = torch.argmax(model(state)).item()

            ai_dir = action_to_direction(action)
            ai.move(ai_dir)

            if ai.nabrak():
                print("AI GAME OVER")

            # makan
            for p in [player, ai]:
                if p.head == apel_pos:
                    p.makan()
                    while True:
                        new = generate_random_position()
                        if new not in player.snake and new not in ai.snake:
                            apel_pos = new
                            break

            last_move_time = current_time

        # DRAW
        screen.blit(bg, [0, 0])
        player.update(screen)
        ai.update(screen)
        screen.blit(apel_img, apel_pos)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()