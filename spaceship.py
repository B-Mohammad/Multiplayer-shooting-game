import pygame
import os
import math
from gun import Bullets
from player import Player

pygame.font.init()


class Spaceship(Player):
    def __init__(self, path_picture, position_x, position_y, angle, is_connected, id, bullets, health, score):
        super().__init__(id, path_picture, position_x, position_y, angle, is_connected, bullets, health, score)
        self.gun = Bullets()
        self.gun.bullets = self.bullets
        self.picture = pygame.image.load(os.path.join('Assets', path_picture)).convert_alpha()
        self.spaceship = pygame.transform.rotate(self.picture, self.angle)
        self.shape = self.spaceship.get_rect(center=(self.x, self.y))

    def rotate_player(self):
        keys_pressed = pygame.key.get_pressed()
        center = self.shape.center
        if keys_pressed[pygame.K_LEFT]:
            self.angle += 2
            self.spaceship = pygame.transform.rotate(self.picture, self.angle)
            self.shape = self.spaceship.get_rect(center=center)
        if keys_pressed[pygame.K_RIGHT]:
            self.angle -= 2
            self.spaceship = pygame.transform.rotate(self.picture, self.angle)
            self.shape = self.spaceship.get_rect(center=center)

    def move_player(self):
        keys_pressed = pygame.key.get_pressed()
        rad = self.angle * math.pi / 180
        if keys_pressed[
            pygame.K_UP]:
            self.speed = min(7, self.speed + self.acc * 2)
            if self.x < 0:
                self.x = 1000
            if self.x > 1000:
                self.x = 0
            if self.y < 0:
                self.y = 700
            if self.y > 700:
                self.y = 0
            else:
                self.y -= self.speed * math.sin(rad)
                self.x += self.speed * math.cos(rad)
        if keys_pressed[
            pygame.K_DOWN]:
            self.speed = 5
            if self.x < 0:
                self.x = 1000
            if self.x > 1000:
                self.x = 0
            if self.y < 0:
                self.y = 700
            if self.y > 700:
                self.y = 0
            else:
                self.y += self.speed * math.sin(rad)
                self.x -= self.speed * math.cos(rad)

        else:
            self.speed = max(5, self.speed - self.acc)
        self.shape = self.spaceship.get_rect(center=(self.x, self.y))

    def draw_health_text(self, window, position_x, position_y, text):
        health_font = pygame.font.SysFont('georgia', 30)
        health_text = health_font.render(
            text + ": " + str(self.health), 1, (255, 255, 255))
        window.blit(health_text, (position_x, position_y))
