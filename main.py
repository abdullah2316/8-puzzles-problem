import copy
import queue

from scipy.spatial.distance import cityblock

from GUI import UI_init
from priorityQ import priorityQ
from puzzleState import puzzle


# 8 puzzle problem is solvable when inversion is even
def is_solvable(puzzle_state):
    list_of_tiles = []
    if puzzle_state[0][0] != -1:
        list_of_tiles.append(puzzle_state[0][0])
    if puzzle_state[0][1] != -1:
        list_of_tiles.append(puzzle_state[0][1])
    if puzzle_state[0][2] != -1:
        list_of_tiles.append(puzzle_state[0][2])
    if puzzle_state[1][2] != -1:
        list_of_tiles.append(puzzle_state[1][2])
    if puzzle_state[2][2] != -1:
        list_of_tiles.append(puzzle_state[2][2])
    if puzzle_state[2][1] != -1:
        list_of_tiles.append(puzzle_state[2][1])
    if puzzle_state[2][0] != -1:
        list_of_tiles.append(puzzle_state[2][0])
    if puzzle_state[1][0] != -1:
        list_of_tiles.append(puzzle_state[1][0])
    if puzzle_state[1][1] != -1:
        list_of_tiles.append(puzzle_state[1][1])

    counter = 0
    for x in range(len(list_of_tiles)):
        for y in range(len(list_of_tiles)):
            if x < y and list_of_tiles[x] > list_of_tiles[y]:
                counter += 1

    if counter % 2 == 0:
        return 1
    else:
        return 0


def get_reversed_tiles(puzzle_state: list) -> int:
    # coordinates of where every number should be in puzzle i.e. the goal state
    goal_st = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]
    count = 0
    temp = copy.deepcopy(puzzle_state)
    for i in range(0, 3):
        for j in range(0, 3):
            if temp[i][j] != -1:
                cost = int(cityblock((i, j,), goal_st[temp[i][j] - 1]))
                if cost == 1:
                    if j - 1 >= 0:  # checking left neighbour
                        if temp[i][j - 1] != -1:
                            if (i, j,) == goal_st[temp[i][j - 1] - 1]:
                                count += 2
                                temp[i][j - 1] = -1
                    if j + 1 <= 2:  # checking right neighbour
                        if temp[i][j + 1] != -1:
                            if (i, j,) == goal_st[temp[i][j + 1] - 1]:
                                count += 2
                                temp[i][j + 1] = -1
                    if i - 1 >= 0:  # checking upper neighbour
                        if temp[i - 1][j] != -1:
                            if (i, j,) == goal_st[temp[i - 1][j] - 1]:
                                count += 2
                                temp[i - 1][j] = -1
                    if i + 1 <= 2:  # checking left neighbour
                        if temp[i + 1][j] != -1:
                            if (i, j,) == goal_st[temp[i + 1][j] - 1]:
                                count += 2
                                temp[i + 1][j] = -1
                    temp[i][j] = -1

    return 2 * count


def get_out_of_place_tiles(state1: puzzle) -> int:
    # coordinates of where every number should be in puzzle i.e. the goal state
    goal_st = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]
    cost = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if state1.puzzle_data[i][j] != -1:
                cost += int(cityblock((i, j,), goal_st[state1.puzzle_data[i][j] - 1]))

    return cost


def goal_test(data: list) -> bool:
    g = [[1, 2, 3], [8, -1, 4], [7, 6, 5]]
    if data == g:
        return True
    else:
        return False


def get_children(parent_state: puzzle, action: str):
    pos = parent_state.empty_tile
    size = [3, 3]
    # data = copy.deepcopy(parent_state.puzzle_data)
    child = None
    # moving agent left
    if action == 'left':
        if pos[1] - 1 >= 0:
            state_data = copy.deepcopy(parent_state.puzzle_data)
            child = puzzle(state_data, parent_state)
            child.empty_tile.append(pos[0])
            child.empty_tile.append(pos[1])
            child.swap_tiles(action)
            child.cost = parent_state.cost + 1
            child.heuristic = get_out_of_place_tiles(child) + get_reversed_tiles(child.puzzle_data)
            # starting state cost,heuristic
            parent_state.children.append(child)

    # moving agent right
    elif action == 'right':
        if pos[1] + 1 <= size[1] - 1:
            state_data = copy.deepcopy(parent_state.puzzle_data)
            child = puzzle(state_data, parent_state)
            child.empty_tile.append(pos[0])
            child.empty_tile.append(pos[1])
            child.swap_tiles(action)
            child.cost = parent_state.cost + 1
            child.heuristic = get_out_of_place_tiles(child) + get_reversed_tiles(child.puzzle_data)
            # starting state cost,heuristic
            parent_state.children.append(child)

    # moving agent up
    elif action == 'up':
        if pos[0] - 1 >= 0:
            state_data = copy.deepcopy(parent_state.puzzle_data)
            child = puzzle(state_data, parent_state)
            child.empty_tile.append(pos[0])
            child.empty_tile.append(pos[1])
            child.swap_tiles(action)
            child.cost = parent_state.cost + 1
            child.heuristic = get_out_of_place_tiles(child) + get_reversed_tiles(child.puzzle_data)
            # starting state cost,heuristic
            parent_state.children.append(child)

        # moving agent down
    else:
        if pos[0] + 1 <= size[0] - 1:
            state_data = copy.deepcopy(parent_state.puzzle_data)
            child = puzzle(state_data, parent_state)
            child.empty_tile.append(pos[0])
            child.empty_tile.append(pos[1])
            child.swap_tiles(action)
            child.cost = parent_state.cost + 1
            child.heuristic = get_out_of_place_tiles(child) + get_reversed_tiles(child.puzzle_data)
            # starting state cost,heuristic
            parent_state.children.append(child)
    return child
    pass


def A_star(start_state: puzzle, visited: list):
    q = priorityQ()
    q.insert(start_state)

    while not q.empty():
        node = q.get()
        visited.append(node.puzzle_data)

        if goal_test(node.puzzle_data):
            return node
        c = get_children(node, 'left')
        if c is not None:
            if check_duplicate(q, c, visited):
                node.children.append(c)

        c = get_children(node, 'right')
        if c is not None:
            if check_duplicate(q, c, visited):
                node.children.append(c)

        c = get_children(node, 'up')
        if c is not None:
            if check_duplicate(q, c, visited):
                node.children.append(c)

        c = get_children(node, 'down')
        if c is not None:
            if check_duplicate(q, c, visited):
                node.children.append(c)

    return None

    pass


def check_duplicate(pqueue: priorityQ, node: puzzle, visited: list):
    index = pqueue.is_in(node)
    if node.puzzle_data in visited:
        return False
    elif index != -1:
        if (pqueue.data[index].cost + pqueue.data[index]) > (node.cost + node.heuristic):
            pqueue.replace(node, index)
            return True
    else:
        pqueue.insert(node)
        return True
    pass


# read starting state of problem from a text file and store it in a list
# -1 in text file stands for empty tile
def populate_grid():
    with open('input.txt') as f:
        pz_state = []
        for line in f:
            line = line.split()
            if line:
                line = [int(i) for i in line]
                pz_state.append(line)
    return pz_state


if __name__ == "__main__":

    starting_state = populate_grid()
    if is_solvable(starting_state):
        start_node = puzzle(starting_state)
        start_node.empty_tile = [2, 1]
        start_node.heuristic = get_out_of_place_tiles(start_node)
        explored = []
        goal = A_star(start_node, explored)
        if goal is not None:
            n = goal
            stack = queue.LifoQueue(maxsize=0)
            while n.parent is not None:
                stack.put(n)
                n = n.parent
            stack.put(n)
            print(goal, " goal")
            print("all nodes expanded:")
            for i in range(0, len(explored)):
                print(explored[i])
            UI_init(stack, [3, 3])
            # print("path to goal:")
            # while not stack.empty():
            #     stack.get().print_grid()
        else:
            print("goal not found")

    else:
        print("puzzle not solvable")
