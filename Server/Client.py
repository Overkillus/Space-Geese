import pickle
import socket
import threading
import time

class Client:
    def __init__(self, server, port):
        self.SERVER = server
        self.PORT = port  # this is the main lobby port.

        self.HEADER_SIZE = 10
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!GETOUT"

        self.IN_GAME = False
        self.connected = False
        self.changing_server = False
        self.sock = None

        # self.start()

    # server - client stuff.
    def send_to_server(self, msg):
        # second message - the data
        message = pickle.dumps(msg)
        # first message - the length
        msg_len = len(message)
        send_len = str(msg_len).encode(self.FORMAT)
        send_len += b' ' * (self.HEADER_SIZE - len(send_len))

        self.sock.send(send_len)
        self.sock.send(message)

    def expect_message(self):
        self.connected = True
        while self.connected:
            # first message = length of message
            msg_len = self.sock.recv(self.HEADER_SIZE).decode(self.FORMAT)
            # second message = data
            if msg_len:
                msg_len = int(msg_len)
                msg = self.sock.recv(msg_len)
                msg = pickle.loads(msg)
                print(f"[SERVER]: {msg}") # test.

                # if statements here for all the actions u want!
                if self.DISCONNECT_MSG in msg:
                    self.connected = False
                    self.console("you've been disconnected.")
                # any other specific messages, send to another function.
                self.handle_server_messages(msg)

    def disconnect(self):
        if self.connected:
            self.send_to_server(self.DISCONNECT_MSG)

    def console(self, msg):
        print("[CLIENT]:", msg)

    # game server functions.
    def handle_server_messages(self, msg):
        if "[SERVER" in msg:  # ignore reposts.
            return

    def start(self):
        self.IN_GAME = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        thread = threading.Thread(target=self.expect_message)
        thread.start()
        time.sleep(0.01)
        # tell server u have arrived?