import sys
import pygame
from pygame import mixer

import poem_generator
import random

pygame.init()


class Game:
    # Art
    goose_art_1 = pygame.image.load("Art/goose1.png")
    x = int((goose_art_1.get_width()) // 2)
    goose_art_1 = pygame.transform.scale(goose_art_1, (x, x))
    goose_art_2 = pygame.image.load("Art/goose2.png")
    goose_art_2 = pygame.transform.scale(goose_art_2, (x, x))
    goose_art_3 = pygame.image.load("Art/goose3.png")
    goose_art_3 = pygame.transform.scale(goose_art_3, (x, x))
    goose_art_4 = pygame.image.load("Art/goose4.png")
    goose_art_4 = pygame.transform.scale(goose_art_4, (x, x))
    projectile_art = pygame.image.load("Art/laser_pink.png")
    player_art_moving = pygame.image.load("Art/spaceship1.png")
    player_art_moving = pygame.transform.scale(player_art_moving, (player_art_moving.get_width()//2, player_art_moving.get_height()//2))
    player_art_stationary = pygame.image.load("Art/spaceship1-no-flame.png")
    player_art_stationary = pygame.transform.scale(player_art_stationary, (player_art_stationary.get_width()//2, player_art_stationary.get_height()//2))
    player_art = player_art_stationary
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
        # Music
        # mixer.music.load('Sound/goose_sandstorm.mp3')
        mixer.music.load('Sound/goose_sandstorm2.wav')
        mixer.music.play(-1)
        mixer.music.set_volume(0.08)
        # Other
        self.is_game_over = False

        # Enemies
        self.is_enemy_going_right = True
        nr = 100
        nr_in_row = 10
        self.enemies = []
        self.projectiles = []
        for i in range(nr):
            enemy_rect = self.goose_art_2.get_rect()
            x = (i % nr_in_row) * (1.5 * self.goose_art_2.get_width()) + self.goose_art_2.get_width() / 2
            y = (i //nr_in_row) * (1.5 * self.goose_art_2.get_height()) + self.goose_art_2.get_height() / 2 - (self.goose_art_2.get_height()*1.5*(nr_in_row-2))
            enemy_rect.center = (x, y)
            self.enemies.append(enemy_rect)

        # Speech Bubbles #TODO
        self.bubbles = []

        # Player 1
        self.player1_rect = self.player_art.get_rect()
        self.player1_x = self.screen.get_width() / 2
        self.player1_y = self.screen.get_height() - 250

        # Player 1
        self.player2_rect = self.player_art.get_rect()
        self.player2_x = self.screen.get_width() / 2
        self.player2_y = self.screen.get_height() - 250

        # Letters
        self.letters = [] # [text_object_ text_rect, letter (char), [nr_line, char_index]]
        self.poem = poem_generator.get_poem()
        self.is_letter_revealed = []
        self.all_letters = []

        for line in self.poem:
            l1 = []
            l2 = []
            for c in line:
                l1.append(c)
                l2.append(False)
            self.all_letters.append(l1)
            self.is_letter_revealed.append(l2)
        print(self.all_letters)
        print(self.is_letter_revealed)

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
                if event.key == pygame.K_EQUALS:
                    mixer.music.set_volume(mixer.music.get_volume() + 0.01)
                    print("test")
                if event.key == pygame.K_MINUS:
                    print("test")
                    mixer.music.set_volume(mixer.music.get_volume() - 0.01)
                if event.key == pygame.K_f:
                    projectile_rect = self.projectile_art.get_rect()
                    projectile_rect.center = (self.player1_rect.center[0], self.player1_rect.center[1] - 60)
                    self.projectiles.append(projectile_rect)

        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.player1_x > self.player1_rect.width/2:
            self.player1_x -= 5
            self.player_art = self.player_art_moving
        elif keys[pygame.K_d] and self.player1_x < self.screen.get_width() - self.player1_rect.width/2:
            self.player1_x += 5
            self.player_art = self.player_art_moving
        else:
            self.player_art = self.player_art_stationary

    def update(self):
        # Player
        self.player1_rect.center = (self.player1_x, self.player1_y)

        # Enemy
        is_swap = False
        for e in self.enemies: # Move all left/right (and check for player collision)
            if e: 
                x = e.center[0]
                y = e.center[1]
                if self.is_enemy_going_right:
                    x += 1
                else:
                    x -= 1
                e.center = (x, y)
                # Check if swap needed (boundary)
                if x < self.goose_art_2.get_width()/2 or x > self.screen.get_width()-self.goose_art_2.get_width()/2:
                    is_swap = True
                # Check for collision
                if e.colliderect(self.player1_rect):
                    self.is_game_over = True

        if is_swap: # Perform a move down and swap direction
            for e in self.enemies:
                if e:
                    x = e.center[0]
                    y = e.center[1]
                    y += 1.5*self.goose_art_2.get_height()
                    e.center = (x, y)
            self.is_enemy_going_right = not self.is_enemy_going_right

        # Move projectiles down
        for p in self.projectiles:
            x = p.center[0]
            y = p.center[1]
            y -= 5
            p.center = (x, y)
            # handle collisions
            for i, e in enumerate(self.enemies):
                if e and p.colliderect(e):
                    self.projectiles.remove(p)
                    self.enemies[i] = None

                    # spawn letter on hit
                    random_letter = self.get_random_letter()
                    text_object_rect = get_text_rect(random_letter[0], (255,0,0), e.center[0], e.center[1])
                    text_object_rect.append(random_letter[0])
                    text_object_rect.append(random_letter[1])
                    self.letters.append(text_object_rect)
                    break

        # Move the letters down
        for l in self.letters:
            l[1].center = (l[1].center[0], l[1].center[1]+3)
            # Reveal if at the bottom
            if l[1].center[1] >= self.screen.get_height()-200:
                self.is_letter_revealed[l[3][0]][l[3][1]] = True

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Background
        self.screen.blit(self.background_art, (0, 0))

        # Enemy
        for i, e in enumerate(self.enemies):
            if e:
                if i % 5 == 0:
                    self.screen.blit(self.goose_art_4, e)
                elif i % 6 == 0:
                    self.screen.blit(self.goose_art_3, e)
                elif i % 3 == 0:
                    self.screen.blit(self.goose_art_2, e)
                else:
                    self.screen.blit(self.goose_art_1, e)

        # Projectile
        for p in self.projectiles:
            self.screen.blit(self.projectile_art, p)


        # Letter
        for l in self.letters:
            self.screen.blit(l[0], l[1])
        # Player
        self.screen.blit(self.player_art, self.player1_rect)

        # Banner
        if self.is_game_over:
            self.screen.blit(self.game_over_art, self.game_over_rect)

        # Poem
        lines = self.get_lines_to_render()
        for i, line in enumerate(lines):
            tr = get_text_rect(line, (255,255,255), self.screen.get_width()/2, (self.screen.get_height()-200/3*(3-i)))
            self.screen.blit(tr[0], tr[1])
        # Show new frame
        pygame.display.flip()

    def get_random_letter(self):
        i = random.randint(0,2)
        print(i)
        index = random.randint(0, len(self.all_letters[i])-1)
        if self.all_letters[i][index] != " " and self.is_letter_revealed[i][index] == False :
            return [self.all_letters[i][index], [i, index]]
        return self.get_random_letter()

    def get_lines_to_render(self):
        lines = []
        for j in range(3):
            l = []
            for i, letter in enumerate(self.all_letters[j]):
                if letter == " " or self.is_letter_revealed[j][i] == True:
                    l.append(letter)
                else:
                    l.append('_')
            lines.append("".join(l))
        return lines
            
        


# Helper Function
def get_text_rect(text, color, x, y):
    font = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
    text_object = font.render(text, 1, color)
    text_rect = text_object.get_rect()
    text_rect.center = (x, y)
    return [text_object, text_rect]




