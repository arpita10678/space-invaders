import pygame, random

class Planet(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        size = random.randint(120, 190)
        self.image = pygame.transform.smoothscale(img, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(80, 600)
        self.rect.y = random.randint(-1600, -400)

    def update(self, scroll_speed):
        self.rect.y += scroll_speed

        if self.rect.top > 600:
            self.rect.x = random.randint(80, 600)
            self.rect.y = random.randint(-1800, -800)
