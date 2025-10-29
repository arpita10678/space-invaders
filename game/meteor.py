import pygame
import random

class Meteor(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 750)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(2, 6)
        self.speed_x = random.choice([-2, -1, 1, 2])  # diagonal drift

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > 600 or self.rect.left < -50 or self.rect.right > 850:
            self.rect.x = random.randint(0, 750)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(2, 6)
            self.speed_x = random.choice([-2, -1, 1, 2])
