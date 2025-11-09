import pygame
import random
import sys

pygame.init()

# Window size
WIDTH = 600
HEIGHT = 400
BLOCK = 20

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

def draw_text(msg, color, x, y):
    text = font.render(msg, True, color)
    window.blit(text, (x, y))

def game_loop():
    x = WIDTH // 2
    y = HEIGHT // 2
    dx = 0
    dy = 0

    snake = []
    snake_length = 1

    food_x = random.randrange(0, WIDTH - BLOCK, BLOCK)
    food_y = random.randrange(0, HEIGHT - BLOCK, BLOCK)

    score = 0
    level = 1
    speed = 10

    while True:
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -BLOCK; dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = BLOCK; dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -BLOCK; dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = BLOCK; dx = 0

        x += dx
        y += dy

        # Border collision → Game over
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            draw_text("Game Over!", (255, 0, 0), WIDTH//2 - 80, HEIGHT//2)
            pygame.display.update()
            pygame.time.wait(1500)
            return

        window.fill((0, 0, 0))

        # Draw food
        pygame.draw.rect(window, (255, 0, 0), [food_x, food_y, BLOCK, BLOCK])

        # Snake movement
        snake.append([x, y])
        if len(snake) > snake_length:
            snake.pop(0)

        # Self collision → Game over
        if [x, y] in snake[:-1]:
            draw_text("Game Over!", (255, 0, 0), WIDTH//2 - 80, HEIGHT//2)
            pygame.display.update()
            pygame.time.wait(1500)
            return

        # Draw snake
        for s in snake:
            pygame.draw.rect(window, (0, 255, 0), [s[0], s[1], BLOCK, BLOCK])

        # Eating food
        if x == food_x and y == food_y:
            snake_length += 1
            score += 1

            # New food
            food_x = random.randrange(0, WIDTH - BLOCK, BLOCK)
            food_y = random.randrange(0, HEIGHT - BLOCK, BLOCK)

            # LEVEL system
            level = score // 5 + 1
            speed = 10 + (level - 1) * 3   # Increase speed every level

        # UI
        draw_text(f"Score: {score}", (255, 255, 255), 10, 10)
        draw_text(f"Level: {level}", (255, 255, 255), 10, 40)

        pygame.display.update()
        clock.tick(speed)  # speed increases with level

# Run
while True:
    game_loop()
