import socket
import sys

class Board:
    def __init__(self, size):
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.size = size
        
    def place_stone(self, x, y, color):
        self.board[x][y] = color
class GoGame:
    def __init__(self, size, conn):
        self.board = Board(size)
        self.current_player = 'B'  # Black plays first
        self.conn = conn
        
    def play(self):
        while not self.game_over():
            self.display()
            x, y = self.make_move()
            self.board.place_stone(x, y, self.current_player)
            self.current_player = 'W' if self.current_player == 'B' else 'B'
            self.send_move(x, y)
            x, y = self.receive_move()
            self.board.place_stone(x, y, self.current_player)
            self.current_player = 'W' if self.current_player == 'B' else 'B'
            
    def make_move(self):
        while True:
            try:
                x = int(input(f"Player {self.current_player}, enter row: "))
                y = int(input(f"Player {self.current_player}, enter column: "))
                if self.board.board[x][y] == '':
                    return x, y
                else:
                    print("That cell is already occupied. Try again.")
            except ValueError:
                print("Invalid input. Enter a valid row and column.")
                
    def game_over(self):
        for row in self.board.board:
            if '' in row:
                return False
        return True
    
    def display(self):
        for row in self.board.board:
            print(' '.join(row))
            
    def send_move(self, x, y):
        self.conn.sendall(f"{x} {y}".encode())
        
    def receive_move(self):
        data = self.conn.recv(1024).decode()
        x, y = map(int, data.split())
        return x, y

# Host side
if len(sys.argv) == 4 and sys.argv[1] == 'host':
    HOST = sys.argv[2]  # The IP address or domain name of the host
    PORT = int(sys.argv[3])  # The port to bind to
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            game = GoGame(19, conn)
            game.play()

# Client side
elif len(sys.argv) == 4 and sys.argv[1] == 'client':
    HOST = sys.argv[2]  # The IP address or domain name of the host
    PORT = int(sys.argv[3])  # The port to connect to
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        game = GoGame(19, s)
        game.play()

else:
    print("Usage: python go_game.py host IP_address port")
    print("       python go_game.py client IP_address port")