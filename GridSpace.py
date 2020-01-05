import pygame
import numpy

class GridSpace:
    # A gridSpace is a pygame Rect object with extra variables to track if a space is a goal, obstacle, etc
    def __init__(self, topLeftX, topLeftY, width, height, isGoalState=False, isObstacle=False):
        self.width = width
        self.height = height
        self.rectangle = pygame.Rect(topLeftX*width, topLeftY*height, width, height)
        self.topLeftX = topLeftX*width
        self.topLeftY = topLeftY*height
        self.bottomRightX = self.topLeftX + width
        self.bottomRightY = self.topLeftY + height

        #Initialize conditional variables
        self.isGoalState = isGoalState
        self.isObstacle = isObstacle
        self.containsPlayer = False

        self.reward = 0
        self.value = 0
        self.rewardFont = pygame.font.SysFont('Times New Roman', 12)
        #self.rewardRect = self.rewardFont.render(str(self.reward), False, (0, 0, 0)) #Creates surface with text containing reward for gridspace on it

        # Used to keep track of a specific gridSpace in the 2d-array that represents the grid
        self.arrayRow = -1
        self.arrayColumn = -1

        #Set color based on what the gridSpace is
        if isGoalState:
            self.color = (0, 255, 0) # green
        elif isObstacle:
            self.color = (125, 125, 125) # something
        else:
            self.color = (255, 255, 255) # white

    #Method to draw the gridSpace, which is just a pygame rectangle
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rectangle)