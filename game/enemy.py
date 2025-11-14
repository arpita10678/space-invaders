import pygame, random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.transform.scale(img, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(80, 700)
        self.rect.y = random.randint(-1200, -300)
        self.speed = random.uniform(1.5, 2.3)

    def update(self, player_rect, scroll_speed):
        # move with world
        self.rect.y += scroll_speed

        # chase horizontally
        if self.rect.centerx < player_rect.centerx:
            self.rect.x += self.speed
        elif self.rect.centerx > player_rect.centerx:
            self.rect.x -= self.speed
        
        # if off-screen, respawn ahead
        if self.rect.top > 600:
            self.rect.x = random.randint(80, 700)
            self.rect.y = random.randint(-1500, -600)
