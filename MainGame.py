import logging
import pygame
import random
import pickle  # pickle is used for high score saving
import os
import Button

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'  # this centers the window to the center of the user's screen

logging.basicConfig(filename='snake.log', level=logging.DEBUG,
                    format='%(levelname)s:	%(message)s	%(asctime)s',
                    datefmt='%d/%m/%Y	%I:%M:%S %p', filemode='w')
logging.info('The Game has booted')
# Color definitions
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
lightRed = (249, 52, 52)
green = (0, 155, 0)
lightGreen = (74, 196, 74)

# Game property constants
blockSize = 20
displayWidth = 800
displayHeight = 600
centerDisplayWidth = displayWidth / 2
centerDisplayHeight = displayHeight / 2
boundX = displayWidth - (blockSize * 2)
boundY = displayHeight - (blockSize * 2)
scoreOffsetX = 140
scoreOffsetY = 27
scoreBoundWidth = displayWidth - 180
scoreBoundHeight = 100 - blockSize

FPS = 10

# Game variables
bAcceptButton = True
degrees = 270
randAppleX, randAppleY = (0,) * 2
randCherryX, randCherryY = (0,) * 2
randEggplantX, randEggplantY = (0,) * 2
endCherryTime = 0
bCherry = False
bEggplant = False
goldenApple = random.randint(1, 10) == 10
leadX = centerDisplayWidth
leadY = centerDisplayHeight
leadXChange = blockSize
leadYChange = 0
appleCounter = 0    # This keeps the length of the snake
scoreCounter = 0   # This keeps the score
highScore = 0
buttonWidth = 150
buttonHeight = 50
snakeList = []
moveList = []
foodList = []# Apple, Golden Apple, Cherries, Eggplant, Chilly, Fire, Fire Lord
foodTimerList = []# Apple, Golden Apple, Cherries, Eggplant, Chilly, Fire, Fire Lord

fIXApple = len(foodList); foodList.append([]); foodTimerList.append("NA")
fIXGoldenApple = len(foodList); foodList.append([]); foodTimerList.append("NA")
fIXCherry = len(foodList); foodList.append([]); foodTimerList.append(5000)
fIXEggplant = len(foodList); foodList.append([]); foodTimerList.append(5000)
fIXChilly = len(foodList); foodList.append([]); foodTimerList.append(4000)
fIXFire = len(foodList); foodList.append([]); foodTimerList.append(5000)
fIXFireLord = len(foodList); foodList.append([]); foodTimerList.append(5000)

bWrap = True

# Importing font
bodyFont = pygame.font.SysFont("comicsansms", 50)
buttonFont = pygame.font.SysFont("comicsansms", 25)

# Importing images
snakeHeadImage = pygame.image.load("images/SnakeHead.png")
snakeBodyImage = pygame.image.load("images/SnakeBody.png")
blueHeadImage = pygame.image.load("images/BlueHead.png")
blueBodyImage = pygame.image.load("images/BlueBody.png")
appleImage = pygame.image.load("images/Apple.png")
cherryImage = pygame.image.load("images/CherryTrans.png")
eggplantImage = pygame.image.load("images/Berry.png")
goldenAppleImage = pygame.image.load("images/GoldenApple.png")
icon = pygame.image.load("images/Icon.png")

# Configuring display
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Snake")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

startButton = Button.button(green, lightGreen, gameDisplay, "START", centerDisplayWidth - (buttonWidth / 2),
                            centerDisplayHeight - 30, buttonWidth, buttonHeight, white, -30, centerDisplayWidth,
                            centerDisplayHeight, buttonFont)

quitButton = Button.button(red, lightRed, gameDisplay, "QUIT", centerDisplayWidth - (buttonWidth / 2),
                           centerDisplayHeight + 50, buttonWidth, buttonHeight, white, 50, centerDisplayWidth,
                           centerDisplayHeight, buttonFont)

# High score loading
try:
    with open('score.dat', 'rb') as file:
        highScore = pickle.load(file)
except:
    highScore = 0
    with open('score.dat', 'wb') as file:
        pickle.dump(highScore, file)

def startScreen():
    """
    This function loads the start screen of the game.
    :return:
    """
    while True:
        fillBackground(True)
        put_message_custom("Welcome to Snake!", green, -80)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitProgram()

        startButton.showButton()
        quitButton.showButton()

        if startButton.isHovered(getCursorPos()) and isLeftMouseClicked():
            reset()
            return
        elif quitButton.isHovered(getCursorPos()) and isLeftMouseClicked():
            quitProgram()

        pygame.display.update()


def showScores(score, new):
    """
    This function displays the scores on the display.
    :param score:
    :param new:
    :return:
    """
    screen_text = pygame.font.SysFont("comicsansms", 15).render("Score: " + str(score), True, black)
    gameDisplay.blit(screen_text, (displayWidth - scoreOffsetX, scoreOffsetY + 20))

    high_score = pygame.font.SysFont("comicsansms", 15).render("High Score: " + str(highScore), True, black)

    if new:
        high_score = pygame.font.SysFont("comicsansms", 13).render("New High Score!", True, red)

    gameDisplay.blit(high_score, (displayWidth - scoreOffsetX, scoreOffsetY))


def pause():
    """
    This function handles the paused event.
    :return:
    """
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitProgram()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        put_message_center("Game Paused", black, )
        put_message_custom("Click to resume..", black, fontSize=30, offsetY=50)
        pygame.display.update()


def randomApple():
    """
    This function handles the random apple generation.
    :return:
    """
    global fIXApple;
    global fIXGoldenApple;
    global fIXCherry;
    global fIXEggplant;
    global fIXChilly;
    global fIXFire;
    global fIXFireLord
    global randAppleX
    global randAppleY
    global goldenApple
    global bCherry
    global randCherryX
    global randCherryY
    global bEggplant
    global randEggplantX
    global randEggplantY
    global foodList

    if random.randint(1, 5) == 1:
        generateThing(fIXGoldenApple, 1)
    else:
        generateThing(fIXApple, 1)

    if random.randint(1, 3) == 1:
        generateThing(fIXCherry, 1)

def generateGoldenApple():
    """
    This function returns if a golden apple should be generated or not.
    :return:
    """
    return random.randint(1, 5) == 1


def generateThing(index, number):
    """
    This will generate anything that can be generated given the index
    :param index:
    :return:
    """
    global foodList
    global foodTimerList
    global blockSize
    global boundX
    global boundY
    count = 0
    while count < number:
        bFound = False
        while bFound is False:
            X = round(random.randint(blockSize * 2, boundX - (blockSize * 4)) / blockSize) * blockSize
            Y = round(random.randint(blockSize * 2, boundY - (blockSize * 4)) / blockSize) * blockSize
            if [X, Y] in snakeList or (X >= scoreBoundWidth and Y <= scoreBoundHeight) or [X, Y] is [leadX, leadY]:
                logging.debug('Stopped spawning food on top of the snake')
                break
            for array in foodList:
                for coord in array:
                    if [X, Y] is [coord[0], coord[1]]:
                        logging.debug('Stopped stacking food on top of each other')
                        break
            ticket = "NA"
            if foodTimerList[index] is not "NA":
                ticket = len(foodList) + index
                pygame.time.set_timer(ticket, foodTimerList[index])
                logging.debug('que item ' + index.__str__() + ' for ' + foodTimerList[index].__str__() + 'ms')

            foodList[index].append([X, Y, ticket])
            count += 1
            bFound = True


def resolveThing(index, entry, bConsumed):
    """
    :param index: refers to the index of the item..ie. fIXCherry
    :param entry: refers to the co-ords and ticket
    :param bConsumed: True if the thing (index) was eaten
    :return: performs the function upon resolution of the 'Thing'
    """
    global fIXApple; global fIXGoldenApple; global fIXCherry; global fIXEggplant; global fIXChilly; global fIXFire; global fIXFireLord
    global scoreCounter; global appleCounter
    global bWrap

    foodList[index].remove(entry)

    if index is fIXApple:
        if bConsumed:
            apples = 1 + len(foodList[fIXApple]) + len(foodList[fIXGoldenApple])
            if apples is 1 or (apples > 1 and random.randint(1, 100) <= 103 - apples*apples):
                if random.randint(1, 6) <= 1:
                    generateThing(fIXGoldenApple, 1)
                else:
                    generateThing(fIXApple, 1)
            if random.randint(1, 4) == 1:
                generateThing(fIXCherry, 1)
            if random.randint(1, 5) == 1 and bWrap is False and len(foodList[fIXEggplant]) is 0:
                generateThing(fIXEggplant, 1)
            scoreCounter += 1
            appleCounter += 1
            logging.debug('Ate Red Apple at (' + entry[0].__str__() + ', ' + entry[1].__str__() + ')')

    elif index is fIXGoldenApple:
        if bConsumed:
            apples = 1 + len(foodList[fIXGoldenApple])
            if random.randint(1, 100) <= 103 - 3*apples*apples:
                generateThing(fIXGoldenApple, 2)
            else:
                generateThing(fIXApple, 2)
            if random.randint(1, 4) == 1:
                generateThing(fIXCherry, 2)
            scoreCounter += 2
            appleCounter += 1
            logging.debug('Ate Gold Apple at (' + entry[0].__str__() + ', ' + entry[1].__str__() + ')')

    elif index is fIXEggplant:
        if bConsumed:
            bWrap = True
            generateThing(fIXEggplant, 1)
            logging.debug('Ate Eggplant at (' + entry[0].__str__() + ', ' + entry[1].__str__() + ')')
        logging.debug('Eggplant timed out at (' + entry[0].__str__() + ', ' + entry[1].__str__() + ')')

    elif index is fIXCherry:
        if bConsumed:
            scoreCounter += 3
            logging.debug('Ate Cherry at (' + entry[0].__str__() + ', ' + entry[1].__str__() + ')')
        logging.debug('Eggplant timed out at (' + entry[0].__str__() + ', ' + entry[1].__str__() + ')')


def snake(snakeCoors):
    """
    This function handles blitting the snake and rotating the head of the snake.
    :param snakeCoors:
    :return:
    """

    if bWrap:
        rotatedHead = pygame.transform.rotate(blueHeadImage, degrees)
        for coor in snakeCoors[:-1]:
            gameDisplay.blit(blueBodyImage, [coor[0], coor[1]])
    else:
        rotatedHead = pygame.transform.rotate(snakeHeadImage, degrees)

        for coor in snakeCoors[:-1]:
            gameDisplay.blit(snakeBodyImage, [coor[0], coor[1]])

    gameDisplay.blit(rotatedHead, (snakeCoors[-1][0], snakeCoors[-1][1]))


def put_message_center(message, color):
    """
    This function displays a message in the center of the screen.
    :param message:
    :param color:
    :return:
    """
    screen_text = bodyFont.render(message, True, color)
    gameDisplay.blit(screen_text, [centerDisplayWidth - (screen_text.get_rect().width / 2), centerDisplayHeight -
                                   (screen_text.get_rect().height / 2)])


def put_message_custom(message, color, offsetY, fontSize=50):
    """
    This function puts a message on the screen based off an offset to the center.
    :param message:
    :param color:
    :param offsetY:
    :param fontSize:
    :return:
    """
    screen_text = pygame.font.SysFont("comicsansms", fontSize).render(message, True, color)
    gameDisplay.blit(screen_text, [centerDisplayWidth - (screen_text.get_rect().width / 2),
                                   (centerDisplayHeight - (screen_text.get_rect().height / 2) + offsetY)])


def quitProgram():
    """
    This function quits the program.
    :return:
    """
    logging.debug("Exit Game")
    pygame.quit()
    exit()


def fillBackground(isStartScreen):
    """
    This function fills the game display background.
    :return:
    """
    gameDisplay.fill(black)
    gameDisplay.fill(white, [blockSize, blockSize, boundX, boundY])

    if not isStartScreen:
        gameDisplay.fill(black, [scoreBoundWidth, blockSize, displayWidth - 150, scoreBoundHeight])
        gameDisplay.fill(white, [(scoreBoundWidth + blockSize, blockSize), (blockSize * 7, 100 - (blockSize * 2))])


def reset():
    """
    This function resets all the variables to their default value (i.e. starting a new game)
    :return:
    """
    logging.info("Starting new game...")
    global bAcceptButton
    global appleCounter
    global scoreCounter
    global degrees
    global highScore
    global leadX
    global leadY
    global leadXChange
    global leadYChange
    global randAppleX
    global randAppleY
    global randCherryX
    global randCherryY
    global snakeList
    global moveList
    global foodList
    global foodTimerList
    foodList = []  # Apple, Golden Apple, Cherries, Eggplant, Chilly, Fire, Fire Lord
    foodTimerList = []  # Apple, Golden Apple, Cherries, Eggplant, Chilly, Fire, Fire Lord

    global fIXApple; global fIXGoldenApple; global fIXCherry; global fIXEggplant; global fIXChilly; global fIXFire; global fIXFireLord

    fIXApple = len(foodList); foodList.append([]); foodTimerList.append("NA")
    fIXGoldenApple = len(foodList); foodList.append([]); foodTimerList.append("NA")
    fIXCherry = len(foodList); foodList.append([]); foodTimerList.append(5000)
    fIXEggplant = len(foodList); foodList.append([]); foodTimerList.append(5000)
    fIXChilly = len(foodList); foodList.append([]); foodTimerList.append(4000)
    fIXFire = len(foodList); foodList.append([]); foodTimerList.append(5000)
    fIXFireLord = len(foodList); foodList.append([]); foodTimerList.append(5000)

    global bWrap
    global goldenApple
    global bCherry
    global bEggplant
    bAcceptButton = True
    bCherry = False
    bEggplant = False
    bWrap = True

    degrees = 270
    leadX = centerDisplayWidth
    leadY = centerDisplayHeight
    leadXChange = blockSize
    leadYChange = 0
    randAppleX, randAppleY, appleCounter, scoreCounter, randCherryX, randCherryY = (0,) * 6
    snakeList = []
    moveList = []
    goldenApple = generateGoldenApple()

    logging.info("Parameters Initialized")


def gameLoop():
    """
    This is the main game loop, called by startScreen() earlier.
    :return:
    """
    global bAcceptButton
    global appleCounter
    global scoreCounter
    global degrees
    global highScore
    global leadX
    global leadY
    global leadXChange
    global leadYChange
    global snakeList
    global moveList
    global foodList
    global foodTimerList
    global bWrap
    global goldenApple
    global bCherry
    global bEggplant
    global FPS
    leadXChange = blockSize
    leadYChange = 0
    gameOver = False
    bWrap = True
    goldenApple = generateGoldenApple()


    generateThing(fIXApple, 1)

    while True:
        events = pygame.event.get()
        fillBackground(False)

        while gameOver:  # the user lost
            logging.info("Score\t" + scoreCounter.__str__())
            if highScore < scoreCounter:
                # set new high score if applicable
                with open('score.dat', 'rb') as fromFile:
                    highScore = pickle.load(fromFile)
                with open('score.dat', 'wb') as fromFile:
                    pickle.dump(scoreCounter, fromFile)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quitProgram()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    reset()
                    gameLoop()


            fillBackground(False)
            showScores(scoreCounter, highScore < scoreCounter)
            put_message_center("Game Over!", red)
            put_message_custom("Click to play again.", black, fontSize=30, offsetY=50)
            pygame.display.update()

        for event in events:
            if event.type == pygame.QUIT:
                quitProgram()
            if event.type == 17:
                bCherry = False
            if event.type == 18:
                bEggplant = False
            for thing in foodList:
                for array in thing:
                    if event.type == array[2]:
                        resolveThing(foodList.index(thing), array, False)

            if len(moveList) > 0 and bAcceptButton:
                if moveList[0] == "L" and (len(snakeList) < 2 or degrees != 270):
                    leadXChange = -blockSize
                    leadYChange = 0
                    degrees = 90
                elif (len(snakeList) < 2 or degrees != 90) and (
                        moveList[0] == "R"):
                    leadXChange = blockSize
                    leadYChange = 0
                    degrees = 270
                elif (len(snakeList) < 2 or degrees != 180) and (moveList[0] == "U"):
                    leadYChange = -blockSize
                    leadXChange = 0
                    degrees = 0
                elif (len(snakeList) < 2 or degrees != 0) and (moveList[0] == "D"):
                    leadYChange = blockSize
                    leadXChange = 0
                    degrees = 180
                del moveList[0]
                bAcceptButton = False

            if event.type == pygame.KEYDOWN:  # key presses
                if (len(snakeList) < 2 or degrees != 270) and (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                    if bAcceptButton:
                        leadXChange = -blockSize
                        leadYChange = 0
                        degrees = 90
                    else:
                        moveList.append("L")
                elif (len(snakeList) < 2 or degrees != 90) and (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                    if bAcceptButton:
                        leadXChange = blockSize
                        leadYChange = 0
                        degrees = 270
                    else:
                        moveList.append("R")
                elif (len(snakeList) < 2 or degrees != 180) and (event.key == pygame.K_UP or event.key == pygame.K_w):
                    if bAcceptButton:
                        leadYChange = -blockSize
                        leadXChange = 0
                        degrees = 0
                    else:
                        moveList.append("U")
                elif (len(snakeList) < 2 or degrees != 0) and (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    if bAcceptButton:
                        leadYChange = blockSize
                        leadXChange = 0
                        degrees = 180
                    else:
                        moveList.append("D")
                elif event.key == pygame.K_p:
                    pause()
                bAcceptButton = False

        leadX += leadXChange
        leadY += leadYChange

        if bWrap:
            if leadX > boundX or (leadX >= scoreBoundWidth and leadY <= scoreBoundHeight and degrees == 270):
                leadX = blockSize
                bWrap = False
            elif leadX < blockSize:
                if leadY > scoreBoundHeight:
                    leadX = boundX
                else:
                    leadX = scoreBoundWidth - blockSize
                bWrap = False
            elif leadY < blockSize or (leadY <= scoreBoundHeight and leadX >= scoreBoundWidth and degrees == 0):
                leadY = boundY
                bWrap = False
            elif leadY > boundY:
                if leadX >= scoreBoundWidth:
                    leadY = scoreBoundHeight + blockSize
                else:
                    leadY = blockSize
                bWrap = False
        else:
            if (leadX > boundX or leadX < blockSize or leadY > boundY or leadY < blockSize) \
                        or (leadX >= scoreBoundWidth and leadY <= scoreBoundHeight):
                    logging.info("Snake hit the edge.")
                    gameOver = True


        for thing in foodList:
            for info in thing:  # if the snake has eaten the thing
                if leadX == info[0] and leadY == info[1]:
                    scoreCounter += 1
                    resolveThing(foodList.index(thing), info, True)

        snakeHead = [leadX, leadY]  # updates the snake's head location
        bAcceptButton = True

        if snakeHead in snakeList[:-1]:
            logging.info("Snake ate itself")
            gameOver = True

        snakeList.append(snakeHead)  # add the snakeHead
        snake(snakeList)  # generate the snake

        if len(snakeList) > appleCounter:  # delete the first element of the snakeList.
            del snakeList[0]
        for coord in foodList[fIXApple]:
            gameDisplay.blit(appleImage, (coord[0], coord[1]))
        for coord in foodList[fIXGoldenApple]:
            gameDisplay.blit(goldenAppleImage, (coord[0], coord[1]))
        for coord in foodList[fIXCherry]:
            gameDisplay.blit(cherryImage, (coord[0], coord[1]))
        for coord in foodList[fIXEggplant]:

            gameDisplay.blit(eggplantImage, (coord[0], coord[1]))

        with open('score.dat', 'rb') as fromFile:  # load high score
            highScore = pickle.load(fromFile)

        showScores(scoreCounter, highScore < scoreCounter)
        pygame.display.update()
        clock.tick(FPS + (appleCounter / 50))  # set FPS, scales with how many apples the user has

def getCursorPos():
    return pygame.mouse.get_pos()


def isLeftMouseClicked():
    return pygame.mouse.get_pressed()[0]


while True:
    startScreen()
    gameLoop()
