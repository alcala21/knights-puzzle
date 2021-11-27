class InvalidMove(Exception):
    ...

class Game:
    def __init__(self):
        self.nrows = 8
        self.ncols = 8
        self.cell_size = 2
        self.board = dict()
        self.pos_moves = [(x, y) for x in range(-2, 3, 1) for y in range(-2, 3, 1) if x ** 2 + y ** 2 == 5]
        self.cur_pos = (0, 0)
        self.occupied = set()
        self.next_moves = dict()
        self.set_board()

    def play(self):
        self.set_move("Enter the knight's starting position: ")
        while self.next_moves:
            self.set_move("Enter your next move: ", False)
        self.exit()

    def set_move(self, message, first=True):
        while True:
            try:
                self.update_board()
                x, y = self.get_values(message)
                if not self.in_board(x, y):
                    raise ValueError

                if not first and ((x, y) in self.occupied or not self.is_available(x, y)):
                    raise InvalidMove

                self.cur_pos = (x, y)
                self.occupied.add((x, y))
                self.board[self.cur_pos] = " " * (self.cell_size - 1) + "X"
                self.get_possible_moves()
                self.draw_board()
                break
            except ValueError:
                print("Invalid dimensions!")
            except InvalidMove:
                print("Invalid move!")

    def is_available(self, x, y):
        return (x - self.cur_pos[0], y - self.cur_pos[1]) in self.pos_moves

    @staticmethod
    def get_values(message):
        return (int(i) for i in input(message).split())

    def set_board(self):
        while True:
            try:
                x, y = self.get_values("Enter your board dimensions: ")
                if x > 0 and y > 0:
                    self.ncols, self.nrows = x, y
                    self.cell_size = len(str(x * y))
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid dimensions!")

    def in_board(self, x, y):
        return 1 <= x <= self.ncols and 1 <= y <= self.nrows

    def update_board(self):
        for i in range(self.ncols):
            for j in range(self.nrows):
                self.board[(i + 1, j + 1)] = "_" * self.cell_size

        for point in self.occupied:
            self.board[point] = " " * (self.cell_size - 1) + "*"

    def get_possible_moves(self):
        self.next_moves = dict()
        for x, y in self.pos_moves:
            nx = self.cur_pos[0] + x
            ny = self.cur_pos[1] + y
            if self.in_board(nx, ny) and (nx, ny) not in self.occupied:
                self.count_possible_moves((nx, ny))

    def count_possible_moves(self, point):
        count = 0
        for x, y in self.pos_moves:
            nx = point[0] + x
            ny = point[1] + y

            if self.in_board(nx, ny) and (nx, ny) not in self.occupied:
                count += 1
        self.next_moves[point] = count
        self.board[point] = " " * (self.cell_size - 1) + str(count)

    def draw_board(self):
        md = len(str(self.nrows))
        board_list = [" " * md + "-" * (self.ncols * (self.cell_size + 1) + 3)]
        for i in range(self.nrows, 0, -1):
            ld = len(str(i))
            rnum = " " * (md - ld) + str(i)
            line = rnum + "| " + " ".join([self.board[(r + 1, i)]
                                          for r in range(self.ncols)]) + " |"
            board_list += [line]

        board_list += [" " * md + "-" * (self.ncols * (self.cell_size + 1) + 3)]
        board_list += [" " * (md + 2) + " ".join(" " * (self.cell_size - len(str(r))) + str(r) for r in range(1, self.ncols + 1))]
        print("\n".join(board_list))

    def exit(self):
        if len(self.occupied) == len(self.board):
            print("What a great tour! Congratulations!")
        else:
            print("No more possible moves!")
            print(f"Your knight visited {len(self.occupied)} squares!")


Game().play()
