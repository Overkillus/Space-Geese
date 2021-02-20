import sys
import pygame
from pygame import mixer

pygame.init()


class Game:
    # Art
    goose_art = pygame.image.load("Art/goose2.png")
    x = int((goose_art.get_width()) // 2)
    goose_art = pygame.transform.scale(goose_art, (x, x))
    player_art_moving = pygame.image.load("Art/spaceship1.png")
    player_art_moving = pygame.transform.scale(player_art_moving, (player_art_moving.get_width()//2, player_art_moving.get_height()//2))
    player_art = pygame.image.load("Art/spaceship1.png")
    player_art = pygame.transform.scale(player_art, (player_art.get_width()//2, player_art.get_height()//2))
    background_art = pygame.image.load("Art/bg.png")
    game_over_art = pygame.image.load("Art/bonk.jpg")

    def __init__(self):
        # Screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # Background
        self.background_art = pygame.transform.scale(self.background_art, (self.screen.get_width(), self.screen.get_height()))
        # Clock
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        # Banners
        self.game_over_rect = self.game_over_art.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2))
        # Other
        self.is_game_over = False

        # Enemies
        self.is_enemy_going_right = True
        nr = 24
        nr_in_row = 8
        self.enemies = []
        for i in range(nr):
            enemy_rect = self.goose_art.get_rect()
            x = (i % nr_in_row) * (1.5*self.goose_art.get_width()) + self.goose_art.get_width()/2
            y = (i //nr_in_row) * (1.5*self.goose_art.get_height()) + self.goose_art.get_height()/2
            enemy_rect.center = (x, y)
            self.enemies.append(enemy_rect)

        # Player 1
        self.player1_rect = self.player_art.get_rect()
        self.player1_x = self.screen.get_width() / 2
        self.player1_y = self.screen.get_height() - 250

        # Player 1
        self.player2_rect = self.player_art.get_rect()
        self.player2_x = self.screen.get_width() / 2
        self.player2_y = self.screen.get_height() - 250

    def tick(self):
        self.delta_time += self.clock.tick() / 1000.0
        while self.delta_time > 1 / 60:
            self.delta_time -= 1 / 60
            self.event_handler()
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
        if keys[pygame.K_a] and self.player1_x > self.player1_rect.width/2:
            self.player1_x -= 5
        if keys[pygame.K_d] and self.player1_x < self.screen.get_width() - self.player1_rect.width/2:
            self.player1_x += 5

    def update(self):

        # Player
        self.player1_rect.center = (self.player1_x, self.player1_y)

        # Enemy
        is_swap = False
        for e in self.enemies: # Move all left/right (and check for player collision)
            x = e.center[0]
            y = e.center[1]
            if self.is_enemy_going_right:
                x += 1
            else:
                x -= 1
            e.center = (x, y)
            # Check if swap needed (boundary)
            if x < self.goose_art.get_width()/2 or x > self.screen.get_width()-self.goose_art.get_width()/2:
                is_swap = True
            # Check for collision
            if e.colliderect(self.player1_rect):
                self.is_game_over = True

        if is_swap: # Perform a move down and swap direction
            for e in self.enemies:
                x = e.center[0]
                y = e.center[1]
                y += 1.5*self.goose_art.get_height()
                e.center = (x, y)
            self.is_enemy_going_right = not self.is_enemy_going_right

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Background
        self.screen.blit(self.background_art, (0, 0))

        # Enemy
        for e in self.enemies:
            self.screen.blit(self.goose_art, e)

        # Player
        self.screen.blit(self.player_art, self.player1_rect)

        # Banner
        if self.is_game_over:
            self.screen.blit(self.game_over_art, self.game_over_rect)

        # Show new frame
        pygame.display.flip()

