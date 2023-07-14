import pygame
import math
from bullet import Bullet


class Bullets:
    def __init__(self):
        self.bullets = []
        self.counter = 0
        self.bullet_ready = False
        self.speed = 10

    def set_ready_true(self):
        self.bullet_ready = True

    def create_bullet(self, player):
        if self.bullet_ready:
            self.bullet_ready = False
            bullet = Bullet(player.angle, player.id, player.shape.center)
            self.bullets.append(bullet)
            self.counter += 1

    def draw_bullet(self, window, enemy, hit):
        for bullet in self.bullets:
            if bullet.x < -50 or bullet.x > 1050:
                self.bullets.remove(bullet)

            if bullet.y < -50 or bullet.y > 750:
                self.bullets.remove(bullet)

        for bullet in self.bullets:
            rad = bullet.angle * math.pi / 180
            bullet.y -= self.speed * math.sin(rad)
            bullet.x += self.speed * math.cos(rad)
            rect = pygame.Rect(bullet.x, bullet.y, 5, 5)
            pygame.draw.rect(window, (255, 255, 255), rect)

            if enemy.shape.colliderect(rect):
                pygame.event.post(pygame.event.Event(hit))
                self.bullets.remove(bullet)

    def shoot(self, window, player, enemy, hit):
        self.create_bullet(player)
        self.draw_bullet(window, enemy, hit)
