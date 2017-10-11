import pygame
import sys
import random


def load():
    PLAYERS_LIST = [
        'assets/sprites/moodyManLeft.png',
        'assets/sprites/moodyManRight.png'
    ]


    PLAYER_NEUTRAL = 'assets/sprites/moodyManNeutral.png'

    BACKGROUNDS_LIST = [
        'assets/sprites/bgdark.png',
        'assets/sprites/bg.png'
    ]

    BLACK_BG = 'assets/sprites/black.png'

    PIPES_LIST = ['assets/sprites/wife.png']

    IMAGES = {}

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

    player_neutral = pygame.image.load(PLAYER_NEUTRAL).convert_alpha()
    player_neutral = pygame.transform.scale(player_neutral, (
        int(player_neutral.get_width()*2), int(player_neutral.get_height()*2)))
    IMAGES['playerNeutral'] = player_neutral
    
    # select random background sprites
    # randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
    # IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()
    IMAGES['background'] = pygame.image.load(BLACK_BG).convert()

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

    return IMAGES

