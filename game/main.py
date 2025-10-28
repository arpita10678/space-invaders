# game/main.py
import pygame, random, sqlite3
from player import Player
from bullet import Bullet
from obstacle import Meteor
from ui import UI

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Survival Shooter")

# Load assets
bg = pygame.image.load("assets/images/background.png").convert()
player_img = pygame.image.load("assets/images/player.png").convert_alpha()
bullet_img = pygame.image.load("assets/images/bullet.png").convert_alpha()
meteor_img = pygame.image.load("assets/images/meteor.png").convert_alpha()

# Groups
player = Player(player_img, 400, 500)
bullets = pygame.sprite.Group()
meteors = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player)

font = pygame.font.Font(None, 36)
ui = UI(font)

clock = pygame.time.Clock()
running = True
spawn_timer = 0

# --- Database setup ---
conn = sqlite3.connect("data/game.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, score INTEGER)")
conn.commit()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shoot bullet
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Bullet(player.rect.centerx, player.rect.top, bullet_img)
            bullets.add(bullet)
            all_sprites.add(bullet)

    keys = pygame.key.get_pressed()
    player.update(keys)

    # Spawn meteors randomly
    spawn_timer += 1
    if spawn_timer > 30:
        meteor = Meteor(meteor_img)
        meteors.add(meteor)
        all_sprites.add(meteor)
        spawn_timer = 0

    # Update bullets & meteors
    bullets.update()
    meteors.update()

    # Collisions
    for bullet in bullets:
        hit_meteors = pygame.sprite.spritecollide(bullet, meteors, True)
        if hit_meteors:
            bullet.kill()
            ui.score += 10

    if pygame.sprite.spritecollide(player, meteors, True):
        ui.lives -= 1
        if ui.lives <= 0:
            c.execute("INSERT INTO scores (score) VALUES (?)", (ui.score,))
            conn.commit()
            running = False

    # Draw everything
    screen.blit(bg, (0, 0))
    all_sprites.draw(screen)
    ui.draw(screen)
    pygame.display.flip()
    clock.tick(60)

conn.close()
pygame.quit()
