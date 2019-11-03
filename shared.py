# Screen Constant
SQUARE_SIZE = 50
FRAME_THICKNESS = 1
RADIUS = int(SQUARE_SIZE/2 - 6)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Board Constant
SNONE  = 0
SBLACK = 1
SWHITE = 2
DRAW = 3

# Othello Constant
COLUMN_COUNT = 8
ROW_COUNT = 8
SIZE = COLUMN_COUNT * ROW_COUNT

# Tensorflow Constant
FACTORS = 25
HIDDENS = 128
RESIDUALS = 8
OUTPUTS = SIZE

LEARNING_RATE = 2e-1
SAVE_STEPS = 10000
SAVE_MAX_TO_KEEP = 100

SUPERVISED_MODEL_NAME = 'smodel'
SEPERATOR = '-'
MODEL_FORMAT = '.h5'


