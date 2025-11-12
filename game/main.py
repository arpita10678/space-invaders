import pygame, random
from player import Player
from bullet import Bullet
from meteor import Meteor
from enemy import Enemy
from planet import Planet

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Survival: Deep Space Run")
clock = pygame.time.Clock()
FPS = 60

# --- Load assets ---
bg_img = pygame.image.load("assets/images/background.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
player_img = pygame.image.load("assets/images/player.png").convert_alpha()
meteor_img = pygame.image.load("assets/images/meteor.png").convert_alpha()
enemy_img = pygame.image.load("assets/images/enemy.png").convert_alpha()
bullet_img = pygame.image.load("assets/images/bullet.png").convert_alpha()
planet_img = pygame.image.load("assets/images/planet.png").convert_alpha()
moon_img = pygame.image.load("assets/images/moon.png").convert_alpha()

WHITE, RED = (255,255,255), (255,60,60)

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def game_loop():
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    meteors = pygame.sprite.Group()
    planets = pygame.sprite.Group()

    player = Player(player_img, WIDTH//2, HEIGHT - 100)
    all_sprites.add(player)

    # Add some planets and moons
    for i in range(1):
        p = Planet(planet_img)
        all_sprites.add(p)
        planets.add(p)
    for i in range(1):
        m = Planet(moon_img)
        all_sprites.add(m)
        planets.add(m)

    bg_y1, bg_y2 = 0, -HEIGHT
    bg_speed = 1.5
    meteor_timer, enemy_timer = 0, 0
    score, lives = 0, 3
    running, game_over = True, False

    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                b = Bullet(bullet_img, player.rect.centerx, player.rect.top)
                all_sprites.add(b)
                bullets.add(b)

        if not game_over:
            # Background scroll
            bg_y1 += bg_speed
            bg_y2 += bg_speed
            if bg_y1 >= HEIGHT: bg_y1 = -HEIGHT
            if bg_y2 >= HEIGHT: bg_y2 = -HEIGHT

            # Meteors occasionally
            meteor_timer += 1
            if meteor_timer > 140:
                m = Meteor(meteor_img)
                all_sprites.add(m)
                meteors.add(m)
                meteor_timer = 0

            # Delay alien spawning at start
            enemy_timer += 1
            if enemy_timer > 180 and len(enemies) < 3:  # wait ~3 seconds before first enemies
                e = Enemy(enemy_img)
                all_sprites.add(e)
                enemies.add(e)

            # Update all
            player.update(keys)
            bullets.update()
            meteors.update()
            for e in enemies:
                e.update(player.rect)
            for p in planets:
                p.update()

            # --- Collisions ---
            for e in pygame.sprite.groupcollide(enemies, bullets, True, True):
                score += 20
            for m in pygame.sprite.groupcollide(meteors, bullets, True, True):
                score += 10

            if pygame.sprite.spritecollide(player, enemies, True):
                lives -= 1
            if pygame.sprite.spritecollide(player, meteors, True):
                lives -= 1
            if pygame.sprite.spritecollide(player, planets, False):
                lives -= 1

            if lives <= 0:
                game_over = True

            # Draw everything
            screen.blit(bg_img, (0, bg_y1))
            screen.blit(bg_img, (0, bg_y2))
            all_sprites.draw(screen)
            draw_text(screen, f"Score: {score}", 30, 70, 20)
            draw_text(screen, f"Lives: {lives}", 30, WIDTH - 80, 20)

        else:
            screen.blit(bg_img, (0, 0))
            draw_text(screen, "GAME OVER", 64, WIDTH//2, HEIGHT//2 - 50, RED)
            draw_text(screen, "Press R to Restart or Q to Quit", 36, WIDTH//2, HEIGHT//2 + 20)
            if keys[pygame.K_r]:
                return True
            if keys[pygame.K_q]:
                running = False

        pygame.display.flip()

    return False

restart = True
while restart:
    restart = game_loop()

pygame.quit()
