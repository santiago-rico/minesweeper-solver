import random

# from game import Board


class Solver:
    def __init__(self):
        self.mines_loc = set()
        self.safe_moves = set()

    def make_move(self, state):
        self.get_mines_loc_set(state)
        self.get_safe_moves_set(state)
        if len(self.safe_moves) == 0:
            flat_board = [
                loc for sublist in state.get_visible_board() for loc in sublist
            ]
            loc = random.choice(range(0, state.get_dim_size() ** 2 - 1))
            row = str(loc // state.get_dim_size())
            col = str(loc % state.get_dim_size())
            move = row, col
            return ",".join(move)
        else:
            possible_moves = self.safe_moves - state.get_dug()
            loc = random.choice(list(possible_moves))
            move = map(str, loc)
            return ",".join(move)

    def get_mines_loc_set(self, state):
        for row, col in state.get_dug():
            if self.num_empty_cells_around(row, col, state) == int(
                state.get_visible_board()[row][col]
            ):
                for r in range(
                    max(0, row - 1),
                    min(state.get_dim_size() - 1, (row + 1)) + 1,
                ):
                    for c in range(
                        max(0, col - 1),
                        min(state.get_dim_size() - 1, (col + 1)) + 1,
                    ):
                        if state.get_visible_board()[r][c] == " ":
                            self.mines_loc.add((r, c))

    def get_safe_moves_set(self, state):
        for row, col in state.get_dug():
            # if (
            #     self.num_empty_cells_around(row, col, state)
            #     == state.get_visible_board()[row][col]
            # ):
            #     # You have already found all the mines around this location so go on
            #     continue

            if self.num_empty_cells_around(row, col, state) > int(
                state.get_visible_board()[row][col]
            ):
                # You still have to dig, but we'll dig safely
                if self.num_detected_mines_around(row, col, state) == int(
                    state.get_visible_board()[row][col]
                ):
                    # We know all the locations of the mines but we haven't dug all the empty space around us. We want to return any locations around ours that are not mines (based on our mines loc set)
                    all_moves = set()
                    for r in range(
                        max(0, row - 1),
                        min(state.get_dim_size() - 1, (row + 1)) + 1,
                    ):
                        for c in range(
                            max(0, col - 1),
                            min(state.get_dim_size() - 1, (col + 1)) + 1,
                        ):
                            if (r, c) not in self.mines_loc and (r, c) != (
                                row,
                                col,
                            ):
                                self.safe_moves.add((r, c))

    def num_empty_cells_around(self, row, col, state):
        num_empty_cells_around = 0
        for r in range(
            max(0, row - 1), min(state.get_dim_size() - 1, (row + 1)) + 1
        ):
            for c in range(
                max(0, col - 1), min(state.get_dim_size() - 1, (col + 1)) + 1
            ):
                if r == row and c == col:
                    # original location, don't check
                    continue
                if state.get_visible_board()[r][c] == " ":
                    num_empty_cells_around += 1
        return num_empty_cells_around

    def num_detected_mines_around(self, row, col, state):
        num_detected_mines = 0
        for r in range(
            max(0, row - 1), min(state.get_dim_size() - 1, (row + 1)) + 1
        ):
            for c in range(
                max(0, col - 1), min(state.get_dim_size() - 1, (col + 1)) + 1
            ):
                if r == row and c == col:
                    continue
                if (r, c) in self.mines_loc:
                    num_detected_mines += 1
        return num_detected_mines
