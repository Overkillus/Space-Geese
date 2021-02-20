import random
import string

from Server.BaseServer import Server

class GameServer(Server):
    def __init__(self, server, port):
        self.STATUS = "running"
        self.PLAYER_COUNT = 0
        self.MAX_PLAYERS = 2

        super().__init__(server, port) # this runs start(), which halts anything below.

    def handle_client_messages(self, connection, address, msg):
        pass

    def close_server(self):
        # tell all clients that game is over?
        self.SERVER_ON = False # close start() thread
        self.STATUS = "closed"

    # return functions.
    def return_port(self):
        return self.PORT

    def return_players(self):
        return len(self.all_connections)

    def return_max_players(self):
        return self.MAX_PLAYERS

    def return_status(self):
        return self.STATUS
