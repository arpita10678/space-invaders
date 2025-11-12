import pygame, random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, delay_time=180):
        super().__init__()
        self.image = pygame.transform.scale(image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, 700)
        self.rect.y = random.randint(-300, -100)
        self.speed = random.uniform(1.8, 2.3)
        self.spawn_delay = delay_time  # frames before moving (≈ 3 seconds at 60fps)

    def update(self, player_rect):
        # Wait for delay before moving
        if self.spawn_delay > 0:
            self.spawn_delay -= 1
            return

        # Move toward player's position
        if self.rect.centerx < player_rect.centerx:
            self.rect.x += self.speed * 0.7
        elif self.rect.centerx > player_rect.centerx:
            self.rect.x -= self.speed * 0.7

        if self.rect.centery < player_rect.centery:
            self.rect.y += self.speed * 0.7

        # Respawn off top if off screen bottom
        if self.rect.top > 600:
            self.rect.x = random.randint(50, 700)
            self.rect.y = random.randint(-250, -100)
            self.spawn_delay = 120  # wait before reentering
