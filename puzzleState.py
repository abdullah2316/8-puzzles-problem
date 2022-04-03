class puzzle:
    def __init__(self, puzzle_data, parent=None, cost=0, heuristic=0):
        self.puzzle_data = puzzle_data
        self.children = []
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.empty_tile = []

    def print_grid(self):
        for r in self.puzzle_data:
            for c in r:

                if c == -1:
                    print("empty", end=" ")
                else:
                    print(c, end=" ")
            print()

    def swap_tiles(self, action: str):
        if action == 'left':
            self.puzzle_data[self.empty_tile[0]][self.empty_tile[1]] = self.puzzle_data[self.empty_tile[0]][
                self.empty_tile[1] - 1]  # empty_tile set to numbered tile
            self.puzzle_data[self.empty_tile[0]][self.empty_tile[1] - 1] = -1  # numbered tile set to empty
            self.empty_tile[1] = self.empty_tile[1] - 1  # update empty tile coordinates
        elif action == 'right':
            self.puzzle_data[self.empty_tile[0]][self.empty_tile[1]] = self.puzzle_data[self.empty_tile[0]][
                self.empty_tile[1] + 1]
            self.puzzle_data[self.empty_tile[0]][self.empty_tile[1] + 1] = -1
            self.empty_tile[1] = self.empty_tile[1] + 1
        elif action == 'up':
            self.puzzle_data[self.empty_tile[0]][self.empty_tile[1]] = self.puzzle_data[self.empty_tile[0] - 1][
                self.empty_tile[1]]
            self.puzzle_data[self.empty_tile[0] - 1][self.empty_tile[1]] = -1
            self.empty_tile[0] = self.empty_tile[0] - 1
        else:
            self.puzzle_data[self.empty_tile[0]][self.empty_tile[1]] = self.puzzle_data[self.empty_tile[0] + 1][
                self.empty_tile[1]]
            self.puzzle_data[self.empty_tile[0] + 1][self.empty_tile[1]] = -1
            self.empty_tile[0] = self.empty_tile[0] + 1
