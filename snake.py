# import modules
import pygame
import random
from datetime import datetime, timedelta

pygame.init() # initialize pygame

# declaration for pygame
SCREEN_SIZE_MAX = 600
BLOCK_SIZE = 20
X_POS_MAX = int(SCREEN_SIZE_MAX / BLOCK_SIZE)
Y_POS_MAX = int(SCREEN_SIZE_MAX / BLOCK_SIZE)

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0, 0, 0)

pygame.display.set_caption("Snake Game!")
screen = pygame.display.set_mode((SCREEN_SIZE_MAX, SCREEN_SIZE_MAX))

done= False
score = 0
clock= pygame.time.Clock()
last_moved_time = datetime.now()
font = pygame.font.SysFont("arial", 20, True, True)

# define a dictionary for directions.
KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}

# define to draw a block.
def draw_block(screen, color, position):
    block = pygame.Rect((position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, color, block)

class Snake:
    def __init__(self):
        self.positions = [(2,0),(1,0),(0,0)]
        self.direction = ''

    def draw(self):
        draw_block(screen, RED, self.positions[0])
        for position in self.positions[1:-1]:
            draw_block(screen, GREEN, position)
        draw_block(screen, BLACK, self.positions[-1])

    def move(self):
        head_position = self.positions[0]
        x, y = head_position
        if self.direction == 'N':
            self.positions = [(x , y - 1)] + self.positions[:-1]
        elif self.direction == 'S':
            self.positions = [(x , y + 1)] + self.positions[:-1]
        elif self.direction == 'W':
            self.positions = [(x - 1, y)] + self.positions[:-1]
        elif self.direction == 'E':
            self.positions = [(x + 1, y)] + self.positions[:-1]

    def grow(self):
        tail_position = self.positions[-1]
        x, y = tail_position
        if self.direction == 'N':
            self.positions.append((x, y + 1))
        elif self.direction == 'S':
            self.positions.append((x, y - 1))
        elif self.direction == 'W':
            self.positions.append((x + 1, y))
        elif self.direction == 'E':
            self.positions.append((x - 1, y))

    def collision(self):
        # self collision.
        if self.positions[0] in self.positions[1:]:
            return True
        else:
            # check out of the boundary.
            x, y = self.positions[0]
            if x in range(0, X_POS_MAX) and y in range(0, Y_POS_MAX):
                return False
            else:
                return True

class Apple:
    def __init__(self, position=(5, 5)):
        self.position = position

    def draw(self):
        draw_block(screen, RED, self.position)

def runGame():
    global done, last_moved_time, score
    snake = Snake()
    apple = Apple()

    while not done:
        clock.tick(60)
        screen.fill(WHITE)
        # display the score.
        text = font.render(f"score = {score}", True, BLUE)
        screen.blit(text, (20, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:
                    snake.direction = KEY_DIRECTION[event.key]

        if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
            snake.move()
            last_moved_time = datetime.now()

        if snake.positions[0] == apple.position:
            score += 1
            snake.grow()
            apple.position = (random.randint(0, X_POS_MAX - 1), random.randint(0, Y_POS_MAX - 1))

        # check a collision
        if snake.collision():
            done = True
        else:
            done = False

        snake.draw()
        apple.draw()
        pygame.display.update()

runGame()
pygame.quit()
