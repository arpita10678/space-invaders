import pygame, random

class Meteor(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        size = random.randint(60, 90)
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20, 760)
        self.rect.y = random.randint(-600, -80)
        self.speed_x = random.choice([-1, 1]) * random.uniform(0.4, 1.0)
        self.speed_y = random.uniform(1.5, 2.5)

    def update(self, scroll_speed):
        self.rect.y += self.speed_y + scroll_speed
        self.rect.x += self.speed_x
        if self.rect.top > 600:
            self.kill()
