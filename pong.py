import os
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import sys

pygame.init()

# Spelarnamn
Player1 = input("Ange namn för spelare 1: ")
Player2 = input("Ange namn för spelare 2: ")

# Fönster
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PING-PONG")
clock = pygame.time.Clock()

# Färger
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Paddlar
paddle_width, paddle_height = 10, 120
left_paddle = pygame.Rect(20, HEIGHT//2 - 60, paddle_width, paddle_height)
right_paddle = pygame.Rect(WIDTH - 30, HEIGHT//2 - 60, paddle_width, paddle_height)

# Boll
ball = pygame.Rect(WIDTH//2, HEIGHT//2, 20, 20)
ball_speed = [4, 4]
normal_speed = [4, 4]

# Poäng
score_left = 0
score_right = 0
font = pygame.font.Font(None, 50)

# Startskärm
game_started = False

# ==========================
#        SPEL-LOOPEN
# ==========================

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = True

    # STARTSKÄRM
    if not game_started:
        screen.fill((0, 0, 0))
        start_text = font.render("Tryck SPACE för att starta", True, WHITE)
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2,
                                 HEIGHT//2 - start_text.get_height()//2))
        pygame.display.flip()
        clock.tick(60)
        continue

    # Tangenttryckningar
    keys = pygame.key.get_pressed()

    # Vänster paddel (W/S)
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= 5
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += 5

    # Höger paddel (UP/DOWN)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= 5
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += 5

    # Bollrörelse
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Studs mot väggar
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] *= -1

    # Studs mot paddlar
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed[0] *= -1
        ball_speed[0] *= 1.06
        ball_speed[1] *= 1.06

    # Poäng
    if ball.left <= 0:
        score_right += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed = normal_speed.copy()

    if ball.right >= WIDTH:
        score_left += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed = normal_speed.copy()

    # Rita allt
    screen.fill((0, 0, 0))

    # Mittlinje
    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 2, y, 4, 10))

    # Paddlar och boll
    pygame.draw.rect(screen, YELLOW, left_paddle)
    pygame.draw.rect(screen, GREEN, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Poängtext vänster spelare
    score_left_text = font.render(f"{Player1}: {score_left}", True, WHITE)
    screen.blit(score_left_text, (20, 20))

    # Poängtext höger spelare
    score_right_text = font.render(f"{Player2}: {score_right}", True, WHITE)
    screen.blit(score_right_text, (WIDTH - score_right_text.get_width() - 20, 20))

    pygame.display.flip()
    clock.tick(60)