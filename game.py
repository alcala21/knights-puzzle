# Write your code here
class Game:
    def __init__(self):
        self.size = 8
        self.board = dict()
        self.set_board()

    def set_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.board[(i + 1, j + 1)] = "_"

    def start(self):
        try:
            x, y = [int(i) for i in input("Enter the knight's starting position: ").split()]

            if 1 <= x <= 8 and 1 <= y <= 8:
                self.board[x, y] = "X"
                self.draw_board()
            else:
                raise Exception
        except:
            print("Invalid dimensions!")

    def draw_board(self):
        board_list = [" -------------------"]
        for i in range(self.size, 0, -1):
            line = f"{i}| " + " ".join([self.board[(r + 1, i)]
                                        for r in range(self.size)]) + " |"
            board_list += [line]

        board_list += [" -------------------"]
        board_list += ["   " + " ".join(str(r) for r in range(1, self.size + 1))]
        print("\n".join(board_list))


Game().start()
