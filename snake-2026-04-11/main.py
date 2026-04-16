# Example file showing a basic pygame "game loop"
import pygame
import random
from collections import deque


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
    def __init__(self):
        self.img = pygame.image.load("graphics/player.png")
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
        FASTERRRRR()
        


def FASTERRRRR():
    global MOVE_DELAY
    MOVE_DELAY = MOVE_DELAY * 95/100


def generate_random_position():
    return (random.randint(0, GRID_SIZE - 1) * CELL_SIZE, random.randint(0, GRID_SIZE - 1) * CELL_SIZE)


def main():

    last_move_time = 0
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    clock = pygame.time.Clock()
    running = True

    bg = pygame.image.load("graphics/background.png")
    player = Player()
    apel = pygame.image.load("graphics/apel.png")

    apel_pos = generate_random_position()

    last_movement = RIGHT
    movement_now = last_movement

    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if keys:= pygame.key.get_pressed():

            if keys[pygame.K_w] and last_movement != DOWN:
                movement_now = UP
            elif keys[pygame.K_s] and last_movement != UP:
                movement_now = DOWN
            elif keys[pygame.K_d] and last_movement != LEFT:
                movement_now = RIGHT
            elif keys[pygame.K_a] and last_movement != RIGHT:
                movement_now = LEFT
        else:
            pass
        
        screen.fill("purple")
        if current_time - last_move_time >= MOVE_DELAY:
            last_movement = movement_now
            # apel_pos = [random.randint(0, 15) * CELL_SIZE, random.randint(0, 15) * CELL_SIZE]
            player.move(movement_now)
            last_move_time = current_time
            if apel_pos == player.head:
                player.makan()
                while True:
                    new = generate_random_position()
                    if new not in player.snake:
                        apel_pos = new
                        break
                

        screen.blit(bg, [0, 0])
        player.update(screen)
        screen.blit(apel, apel_pos)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()