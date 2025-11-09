import pygame
import random
import sys
import time
import os

pygame.init()

# Window size
WIDTH = 600
HEIGHT = 400
BLOCK = 20

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# ==============================
# HIGH SCORE SYSTEM
# ==============================
HS_FILE = "highscore.txt"

def load_high_score():
    if not os.path.exists(HS_FILE):
        with open(HS_FILE, "w") as f:
            f.write("0")
        return 0
    with open(HS_FILE, "r") as f:
        try:
            return int(f.read().strip())
        except:
            return 0

def save_high_score(new_score):
    with open(HS_FILE, "w") as f:
        f.write(str(new_score))

high_score = load_high_score()
# ==============================


# Load sounds
try:
    eat_sound = pygame.mixer.Sound("eat.mp3")
    gameover_sound = pygame.mixer.Sound("gameover.mp3")
except:
    print("Warning: MP3 loading error. Try WAV if no sound plays.")

# Color themes per level
COLOR_THEMES = [
    ((0, 0, 0), (0, 255, 0), (255, 0, 0)),
    ((20, 10, 40), (0, 200, 255), (255, 150, 0)),
    ((25, 0, 35), (200, 0, 255), (255, 255, 0)),
    ((0, 30, 0), (0, 255, 140), (255, 50, 200)),
    ((40, 10, 0), (255, 100, 30), (0, 255, 255)),
]

def theme_for_level(level):
    return COLOR_THEMES[(level-1) % len(COLOR_THEMES)]

def draw_text(msg, color, x, y):
    text = font.render(msg, True, color)
    window.blit(text, (x, y))


# ===============================
# MAIN MENU
# ===============================
def main_menu():
    global high_score
    while True:
        window.fill((0, 0, 0))
        draw_text("SNAKE GAME", (0, 255, 0), WIDTH//2 - 100, HEIGHT//2 - 80)
        draw_text("Press ENTER to Start", (255, 255, 255), WIDTH//2 - 130, HEIGHT//2 - 10)
        draw_text("Press Q to Quit", (255, 255, 255), WIDTH//2 - 100, HEIGHT//2 + 30)

        draw_text(f"High Score: {high_score}", (255, 215, 0), WIDTH//2 - 100, HEIGHT//2 + 80)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()


# ===============================
# OBSTACLES
# ===============================
def generate_moving_obstacles(num):
    obs = []
    for _ in range(num):
        ox = random.randrange(0, WIDTH - BLOCK, BLOCK)
        oy = random.randrange(0, HEIGHT - BLOCK, BLOCK)

        dx = random.choice([-BLOCK, BLOCK])
        dy = 0 if random.random() < 0.5 else random.choice([-BLOCK, BLOCK])

        obs.append([ox, oy, dx, dy])
    return obs

def move_obstacles(obs):
    for o in obs:
        o[0] += o[2]
        o[1] += o[3]
        if o[0] < 0 or o[0] >= WIDTH:
            o[2] *= -1
        if o[1] < 0 or o[1] >= HEIGHT:
            o[3] *= -1

# ===============================
# SPECIAL FOOD
# ===============================
SPECIAL_TYPES = ["gold", "slow", "levelup"]

def spawn_special_food():
    return [
        random.randrange(0, WIDTH - BLOCK, BLOCK),
        random.randrange(0, HEIGHT - BLOCK, BLOCK),
        random.choice(SPECIAL_TYPES)
    ]

# ===============================
# SNAKE FACE
# ===============================
def draw_snake_head(x, y, dx, dy, color):
    pygame.draw.rect(window, color, [x, y, BLOCK, BLOCK])

    # Eyes
    if dx > 0:  # right
        e1 = (x+12, y+3); e2 = (x+12, y+12)
    elif dx < 0:
        e1 = (x+3, y+3); e2 = (x+3, y+12)
    elif dy > 0:
        e1 = (x+3, y+12); e2 = (x+12, y+12)
    else:
        e1 = (x+3, y+3); e2 = (x+12, y+3)

    pygame.draw.circle(window, (255, 255, 255), e1, 3)
    pygame.draw.circle(window, (255, 255, 255), e2, 3)

    # Tongue
    if random.random() < 0.1:
        if dx > 0: pygame.draw.rect(window, (255, 0, 0), [x+BLOCK, y+8, 6, 4])
        if dx < 0: pygame.draw.rect(window, (255, 0, 0), [x-6, y+8, 6, 4])
        if dy > 0: pygame.draw.rect(window, (255, 0, 0), [x+8, y+BLOCK, 4, 6])
        if dy < 0: pygame.draw.rect(window, (255, 0, 0), [x+8, y-6, 4, 6])

# ===============================
# RESTART MENU
# ===============================
def restart_menu(score):
    global high_score

    if score > high_score:
        high_score = score
        save_high_score(high_score)

    while True:
        window.fill((0, 0, 0))
        draw_text("GAME OVER", (255, 0, 0), WIDTH//2 - 80, HEIGHT//2 - 60)
        draw_text(f"Your Score: {score}", (255, 255, 255), WIDTH//2 - 90, HEIGHT//2 - 10)
        draw_text(f"High Score: {high_score}", (255, 215, 0), WIDTH//2 - 90, HEIGHT//2 + 25)

        draw_text("Press R to Restart", (255, 255, 255), WIDTH//2 - 110, HEIGHT//2 + 70)
        draw_text("Press Q to Quit", (255, 255, 255), WIDTH//2 - 90, HEIGHT//2 + 105)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return True
                if event.key == pygame.K_q: pygame.quit(); sys.exit()


# ===============================
# PAUSE SYSTEM
# ===============================
def pause_game(window_surface):
    paused = True

    # -------------------------------------
    # Capture the current game frame (frozen)
    # -------------------------------------
    frozen_frame = window_surface.copy()

    # First — show "PAUSED" screen
    while paused:
        window.blit(frozen_frame, (0, 0))
        draw_text("GAME PAUSED", (255,255,0), WIDTH//2 - 110, HEIGHT//2 - 20)
        draw_text("Press R to Resume", (255,255,255), WIDTH//2 - 120, HEIGHT//2 + 20)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    paused = False

        clock.tick(5)

    # -------------------------------------
    # Resume Countdown WITHOUT clearing frame
    # -------------------------------------
    for sec in range(3, 0, -1):
        window.blit(frozen_frame, (0, 0))
        draw_text(f"Resuming in {sec}...", (0,255,0), WIDTH//2 - 100, HEIGHT//2 - 20)
        pygame.display.update()
        time.sleep(1)


# ===============================
# MAIN GAME LOOP
# ===============================
def game_loop():
    global high_score

    x = WIDTH//2
    y = HEIGHT//2
    dx = dy = 0

    snake = []
    snake_length = 1

    food_x = random.randrange(0, WIDTH-BLOCK, BLOCK)
    food_y = random.randrange(0, HEIGHT-BLOCK, BLOCK)

    score = 0
    level = 1
    speed = 10

    obstacles = generate_moving_obstacles(level + 2)

    special_food = None
    next_special_time = time.time() + random.randint(7, 12)

    slow_mode_timer = 0

    while True:
        # INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                # MOVE
                if event.key == pygame.K_LEFT and dx==0:
                    dx = -BLOCK; dy = 0
                elif event.key == pygame.K_RIGHT and dx==0:
                    dx = BLOCK; dy = 0
                elif event.key == pygame.K_UP and dy==0:
                    dy = -BLOCK; dx = 0
                elif event.key == pygame.K_DOWN and dy==0:
                    dy = BLOCK; dx = 0

                # PAUSE
                if event.key == pygame.K_p:
                    pause_game()

        x += dx
        y += dy

        # Border death
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            gameover_sound.play(); pygame.time.wait(500)
            return score

        # Theme
        bg, snake_color, food_color = theme_for_level(level)
        window.fill(bg)

        # Move obstacles
        move_obstacles(obstacles)
        for o in obstacles:
            pygame.draw.rect(window, (120,120,120), [o[0], o[1], BLOCK, BLOCK])

        if [x,y] in [o[:2] for o in obstacles]:
            gameover_sound.play(); pygame.time.wait(500)
            return score

        # Normal food
        pygame.draw.rect(window, food_color, [food_x, food_y, BLOCK, BLOCK])

        # Spawn special food
        if special_food is None and time.time() >= next_special_time:
            special_food = spawn_special_food()

        # Draw special food
        if special_food:
            fx, fy, t = special_food
            color = {"gold":(255,215,0),"slow":(0,200,255),"levelup":(255,0,255)}[t]
            pygame.draw.rect(window, color, [fx, fy, BLOCK, BLOCK])

        # Eat special food
        if special_food and x==fx and y==fy:
            eat_sound.play()

            if t == "gold":
                score += 5
                snake_length += 1

            elif t == "slow":
                slow_mode_timer = time.time() + 4

            elif t == "levelup":
                level += 1

            special_food = None
            next_special_time = time.time() + random.randint(7, 12)

        # Snake update
        snake.append([x,y])
        if len(snake) > snake_length: snake.pop(0)

        if [x,y] in snake[:-1]:
            gameover_sound.play(); pygame.time.wait(500)
            return score

        # Draw body
        for i, s in enumerate(snake[:-1]):
            shade = 20 * (i % 5)
            col = (max(0, snake_color[0]-shade),
                   max(0, snake_color[1]-shade),
                   max(0, snake_color[2]-shade))
            pygame.draw.rect(window, col, [s[0], s[1], BLOCK, BLOCK])

        # Draw HEAD with eyes + tongue
        draw_snake_head(x, y, dx, dy, snake_color)

        # Eat food
        if x == food_x and y == food_y:
            eat_sound.play()
            snake_length += 1
            score += 1

            food_x = random.randrange(0, WIDTH-BLOCK, BLOCK)
            food_y = random.randrange(0, HEIGHT-BLOCK, BLOCK)

            level = score//5 + 1
            obstacles = generate_moving_obstacles(level + 2)

        # UI
        draw_text(f"Score: {score}", (255,255,255), 10, 10)
        draw_text(f"High Score: {high_score}", (255,215,0), 10, 40)
        draw_text(f"Level: {level}", (255,255,255), 10, 70)
        draw_text("Press P to Pause", (255,255,255), WIDTH - 200, 10)

        # Speed control
        current_speed = speed + (level-1)*3
        if slow_mode_timer > time.time():
            current_speed = max(5, current_speed//2)

        pygame.display.update()
        clock.tick(current_speed)


# START GAME
main_menu()
while True:
    score = game_loop()
    restart_menu(score)
