import pygame
import random
import sys

pygame.init()

# Window settings
WIDTH = 600
HEIGHT = 400
BLOCK = 20

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# --------- SOUND EFFECTS (MP3) ----------
# Make sure eat.mp3 and gameover.mp3 are in the same folder
try:
    eat_sound = pygame.mixer.Sound("eat.mp3")
    gameover_sound = pygame.mixer.Sound("gameover.mp3")
except:
    print("Error loading MP3 sounds. Try converting to WAV if issues occur.")
# ----------------------------------------

def draw_text(msg, color, x, y):
    text = font.render(msg, True, color)
    window.blit(text, (x, y))

def restart_menu():
    """Display restart menu after game over."""
    while True:
        window.fill((0, 0, 0))
        draw_text("GAME OVER", (255, 0, 0), WIDTH//2 - 80, HEIGHT//2 - 40)
        draw_text("Press R to Restart", (255, 255, 255), WIDTH//2 - 110, HEIGHT//2 + 10)
        draw_text("Press Q to Quit", (255, 255, 255), WIDTH//2 - 90, HEIGHT//2 + 45)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

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
        # Event handling
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

        # Border collision
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            gameover_sound.play()
            pygame.time.wait(500)
            return

        window.fill((0, 0, 0))

        # Draw food
        pygame.draw.rect(window, (255, 0, 0), [food_x, food_y, BLOCK, BLOCK])

        # Update snake
        snake.append([x, y])
        if len(snake) > snake_length:
            snake.pop(0)

        # Self-collision
        if [x, y] in snake[:-1]:
            gameover_sound.play()
            pygame.time.wait(500)
            return

        # Draw snake
        for s in snake:
            pygame.draw.rect(window, (0, 255, 0), [s[0], s[1], BLOCK, BLOCK])

        # Eat food
        if x == food_x and y == food_y:
            eat_sound.play()
            snake_length += 1
            score += 1

            food_x = random.randrange(0, WIDTH - BLOCK, BLOCK)
            food_y = random.randrange(0, HEIGHT - BLOCK, BLOCK)

            # Leveling system
            level = score // 5 + 1
            speed = 10 + (level - 1) * 3

        # UI Display
        draw_text(f"Score: {score}", (255, 255, 255), 10, 10)
        draw_text(f"Level: {level}", (255, 255, 255), 10, 40)

        pygame.display.update()
        clock.tick(speed)

# Main program loop
while True:
    game_loop()
    restart_menu()
