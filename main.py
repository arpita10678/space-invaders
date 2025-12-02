import pygame
import random
from settings import WIDTH, HEIGHT, FPS
from db import init_db, update_stats, get_high_scores

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE ATTACK")

clock = pygame.time.Clock()

# ---------------------------------------------------------
# COLOR PALETTE — PALETTE 2 (Cyan Midnight Blue + Neon Violet)
# ---------------------------------------------------------
CYAN_BLUE = (0, 170, 255)      # main cyan blue
NEON_VIOLET = (170, 0, 255)    # violet
SHADOW_GLOW = (20, 20, 100)     # soft dark glow
BUTTON_CYAN = (0, 150, 255)    # cyan for hover
WHITE = (255, 255, 255)

# ---------------------------------------------------------
# LOAD ASSETS
# ---------------------------------------------------------
HOMEPAGE = pygame.image.load("assets/bg.png").convert()
HOMEPAGE = pygame.transform.scale(HOMEPAGE, (WIDTH, HEIGHT))

BG = pygame.image.load("assets/bg.png").convert()

SHIP = pygame.image.load("assets/ship.png").convert_alpha()
UFO = pygame.image.load("assets/ufo.png").convert_alpha()
BULLET = pygame.image.load("assets/bullet.png").convert_alpha()

PLANETS = [
    pygame.image.load("assets/planet1.png").convert_alpha(),
    pygame.image.load("assets/planet2.png").convert_alpha(),
    pygame.image.load("assets/planet3.png").convert_alpha(),
    pygame.image.load("assets/planet4.png").convert_alpha(),
]

METEOR = pygame.image.load("assets/meteor.png").convert_alpha()
EXPLOSION = pygame.image.load("assets/explosion.png").convert_alpha()
SMALL_EXPL = pygame.image.load("assets/small_explosion.png").convert_alpha()

# ---------------------------------------------------------
# FONTS
# ---------------------------------------------------------
TITLE_FONT = pygame.font.Font("assets/fonts/PressStart2P.ttf", 58)
BUTTON_FONT = pygame.font.Font("assets/fonts/PressStart2P.ttf", 32)
STAT_FONT = pygame.font.Font("assets/fonts/PressStart2P.ttf", 24)
HUD_FONT = pygame.font.Font("assets/fonts/PressStart2P.ttf", 26)
GAMEOVER_FONT = pygame.font.Font("assets/fonts/PressStart2P.ttf", 72)

# ---------------------------------------------------------
# SCALE GAME SPRITES 
# ---------------------------------------------------------
SHIP = pygame.transform.scale(
    SHIP, (int(85 * 0.99), int(110 * 0.99))
)

UFO = pygame.transform.scale(
    UFO, (int(90 * 1.01), int(60 * 1.01))
)

BULLET = pygame.transform.scale(BULLET, (7.5, 15))
METEOR = pygame.transform.scale(METEOR, (90, 90))

PLANETS = [
    pygame.transform.scale(PLANETS[0], (int(150 * 0.99), int(150 * 0.99))),
    pygame.transform.scale(PLANETS[1], (int(160 * 0.99), int(160 * 0.99))),
    pygame.transform.scale(PLANETS[2], (int(130 * 1.18), int(130 * 1.18))),
    pygame.transform.scale(PLANETS[3], (int(150 * 0.99), int(150 * 0.99))),
]

EXPLOSION = pygame.transform.scale(EXPLOSION, (150, 150))
SMALL_EXPL = pygame.transform.scale(SMALL_EXPL, (80, 80))

# ---------------------------------------------------------
# GAME STATE VARIABLES
# ---------------------------------------------------------
scroll_y = 0
distance_traveled = 0

bullets = []
enemies = []
planets = []
meteors = []
small_explosions = []

ship_explosion = None
score = 0
kills = 0
lives = 3

paused = False
pause_start = 0
invincible = False
inv_timer = 0

# used to avoid planet repetitions
last_planet_used = None

# ---------------------------------------------------------
# FADE SETTINGS
# ---------------------------------------------------------
FADE_DURATION = 800
# ---------------------------------------------------------
# FADE FUNCTION (Smooth screen fade)
# ---------------------------------------------------------
def fade_screen():
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))

    step = int(255 / (FADE_DURATION / 16))

    for alpha in range(0, 255, step):
        fade_surface.set_alpha(alpha)
        WIN.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(16)


# ---------------------------------------------------------
# BUTTON CLASS — white text + cyan neon outline on hover
# ---------------------------------------------------------
class Button:
    def __init__(self, text, y, center_x=None):
        self.text = text
        self.font = BUTTON_FONT
        self.y = y
        self.center_x = center_x if center_x else WIDTH // 2
        self.hovered = False

    def draw(self):
        mx, my = pygame.mouse.get_pos()
        base_surface = self.font.render(self.text, True, WHITE)
        w, h = base_surface.get_size()

        rect = pygame.Rect(self.center_x - w // 2, self.y, w, h)
        self.hovered = rect.collidepoint(mx, my)

        # Hover outline glow (light neon cyan)
        if self.hovered:
            offsets = [
                (-2, 0), (2, 0),
                (0, -2), (0, 2),
                (-2, -2), (2, -2),
                (-2, 2), (2, 2)
            ]
            for ox, oy in offsets:
                glow = self.font.render(self.text, True, BUTTON_CYAN)
                WIN.blit(glow, (self.center_x - w // 2 + ox, self.y + oy))

        WIN.blit(base_surface, (self.center_x - w // 2, self.y))
        return rect


# ---------------------------------------------------------
# PLANET NON-OVERLAP CHECK
# ---------------------------------------------------------
def can_place_planet(new_x, new_y, sprite):
    nw, nh = sprite.get_width(), sprite.get_height()
    new_rect = pygame.Rect(new_x, new_y, nw, nh)

    for px, py, spr in planets:
        pw, ph = spr.get_width(), spr.get_height()
        p_rect = pygame.Rect(px, py, pw, ph)

        # No overlap allowed
        if new_rect.colliderect(p_rect):
            return False

        # No too-close stacking
        if abs(new_x - px) < (nw // 2 + pw // 2 + 100) and abs(new_y - py) < (nh // 2 + ph // 2 + 100):
            return False

    return True


# ---------------------------------------------------------
# UFO COLLISION CHECK
# ---------------------------------------------------------
def ufo_collides_planet(x, y):
    rect = pygame.Rect(x, y, UFO.get_width(), UFO.get_height())
    for p in planets:
        if rect.colliderect(pygame.Rect(p[0], p[1], p[2].get_width(), p[2].get_height())):
            return True
    return False


# ---------------------------------------------------------
# LIFE LOST PAUSE SCREEN
# ---------------------------------------------------------
def start_life_lost_pause(px, py):
    global paused, pause_start, ship_explosion, invincible, inv_timer
    global enemies, meteors, bullets, planets

    paused = True
    pause_start = pygame.time.get_ticks()
    ship_explosion = (px - 30, py - 30)

    invincible = True
    inv_timer = pygame.time.get_ticks()

    enemies = []
    meteors = []
    bullets = []

    clean_planets = []
    ship_rect = pygame.Rect(px, py, SHIP.get_width(), SHIP.get_height())

    for p in planets:
        if not ship_rect.colliderect(pygame.Rect(p[0], p[1], p[2].get_width(), p[2].get_height())):
            clean_planets.append(p)

    planets = clean_planets


def update_pause(px, py):
    global paused
    elapsed = pygame.time.get_ticks() - pause_start

    if elapsed >= 1200:
        paused = False
        return

    WIN.fill((0, 0, 0))

    if ship_explosion:
        WIN.blit(EXPLOSION, ship_explosion)

    if (pygame.time.get_ticks() // 150) % 2 == 0:
        WIN.blit(SHIP, (px, py))

    txt = GAMEOVER_FONT.render("LIFE LOST!", True, (255, 50, 50))
    WIN.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 100))

    pygame.display.update()


# ---------------------------------------------------------
# HOMEPAGE (with neon glow + fade into game)
# ---------------------------------------------------------
def homepage_screen():
    play_btn = Button("PLAY", 360)
    stats_btn = Button("VIEW STATS", 450)

    while True:
        WIN.blit(HOMEPAGE, (0, 0))
        shadow = TITLE_FONT.render("SPACE ATTACK", True, SHADOW_GLOW)
        WIN.blit(shadow, (WIDTH // 2 - shadow.get_width() // 2 + 3, 130 + 3))
        title = TITLE_FONT.render("SPACE ATTACK", True, NEON_VIOLET)
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 130))

        play_rect = play_btn.draw()
        stats_rect = stats_btn.draw()

        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_rect.collidepoint(mx, my):
                    fade_screen()
                    return
                if stats_rect.collidepoint(mx, my):
                    stats_screen()


# ---------------------------------------------------------
# STATS SCREEN (neon cyan + violet)
# ---------------------------------------------------------
def stats_screen():
    back_btn = Button("BACK", 40, center_x=130)
    scores = get_high_scores()
    while True:
        WIN.blit(HOMEPAGE, (0, 0))
        shadow = TITLE_FONT.render("HIGH SCORES", True, SHADOW_GLOW)
        WIN.blit(shadow, (WIDTH // 2 - shadow.get_width() // 2 + 3, 96 + 3))
        header = TITLE_FONT.render("HIGH SCORES", True, NEON_VIOLET)
        WIN.blit(header, (WIDTH // 2 - header.get_width() // 2, 96))
        y = 210
        if scores:
            for s, k in scores[:10]:
                row = STAT_FONT.render(f"SCORE {s}     KILLS {k}", True, CYAN_BLUE)
                WIN.blit(row, (WIDTH // 2 - row.get_width() // 2, y))
                y += 45
        else:
            msg = STAT_FONT.render("NO DATA FOUND", True, CYAN_BLUE)
            WIN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 330))
        back_rect = back_btn.draw()
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back_rect.collidepoint(mx, my):
                    return
# ---------------------------------------------------------
# DRAW GAME WINDOW (HUD + scrolling background)
# ---------------------------------------------------------
def draw_window(px, py):
    global scroll_y

    scroll_y += 2
    if scroll_y >= BG.get_height():
        scroll_y = 0

    # Background loop
    WIN.blit(BG, (0, scroll_y - BG.get_height()))
    WIN.blit(BG, (0, scroll_y))

    # Planets
    for p in planets:
        WIN.blit(p[2], (p[0], p[1]))

    # Meteors
    for m in meteors:
        WIN.blit(METEOR, (m[0], m[1]))

    # UFOs
    for e in enemies:
        WIN.blit(UFO, (e[0], e[1]))

    # Bullets
    for b in bullets:
        WIN.blit(BULLET, (b[0], b[1]))

    # Explosions
    for ex in small_explosions:
        WIN.blit(SMALL_EXPL, (ex[0], ex[1]))

    # Ship blink when invincible
    if not invincible or (pygame.time.get_ticks() // 150) % 2 == 0:
        WIN.blit(SHIP, (px, py))

    # HUD (cyan and purple)
    score_txt = HUD_FONT.render(f"SCORE: {score}", True, CYAN_BLUE)
    lives_txt = HUD_FONT.render(f"LIVES: {lives}", True, NEON_VIOLET)

    WIN.blit(score_txt, (10, 10))
    WIN.blit(lives_txt, (WIDTH - lives_txt.get_width() - 10, 10))

    pygame.display.update()


# ---------------------------------------------------------
# MAIN GAME LOOP
# ---------------------------------------------------------
def main_game():
    global bullets, enemies, meteors, planets, small_explosions
    global score, kills, lives, paused, invincible, distance_traveled, last_planet_used

    bullets = []
    enemies = []
    meteors = []
    planets = []
    small_explosions = []
    score = 0
    kills = 0
    lives = 3
    paused = False
    invincible = False
    distance_traveled = 0
    last_planet_used = None  # IMPORTANT: prevents planet repeats
    # Ship position
    px = WIDTH // 2 - SHIP.get_width() // 2
    py = HEIGHT - 150
    enemy_timer = 0
    meteor_timer = 0
    UFO_AVOID_COOLDOWN = 300
    ufo_avoid_timer = 0

    # -------------------------------
    # GAME LOOP
    # -------------------------------
    while True:
        clock.tick(FPS)
        now = pygame.time.get_ticks()

        # QUIT EVENT
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                update_stats(score, kills)
                return

        # --------------------------------------
        # PAUSE AFTER LIFE LOST
        # --------------------------------------
        if paused:
            update_pause(px, py)

            if not paused:
                if lives <= 0:
                    fade_screen()
                    update_stats(score, kills)
                    result = game_over_screen(score, kills)
                    if result == "RESTART":
                        return "RESTART"
                    return
            continue

        # --------------------------------------
        # SHIP MOVEMENT
        # --------------------------------------
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and px > 0:
            px -= 5
        if keys[pygame.K_RIGHT] and px < WIDTH - SHIP.get_width():
            px += 5

        # Smooth bullet fire
        if keys[pygame.K_SPACE] and len(bullets) < 9:
            bullets.append([px + SHIP.get_width() // 2 - 4, py - 12])

        # --------------------------------------
        # BULLET MOVEMENT
        # --------------------------------------
        for b in bullets[:]:
            b[1] -= 12
            if b[1] < -40:
                bullets.remove(b)

        # --------------------------------------
        # DISTANCE FOR SPAWN TIMING
        # --------------------------------------
        distance_traveled += 2

        # ====================================================
        # PLANET SPAWN — FIXED: NO REPEATING PLANETS
        # ====================================================
        if distance_traveled % random.randint(900, 1600) < 5:

            # Choose planet NOT equal to previous one
            available = [p for p in PLANETS if p != last_planet_used]

            if available:
                sprite = random.choice(available)
            else:
                sprite = random.choice(PLANETS)

            last_planet_used = sprite  # store last used planet

            # Place without overlap
            for i in range(25):
                x = random.randint(80, WIDTH - sprite.get_width() - 80)
                y = random.randint(-350, -200)

                if can_place_planet(x, y, sprite):
                    planets.append([x, y, sprite])
                    break

        # Move planets
        for p in planets[:]:
            p[1] += 2
            if p[1] > HEIGHT + 260:
                planets.remove(p)

        # --------------------------------------
        # UFO SPAWN + MOVEMENT
        # --------------------------------------
        enemy_timer += 1
        if enemy_timer > 135:
            enemies.append([random.randint(60, WIDTH - 100), -80, 0])
            enemy_timer = 0

        for e in enemies[:]:
            ex, ey, drift = e

            # Smooth chase
            if ex < px - 15: ex += 1.5
            elif ex > px + 15: ex -= 1.5
            else: ex += (px - ex) * 0.03

            # Avoid planets
            if now - ufo_avoid_timer < UFO_AVOID_COOLDOWN:
                ex += drift * 1.25
            else:
                if ufo_collides_planet(ex, ey):
                    drift = 1 if random.random() < 0.5 else -1
                    ufo_avoid_timer = now

            # Clamp
            ex = max(40, min(WIDTH - 140, ex))
            ey += 2

            # Remove if off screen
            if ey > HEIGHT:
                enemies.remove(e)
                continue

            e[0], e[1], e[2] = ex, ey, drift

            # Bullet hits UFO
            ufo_rect = pygame.Rect(ex, ey, UFO.get_width(), UFO.get_height())
            for b in bullets[:]:
                if ufo_rect.colliderect(pygame.Rect(b[0], b[1], 10, 20)):
                    small_explosions.append([ex, ey, now])
                    enemies.remove(e)
                    bullets.remove(b)
                    score += 20
                    kills += 1
                    break

        # Remove explosion sprites
        for ex in small_explosions[:]:
            if now - ex[2] > 240:
                small_explosions.remove(ex)

        # --------------------------------------
        # METEOR SPAWN (TOP RIGHT ONLY)
        # --------------------------------------
        meteor_timer += 1
        if meteor_timer > 240:
            meteors.append([WIDTH + 50, random.randint(-120, -40)])
            meteor_timer = 0

        for m in meteors[:]:
            m[0] -= 2.7
            m[1] += 3.2
            if m[1] > HEIGHT + 150:
                meteors.remove(m)

        # Bullet hits meteor
        for m in meteors[:]:
            meteor_rect = pygame.Rect(m[0], m[1], 70, 70)
            for b in bullets[:]:
                if meteor_rect.colliderect(pygame.Rect(b[0], b[1], 10, 20)):
                    meteors.remove(m)
                    bullets.remove(b)
                    score += 10
                    small_explosions.append([m[0], m[1], now])
                    break

        # --------------------------------------
        # INVINCIBILITY TIMEOUT
        # --------------------------------------
        if invincible and now - inv_timer > 1500:
            invincible = False

        # --------------------------------------
        # SHIP COLLISIONS
        # --------------------------------------
        ship_rect = pygame.Rect(px, py, SHIP.get_width(), SHIP.get_height())

        # Meteor collision
        for m in meteors:
            if ship_rect.colliderect(pygame.Rect(m[0], m[1], 70, 70)) and not invincible:
                lives -= 1
                start_life_lost_pause(px, py)
                break

        # Planet collision
        for p in planets:
            if ship_rect.colliderect(pygame.Rect(p[0], p[1], p[2].get_width(), p[2].get_height())) and not invincible:
                lives -= 1
                start_life_lost_pause(px, py)
                break

        # UFO collision
        for ex, ey, drift in enemies:
            if ship_rect.colliderect(pygame.Rect(ex, ey, UFO.get_width(), UFO.get_height())) and not invincible:
                lives -= 1
                start_life_lost_pause(px, py)
                break

        # --------------------------------------
        # DRAW EVERYTHING
        # --------------------------------------
        draw_window(px, py)
# ---------------------------------------------------------
# GAME OVER SCREEN (Neon Palette + Fade In)
# ---------------------------------------------------------
def game_over_screen(final_score, final_kills):

    playagain_btn = Button("RESTART", 430)
    end_btn = Button("END", 520)

    # Fade into game over
    fade_screen()

    while True:
        WIN.blit(HOMEPAGE, (0, 0))

        # Shadow behind "GAME OVER"
        shadow = GAMEOVER_FONT.render("GAME OVER", True, SHADOW_GLOW)
        WIN.blit(shadow, (
            WIDTH // 2 - shadow.get_width() // 2 + 4,
            138 + 4
        ))

        # Neon Violet title
        title = GAMEOVER_FONT.render("GAME OVER", True, NEON_VIOLET)
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 138))

        # Score (Cyan Blue)
        score_txt = HUD_FONT.render(f"SCORE: {final_score}", True, CYAN_BLUE)
        WIN.blit(score_txt, (WIDTH // 2 - score_txt.get_width() // 2, 270))

        # Kills (Neon Violet)
        kills_txt = HUD_FONT.render(f"KILLS: {final_kills}", True, NEON_VIOLET)
        WIN.blit(kills_txt, (WIDTH // 2 - kills_txt.get_width() // 2, 315))

        # Buttons
        again_rect = playagain_btn.draw()
        end_rect = end_btn.draw()

        pygame.display.update()

        # EVENTS
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Restart game
                if again_rect.collidepoint(mx, my):
                    fade_screen()
                    return "RESTART"

                # Exit game
                if end_rect.collidepoint(mx, my):
                    pygame.quit(); exit()


# ---------------------------------------------------------
# MAIN LOOP (Homepage → Game → Restart)
# ---------------------------------------------------------
if __name__ == "__main__":
    init_db()

    while True:
        homepage_screen()
        result = main_game()

        if result == "RESTART":
            continue
