import socket
import threading
import pickle
from player import Player

IP_ADDRESS = "127.0.0.1"
PORT = 9999
ADDRESS = (IP_ADDRESS, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDRESS)

players = [Player(1, 'spaceship_yellow.png', 300, 350, 0, False),
           Player(2, 'spaceship_red.png', 700, 350, 180, False)]


def handle_clients(conn, player):
    try:
        print(f"index : {player}")
        conn.send(pickle.dumps(players[player]))
        while True:
            players[player] = pickle.loads(conn.recv(2048))

            if player == 0:
                conn.send(pickle.dumps(players[1]))
            else:
                conn.send(pickle.dumps(players[0]))

    except EOFError:
        players[player].is_connected = False

        print(f"Player {players[player].id} Disconnected...")
        conn.close()

        if player == 0:
            players[player] = Player(1, 'spaceship_yellow.png', 300, 350, 0, False)
        if player == 1:
            players[player] = Player(2, 'spaceship_red.png', 700, 350, 180, False)


def start():
    print(f"Server is Started by {IP_ADDRESS} \nWaiting for connection...")
    s.listen()
    while True:
        c, address = s.accept()
        print(address)

        if players[0].is_connected:  # If p1 is connected. We give the index of p2
            player = 1

        elif players[1].is_connected:  # If p2 is connected. We give the index of p1
            player = 0

        else:
            player = 0

        players[player].is_connected = True
        thread = threading.Thread(target=handle_clients, args=(c, player))
        thread.start()
        print(f"\nConnections : {threading.active_count() - 1}")


start()
