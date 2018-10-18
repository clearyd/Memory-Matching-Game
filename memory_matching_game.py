# Memory Matching Game
# By: Destiny Cleary

import pygame, random
from pygame.locals import *


#**********************Check these**********************************************
# Initialize constants for the game board
FPS = 30
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
CARD_SIZE = 40
GAP_SIZE = 10
BOARD_WIDTH = 6
BOARD_HEIGHT = 5
X_MARGIN = (WINDOW_WIDTH - (BOARD_WIDTH * (CARD_SIZE + GAP_SIZE))) // 2
Y_MARGIN = (WINDOW_HEIGHT - (BOARD_HEIGHT * (CARD_SIZE + GAP_SIZE))) // 2
# Make sure board size is even for pairs of cards
assert (BOARD_HEIGHT * BOARD_WIDTH) % 2 == 0

# Card Shape Colors
AQUA = (0, 255, 255)
GREEN = (0, 255, 0)
PLUM = (126, 53, 77)
MAGENTA = (255, 0, 255)
BLUE = (0, 3, 165)

COLORS = (AQUA, GREEN, PLUM, MAGENTA, BLUE)

# Display colors
BGCOLOR = (176, 226, 240)
CARDCOLOR = (24, 22, 32)
HIGHLIGHTCOLOR = (254, 19, 129)

# Shapes on cards
CIRCLE = 'circle'
TRIANGLE = 'triangle'
SQUARE = 'square'

SHAPES = (CIRCLE, TRIANGLE, SQUARE)
