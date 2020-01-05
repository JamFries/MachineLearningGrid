import pygame
import numpy
import Grid

pygame.init()

windowWidth = 500
windowHeight = 500
screen = pygame.display.set_mode((windowWidth, windowHeight))

rows = 10
columns = 10
programGrid = Grid.Grid(windowWidth, windowHeight, rows, columns)
programGrid.setRandomGoalState()
programGrid.setObstacles(15)
programGrid.setStartingLocation()
programGrid.setRewards()

programGrid.valueIteration(100) #Run's value iteration on the grid. The final values should converge to the optimal path the agent should take

programRunning = True
while programRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            programRunning = False
        elif event.type == pygame.KEYDOWN: #check for keys that were pressed at that single frame
            if event.key == pygame.K_SPACE: #when the space bar is pressed then move the agent one step
                programGrid.agent.move(programGrid)
                programGrid.agent.checkTerminalState(programGrid)



    #drawing phase
    programGrid.drawGrid(screen)
    programGrid.drawGridLines(screen)

    #update the screen after drawing
    pygame.display.update()