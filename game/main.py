import pygame
import random
from player import Player
from meteor import Meteor
from bullet import Bullet

pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Survival Shooter")
clock = pygame.time.Clock()
FPS = 60

# --- Assets ---
bg_img = pygame.image.load("assets/images/background.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

player_img = pygame.image.load("assets/images/player.png").convert_alpha()
meteor_img = pygame.image.load("assets/images/meteor.png").convert_alpha()
bullet_img = pygame.image.load("assets/images/bullet.png").convert_alpha()

# --- Colors ---
WHITE = (255, 255, 255)
RED = (255, 60, 60)

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# --- Game Loop ---
def game_loop():
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    meteors = pygame.sprite.Group()

    player = Player(player_img, WIDTH // 2, HEIGHT - 100)
    all_sprites.add(player)

    for _ in range(6):
        meteor = Meteor(meteor_img)
        all_sprites.add(meteor)
        meteors.add(meteor)

    score = 0
    lives = 3
    running = True
    game_over = False

    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(bullet_img, player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        if not game_over:
            # --- Update ---
            player.update(keys)
            meteors.update()
            bullets.update()

            # --- Collisions ---
            # Bullets hit meteors
            hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
            for _ in hits:
                score += 10
                m = Meteor(meteor_img)
                all_sprites.add(m)
                meteors.add(m)

            # Meteors hit player
            hits = pygame.sprite.spritecollide(player, meteors, True)
            for _ in hits:
                lives -= 1
                m = Meteor(meteor_img)
                all_sprites.add(m)
                meteors.add(m)
                if lives <= 0:
                    game_over = True

            # --- Draw everything ---
            screen.blit(bg_img, (0, 0))
            all_sprites.draw(screen)
            draw_text(screen, f"Score: {score}", 30, 70, 20)
            draw_text(screen, f"Lives: {lives}", 30, WIDTH - 80, 20)

        else:
            screen.blit(bg_img, (0, 0))
            draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT // 2 - 50, RED)
            draw_text(screen, "Press R to Restart or Q to Quit", 36, WIDTH // 2, HEIGHT // 2 + 20)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                return True
            if keys[pygame.K_q]:
                running = False

        pygame.display.flip()

    return False

# --- Restart loop ---
restart = True
while restart:
    restart = game_loop()

pygame.quit()
