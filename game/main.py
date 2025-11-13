import pygame, random
from player import Player
from bullet import Bullet
from meteor import Meteor
from enemy import Enemy
from planet import Planet

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Survival")
clock = pygame.time.Clock()
FPS = 60

# Load assets
bg_img = pygame.image.load("assets/images/background.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

player_img = pygame.image.load("assets/images/player.png").convert_alpha()
meteor_img = pygame.image.load("assets/images/meteor.png").convert_alpha()
enemy_img = pygame.image.load("assets/images/enemy.png").convert_alpha()
bullet_img = pygame.image.load("assets/images/bullet.png").convert_alpha()
planet_img = pygame.image.load("assets/images/planet.png").convert_alpha()
moon_img = pygame.image.load("assets/images/moon.png").convert_alpha()

WHITE, RED = (255, 255, 255), (255, 40, 40)

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    surface.blit(surf, rect)

def game_loop():
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    meteors = pygame.sprite.Group()
    planets = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Player sits slightly above bottom center
    player = Player(player_img, WIDTH//2, HEIGHT - 150)
    all_sprites.add(player)

    # Background scroll
    bg_y1, bg_y2 = 0, -HEIGHT
    scroll_speed = 2  # world moving forward

    # Spawn initial planets/moons
    for _ in range(2):
        p = Planet(planet_img)
        all_sprites.add(p)
        planets.add(p)

    for _ in range(2):
        m = Planet(moon_img)
        all_sprites.add(m)
        planets.add(m)

    score, lives = 3, 3
    meteor_timer = 0
    enemy_timer = 0
    running = True
    game_over = False

    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Player fires
            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    b = Bullet(bullet_img, player.rect.centerx, player.rect.top)
                    all_sprites.add(b)
                    bullets.add(b)

        if not game_over:
            # Scroll background
            bg_y1 += scroll_speed
            bg_y2 += scroll_speed
            if bg_y1 >= HEIGHT:
                bg_y1 = -HEIGHT
            if bg_y2 >= HEIGHT:
                bg_y2 = -HEIGHT

            # Spawn meteors occasionally
            meteor_timer += 1
            if meteor_timer > 110:
                m = Meteor(meteor_img)
                all_sprites.add(m)
                meteors.add(m)
                meteor_timer = 0

            # Spawn enemies (delay at start)
            enemy_timer += 1
            if enemy_timer > 180 and len(enemies) < 3:
                e = Enemy(enemy_img)
                all_sprites.add(e)
                enemies.add(e)
                enemy_timer = 0

            # Update objects
            player.update(keys)
            bullets.update()

            for e in enemies:
                e.update(player.rect, scroll_speed)

            for m in meteors:
                m.update(scroll_speed)

            for p in planets:
                p.update(scroll_speed)

            # --- Collisions ---
            # Bullets hit meteors
            for m in pygame.sprite.groupcollide(meteors, bullets, True, True):
                score += 1

            # Bullets hit enemies
            for e in pygame.sprite.groupcollide(enemies, bullets, True, True):
                score += 2

            # Ship hits anything dangerous
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
            draw_text(screen, f"Score: {score}", 30, 80, 30)
            draw_text(screen, f"Lives: {lives}", 30, WIDTH - 80, 30)

        else:
            screen.blit(bg_img, (0, 0))
            draw_text(screen, "GAME OVER", 64, WIDTH//2, HEIGHT//2 - 40, RED)
            draw_text(screen, "Press R to Restart", 36, WIDTH//2, HEIGHT//2 + 20)

            if keys[pygame.K_r]:
                return True

        pygame.display.flip()

    return False

restart = True
while restart:
    restart = game_loop()

pygame.quit()
