import pygame
import numpy as np

size = (6, 6)
window_size = 60
tile_size = 10
pre_board = np.zeros(36).reshape((6, 6))
bgColor = (240, 160, 100, 128)
global_i = 0
winner_global = 1
done = False


def convertToArray(string):
    array = list(map(int, string.split(",")[:-1]))
    array = np.array(array)
    return np.reshape(array, (-1, 6))


def drawCircle(game_display, pos, player_id):
    global bgColor
    if player_id == 0:
        return
    elif player_id == 1:
        pygame.draw.circle(game_display, (240, 160, 100), pos, 15)
        pygame.draw.circle(game_display, "white", pos, 10)
    elif player_id == 2:
        pygame.draw.circle(game_display, (200, 100, 200), pos, 15)
        pygame.draw.circle(game_display, "white", pos, 10)


def drawGrid(gameDisplay, board):
    global bgColor
    global pre_board
    global global_i
    global done
    global winner_global

    diff = pre_board - board
    for x in range(6):
        for y in range(6):

            if diff[x][y] != 0:
                rect = pygame.Rect(
                    y * window_size + 440, x * window_size, window_size, window_size
                )
                pygame.draw.rect(gameDisplay, (70, 180, 200), rect, 5, 7)
                drawCircle(gameDisplay, rect.center, board[x][y])
            else:
                rect = pygame.Rect(
                    y * window_size + 440, x * window_size, window_size, window_size
                )
                pygame.draw.rect(gameDisplay, (0, 0, 0), rect, 1, 7)
                drawCircle(gameDisplay, rect.center, board[x][y])

            if diff[x][y] != 0:
                rect_pre = pygame.Rect(
                    y * window_size, x * window_size, window_size, window_size
                )
                pygame.draw.rect(gameDisplay, (70, 180, 180), rect_pre, 5, 7)
                drawCircle(gameDisplay, rect_pre.center, pre_board[x][y])
            else:
                rect_pre = pygame.Rect(
                    y * window_size, x * window_size, window_size, window_size
                )
                pygame.draw.rect(gameDisplay, (0, 0, 0), rect_pre, 1, 7)
                drawCircle(gameDisplay, rect_pre.center, pre_board[x][y])

            # Drawing the arrow
            pygame.draw.polygon(
                gameDisplay,
                (100, 200, 200),
                (
                    [370.0, 170.0],
                    [370.0, 190.0],
                    [410.0, 190.0],
                    [410.0, 200.0],
                    [430.0, 180.0],
                    [410.0, 160.0],
                    [410.0, 170.0],
                ),
            )

            # turn Color
            rectTurn = pygame.Rect(385, 100, 30, 30)
            pygame.draw.rect(gameDisplay, bgColor, rectTurn)

            # turn Number
            font = pygame.font.Font("freesansbold.ttf", 16)
            text = font.render("move: " + str(global_i), True, "black", "white")
            textRect = text.get_rect()
            textRect.center = (400, 60)
            gameDisplay.blit(text, textRect)

            if done:
                font = pygame.font.Font("freesansbold.ttf", 72)
                text = font.render(
                    "player: " + str(winner_global) + " Wins!", True, "white", "black"
                )
                textRect = text.get_rect()
                textRect.center = (400, 180)
                gameDisplay.blit(text, textRect)


pygame.init()


def changeBgColor():
    global bgColor
    if bgColor == (240, 160, 100, 128):
        bgColor = (200, 100, 200, 128)
    elif bgColor == (200, 100, 200, 128):
        bgColor = (240, 160, 100, 128)


def display(winner="draw"):
    global bgColor
    global pre_board
    global global_i
    global winner_global
    global done

    winner_global = winner
    f = open("record.hbd")
    history = f.readlines()
    f.close()
    gameDisplay = pygame.display.set_mode((800, 360))
    pygame.display.set_caption("PENTAGO")
    pygame.display.update()
    clock = pygame.time.Clock()
    i = 1
    board = convertToArray(history[i])

    # ============================ Time Based =============================
    while True:
        gameDisplay.fill((240, 255, 250))
        drawGrid(gameDisplay, board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if i >= len(history) - 1:
            font = pygame.font.Font("freesansbold.ttf", 72)
            if str(winner_global) == "draw":
                text = font.render("Draw", True, "w hite", "black")
            else:
                text = font.render(
                    "player: " + str(winner_global) + " Wins!", True, "white", "black"
                )
            textRect = text.get_rect()
            textRect.center = (400, 180)
            gameDisplay.blit(text, textRect)
            pygame.display.update()
            pygame.time.wait(5000)
            break
        pygame.time.wait(1000)
        i += 1
        global_i += 1
        pre_board = board
        board = convertToArray(history[i])
        changeBgColor()

        pygame.display.update()
    # ============================ Time Based =============================

    # ============================ Click Based =============================
    # while True:
    #     gameDisplay.fill((240, 255, 250))
    #     drawGrid(gameDisplay, board)
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             quit()
    #         elif event.type == pygame.MOUSEBUTTONDOWN and i < len(history) - 1:
    #             i += 1
    #             global_i += 1
    #             pre_board = board
    #             board = convertToArray(history[i])
    #             changeBgColor()
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             # print("whyyyy")
    #             # pygame.quit()
    #             # quit()
    #             done = True
    #     pygame.display.update()
    # ============================ Click Based =============================
