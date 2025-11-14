import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pygame, random
from player import Player
from bullet import Bullet
from meteor import Meteor
from enemy import Enemy
from planet import Planet
from db import init_db, load_stats, save_stats

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Survival Shooter")
clock = pygame.time.Clock()
FPS = 60

bg_img = pygame.transform.scale(pygame.image.load("assets/images/background.png").convert(), (WIDTH, HEIGHT))
player_img = pygame.image.load("assets/images/player.png").convert_alpha()
meteor_img = pygame.image.load("assets/images/meteor.png").convert_alpha()
enemy_img = pygame.image.load("assets/images/enemy.png").convert_alpha()
bullet_img = pygame.image.load("assets/images/bullet.png").convert_alpha()
planet_img = pygame.image.load("assets/images/planet.png").convert_alpha()
explosion_img = pygame.transform.scale(pygame.image.load("assets/images/explosion.png").convert_alpha(), (90, 90))

WHITE = (255,255,255)
RED = (255,40,40)

init_db()
stats = load_stats()

def draw_text(txt, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    surf = font.render(txt, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)

def show_explosion(player, bg1_y, bg2_y):
    screen.blit(bg_img, (0, bg1_y))
    screen.blit(bg_img, (0, bg2_y))
    screen.blit(explosion_img, (player.rect.x - 10, player.rect.y - 10))
    draw_text("LIFE LOST!", 50, WIDTH//2, HEIGHT//2, RED)
    pygame.display.flip()

def pause_explosion(player, bg1_y, bg2_y):
    end_time = pygame.time.get_ticks() + 700
    while pygame.time.get_ticks() < end_time:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
        show_explosion(player, bg1_y, bg2_y)
        clock.tick(60)

def game_loop():
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    meteors = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    planets = pygame.sprite.Group()

    player = Player(player_img, WIDTH//2, HEIGHT - 150)
    all_sprites.add(player)

    bg1_y, bg2_y = 0, -HEIGHT
    scroll_speed = 2

    score = 0
    lives = 3
    enemy_kills = 0
    meteor_kills = 0

    spawn_meteor = 0
    spawn_enemy = 0
    spawn_planet = 0

    for _ in range(2):
        p = Planet(planet_img)
        planets.add(p)
        all_sprites.add(p)

    running = True
    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    b = Bullet(bullet_img, player.rect.centerx, player.rect.top)
                    all_sprites.add(b)
                    bullets.add(b)

        bg1_y += scroll_speed
        bg2_y += scroll_speed
        if bg1_y >= HEIGHT: bg1_y = -HEIGHT
        if bg2_y >= HEIGHT: bg2_y = -HEIGHT

        spawn_meteor += 1
        spawn_enemy += 1

        if spawn_meteor > 120:
            m = Meteor(meteor_img)
            meteors.add(m); all_sprites.add(m)
            spawn_meteor = 0

        if spawn_enemy > 150 and len(enemies) < 3:
            e = Enemy(enemy_img)
            enemies.add(e); all_sprites.add(e)
            spawn_enemy = 0

        player.update(keys)
        bullets.update()
        for m in meteors: m.update(scroll_speed)
        for e in enemies: e.update(player.rect, scroll_speed)
        for p in planets: p.update(scroll_speed)

        enemy_hit = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask)
        meteor_hit = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_mask)
        planet_hit = pygame.sprite.spritecollide(player, planets, False, pygame.sprite.collide_mask)

        crashed = None
        if enemy_hit: crashed = enemy_hit[0]
        elif meteor_hit: crashed = meteor_hit[0]
        elif planet_hit: crashed = planet_hit[0]

        if crashed:
            lives -= 1
            if crashed in planets:
                crashed.rect.y = random.randint(-1800, -1200)
                crashed.rect.x = random.randint(80, 600)
            pause_explosion(player, bg1_y, bg2_y)
            player.rect.y += 10
            if lives <= 0:
                break

        hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
        meteor_kills += len(hits)
        score += len(hits) * 10

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        enemy_kills += len(hits)
        score += len(hits) * 20

        screen.blit(bg_img, (0, bg1_y))
        screen.blit(bg_img, (0, bg2_y))
        all_sprites.draw(screen)
        draw_text(f"Score: {score}", 30, 80, 30)
        draw_text(f"Lives: {lives}", 30, WIDTH - 80, 30)
        pygame.display.flip()

    high = max(score, stats["high_score"])
    save_stats(high, 0, enemy_kills, meteor_kills)
    return True

while game_loop():
    pass

pygame.quit()
