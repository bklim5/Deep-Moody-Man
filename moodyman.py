import pygame
import random
import sys
from pygame.locals import *


FPS = 30
SCREENWIDTH  = 272
SCREENHEIGHT = 408

GAP_BETWEEN_ONE_SET_OF_OBSTACLES = 110

# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

PLAYERS_LIST = [
    'assets/sprites/moodyManLeft.png',
    'assets/sprites/moodyManRight.png'
]


PLAYER_NEUTRAL = 'assets/sprites/moodyManNeutral.png'

BACKGROUNDS_LIST = [
    'assets/sprites/bgdark.png',
    'assets/sprites/bg.png'
]

PIPES_LIST = ['assets/sprites/wife.png']


try:
    xrange
except NameError:
    xrange = range


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Moody Man')

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )

    while True:
        player_neutral = pygame.image.load(PLAYER_NEUTRAL).convert_alpha()
        player_neutral = pygame.transform.scale(player_neutral, (
            int(player_neutral.get_width()*2), int(player_neutral.get_height()*2)))
        IMAGES['playerNeutral'] = player_neutral
        
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        # select random player sprites
        player_left = pygame.image.load(PLAYERS_LIST[0]).convert_alpha()
        player_left = pygame.transform.scale(player_left, (
            int(player_left.get_width()*2), int(player_left.get_height()*2)))
        player_right = pygame.image.load(PLAYERS_LIST[1]).convert_alpha()
        player_right = pygame.transform.scale(player_right, (
            int(player_right.get_width()*2), int(player_right.get_height()*2)))
         
        IMAGES['player'] = [
            player_left,
            player_right
        ]

        # select random pipe sprites
        wife = pygame.image.load(PIPES_LIST[0]).convert_alpha()
        wife = pygame.transform.scale(wife, (
            int(wife.get_width()*0.5), int(wife.get_height()*0.5)))
        IMAGES['pipe'] = [
            wife
        ]

        # hismask for pipes
        HITMASKS['pipe'] = [
            getHitmask(IMAGES['pipe'][0])
        ]

        # hitmask for player
        HITMASKS['player'] = [
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
        ]

        movementInfo = showWelcomeAnimation()
        crashInfo = mainGame(movementInfo)


def showWelcomeAnimation():
    playerx = int(SCREENWIDTH / 2)
    playery = int(SCREENHEIGHT * 0.8)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # make first flap sound and return values for mainGame
                return {
                    'playerx': playerx
                }
        
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['playerNeutral'],
                    (playerx - IMAGES['playerNeutral'].get_width() / 2, playery))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame(movementInfo):
    score = playerIndex = loopIter = 0
    playerx = movementInfo['playerx']
    playery = int(SCREENHEIGHT * 0.8)

    # get 2 obstacles
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    newPipe3 = getRandomPipe()

    # list of upper pipes
    leftPipes = [
        {'x': newPipe1[0]['x'], 'y': newPipe1[0]['y'], 'width': newPipe1[0]['width'], 'is_scored': False},
        {'x': newPipe2[0]['x'], 'y': newPipe1[0]['y'] - (SCREENHEIGHT / 2), 'width': newPipe2[0]['width'], 'is_scored': False},
        {'x': newPipe3[0]['x'], 'y': newPipe1[0]['y'] - (SCREENHEIGHT / 2) * 2, 'width': newPipe3[0]['width'], 'is_scored': False}
    ]

    # list of lowerpipe
    rightPipes = [
        {'x': newPipe1[1]['x'], 'y': newPipe1[1]['y']},
        {'x': newPipe2[1]['x'], 'y': newPipe1[1]['y'] - (SCREENHEIGHT / 2)},
        {'x': newPipe3[1]['x'], 'y': newPipe1[1]['y'] - (SCREENHEIGHT / 2) * 2}
    ]

    pipeVelY = 5

    # player velocity, max velocity, downward accleration, accleration on flap
    playerVelX    =  0.5  # player's velocity along X, default same as playerFlapped
    playerMaxVelX =  7.5   # max vel along Y, max descend speed
    playerMinVelX =  -7.5   # min vel along Y, max ascend speed
    playerAccX    =   7.5   # players downward accleration
    playerFlapped = False
    gap_offset = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                playerVelX = -1 / 10 * playerVelX
                playerAccX *= - 1
                playerFlapped = not playerFlapped

        # check for score
        playerMidPos = playery + IMAGES['playerNeutral'].get_height() / 2
        for pipe in leftPipes:
            pipeMidPos = pipe['y']
            if pipeMidPos >= playerMidPos and not pipe['is_scored']:
                pipe['is_scored'] = True
                score += 1
                if score % 10 == 0:
                    gap_offset += 2
                    gap_offset = 10 if gap_offset > 10 else gap_offset
        
        
        playerVelX += playerAccX
        if playerVelX > playerMaxVelX:
            playerVelX = playerMaxVelX
        
        
        if playerVelX < playerMinVelX:
            playerVelX = playerMinVelX

        playerx += playerVelX
        

        for lPipe, rPipe in zip(leftPipes, rightPipes):
            lPipe['y'] += pipeVelY
            rPipe['y'] += pipeVelY
        
        if leftPipes[0]['y'] > SCREENHEIGHT:
            newPipe = getRandomPipe()
            leftPipes.append({'x': newPipe[0]['x'], 'y': leftPipes[-1]['y'] - SCREENHEIGHT / 2 + gap_offset, 'width': newPipe[0]['width'], 'is_scored': False})
            rightPipes.append({'x': newPipe[1]['x'], 'y': rightPipes[-1]['y'] - SCREENHEIGHT / 2 + gap_offset})
            leftPipes.pop(0)
            rightPipes.pop(0)

        isCrash = checkCrash({'x': playerx, 'y': playery}, leftPipes, rightPipes)
        if isCrash:
            return         

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for lPipe, rPipe in zip(leftPipes, rightPipes):
            startDrawX = lPipe['x']
            while startDrawX < (lPipe['x'] + lPipe['width']):
                SCREEN.blit(IMAGES['pipe'][0], (startDrawX, lPipe['y']))
                startDrawX += IMAGES['pipe'][0].get_width()

            startDrawX = rPipe['x']
            while startDrawX < SCREENWIDTH:
                SCREEN.blit(IMAGES['pipe'][0], (startDrawX, lPipe['y']))
                startDrawX += IMAGES['pipe'][0].get_width()

        showScore(score)

        SCREEN.blit(IMAGES['player'][0] if playerFlapped else IMAGES['player'][1], (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        

def checkCrash(player, leftPipes, rightPipes):
    player['w'] = IMAGES['playerNeutral'].get_width()
    player['h'] = IMAGES['playerNeutral'].get_height()

    # if crashes wall
    if player['x'] + player['w'] > SCREENWIDTH + 2 or player['x'] < -2:
        return True
    else:
        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        pipeH = IMAGES['pipe'][0].get_height()

        for lPipe, rPipe in zip(leftPipes, rightPipes):
            # upper and lower pipe rects
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], lPipe['width'], pipeH)
            rPipeRect = pygame.Rect(rPipe['x'], rPipe['y'], lPipe['width'], pipeH)

            # # player and upper/lower pipe hitmasks
            # pHitMask = HITMASKS['player'][pi]
            # lHitmask = HITMASKS['pipe'][0]
            # rHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            lCollide = playerRect.colliderect(lPipeRect)
            rCollide = playerRect.colliderect(rPipeRect)

            if lCollide or rCollide:
                return True

    return False


def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    width = random.randint(0, 2) * IMAGES['pipe'][0].get_width() + IMAGES['pipe'][0].get_width()
    return [
        {'x': 0, 'y': 10, 'width': width},  # left obstacles
        {'x': width + GAP_BETWEEN_ONE_SET_OF_OBSTACLES, 'y': 10} # right obstacles
    ]


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask


if __name__ == '__main__':
    main()
