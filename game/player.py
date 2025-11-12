import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, (70, 70))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 5
        self.forward_speed = 1.5  # 👈 much slower automatic forward motion

    def update(self, keys):
        # Auto move forward (upwards)
        self.rect.y -= self.forward_speed

        # Move left and right manually
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed_x
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed_x

        # Loop ship when it flies off top
        if self.rect.bottom < 0:
            self.rect.top = 600
