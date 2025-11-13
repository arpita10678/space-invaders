import pygame, random

class Planet(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        size = random.randint(120, 200)
        self.image = pygame.transform.smoothscale(image, (size, size))
        self.rect = self.image.get_rect()

        # NEVER spawn inside player zone
        self.rect.x = random.randint(80, 600)
        self.rect.y = random.randint(-800, -300)

    def update(self, scroll_speed):
        self.rect.y += scroll_speed
        if self.rect.top > 600:
            self.rect.x = random.randint(80, 600)
            self.rect.y = random.randint(-900, -400)
