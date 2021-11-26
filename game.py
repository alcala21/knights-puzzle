class Game:
    def __init__(self):
        self.nrows = 8
        self.ncols = 8
        self.cell_size = 2
        self.board = dict()
        self.set_board()

    def set_board(self):
        try:
            x, y = [int(i) for i in input("Enter your board dimensions: ").split()]
            if x > 0 and y > 0:
                self.ncols, self.nrows = x, y
                self.cell_size = self.get_digits(x * y)
                for i in range(self.ncols):
                    for j in range(self.nrows):
                        self.board[(i + 1, j + 1)] = "_" * self.cell_size
            else:
                raise Exception
        except:
            print("Invalid dimensions!")

    @staticmethod
    def get_digits(num):
        count = 0
        while num > 0:
            count += 1
            num //= 10
        return count

    def start(self):
        while self.board:
            try:
                x, y = [int(i) for i in input("Enter the knight's starting position: ").split()]

                if 1 <= x <= self.ncols and 1 <= y <= self.nrows:
                    self.board[x, y] = " " * (self.cell_size - 1) + "X"
                    self.draw_board()
                    break
                else:
                    raise Exception
            except:
                print("Invalid dimensions!")

    def draw_board(self):
        md = self.get_digits(self.nrows)
        board_list = [" " * md + "-" * (self.ncols * (self.cell_size + 1) + 3)]
        for i in range(self.nrows, 0, -1):
            ld = self.get_digits(i)
            rnum = " " * (md - ld) + str(i)
            line = rnum + "| " + " ".join([self.board[(r + 1, i)]
                                        for r in range(self.ncols)]) + " |"
            board_list += [line]

        board_list += [" " * md + "-" * (self.ncols * (self.cell_size + 1) + 3)]
        board_list += [" " * (md + 2) + " ".join(" " * (self.cell_size - self.get_digits(r)) + str(r) for r in range(1, self.ncols + 1))]
        print("\n".join(board_list))


Game().start()
