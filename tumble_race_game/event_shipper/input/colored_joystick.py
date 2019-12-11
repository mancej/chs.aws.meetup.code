import pygame


class ColoredJoystick:

    def __init__(self, index: int, color: str):
        self.color = color
        self.index = index
        self.joystick = pygame.joystick.Joystick(index)
        self.joystick.init()


class MockJoystick:
    def __init__(self, index: int, color: str):
        self.color = color
        self.index = index
