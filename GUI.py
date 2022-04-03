import queue
import sys

import pygame

import gamedata
import puzzleState


def get_box_color(tile_contents):
    tile_color = gamedata.DARKGREY
    if tile_contents == -1:
        tile_color = gamedata.BLACK

    return tile_color


def draw_map(surface, grid_boxes):
    gamedata.BLOCK_HEIGHT = round(gamedata.SCREEN_HEIGHT / gamedata.NUMBER_OF_BLOCKS_HIGH)
    gamedata.BLOCK_WIDTH = round(gamedata.SCREEN_WIDTH / gamedata.NUMBER_OF_BLOCKS_WIDE)
    for j, row in enumerate(grid_boxes):
        for i, box in enumerate(row):
            my_rectangle = pygame.Rect(i * gamedata.BLOCK_WIDTH, j * gamedata.BLOCK_HEIGHT, gamedata.BLOCK_WIDTH,
                                       gamedata.BLOCK_HEIGHT)
            pygame.draw.rect(surface, get_box_color(box), my_rectangle)
            font = pygame.font.SysFont('Arial', 25)
            if box == -1:
                num = ""
            else:
                num = str(box)
            text = font.render(num, True, gamedata.LIGHTGREY)
            # surface.blit(font.render('Hello!', True, (255, 0, 0)), (200, 100))
            text_rect = text.get_rect(
                center=((i * gamedata.BLOCK_WIDTH) + gamedata.BLOCK_WIDTH / 2,
                        (j * gamedata.BLOCK_HEIGHT) + gamedata.BLOCK_HEIGHT / 2))
            surface.blit(text, text_rect)


def draw_grid(surface):
    for i in range(gamedata.NUMBER_OF_BLOCKS_WIDE):
        new_height = round(i * gamedata.BLOCK_HEIGHT)
        new_width = round(i * gamedata.BLOCK_WIDTH)

        pygame.draw.line(surface, gamedata.BLACK, (0, new_height), (gamedata.SCREEN_WIDTH, new_height), 2)
        pygame.draw.line(surface, gamedata.BLACK, (new_width, 0), (new_width, gamedata.SCREEN_HEIGHT), 2)


def game_loop(surface, path_goal: queue.LifoQueue):
    count = 0
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        if not path_goal.empty():
            node: puzzleState.puzzle = path_goal.get()
            draw_map(surface, node.puzzle_data)
            draw_grid(surface)
        pygame.time.wait(1000)

        pygame.display.update()

        count += 1


def initialize_game():
    pygame.init()
    surface = pygame.display.set_mode((gamedata.SCREEN_WIDTH, gamedata.SCREEN_HEIGHT))
    pygame.display.set_caption(gamedata.TITLE)
    surface.fill(gamedata.UGLY_PINK)
    return surface


def UI_init(path_goal, size):
    gamedata.NUMBER_OF_BLOCKS_WIDE = size[1]  # columns
    gamedata.NUMBER_OF_BLOCKS_HIGH = size[0]  # rows
    surface = initialize_game()

    game_loop(surface, path_goal)

# goal = [[1, 2, 3], [8, -1, 4], [7, 6, 5]]
# to_goal = queue.LifoQueue(maxsize=0)
# UI_init(to_goal, [3, 3])
