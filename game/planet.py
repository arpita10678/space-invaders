import pygame, random

class Planet(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        size = random.randint(130, 200)
        self.image = pygame.transform.smoothscale(image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, 600)
        self.rect.y = random.randint(150, 400)
        self.scroll_speed = 1.5  # slow gentle motion

    def update(self):
        self.rect.y += self.scroll_speed
        if self.rect.top > 600:
            self.rect.y = random.randint(-300, -100)
            self.rect.x = random.randint(50, 600)
