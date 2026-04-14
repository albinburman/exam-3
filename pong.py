import os
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
import sys

pygame.init()

# Spelarnamn
Player1 = input("Ange namn för lag 1 (vänster/botten): ")
Player2 = input("Ange namn för lag 2 (höger/top): ")

# Fönster
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-LAG PONG")
clock = pygame.time.Clock()

# Färger
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 150, 255)
RED = (255, 80, 80)

# Paddlar
paddle_width, paddle_height = 10, 120
left_paddle = pygame.Rect(20, HEIGHT//2 - 60, paddle_width, paddle_height)
right_paddle = pygame.Rect(WIDTH - 30, HEIGHT//2 - 60, paddle_width, paddle_height)

# Top & bottom paddlar
top_paddle = pygame.Rect(WIDTH//2 - 60, 20, 120, 10)
bottom_paddle = pygame.Rect(WIDTH//2 - 60, HEIGHT - 30, 120, 10)

# Boll
ball = pygame.Rect(WIDTH//2, HEIGHT//2, 20, 20)
ball_speed = [4, 4]
normal_speed = [4, 4]

# Poäng (lag)
score_team_left = 0      # vänster + botten
score_team_right = 0     # höger + top

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

    # Lag 1 – vänster paddel (W/S)
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= 5
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += 5

    # Lag 2 – höger paddel (UP/DOWN)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= 5
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += 5

    # Lag 2 – top paddel (O/P)
    if keys[pygame.K_o] and top_paddle.left > 0:
        top_paddle.x -= 5
    if keys[pygame.K_p] and top_paddle.right < WIDTH:
        top_paddle.x += 5

    # Lag 1 – bottom paddel (V/C)
    if keys[pygame.K_c] and bottom_paddle.left > 0:
        bottom_paddle.x -= 5
    if keys[pygame.K_v] and bottom_paddle.right < WIDTH:
        bottom_paddle.x += 5

    # Bollrörelse
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Poänglogik
    if ball.left <= 0:  # vänster vägg → lag 2 får poäng
        score_team_right += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed = normal_speed.copy()

    if ball.right >= WIDTH:  # höger vägg → lag 1 får poäng
        score_team_left += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed = normal_speed.copy()

    if ball.top <= 0:  # top → lag 1 får poäng
        score_team_left += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed = normal_speed.copy()

    if ball.bottom >= HEIGHT:  # bottom → lag 2 får poäng
        score_team_right += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed = normal_speed.copy()

    # Studs mot paddlar
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed[0] *= -1
        ball_speed[0] *= 1.06
        ball_speed[1] *= 1.06

    if ball.colliderect(top_paddle) or ball.colliderect(bottom_paddle):
        ball_speed[1] *= -1
        ball_speed[0] *= 1.06
        ball_speed[1] *= 1.06

    # Rita allt
    screen.fill((0, 0, 0))

    # Mittlinje
    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 2, y, 4, 10))

    # Paddlar
    pygame.draw.rect(screen, YELLOW, left_paddle)
    pygame.draw.rect(screen, GREEN, right_paddle)
    pygame.draw.rect(screen, BLUE, top_paddle)
    pygame.draw.rect(screen, RED, bottom_paddle)

    # Boll
    pygame.draw.ellipse(screen, WHITE, ball)

    # Poängtext
    score_left_text = font.render(f"{Player1}: {score_team_left}", True, WHITE)
    screen.blit(score_left_text, (20, 20))

    score_right_text = font.render(f"{Player2}: {score_team_right}", True, WHITE)
    screen.blit(score_right_text, (WIDTH - score_right_text.get_width() - 20, 20))

    pygame.display.flip()
    clock.tick(60)