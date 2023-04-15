import pygame, random, time
from pygame.locals import *

import pygame, random, time
from pygame.locals import *

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

TAMANHO_COBRA = 30
TAMANHO_HORIZONTAL = 30
TAMANHO_VERTICAL = 20

EXPLOSAO_QUANTIDADE = 100
EXPLOSAO_RAIO_HORIZONTAL = 30
EXPLOSAO_RAIO_VERITCAL = 15
EXPLOSAO_TAMANHO = 3
EXPLOSAO_GRAVIDADE_POR_PESO = 2
EXPLOSAO_CHANCE_DIMINUIR_TAMANHO = 20
EXPLOSAO_GRAVIDADE = 4

VELOCIDADE_INICIAL = 12
VELOCIDADE_INCREMENTO = 0.01

efect = []

def on_grid_random():
    x = random.randint(0,TAMANHO_HORIZONTAL-1)
    y = random.randint(0,TAMANHO_VERTICAL-1)
    return (x, y)

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

def test_death(s):
    for pos in s[1:]:
        if collision(snake[0], pos):
            return True

pygame.init()
screen = pygame.display.set_mode((TAMANHO_HORIZONTAL*TAMANHO_COBRA,TAMANHO_VERTICAL*TAMANHO_COBRA))
pygame.display.set_caption('COBRA GAY')

clock = pygame.time.Clock()


color = (255,255,255) 
color_light = (170,170,170) 
color_dark = (100,100,100) 
width = screen.get_width() 
height = screen.get_height() 
smallfont = pygame.font.SysFont('Corbel',35) 
menu = True

while True:
    snake = [(3, 3),(4, 3),(5, 3)]
    snake_skin = pygame.Surface((TAMANHO_COBRA,TAMANHO_COBRA))
    snake_skin.fill((255,215,0))

    apple_pos = on_grid_random()
    apple = pygame.Surface((TAMANHO_COBRA,TAMANHO_COBRA))
    apple.fill((255,0,0))

    my_direction = LEFT

    while True:
        clock.tick(VELOCIDADE_INICIAL)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_UP and my_direction != DOWN:
                    my_direction = UP
                if event.key == K_DOWN and my_direction != UP:
                    my_direction = DOWN
                if event.key == K_LEFT and my_direction != RIGHT:
                    my_direction = LEFT
                if event.key == K_RIGHT and my_direction != LEFT:
                    my_direction = RIGHT

        if collision(snake[0], apple_pos):
            for i in range(EXPLOSAO_QUANTIDADE):
                efect.append([apple_pos[0]*TAMANHO_COBRA,apple_pos[1]*TAMANHO_COBRA, random.randint((EXPLOSAO_RAIO_HORIZONTAL/2)*-1,EXPLOSAO_RAIO_HORIZONTAL/2), random.randint(0,EXPLOSAO_RAIO_VERITCAL), random.randint(1,EXPLOSAO_TAMANHO),[255,random.randint(0,255),0]])

            VELOCIDADE_INICIAL += VELOCIDADE_INCREMENTO

            apple_pos = on_grid_random()
            snake.append((0,0))

        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i-1][0], snake[i-1][1])

        if my_direction == UP:
            if(snake[0][1] == 0):
                snake[0] = (snake[0][0], TAMANHO_VERTICAL-1)
            else:
                snake[0] = (snake[0][0], snake[0][1] - 1)

        if my_direction == DOWN:
            if(snake[0][1] == TAMANHO_VERTICAL-1):
                snake[0] = (snake[0][0], 0)
            else:
                snake[0] = (snake[0][0], snake[0][1] + 1)
        if my_direction == RIGHT:
            if(snake[0][0] == TAMANHO_HORIZONTAL-1):
                snake[0] = (0, snake[0][1])
            else:
                snake[0] = (snake[0][0] + 1, snake[0][1])
        if my_direction == LEFT:
            if(snake[0][0] == 0):
                snake[0] = (TAMANHO_HORIZONTAL-1, snake[0][1])
            else:
                snake[0] = (snake[0][0] - 1, snake[0][1])

        screen.fill((0,0,0))
        screen.blit(apple, [apple_pos[0]*TAMANHO_COBRA,apple_pos[1]*TAMANHO_COBRA])
        
                
        for pos in snake:
            screen.blit(snake_skin,[pos[0]*TAMANHO_COBRA,pos[1]*TAMANHO_COBRA])

        for e in efect:
            if(e[1] > TAMANHO_VERTICAL*TAMANHO_COBRA or e[4] == 0):
                efect.remove(e)
                continue
            fagulha = pygame.Surface((e[4],e[4]))
            fagulha.fill(e[5])
            screen.blit(fagulha,[e[0],e[1]])
            e[0] -= e[2]
            e[1] -= e[3]
            e[3] -= EXPLOSAO_GRAVIDADE + (e[4] / EXPLOSAO_GRAVIDADE_POR_PESO)
            if(random.randint(0,100) >= 0 and random.randint(0,100) <= EXPLOSAO_CHANCE_DIMINUIR_TAMANHO):
                e[4] -= 1
        if(test_death(snake)):
            screen.fill((255,0,0))
            pygame.display.update()
            time.sleep(0.2)
            break

        pygame.display.update()