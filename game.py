class InvalidMove(Exception):
    ...


class Game:
    def __init__(self):
        self.nrows = 8
        self.ncols = 8
        self.cell_size = 2
        self.board = dict()
        self.pos_moves = [(x, y) for x in range(-2, 3, 1) for y in range(-2, 3, 1) if x ** 2 + y ** 2 == 5]
        self.occupied = list()
        self.next_moves = dict()
        self.solution = []

    def play(self):
        self.set_board()
        self.make_move("Enter the knight's starting position: ")
        while True:
            doit = input("Do you want to try the puzzle? (y/n): ")
            if doit in ['y', 'n']:
                break
            print("Invalid input!")
        if not self.solve():
            self.exit(solution=False)
            return
        if doit == 'y':
            self.fill_board()
            while self.next_moves:
                self.draw_board()
                self.make_move("Enter your next move: ", False)
                self.fill_board()
        else:
            self.fill_solution()
        self.exit(manual=doit == "y")

    def solve(self):
        if not self.next_moves:
            if len(self.occupied) == len(self.board):
                self.solution = self.occupied.copy()
                return True
            return False
        _next_moves = sorted(self.next_moves.items(), key=lambda x: x[1])
        s_index = 0
        if len(_next_moves) > 1 and _next_moves[0][1] == 0:
            s_index = 1
        for i in range(s_index, len(_next_moves)):
            self.occupied.append(_next_moves[i][0])
            self.get_possible_moves()
            _solution = self.solve()
            self.occupied.pop(-1)
            if _solution:
                self.next_moves = dict(_next_moves)
                return True
        return False

    def make_move(self, message, first=True):
        while True:
            try:
                x, y = self.get_values(message)
                if not self.in_board(x, y):
                    raise ValueError

                if not first and ((x, y) in self.occupied or not self.is_available(x, y)):
                    raise InvalidMove

                self.occupied.append((x, y))
                self.get_possible_moves()
                break
            except ValueError:
                print("Invalid dimensions!")
            except InvalidMove:
                print("Invalid move!", end=" ")

    def is_available(self, x, y):
        return (x - self.occupied[-1][0], y - self.occupied[-1][1]) in self.pos_moves

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
                    self.fill_board()
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid dimensions!")

    def in_board(self, x, y):
        return 1 <= x <= self.ncols and 1 <= y <= self.nrows

    def fill_board(self):
        for i in range(self.ncols):
            for j in range(self.nrows):
                self.update_cell((i + 1, j + 1), "_" * self.cell_size)

        for point in self.occupied:
            self.update_cell(point, " " * (self.cell_size - 1) + "*")

        for point, count in self.next_moves.items():
            self.update_cell(point, " " * (self.cell_size - 1) + str(count))

        if self.occupied:
            self.update_cell(self.occupied[-1], " " * (self.cell_size - 1) + "X")


    def fill_solution(self):
        for i, point in enumerate(self.solution):
            self.update_cell(point, " " * (self.cell_size - len(str(i + 1))) + str(i + 1))

    def update_cell(self, point, value):
        self.board[point] = value

    def get_possible_moves(self):
        self.next_moves = dict()
        for x, y in self.pos_moves:
            nx = self.occupied[-1][0] + x
            ny = self.occupied[-1][1] + y
            if self.in_board(nx, ny) and (nx, ny) not in self.occupied:
                self.count_ahead_moves((nx, ny))

    def count_ahead_moves(self, point):
        count = 0
        for x, y in self.pos_moves:
            nx = point[0] + x
            ny = point[1] + y

            if self.in_board(nx, ny) and (nx, ny) not in self.occupied:
                count += 1
        self.next_moves[point] = count

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

    def exit(self, solution=True, manual=True):
        if not solution:
            print("No solution exists!")
        elif not manual:
            print("Here's the solution!")
            self.draw_board()
        elif len(self.occupied) == len(self.board):
            print("What a great tour! Congratulations!")
        else:
            print("No more possible moves!")
            print(f"Your knight visited {len(self.occupied)} squares!")


Game().play()