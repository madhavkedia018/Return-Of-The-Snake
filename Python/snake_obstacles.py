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

# ---------- LOAD SOUNDS ----------
try:
    eat_sound = pygame.mixer.Sound("eat.mp3")
    gameover_sound = pygame.mixer.Sound("gameover.mp3")
except Exception as e:
    print("Error loading MP3s:", e)
# ---------------------------------


# -------------------------------------------------------
# COLOR THEMES (background, snake base shade, food color)
# -------------------------------------------------------
COLOR_THEMES = [
    ((0, 0, 0), (0, 255, 0), (255, 0, 0)),        # Level 1
    ((15, 10, 30), (0, 200, 255), (255, 150, 0)), # Level 2
    ((25, 0, 25), (200, 0, 255), (255, 255, 0)),  # Level 3
    ((0, 20, 0), (0, 255, 120), (255, 50, 200)),  # Level 4
    ((30, 10, 0), (255, 100, 0), (0, 255, 255)),  # Level 5
]

def theme_for_level(level):
    return COLOR_THEMES[(level - 1) % len(COLOR_THEMES)]


def draw_text(msg, color, x, y):
    text = font.render(msg, True, color)
    window.blit(text, (x, y))


def generate_obstacles(num):
    """Generate obstacle blocks"""
    obs = []
    for _ in range(num):
        ox = random.randrange(0, WIDTH - BLOCK, BLOCK)
        oy = random.randrange(0, HEIGHT - BLOCK, BLOCK)
        obs.append([ox, oy])
    return obs


def restart_menu():
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
    dx = dy = 0

    snake = []
    snake_length = 1

    food_x = random.randrange(0, WIDTH - BLOCK, BLOCK)
    food_y = random.randrange(0, HEIGHT - BLOCK, BLOCK)

    score = 0
    level = 1
    speed = 10

    # Obstacles increase each level
    obstacles = generate_obstacles(level + 2)

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

        # Border collision
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            gameover_sound.play()
            pygame.time.wait(500)
            return

        # Theme for this level
        bg_color, snake_color, food_color = theme_for_level(level)
        window.fill(bg_color)

        # Obstacles
        for ox, oy in obstacles:
            pygame.draw.rect(window, (100, 100, 100), [ox, oy, BLOCK, BLOCK])

        # If snake hits obstacle → game over
        if [x, y] in obstacles:
            gameover_sound.play()
            pygame.time.wait(500)
            return

        # Food
        pygame.draw.rect(window, food_color, [food_x, food_y, BLOCK, BLOCK])

        # Snake movement
        snake.append([x, y])
        if len(snake) > snake_length:
            snake.pop(0)

        # Self collision
        if [x, y] in snake[:-1]:
            gameover_sound.play()
            pygame.time.wait(500)
            return

        # Snake Animation (shaded)
        for i, s in enumerate(snake):
            shade = 20 * (i % 5)   # animated gradient shade
            animated_color = (
                max(0, snake_color[0] - shade),
                max(0, snake_color[1] - shade),
                max(0, snake_color[2] - shade),
            )
            pygame.draw.rect(window, animated_color, [s[0], s[1], BLOCK, BLOCK])

        # Eating food
        if x == food_x and y == food_y:
            eat_sound.play()
            snake_length += 1
            score += 1

            # New food
            food_x = random.randrange(0, WIDTH - BLOCK, BLOCK)
            food_y = random.randrange(0, HEIGHT - BLOCK, BLOCK)

            # Level Up
            level = score // 5 + 1
            speed = 10 + (level - 1) * 3

            # New obstacles based on level
            obstacles = generate_obstacles(level + 2)

        # UI
        draw_text(f"Score: {score}", (255, 255, 255), 10, 10)
        draw_text(f"Level: {level}", (255, 255, 255), 10, 40)

        pygame.display.update()
        clock.tick(speed)


# ----------- GAME START -----------
while True:
    game_loop()
    restart_menu()
