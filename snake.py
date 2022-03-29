import pygame # 1. pygame 선언
import random
from datetime import datetime, timedelta

pygame.init() # 2. pygame 초기화

# 3. pygame에 사용되는 전역변수 선언
# 사각형의 사이즈를 정하자.
SCREEN_MAX = 600
BLOCK_SIZE = 20
size = [SCREEN_MAX, SCREEN_MAX]
size = [SCREEN_MAX, SCREEN_MAX]
X_MAX = int(SCREEN_MAX / BLOCK_SIZE)
Y_MAX = int(SCREEN_MAX / BLOCK_SIZE)

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
pygame.display.set_caption("Snake Game!")
screen = pygame.display.set_mode(size)

done= False
clock= pygame.time.Clock()
last_moved_time = datetime.now()
score = 0
font = pygame.font.SysFont("arial", 30, True, True)

# 방향키 값을 딕션너리로 설정하여 나중에 비교하는데 사용한다.
KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}

def draw_block(screen, color, position):
    block = pygame.Rect((position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, color, block)

class Snake:
    def __init__(self):
        # 좌표(tuple)를 list자료형으로 저장하여 뱀의 위치를 저장한다.
        self.positions = [(2,0),(1,0),(0,0)]  # 뱀의 위치
        self.direction = ''

    def draw(self):
        # for문을 이용해서 뱀의 위치를 그린다.
        for position in self.positions:
            draw_block(screen, GREEN, position)

    def move(self):
        head_position = self.positions[0]
        x, y = head_position
        if self.direction == 'N':
            # 북쪽방향으로 이동하고 있기 때문에 머리의 북쪽방향에 하나를 추가하고 꼬리를 자른다.
            self.positions = [(x , y - 1)] + self.positions[:-1]
        elif self.direction == 'S':
            # 남쪽방향으로 이동하고 있기 때문에 머리의 남쪽방향에 하나를 추가하고 꼬리를 자른다.
            self.positions = [(x , y + 1)] + self.positions[:-1]
        elif self.direction == 'W':
            # 서쪽방향으로 이동하고 있기 때문에 머리의 서쪽방향에 하나를 추가하고 꼬리를 자른다.
            self.positions = [(x - 1, y)] + self.positions[:-1]
        elif self.direction == 'E':
            # 동쪽방향으로 이동하고 있기 때문에 머리의 동쪽방향에 하나를 추가하고 꼬리를 자른다.
            self.positions = [(x + 1, y)] + self.positions[:-1]

    def grow(self):
        tail_position = self.positions[-1]
        x, y = tail_position
        if self.direction == 'N':
            # 북쪽방향으로 이동하고 있기 때문에 꼬리의 남쪽방향에 하나를 추가한다.
            self.positions.append((x, y + 1))
        elif self.direction == 'S':
            # 남쪽방향으로 이동하고 있기 때문에 꼬리의 북쪽방향에 하나를 추가한다.
            self.positions.append((x, y - 1))
        elif self.direction == 'W':
            # 서쪽방향으로 이동하고 있기 때분에 꾜리의 동쪽방향으로 하나를 추가한다.
            self.positions.append((x + 1, y))
        elif self.direction == 'E':
            # 동쪽방향으로 이동하고 있기 때문에 꼬리의 서쪽방향으로 하나를 추가한다.
            self.positions.append((x - 1, y))


class Apple:
    def __init__(self, position=(5, 5)):
        self.position = position

    def draw(self):
        draw_block(screen, RED, self.position)

# 4. pygame 무한루프
def runGame():
    global done, last_moved_time, score
    #게임 시작 시, 뱀과 사과를 초기화
    snake = Snake()
    apple = Apple()

    while not done:
        # 화면을 흰색으로 지운다.
        clock.tick(60)
        screen.fill(WHITE)
        # display the score.
        text = font.render(f"score = {score}", True, BLUE) 
        screen.blit(text, (20, 0))

        # 방향값을 받아서 이동방향을 결정한다.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:
                    snake.direction = KEY_DIRECTION[event.key]

        # 시간이 경과하면 뱀이 움직이도록한다.
        if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
            snake.move()
            last_moved_time = datetime.now()

        # 뱀이 사과를 먹으면 뱀의 길이가 늘어나도록 한다.
        if snake.positions[0] == apple.position:
            score += 1
            snake.grow()
            apple.position = (random.randint(0, X_MAX - 1), random.randint(0, Y_MAX - 1))

        # 뱀이 자신의 위치과 겹치면 종료한다.
        if snake.positions[0] in snake.positions[1:]:
            done = True

        # 뱀이 경계를 넘어가면 종료한다.
        x,y = snake.positions[0]
        if x in range(0, X_MAX) and y in range(0, Y_MAX) and done != True:
            done = False
        else:
            done = True

        snake.draw()
        apple.draw()
        pygame.display.update()

runGame()
pygame.quit()
