import pickle
import socket
import threading

class Server:
    def __init__(self, server, port):
        self.SERVER = server
        self.PORT = port

        self.HEADER_SIZE = 10
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!GETOUT"
        self.ENTERGAME_MSG = "!ENTERGAME"

        self.all_connections = []
        self.SERVER_ON = True # when False, start() stops running.

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.SERVER, self.PORT))

        t = threading.Thread(target=self.start, args=()) # nice.
        t.start()

    def console(self, msg): # easier output. overridable too.
        print(f"[SERVER-{self.PORT}]:", msg)

    def send_to_client(self, connection, msg):
        # second message - the data
        message = pickle.dumps(msg)
        # first message - the length
        msg_len = len(message)
        send_len = str(msg_len).encode(self.FORMAT)
        send_len += b' ' * (self.HEADER_SIZE - len(send_len))

        try:
            connection.send(send_len)
            connection.send(message)
        except:
            self.close_connection(connection)
            self.console("message send fail - means connection is dead.")

    def close_connection(self, connection):
        connection.close()
        if connection in self.all_connections:
            self.all_connections.remove(connection)

    # any other specific messages. overriden by children.
    def handle_client_messages(self, connection, address, msg):
        pass

    # handles individual connections
    def handle_client(self, connection, address):
        counter = 0 # just for test purposes. counts individual total of client msgs.
        connected = True
        while connected and connection.fileno() != -1:
            try: # capture client disconnecting prematurely.
                # first message = length of message
                msg_len = connection.recv(self.HEADER_SIZE).decode(self.FORMAT)
                # second message = data
                if msg_len:
                    msg_len = int(msg_len)
                    msg = connection.recv(msg_len)
                    msg = pickle.loads(msg)
                    self.console(f"[{address}] said: {msg}")

                    if msg == self.DISCONNECT_MSG:
                        connected = False
                        self.send_to_client(connection, self.DISCONNECT_MSG)
                        self.console(f"[{address}] has disconnected")
                    # handle any other messages.
                    self.handle_client_messages(connection, address, msg)

                    counter += 1
                    #self.send_to_client(connection, f"msg received ({counter})")
            except:
                connected = False
                self.console(f"Client message error. Connection cut with {address}")

        self.close_connection(connection)

    # handles new connections
    def start(self):
        self.sock.listen()
        self.console(f"Hello world! Listening on {self.SERVER}.")
        while self.SERVER_ON:
            connection, address = self.sock.accept()
            self.all_connections.append(connection)
            self.console(f"new connection = {address}")
            self.console(f"connected clients = {len(self.all_connections)}")
            thread = threading.Thread(target=self.handle_client
                                      , args=(connection, address))
            thread.start()
            #self.send_to_all_clients(None) # clean-up all_connections

s = Server(socket.gethostname(), 2000)