# Memory Matching Game
# By: Destiny Cleary

# Code created with the help of Stack Exchange question
# https://codereview.stackexchange.com/questions/127836/memory-game-using-python-and-pygame
# Question by Boopesh:
# https://codereview.stackexchange.com/users/104920/boopesh
# Answer by zondo:
# https://codereview.stackexchange.com/users/99934/zondo

# Code created based upon
# http://inventwithpython.com/pygame
# By Al Sweigart al@inventwithpython.com
# Released under a "Simplified BSD" license

import pygame, random
from pygame.locals import *

# Initialize constants for the game board
FPS = 30
SPEED = 10
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CARD_SIZE = 40
GAP_SIZE = 10
BOARD_WIDTH = 6
BOARD_HEIGHT = 5
X_MARGIN = (WINDOW_WIDTH - (BOARD_WIDTH * (CARD_SIZE + GAP_SIZE))) // 2
Y_MARGIN = (WINDOW_HEIGHT - (BOARD_HEIGHT * (CARD_SIZE + GAP_SIZE))) // 2
# Make sure board size is even for pairs of cards
assert (BOARD_HEIGHT * BOARD_WIDTH) % 2 == 0

# Card Colors
AQUA = (0, 255, 255)
GREEN = (0, 255, 0)
PLUM = (139, 0, 139)
MAGENTA = (255, 0, 255)
BLUE = (0, 3, 165)

COLORS = (AQUA, GREEN, PLUM, MAGENTA, BLUE)

# Display colors
BG_COLOR = (220, 220, 220)
DARK_BG_COLOR = (47, 79, 79)
CARD_COLOR = (24, 22, 32)
HIGHLIGHT_COLOR = (254, 19, 129)

# Shapes on cards
CIRCLE = 'circle'
TRIANGLE = 'triangle'
SQUARE = 'square'

SHAPES = (CIRCLE, TRIANGLE, SQUARE)


# Main function
def main():
    # Initliaze pygame
    pygame.init()

    # Set up the CLOCK
    global CLOCK
    CLOCK = pygame.time.Clock()

    # Set up the display
    global DISPLAY
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Memory Matching Game')
    DISPLAY.fill(BG_COLOR)

    # Set up mouse
    mouse_x = 0
    mouse_y = 0
    mouse_click = False
    # stores coordinates of first card selected
    first_selection = None

    # Set up the game board
    board = generateRandomizedBoard()
    revealed = generateRevealedCards(False)
    startGameAnimation(board)

    # Variable for running the game
    playing = True

    # Let the user interact with the game
    while playing:
        # Update display and mouse
        mouse_click = False
        DISPLAY.fill(BG_COLOR)
        drawBoard(board, revealed)

        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouse_click = True

        # Convert the mouse coordinates into usable card coordinates
        card_x, card_y = getPosition(mouse_x, mouse_y)

        # If the mouse is over a card
        if card_x is not None and card_y is not None:
            # If the card is not already revealed
            if not revealed[card_x][card_y]:
                # If mouse is clicked, reveal the card and check for match
                if mouse_click:
                    showCardAnimation(board, [(card_x, card_y)])
                    revealed[card_x][card_y] = True
                    if first_selection is None:
                        first_selection = (card_x, card_y)
                    else:
                        pygame.time.wait(1000)
                        # If the cards match, leave them uncovered
                        if board[card_x][card_y] is \
                            board[first_selection[0]][first_selection[1]]:
                            revealed[card_x][card_y] = True
                            revealed[first_selection[0]][first_selection[1]] = \
                            True
                            first_selection = None
                        # If cards do not match, recover them
                        elif board[card_x][card_y] is not \
                            board[first_selection[0]][first_selection[1]]:
                            revealed[card_x][card_y] = False
                            revealed[first_selection[0]][first_selection[1]] = \
                            False
                            first_selection = None
                    # If all the cards are uncovered, the player has won
                    if gameWon(revealed):
                        gameWonAnimation(board, revealed)
                        pygame.time.wait(1000)

                        # Reset the gameboard
                        board = generateRandomizedBoard()
                        revealed =generateRevealedCards(False)
                        drawBoard(board, revealed)
                        pygame.display.update()
                        startGameAnimation(board)
                        first_selection = None

                # If mouse is just hovering, highlight the card
                else:
                    x, y = getCoordinates(card_x, card_y)
                    pygame.draw.rect(DISPLAY, HIGHLIGHT_COLOR,
                        (x - 5, y - 5, CARD_SIZE + 10, CARD_SIZE + 10), 3)

        # Update the screen and wait
        mouse_click = False
        pygame.display.update()
        CLOCK.tick(FPS)


# Function to set up the cards randomly on the game Board
def generateRandomizedBoard():
    # Make a list of possible pictures on cards
    pics = []
    for shape in SHAPES:
        for color in COLORS:
            pics.append((shape, color))

    # Get the number of cards needed and randomize the pictures
    num_pics = BOARD_HEIGHT * BOARD_WIDTH // 2
    pics = pics[:num_pics] * 2
    random.shuffle(pics)

    # Put the pictures on cards on the gamebaord
    board = []
    for i in range(BOARD_HEIGHT):
        row = []
        for j in range(BOARD_WIDTH):
            row.append(pics[0])
            del pics[0]
        board.append(row)
    return board


# Store data when a new box is revealed
def generateRevealedCards(value):
    revealed = []
    for i in range(BOARD_HEIGHT):
        revealed.append([value] * BOARD_WIDTH)
    return revealed


# Flashes the cards at the beginning of the game
def startGameAnimation(board):
    # Get the cards
    revealed = generateRevealedCards(False)

    # Make a random list of the cards
    cards = []
    for x in range(BOARD_HEIGHT):
        for y in range(BOARD_WIDTH):
            cards.append((x,y))
    random.shuffle(cards)

    # Put the cards into a group
    groups = []
    for i in range(0, len(cards), 30):
        groups.append(cards[i:i + 30])

    drawBoard(board, revealed)

    # Flash the cards
    for j in groups:
        showCardAnimation(board, j)
        hideCardAnimation(board, j)


# Draw all of the cards in proper state
def drawBoard(board, revealed):
    # Get the coordinates of each card
    for card_x in range(BOARD_HEIGHT):
        for card_y in range(BOARD_WIDTH):
            x, y = getCoordinates(card_x, card_y)
            # If the card is not revealed, draw the back of the card
            if not revealed[card_x][card_y]:
                pygame.draw.rect(DISPLAY, CARD_COLOR,
                    (x,y, CARD_SIZE, CARD_SIZE))
            # If the card is revealed, draw its picture
            else:
                shape = board[card_x][card_y][0]
                color = board[card_x][card_y][1]
                drawCard(shape, color, card_x, card_y)


# Reveal the cards
def showCardAnimation(board, cards_show):
    # Show the cards at specified speed
    for cover in range(CARD_SIZE, -SPEED * 4, -SPEED * 4):
        for card in cards_show:
            x, y = getCoordinates(card[0], card[1])
            pygame.draw.rect(DISPLAY, BG_COLOR, (x, y, CARD_SIZE, CARD_SIZE))
            shape, color = getCard(board, card[0], card[1])
            drawCard(shape, color, card[0], card[1])
            if cover > 0:
                pygame.draw.rect(DISPLAY, CARD_COLOR, (x, y, cover, CARD_SIZE))
            pygame.display.update()
            CLOCK.tick(FPS)


# Cover the cards that do not match
def hideCardAnimation(board, cards_hide):
    # Recover the cards at the specified speed
    for cover in range(0, CARD_SIZE + SPEED, 4 * SPEED):
        for card in cards_hide:
            x, y = getCoordinates(card[0], card[1])
            pygame.draw.rect(DISPLAY, BG_COLOR, (x, y, CARD_SIZE, CARD_SIZE))
            shape, color = getCard(board, card[0], card[1])
            drawCard(shape, color, card[0], card[1])
            if cover > 0:
                pygame.draw.rect(DISPLAY, CARD_COLOR, (x, y, cover, CARD_SIZE))
            pygame.display.update()
            CLOCK.tick(FPS)


# Convert mouse coordinates into card coordinates
def getPosition(x, y):
    # If the mouse is outside the margins don't return anything
    if x < X_MARGIN or y < Y_MARGIN:
        return None, None
    else:
        card_x = (y - Y_MARGIN) // (CARD_SIZE + GAP_SIZE)
        card_y = (x - X_MARGIN) // (CARD_SIZE + GAP_SIZE)
        # If the mouse is not on a card don't return anything
        if card_x >= BOARD_HEIGHT or card_y >= BOARD_WIDTH:
            return None, None
        elif (card_x - X_MARGIN) % (CARD_SIZE + GAP_SIZE) > CARD_SIZE or \
            (card_y - Y_MARGIN) % (CARD_SIZE + GAP_SIZE) > CARD_SIZE:
            return None, None
        else:
            return card_x, card_y


# Get the position of the card (upper left corner)
def getCoordinates(x, y):
    card_x = X_MARGIN + y * (CARD_SIZE + GAP_SIZE)
    card_y = Y_MARGIN + x * (CARD_SIZE + GAP_SIZE)
    return card_x, card_y


# Get the card's shape and color
def getCard(board, card_x, card_y):
    return board[card_x][card_y][0], board[card_x][card_y][1]


# Draw the shape on the card
def drawCard(shape, color, card_x, card_y):
    # Get sizes of parts of the cards for help with drawing
    half = int(CARD_SIZE * 0.5)
    quarter = int(CARD_SIZE * 0.25)

    # Get the coordinates of the upper left corner of card
    x, y = getCoordinates(card_x, card_y)

    # Draw the card based on shape and color specified
    if shape == CIRCLE:
        pygame.draw.circle(DISPLAY, color, (x + half, y + half), half - 10)
    elif shape == TRIANGLE:
        pygame.draw.polygon(DISPLAY, color, ((x + half, y + quarter),
        (x + quarter, y + CARD_SIZE - quarter),
        (x + CARD_SIZE - quarter, y + CARD_SIZE - quarter)))
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAY, color, (x + quarter, y + quarter,
        CARD_SIZE - half, CARD_SIZE - half))


# Check if the user has won the game
def gameWon(revealed):
    for i in revealed:
        if False in i:
            return False
    return True


# Flash colors of the screen when the user wins the game
def gameWonAnimation(board, revealed):
    color1 = BG_COLOR
    color2 = DARK_BG_COLOR
    # Switch the color of the background 16 times quickly
    for i in range(16):
        color1, color2 = color2, color1
        DISPLAY.fill(color1)
        drawBoard(board, revealed)
        pygame.display.update()
        pygame.time.wait(300)


if __name__ == '__main__':
    main()
