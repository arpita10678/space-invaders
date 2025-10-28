# game/ui.py
import pygame

class UI:
    def __init__(self, font):
        self.font = font
        self.score = 0
        self.lives = 3

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, (255,255,255))
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255,100,100))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
