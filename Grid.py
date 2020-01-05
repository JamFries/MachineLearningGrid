import pygame
import numpy as np
import GridSpace as gs
import Robot as r
import random

class Grid:

    def __init__(self, totalWidth, totalHeight, rows, columns):
        # info used to determine evenly spaced square/rectangles for the grid
        self.gridWidth = totalWidth
        self.gridHeight = totalHeight
        self.rows = rows
        self.columns = columns

        # find and store the measurements for a grid space
        self.gridSpaceWidth = totalWidth // columns
        self.gridSpaceHeight = totalHeight // rows

        #initialize a 2d-array to store all rectangles that will make the grid (array is rows by columns and stores gridSpaces)
        self.allGridSpaces = np.zeros(shape=(rows, columns), dtype=gs.GridSpace)
        # Instantiate pygame rectangles to be drawn for each grid space
        for i in range(rows):
            for j in range(columns):
                space = gs.GridSpace(j, i, self.gridSpaceWidth, self.gridSpaceHeight)
                space.arrayRow = i
                space.arrayColumn = j
                self.allGridSpaces[i][j] = space

        self.agent = r.Robot(0, 0) #initialize the agent for this grid
        self.gamma = 0.9
        self.values = np.zeros(shape=(self.rows, self.columns))
        self.valUp = np.zeros(shape=(self.rows, self.columns))
        self.valDown = np.zeros(shape=(self.rows, self.columns))
        self.valRight = np.zeros(shape=(self.rows, self.columns))
        self.valLeft = np.zeros(shape=(self.rows, self.columns))
        self.valStop = np.zeros(shape=(self.rows, self.columns))

        # choose a random gridSpace to be the goalState, startLocation, etc
        self.goalSpace = None




    #Method that draws the gridspaces onto a pygame surface
    def drawGrid(self, surface):
        #Draw every rectangle stored in the 2d-array
        for i in range(len(self.allGridSpaces)):
            for j in range(len(self.allGridSpaces[0])):
                rect = self.allGridSpaces[i][j] # holds a gridSpace object
                pygame.draw.rect(surface, rect.color, rect.rectangle)
                #rectRewardText = rect.rewardFont.render(str(rect.reward), False, (0, 0, 0))
                #surface.blit(rectRewardText, (rect.topLeftX + (rect.width // 2), rect.topLeftY + (rect.height // 2)))
                rectValueText = rect.rewardFont.render(str(self.values[i][j]), False, (0, 0, 0))
                surface.blit(rectValueText, (rect.topLeftX + (rect.width // 2), rect.topLeftY + (rect.height // 2)))
                # If this gridSpace contains the player, then draw a circle after the rect is drawn to indicate the player's spot on the grid
                if rect.containsPlayer:
                    centerX = rect.topLeftX + (rect.width // 2)
                    centerY = rect.topLeftY + (rect.height // 2)
                    radius = rect.width // 4
                    pygame.draw.circle(surface, (0, 0, 255), (centerX, centerY), radius)

    #Method that draws gridLines to more easily view the spaces
    def drawGridLines(self, surface):
        # For every row draw a horizontal line
        for i in range(self.rows):
            pygame.draw.line(surface, (0, 0, 0), (0, i*self.gridSpaceHeight), (self.gridWidth, i*self.gridSpaceHeight))
        # For every column draw a vertical line
        for i in range(self.columns):
            pygame.draw.line(surface, (0, 0, 0), (i*self.gridSpaceWidth, 0), (i*self.gridSpaceWidth, self.gridHeight))

    #Method that chooses a random grid position and makes it the goal
    def setRandomGoalState(self):
        #Check if there is no previous goalState
        if self.goalSpace is None:
            # Choose a random row and column
            randRow = random.randrange(0, self.rows)
            randCol = random.randrange(0, self.columns)

            # Sets the gridSpace object at that index to be the goalState
            self.allGridSpaces[randRow][randCol].isGoalState = True
            self.allGridSpaces[randRow][randCol].color = (0, 255, 0)  # set the goalState space to green
            self.goalSpace = self.allGridSpaces[randRow][randCol]
        else:
            # Choose a random row and column
            randRow = random.randrange(0, self.rows)
            randCol = random.randrange(0, self.columns)
            #Retry if the indices are the same as the previous goalState
            while randRow==self.goalSpace.arrayRow and randCol==self.goalSpace.arrayColumn:
                # Choose a random row and column
                randRow = random.randrange(0, self.rows)
                randCol = random.randrange(0, self.columns)
            #Set the old gridSpace to a normal space
            self.allGridSpaces[self.goalSpace.arrayRow][self.goalSpace.arrayColumn].isGoalState = False
            self.allGridSpaces[self.goalSpace.arrayRow][self.goalSpace.arrayColumn].color = (255, 255, 255)
            #Set the new goalState
            self.allGridSpaces[randRow][randCol].isGoalState = True
            self.allGridSpaces[randRow][randCol].color = (0, 255, 0)  # set the goalState space to green
            self.goalSpace = self.allGridSpaces[randRow][randCol]

    #Method that sets up a specified number of obstacles
    def setObstacles(self, numOfObstacles):
        for i in range(numOfObstacles):
            randRow = random.randrange(0, self.rows)
            randCol = random.randrange(0, self.columns)
            while self.allGridSpaces[randRow][randCol].isObstacle or self.allGridSpaces[randRow][randCol].isGoalState: #ensure location is not the goal or an existing obstacle
                randRow = random.randrange(0, self.rows)
                randCol = random.randrange(0, self.columns)
            self.allGridSpaces[randRow][randCol].isObstacle = True
            self.allGridSpaces[randRow][randCol].color = (125, 125, 125)



    #Method that assigns reward values to each state
    def setRewards(self):
        #Option 1: Static values for each type of gridspace (goal=100, normal=0, obstacle=-1, etc)
        for i in range(len(self.allGridSpaces)):
            for j in range(len(self.allGridSpaces[0])):
                if self.allGridSpaces[i][j].containsPlayer == False:
                    if self.allGridSpaces[i][j].isGoalState:
                        self.allGridSpaces[i][j].reward = 10
                    elif self.allGridSpaces[i][j].isObstacle:
                        self.allGridSpaces[i][j].reward = -1000 # -1000 allows for obvious no traversal without having to modify transition values by checking for obstacles as well
                    else:
                        self.allGridSpaces[i][j].reward = 0
        #Option 2: Random values for all states except for the goalState and starting state
        # for i in range(len(self.allGridSpaces)):
        #     for j in range(len(self.allGridSpaces[0])):
        #         if self.allGridSpaces[i][j].containsPlayer == False:
        #             if self.allGridSpaces[i][j].isGoalState:
        #                 self.allGridSpaces[i][j].reward = 10 #goalState reward is 10
        #             else:
        #                 randVal = (random.random() - 0.5) * 2  # Allows for a random value from -1 to 1
        #                 self.allGridSpaces[i][j].reward = randVal

    #Method that assigns a starting location for the robot to traverse the grid
    def setStartingLocation(self):
        goalRow = self.goalSpace.arrayRow
        goalCol = self.goalSpace.arrayColumn
        # Choose a random row and column
        randRow = random.randrange(0, self.rows)
        randCol = random.randrange(0, self.columns)
        while (randRow==goalRow and randCol==goalCol) or self.allGridSpaces[randRow][randCol].isObstacle: #Ensure the player doesnt start at the goal or in a wall
            # Choose a random row and column
            randRow = random.randrange(0, self.rows)
            randCol = random.randrange(0, self.columns)
        # Set the starting location to the gridSpace of the random indices
        self.allGridSpaces[randRow][randCol].containsPlayer = True #Sets the gridSpace holding the agent to true
        self.agent.posRow = randRow
        self.agent.posCol = randCol
        self.agent.path.append((self.agent.posRow, self.agent.posCol))

    #Method that runs value iteration on the environment
    def valueIteration(self, numOfIterations):
        for i in range(numOfIterations):
            self.calculateValueUp()
            self.calculateValueDown()
            self.calculateValueRight()
            self.calculateValueLeft()
            self.calculateValueStop()
            for j in range(self.rows):
                for k in range(self.columns):
                    val = max(self.valUp[j][k], self.valDown[j][k], self.valRight[j][k], self.valLeft[j][k], self.valStop[j][k])
                    self.values[j][k] = val
    def calculateValueUp(self):
        # start at row 1 because row 0 has nothing above to check
        for i in range(1, self.rows):
            for j in range(0, self.columns):
                self.valUp[i][j] = -1 + (self.allGridSpaces[i][j].reward) + self.gamma * self.values[i-1][j]
    def calculateValueDown(self):
        for i in range(0, self.rows-1):
            for j in range(0, self.columns):
                self.valDown[i][j] = -1 + (self.allGridSpaces[i][j].reward) + self.gamma * self.values[i+1][j]
    def calculateValueRight(self):
        for i in range(0, self.rows):
            for j in range(0, self.columns-1):
                self.valRight[i][j] = -1 + (self.allGridSpaces[i][j].reward) + self.gamma * self.values[i][j+1]
    def calculateValueLeft(self):
        for i in range(0, self.rows):
            for j in range(1, self.columns):
                self.valLeft[i][j] = -1 + (self.allGridSpaces[i][j].reward) + self.gamma * self.values[i][j-1]
    def calculateValueStop(self):
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                self.valStop[i][j] = (self.allGridSpaces[i][j].reward) + self.gamma * self.values[i][j]