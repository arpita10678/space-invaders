import pygame
import random

class Meteor(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (60, 60))  # resize meteor
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 740)
        self.rect.y = random.randint(-150, -50)
        self.speedy = random.randint(3, 7)
        self.speedx = random.randint(-2, 2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # If meteor goes off screen, respawn
        if self.rect.top > 600 or self.rect.left < -100 or self.rect.right > 900:
            self.rect.x = random.randint(0, 740)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(3, 7)
