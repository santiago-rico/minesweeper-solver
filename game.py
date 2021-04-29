import random
import re


class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board()
        self.assign_values_to_board()

        # set that keeps track of which locations we've uncovered
        self.dug = set()  # if we dig at 0,0 self.dug = {(0,0)}

    def get_dim_size(self):
        return self.dim_size

    def set_dug(self, new_set):
        self.dug = new_set

    def make_new_board(self):
        # Empty board
        board = [
            [None for _ in range(self.dim_size)] for _ in range(self.dim_size)
        ]

        # Plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == "*":
                continue

            board[row][col] = "*"
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    # we don't want to calculate number of bombs around a bomb
                    continue

                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, (row + 1)) + 1):
            for c in range(
                max(0, col - 1), min(self.dim_size - 1, (col + 1)) + 1
            ):
                if r == row and c == col:
                    # original location, don't check
                    continue
                if self.board[r][c] == "*":
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        # returns true if a successful dig (no bomb)
        # false if the player hit a bomb

        # a few scenarios
        # hit a bomb -> game over
        # dig at a location with neighboring bombs -> finish dig
        # dig at a location with no neighboring bombs -> recursively dig neighbors

        self.dug.add((row, col))  # keep track that we dug here

        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][ccol] == "0" (no neighboring bombs)
        for r in range(max(0, row - 1), min(self.dim_size - 1, (row + 1)) + 1):
            for c in range(
                max(0, col - 1), min(self.dim_size - 1, (col + 1)) + 1
            ):
                if (r, c) in self.dug:
                    continue  # don't dig where you already dug
                self.dig(r, c)

        return True

    def __str__(self):
        visible_board = [
            [None for _ in range(self.dim_size)] for _ in range(self.dim_size)
        ]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "

        # put this together in a string
        string_rep = ""
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key=len)))

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = "   "
        cells = []
        for idx, col in enumerate(indices):
            format = "%-" + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += "  ".join(cells)
        indices_row += "  \n"

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f"{i} |"
            cells = []
            for idx, col in enumerate(row):
                format = "%-" + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += " |".join(cells)
            string_rep += " |\n"

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = (
            indices_row + "-" * str_len + "\n" + string_rep + "-" * str_len
        )

        return string_rep


def play(dim_size=10, num_bombs=10):
    board = Board(dim_size, num_bombs)

    safe = True

    while len(board.dug) < board.get_dim_size() ** 2 - num_bombs:
        print(board)
        user_input = re.split(
            ",(\\s)*",
            input("Where would you like to dig? Input as row, col: "),
        )

        row, col = int(user_input[0]), int(user_input[-1])

        if (
            row < 0
            or row >= board.get_dim_size()
            or col < 0
            or col >= board.get_dim_size()
        ):
            print("Invalid location. Try again")
            continue

        # If it's valid, dig!!
        safe = board.dig(row, col)

        if not safe:
            # dug a bomb D:
            break  # game over

    if safe:
        print("Amazing, you won!")
    else:
        print("Sorry, game over :(")

        board.set_dug(
            [
                (r, c)
                for r in range(board.get_dim_size())
                for c in range(board.get_dim_size())
            ]
        )
        print(board)


if __name__ == "__main__":
    play()
