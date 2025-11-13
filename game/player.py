import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, (70, 70))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 6  # left/right only

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed_x
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed_x
