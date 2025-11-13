import pygame, random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(80, 700)
        self.rect.y = random.randint(-700, -200)
        self.speed = random.uniform(1.5, 2.3)

    def update(self, player_rect, scroll_speed):
        # Move forward with world
        self.rect.y += scroll_speed

        # Chase horizontally
        if self.rect.centerx < player_rect.centerx:
            self.rect.x += self.speed
        elif self.rect.centerx > player_rect.centerx:
            self.rect.x -= self.speed

        # Move vertically toward player slightly
        if self.rect.centery < player_rect.centery:
            self.rect.y += self.speed * 0.4

        # Respawn far ahead
        if self.rect.top > 600:
            self.rect.x = random.randint(80, 700)
            self.rect.y = random.randint(-900, -300)
