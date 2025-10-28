# game/obstacle.py
import pygame, random

class Meteor(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        size = random.randint(40, 80)
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect(center=(random.randint(50, 750), -50))
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()
