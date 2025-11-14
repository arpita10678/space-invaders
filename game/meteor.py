import pygame, random

class Meteor(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        size = random.randint(55, 90)
        self.image = pygame.transform.scale(img, (size, size))
        self.rect = self.image.get_rect()

        # Spawn mostly near top-right area
        self.rect.x = random.randint(420, 780)
        self.rect.y = random.randint(-800, -200)

        # Diagonal movement: down-left
        self.speed_x = -random.uniform(1.2, 2.0)   # left
        self.speed_y = random.uniform(1.0, 2.0)    # down

    def update(self, scroll_speed):
        self.rect.y += self.speed_y + scroll_speed
        self.rect.x += self.speed_x

        # Remove when off screen
        if self.rect.top > 600 or self.rect.right < 0:
            self.kill()
