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

WHITE   = (255,255,255)
RED     = (255,  0,  0)
GREEN   = (  0,255,  0)
BLUE    = (  0,  0,255)
BLACK   = (  0,  0,  0)

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

# define to draw a line
def draw_line(screen, color, start_position, end_position):
    start_pos = [start_position[0] * BLOCK_SIZE, start_position[1] * BLOCK_SIZE]
    end_pos = [end_position[0] * BLOCK_SIZE, end_position[1] * BLOCK_SIZE]
    width = 1
    pygame.draw.line(screen, color, start_pos, end_pos, width)

# define to draw a circle
def draw_circle(screen, color, position):
    radius = int(BLOCK_SIZE / 2)
    x = position[0] * BLOCK_SIZE + radius
    y = position[1] * BLOCK_SIZE + radius
    pygame.draw.circle(screen, color, [x, y], radius)

# define to draw a triangle
def draw_triangle(screen, color, position):
    pos = [position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE]
    half = int(BLOCK_SIZE/2)
    width = 0 # zero is filled with color
    x = [pos[0] + half, pos[1]]
    y = [pos[0], pos[1] + BLOCK_SIZE]
    z = [pos[0] + BLOCK_SIZE, pos[1] + BLOCK_SIZE]
    pygame.draw.polygon(screen, color, [x, y, z], width)

def draw_triangle_direction(screen, color, position, direction):
    pos = [position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE]
    half = int(BLOCK_SIZE/2)
    width = 0 # zero is filled with color

    if direction == 'N':
        x = [pos[0], pos[1]]
        y = [pos[0] + BLOCK_SIZE, pos[1]]
        z = [pos[0] + half, pos[1] + BLOCK_SIZE]
    elif direction == 'S':
        x = [pos[0] + half, pos[1]]
        y = [pos[0], pos[1] + BLOCK_SIZE]
        z = [pos[0] + BLOCK_SIZE, pos[1] + BLOCK_SIZE]
    elif direction == 'W':
        x = [pos[0], pos[1]]
        y = [pos[0], pos[1] + BLOCK_SIZE]
        z = [pos[0] + BLOCK_SIZE, pos[1] + half]
    elif direction == 'E':
        x = [pos[0] + BLOCK_SIZE, pos[1]]
        y = [pos[0] + BLOCK_SIZE, pos[1] + BLOCK_SIZE]
        z = [pos[0], pos[1] + half]
    else:
        x = [pos[0] + BLOCK_SIZE, pos[1]]
        y = [pos[0] + BLOCK_SIZE, pos[1] + BLOCK_SIZE]
        z = [pos[0], pos[1] + half]
    
    pygame.draw.polygon(screen, color, [x, y, z], width)

class Snake:
    def __init__(self):
        #self.positions = [(2,0),(1,0),(0,0)]
        self.positions = [(3,1),(2,1),(1,1)]
        self.direction = ''

    def draw(self):
        draw_block(screen, RED, self.positions[0])
        for position in self.positions[1:-1]:
            draw_block(screen, GREEN, position)
        diff = [self.positions[-1][0] - self.positions[-2][0], self.positions[-1][1] - self.positions[-2][1]]
        if diff == [0, -1]:
            direction = 'S'
        elif diff == [0, 1]:
            direction = 'N'
        elif diff == [1, 0]:
            direction = 'W'
        elif diff == [-1, 0]:
            direction = 'E'
        else:
            pass
        draw_triangle_direction(screen, BLACK, self.positions[-1], direction)

    def move(self):
        head_position = self.positions[0]
        x, y = head_position

        if self.direction == 'S':
            self.positions = [(x , y + 1)] + self.positions[:-1]
        elif self.direction == 'N':
            self.positions = [(x , y - 1)] + self.positions[:-1]
        elif self.direction == 'W':
            self.positions = [(x - 1, y)] + self.positions[:-1]
        elif self.direction == 'E':
            self.positions = [(x + 1, y)] + self.positions[:-1]

    def grow(self):
        tail_position = self.positions[-1]
        x, y = tail_position

        diff = [self.positions[-1][0] - self.positions[-2][0], self.positions[-1][1] - self.positions[-2][1]]
        if diff == [0, -1]:
            direction = 'S'
        elif diff == [0, 1]:
            direction = 'N'
        elif diff == [1, 0]:
            direction = 'W'
        elif diff == [-1, 0]:
            direction = 'E'
        else:
            pass

        if direction == 'N':
            self.positions.append((x, y + 1))
        elif direction == 'S':
            self.positions.append((x, y - 1))
        elif direction == 'W':
            self.positions.append((x + 1, y))
        elif direction == 'E':
            self.positions.append((x - 1, y))

    def collision(self):
        # self collision.
        if self.positions[0] in self.positions[1:]:
            return True
        else:
            # check out of the boundary.
            x, y = self.positions[0]
            if x in range(1, X_POS_MAX - 1) and y in range(1, Y_POS_MAX - 1):
                return False
            else:
                return True

class Apple:
    def __init__(self, position=(5, 5)):
        self.position = position

    def draw(self):
        #draw_block(screen, RED, self.position)
        draw_circle(screen, RED, self.position)

    def move(self):
        #self.position = (random.randint(0, X_POS_MAX - 1), random.randint(0, Y_POS_MAX - 1))
        self.position = (random.randint(1, X_POS_MAX - 2), random.randint(1, Y_POS_MAX - 2))

def runGame():
    global done, last_moved_time, score
    snake = Snake()
    apple = Apple()

    while not done:
        clock.tick(60)
        # clear screen with white
        screen.fill(WHITE)

        # draw box with red line
        draw_line(screen, RED, [1, 1], [X_POS_MAX - 1, 1])
        draw_line(screen, RED, [1, 1], [1, Y_POS_MAX - 1])
        draw_line(screen, RED, [X_POS_MAX - 1, 1], [X_POS_MAX - 1, Y_POS_MAX - 1])
        draw_line(screen, RED, [1, Y_POS_MAX - 1], [X_POS_MAX - 1, Y_POS_MAX - 1])
        # display the score.
        text = font.render(f"score = {score}", True, BLUE)
        screen.blit(text, (20, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:
                    snake.direction = KEY_DIRECTION[event.key]

        # move the snake.
        if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
            snake.move()
            last_moved_time = datetime.now()

        # check if the snake eats a apple.
        if snake.positions[0] == apple.position:
            score += 1
            snake.grow()
            apple.move()

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
