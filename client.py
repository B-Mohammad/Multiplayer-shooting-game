import pygame
import os
from sys import exit
from spaceship import Spaceship
from player import Player
import socket
import pickle

pygame.font.init()
pygame.mixer.init()

IP_ADDRESS = "127.0.0.1"  # Enter your server host
PORT = 9999
ADDRESS = (IP_ADDRESS, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

# create window
WINDOWWIDTH, WINDOWHEIGHT = 1000, 700
WINDOW = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Come To Die")
background = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')).convert(), (WINDOWWIDTH, WINDOWHEIGHT))


def draw(player1, player2, player1_gun, player2_gun, player1_hit, player2_hit):
    WINDOW.blit(background, (0, 0))
    player2_gun.shoot(WINDOW, player2, player1, player1_hit)
    player1_gun.shoot(WINDOW, player1, player2, player2_hit)

    WINDOW.blit(player1.spaceship, player1.shape)
    WINDOW.blit(player2.spaceship, player2.shape)

    player1.draw_health_text(WINDOW, 20, 20, "your health")
    player2.draw_health_text(WINDOW, 680, 20, "your enemy's health")


def successful_shoot(player1, player2):
    finish = False
    winner_font = pygame.font.SysFont('georgia', 100)
    winner_text = ""
    if player2.health <= 0:
        winner_text = "You Lose!"
    if player1.health <= 0:
        winner_text = "You win!"
    if winner_text != "":
        finish = True
        draw_text = winner_font.render(winner_text, 1, (255, 255, 255))
        WINDOW.blit(draw_text, (WINDOWWIDTH / 2 - draw_text.get_width() /
                                2, WINDOWHEIGHT / 2 - draw_text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(5000)
    return finish


def crash(WINDOW, WINDOWWIDTH, WINDOWHEIGHT):
    game_over_sound = pygame.mixer.Sound('Assets/game-over.wav')
    text = "Crashed!"
    text_font = pygame.font.SysFont('georgia', 100)
    draw_text = text_font.render(text, 1, (255, 255, 255))
    WINDOW.blit(draw_text, (WINDOWWIDTH / 2 - draw_text.get_width() /
                            2, WINDOWHEIGHT / 2 - draw_text.get_height() / 2))
    game_over_sound.play()
    pygame.display.update()
    pygame.time.delay(3000)


def game_over():
    client.close()
    pygame.quit()
    exit()


def main():
    # create objects
    p1 = pickle.loads(client.recv(2048))
    player1 = Spaceship(p1.path, p1.x, p1.y, p1.angle, p1.is_connected, p1.id, p1.bullets, p1.health, p1.score)
    player1_hit = pygame.USEREVENT + 1
    player2_hit = pygame.USEREVENT + 2
    crash_hit = pygame.USEREVENT + 3
    clock = pygame.time.Clock()
    bullet_hit_sound = pygame.mixer.Sound('Assets/Grenade+1.mp3')
    bullet_fire_sound = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

    main_game = False
    menu = True

    # loading menu window
    menu_background = pygame.transform.scale(pygame.image.load(
        os.path.join('Assets', 'loading.png')).convert(), (WINDOWWIDTH, WINDOWHEIGHT))
    text_font = pygame.font.SysFont('georgia', 50)
    text = text_font.render(
        "waiting for players!", 1, (0, 0, 0))
    while menu:
        print('Waiting for players to join...')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()

        client.send(pickle.dumps(p1))
        p2 = pickle.loads(client.recv(2048))
        player2 = Spaceship(p2.path, p2.x, p2.y, p2.angle, p2.is_connected, p2.id, p2.bullets, p2.health, p1.score)

        if player1.is_connected and player2.is_connected:
            menu = False
            main_game = True

        WINDOW.blit(menu_background, (0, 0))
        WINDOW.blit(text, (WINDOWWIDTH / 2 - text.get_width() /
                           2, 500))
        pygame.display.update()
        clock.tick(1)

    while main_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_game = False
                game_over()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1.gun.set_ready_true()
                    bullet_fire_sound.play()

            if event.type == player2_hit:
                player1.score += 1
                bullet_hit_sound.play()

            if event.type == player1_hit:
                bullet_hit_sound.play()

            if event.type == crash_hit:
                crash(WINDOW, WINDOWWIDTH, WINDOWHEIGHT)
                game_over()

        if successful_shoot(player2, player1):
            main_game = False
            game_over()


        if not player2.is_connected:
            win_text_font = pygame.font.SysFont('georgia', 100)
            win_text = win_text_font.render(
                "You won!", 1, (255, 255, 255))
            WINDOW.blit(win_text, (WINDOWWIDTH / 2 - win_text.get_width() /
                                   2, WINDOWHEIGHT / 2 - win_text.get_height() /
                                   2))
            pygame.display.update()
            pygame.time.delay(3000)
            main_game = False
            game_over()


        player1.health = 5 - player2.score

        p1 = Player(player1.id, player1.path, player1.x, player1.y, player1.angle, player1.is_connected,
                    player1.bullets, player1.health, player1.score)
        client.send(pickle.dumps(p1))
        p2 = pickle.loads(client.recv(2048))
        player2 = Spaceship(p2.path, p2.x, p2.y, p2.angle, p2.is_connected, p2.id, p2.bullets, p2.health, p2.score)

         # crash two players
        if player1.shape.collidepoint(player2.shape.centerx,player2.shape.centery) or player2.shape.collidepoint(player1.shape.centerx,player1.shape.centery):
            pygame.event.post(pygame.event.Event(crash_hit))

        draw(player1, player2, player1.gun, player2.gun, player1_hit, player2_hit)
        player1.move_player()
        player1.rotate_player()
        player2.move_player()
        player2.rotate_player()
       
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()