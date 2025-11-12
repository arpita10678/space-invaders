import pygame, random

class Meteor(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        size = random.randint(70, 100)
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 750)
        self.rect.y = random.randint(-300, -50)
        self.speed_y = random.uniform(1.5, 2.5)
        self.speed_x = random.choice([-1, 1]) * random.uniform(0.3, 0.7)

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > 600:
            self.kill()
