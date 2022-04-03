from puzzleState import puzzle


class priorityQ:
    def __init__(self):
        self.data: list[puzzle] = []

    def insert(self, element: puzzle):
        self.data.append(element)
        self.data.sort(key=lambda x: x.heuristic+x.cost)

    def is_in(self, element: puzzle) -> int:
        for i in range(0, len(self.data)):
            if self.data[i].puzzle_data == element.puzzle_data:
                return i
        return -1

    def printQ(self):
        for g in self.data:
            print(g.cost+g.heuristic, end=" ")
        print()

    def replace(self, element: puzzle, index: int):
        del self.data[index]
        self.insert(element)

    def empty(self):
        if len(self.data) == 0:
            return True
        return False

    def get(self):
        node = self.data.pop(0)
        self.data.sort(key=lambda x: x.heuristic+x.cost)
        return node
