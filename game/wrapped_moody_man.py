import pygame
import random
import sys
import game.moody_man_utils as utils
from pygame.locals import *



FPS = 30
SCREENWIDTH  = 272
SCREENHEIGHT = 408
GAP_BETWEEN_ONE_SET_OF_OBSTACLES = 110


pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Moody Man')
IMAGES = utils.load()


try:
    xrange
except NameError:
    xrange = range


class GameState:
    def __init__(self):
        self.score = 0
        self.playerx = int(SCREENWIDTH / 2)
        self.playery = int(SCREENHEIGHT * 0.8)

        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()
        newPipe3 = getRandomPipe()

         # list of upper pipes
        self.leftPipes = [
            {'x': newPipe1[0]['x'], 'y': newPipe1[0]['y'], 'width': newPipe1[0]['width'], 'is_scored': False},
            {'x': newPipe2[0]['x'], 'y': newPipe1[0]['y'] - (SCREENHEIGHT / 2), 'width': newPipe2[0]['width'], 'is_scored': False},
            {'x': newPipe3[0]['x'], 'y': newPipe1[0]['y'] - (SCREENHEIGHT / 2) * 2, 'width': newPipe3[0]['width'], 'is_scored': False}
        ]

        # list of lowerpipe
        self.rightPipes = [
            {'x': newPipe1[1]['x'], 'y': newPipe1[1]['y']},
            {'x': newPipe2[1]['x'], 'y': newPipe1[1]['y'] - (SCREENHEIGHT / 2)},
            {'x': newPipe3[1]['x'], 'y': newPipe1[1]['y'] - (SCREENHEIGHT / 2) * 2}
        ]

        self.pipeVelY = 5

        # player velocity, max velocity, downward accleration, accleration on flap
        self.playerVelX    =  0.5  # player's velocity along X, default same as playerFlapped
        self.playerMaxVelX =  7.5   # max vel along Y, max descend speed
        self.playerMinVelX =  -7.5   # min vel along Y, max ascend speed
        self.playerAccX    =   7.5   # players downward accleration
        self.playerFlapped = False
        self.gap_offset = 0
    
    
    def frame_step(self, input_actions):
        pygame.event.pump()
        reward = 0.1
        terminal = False

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')

        if input_actions[1] == 1:
            self.playerVelX = -1 / 10 * self.playerVelX
            self.playerAccX *= - 1
            self.playerFlapped = not self.playerFlapped


        # check for score
        playerMidPos = self.playery + IMAGES['playerNeutral'].get_height() / 2
        for pipe in self.leftPipes:
            pipeMidPos = pipe['y']
            if pipeMidPos >= playerMidPos and not pipe['is_scored']:
                pipe['is_scored'] = True
                self.score += 1
                reward = 1
                if self.score % 10 == 0:
                    self.gap_offset += 2
                    self.gap_offset = 10 if self.gap_offset > 10 else self.gap_offset
        
        # player's movement
        self.playerVelX += self.playerAccX
        if self.playerVelX > self.playerMaxVelX:
            self.playerVelX = self.playerMaxVelX
        
        
        if self.playerVelX < self.playerMinVelX:
            self.playerVelX = self.playerMinVelX

        self.playerx += self.playerVelX
        
        # pipe's movement
        for lPipe, rPipe in zip(self.leftPipes, self.rightPipes):
            lPipe['y'] += self.pipeVelY
            rPipe['y'] += self.pipeVelY
        
        # add new pipe and remove first pipe when it exceed bottom of screen
        if self.leftPipes[0]['y'] > SCREENHEIGHT:
            newPipe = getRandomPipe()
            self.leftPipes.append({'x': newPipe[0]['x'], 'y': self.leftPipes[-1]['y'] - SCREENHEIGHT / 2 + self.gap_offset, 'width': newPipe[0]['width'], 'is_scored': False})
            self.rightPipes.append({'x': newPipe[1]['x'], 'y': self.rightPipes[-1]['y'] - SCREENHEIGHT / 2 + self.gap_offset})
            self.leftPipes.pop(0)
            self.rightPipes.pop(0)


        isCrash = checkCrash({'x': self.playerx, 'y': self.playery}, self.leftPipes, self.rightPipes)
        if isCrash:
            terminal = True
            self.__init__()
            reward = -1

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for lPipe, rPipe in zip(self.leftPipes, self.rightPipes):
            startDrawX = lPipe['x']
            while startDrawX < (lPipe['x'] + lPipe['width']):
                SCREEN.blit(IMAGES['pipe'][0], (startDrawX, lPipe['y']))
                startDrawX += IMAGES['pipe'][0].get_width()

            startDrawX = rPipe['x']
            while startDrawX < SCREENWIDTH:
                SCREEN.blit(IMAGES['pipe'][0], (startDrawX, lPipe['y']))
                startDrawX += IMAGES['pipe'][0].get_width()

        # showScore(score)

        SCREEN.blit(IMAGES['player'][0] if self.playerFlapped else IMAGES['player'][1], (self.playerx, self.playery))
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        return image_data, reward, terminal

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

