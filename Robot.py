import pygame
import numpy
import random

class Robot:

    def __init__(self, posRow, posColumn):
        #Stores the indices where the robot is on the grid. This can be used to help draw onto a pygame surface
        self.posRow = posRow
        self.posCol = posColumn
        self.path = [] #list used to store the total path taken to get to the goalState

    #Method to move the agent to a new gridSpace in the grid (by using the values array to take the maximum value)
    def move(self, grid):
        currentValue = grid.values[self.posRow][self.posCol] # Will be compared with values of other states to determine where the robot moves
        #Account for corners of grid before more general conditions
        if self.posRow==0 and self.posCol==0: #top left of the grid
            down = self.lookDown(grid)
            right = self.lookRight(grid)
            maxVal = max([currentValue, down, right]) #Gets the best choice from the available actions
            if maxVal==down:
                self.moveDown(grid)
            elif maxVal==right:
                self.moveRight(grid)
            else:
                self.noMove(grid)
        elif self.posRow==0 and self.posCol==(len(grid.allGridSpaces[0])-1): #top right of the grid
            down = self.lookDown(grid)
            left = self.lookLeft(grid)
            maxVal = max([currentValue, down, left])  # Gets the best choice from the available actions
            if maxVal==down:
                self.moveDown(grid)
            elif maxVal==left:
                self.moveLeft(grid)
            else:
                self.noMove(grid)
        elif self.posRow==(len(grid.allGridSpaces)-1) and self.posCol==0: #bottom left of the grid
            up = self.lookUp(grid)
            right = self.lookRight(grid)
            maxVal = max([currentValue, up, right])  # Gets the best choice from the available actions
            if maxVal==up:
                self.moveUp(grid)
            elif maxVal==right:
                self.moveRight(grid)
            else:
                self.noMove(grid)
        elif self.posRow==(len(grid.allGridSpaces)-1) and self.posCol==(len(grid.allGridSpaces[0])-1): #bottom right of the grid
            up = self.lookUp(grid)
            left = self.lookLeft(grid)
            maxVal = max([currentValue, up, left])  # Gets the best choice from the available actions
            if maxVal==up:
                self.moveUp(grid)
            elif maxVal==left:
                self.moveLeft(grid)
            else:
                self.noMove(grid)
        elif self.posRow == 0: #top row of grid. so dont move up
            down = self.lookDown(grid)
            right = self.lookRight(grid)
            left = self.lookLeft(grid)
            maxVal = max([currentValue, down, right, left])  # Gets the best choice from the available actions
            if maxVal==down:
                self.moveDown(grid)
            elif maxVal==right:
                self.moveRight(grid)
            elif maxVal==left:
                self.moveLeft(grid)
            else:
                self.noMove(grid)
        elif self.posRow == len(grid.allGridSpaces)-1: # bottom of the grid, so dont move down
            up = self.lookUp(grid)
            right = self.lookRight(grid)
            left = self.lookLeft(grid)
            maxVal = max([currentValue, up, right, left])  # Gets the best choice from the available actions
            if maxVal == up:
                self.moveUp(grid)
            elif maxVal == right:
                self.moveRight(grid)
            elif maxVal == left:
                self.moveLeft(grid)
            else:
                self.noMove(grid)
        elif self.posCol == 0: #left column of the grid, so dont move left
            up = self.lookUp(grid)
            down = self.lookDown(grid)
            right = self.lookRight(grid)
            maxVal = max([currentValue, down, right, up])  # Gets the best choice from the available actions
            if maxVal == down:
                self.moveDown(grid)
            elif maxVal == right:
                self.moveRight(grid)
            elif maxVal == up:
                self.moveUp(grid)
            else:
                self.noMove(grid)
        elif self.posCol == len(grid.allGridSpaces[0])-1: #right column of the grid, so dont move right
            up = self.lookUp(grid)
            down = self.lookDown(grid)
            left = self.lookLeft(grid)
            maxVal = max([currentValue, down, up, left])  # Gets the best choice from the available actions
            if maxVal == down:
                self.moveDown(grid)
            elif maxVal == up:
                self.moveUp(grid)
            elif maxVal == left:
                self.moveLeft(grid)
            else:
                self.noMove(grid)
        else: #middle parts of the grid, can move any direction
            up = self.lookUp(grid)
            down = self.lookDown(grid)
            right = self.lookRight(grid)
            left = self.lookLeft(grid)
            maxVal = max([currentValue, up, down, right, left])  # Gets the best choice from the available actions
            if maxVal == up:
                self.moveUp(grid)
            elif maxVal == down:
                self.moveDown(grid)
            elif maxVal == right:
                self.moveRight(grid)
            elif maxVal == left:
                self.moveLeft(grid)
            else:
                self.noMove(grid)

    def lookUp(self, grid):
        retVal = grid.values[self.posRow-1][self.posCol]
        return retVal
    def lookDown(self, grid):
        retVal = grid.values[self.posRow+1][self.posCol]
        return retVal
    def lookRight(self, grid):
        retVal = grid.values[self.posRow][self.posCol+1]
        return retVal
    def lookLeft(self, grid):
        retVal = grid.values[self.posRow][self.posCol-1]
        return retVal

    def moveUp(self, grid):
        grid.allGridSpaces[self.posRow][self.posCol].containsPlayer = False #The previous location of the robot no longer contains the robot
        #Then update the robot's position
        self.posRow -= 1
        #Set the robot to the new gridSpace in the grid
        grid.allGridSpaces[self.posRow][self.posCol].containsPlayer = True # The new gridSpace now contains the player and will be drawing it there now
        self.path.append((self.posRow, self.posCol))
    def moveDown(self, grid):
        grid.allGridSpaces[self.posRow][self.posCol].containsPlayer = False
        self.posRow += 1
        grid.allGridSpaces[self.posRow][self.posCol].containsPlayer = True
        self.path.append((self.posRow, self.posCol))
    def moveRight(self, grid):
        grid.allGridSpaces[self.posRow][self.posCol].containsPlayer = False
        self.posCol += 1
        grid.allGridSpaces[self.posRow][self.posCol].containsPlayer = True
        self.path.append((self.posRow, self.posCol))
    def moveLeft(self, grid):
        grid.allGridSpaces[self.posRow][self.posCol].containsPlayer = False
        self.posCol -= 1
        grid.allGridSpaces[self.posRow][self.posCol].containsPlayer = True
        self.path.append((self.posRow, self.posCol))
    def noMove(self, grid):
        pass #the robot doesnt move but the method is here in case we want to do something for staying still

    #Method to check if the robot has arrived at a terminal state
    def checkTerminalState(self, grid):
        if grid.allGridSpaces[self.posRow][self.posCol] == grid.goalSpace:
            print(self.path)
