import sys
import pygame
from pygame import mixer

pygame.init()


class Game:
    # Art
    # <LOAD HERE>

    def __init__(self):
        # Screen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((900, 600), pygame.RESIZABLE)
        # Clock
        self.clock = pygame.time.Clock()
        self.delta_time = 0

    def tick(self):
        self.event_handler()
        self.delta_time += self.clock.tick() / 1000.0
        while self.delta_time > 1 / 24:
            self.delta_time -= 1 / 24
            self.update()
            self.render()

    def event_handler(self):
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.type == pygame.K_q:
                print("test")
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.type == pygame.K_ESCAPE:
                sys.exit(0)

    def update(self):
        ...

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Show new frame
        pygame.display.flip()

