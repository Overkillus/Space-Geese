import sys
import pygame
from pygame import mixer

pygame.init()


class Game:
    # Art
    goose_art = pygame.image.load("Art/Goose.png")
    player_art = pygame.image.load("Art/spaceship1.png")
    background_art = pygame.image.load("Art/bg.png")

    def __init__(self):
        # Screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # Clock
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        # Player
        self.player_rect = self.player_art.get_rect()
        self.player_x = self.screen.get_width()/2
        self.player_y = self.screen.get_height() - 100

    def tick(self):
        self.event_handler()
        self.delta_time += self.clock.tick() / 1000.0
        while self.delta_time > 1 / 24:
            self.delta_time -= 1 / 24
            self.update()
            self.render()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit(0)
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)

        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_x -= 0.002
        if keys[pygame.K_d]:
            self.player_x += 0.002

    def update(self):
        self.player_rect.center = (self.player_x, self.player_y)

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Background
        self.screen.blit(self.background_art, (0, 0))

        # Player
        self.screen.blit(self.player_art, self.player_rect)

        # Show new frame
        pygame.display.flip()

