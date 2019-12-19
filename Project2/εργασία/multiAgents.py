# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import math

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        # successorGameState = currentGameState.generatePacmanSuccessor(action)
        # newPos = successorGameState.getPacmanPosition()

        "*** YOUR CODE HERE ***"

        # get the succesors and get the new position of pacman
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()

        # if succesor state is win (after the move we get to a win state) return a high number
        # else if its lose return a lower number than win in order to avoid dying in the last move
        if successorGameState.isWin():
            return 10**33
        elif successorGameState.isLose():
            return -10**36

        # get some values of the successor state. Capsules , ghost position and food grid
        capsules  = successorGameState.getCapsules()
        GhostsPos = successorGameState.getGhostPositions()
        food      = successorGameState.getFood()

        # get the food count from food grid
        foodCount = 0
        for i, itemI in enumerate(food):
            for j, itemJ in enumerate(itemI):
                if itemJ:
                    foodCount += 1
        # get a factor for the capsules based on test-runs(duck typing)
        if capsules:
            capsulesFactor = 5.0/len(capsules)
        else:
            capsulesFactor= 10

        # get a factor for the food count based on test-runs(duck typing)
        if foodCount > 25:
            foodFactor = 50.0/foodCount
        else:
            foodFactor = 25.0/foodCount

        # get a ghost factor based on the number of ghost agents (again the final value was computed bu test-runs)
        if successorGameState.getNumAgents() > 1:
            agentFactor = 1.5/(successorGameState.getNumAgents()-1)
        else:
            agentFactor = 0

        # get the coordinates of the closest food,closest ghost closest capsule and farthest food from pacmans new position
        closefood = closestFood(newPos, food)
        closeghost = closestGhost(newPos, GhostsPos)
        closecapsules = closestCapsule(newPos, capsules)
        farfood = farthestFood(newPos,food)

        # assign the values with the factors and some manipulation for cases of 0 denominator
        x = (foodFactor/(farfood+0.5))
        y = (foodFactor/(closefood+0.2))
        z = (agentFactor/(closeghost+0.2))
        w = (capsulesFactor/(closecapsules+0.2))
        q = foodFactor
        t = capsulesFactor

        # get the usual score
        score = successorGameState.getScore()

        # get the linear combination of those values (the only (true) negative value is the value of the ghost( how close to pacman and its factor multiplied)
        value = q+x+y-z+w+score+t

        return value


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.kounter =0

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        
        #  initialization of some values
        curDepth = 0
        agentIndex = 0
        self.numAgents = gameState.getNumAgents()

        maxValue, maxAction = self.minimax(gameState, agentIndex, curDepth)  # get the maximum action , maxValue dummy variable
        return maxAction

    def minimax(self, gameState, agentIndex, curDepth):
        """Minimax function that handles the cases and calls the appropriate function"""

        # if terminal state
        if curDepth == self.depth and agentIndex % self.numAgents == 0:
            return self.evaluationFunction(gameState), None

        # if agent 0 return maxValue else return minValue (after increasing agent every time by 1, modulo numAgents gives the agentIndex)
        if agentIndex % self.numAgents == 0 :
            return self.maxValue(gameState, agentIndex % self.numAgents, curDepth)
        else:
            return self.minValue(gameState,agentIndex % self.numAgents, curDepth)

    def maxValue(self, gameState, agentIndex, curDepth):
        """Max function that computes the maximum action and returns maximum,maximum action"""

        # if terminal state
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), None

        # initialize the value(v) and the action to be returned
        v = -float('inf')
        maxAction = None

        # create all the successors at once since minimax will expand the whole tree.
        successors = [(gameState.generateSuccessor(agentIndex, action), action) for action in gameState.getLegalActions(agentIndex)]

        for sucState,action in successors:
            value, sucAction = self.minimax(sucState, agentIndex+1, curDepth+1)  # increase the agent and depth since we are on a max node again, sucAction dummy variable

            # update the max value and keep the action of max value
            if value > v:
                v = value
                maxAction = action

        return v, maxAction

    def minValue(self, gameState, agentIndex, curDepth):
        """Min function that computes the minimum action and returns minimum,minimum action"""

        # if terminal state
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), None

        # initialize the value(v) and the action to be returned
        v = float('inf')
        minAction = None

        # create all the successors at once since minimax will expand the whole tree.
        successors = [(gameState.generateSuccessor(agentIndex, action), action) for action in gameState.getLegalActions(agentIndex)]
        for sucState, action in successors:
            value, sucAction = self.minimax(sucState, agentIndex+1, curDepth)  # increase the agent but not the depth, sucAction dummy variable

            # update the min value and keep the action of the min value
            if value < v:
                v = value
                minAction = action

        return v, minAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # initialization of some values
        curDepth = 0
        agentIndex = 0
        self.numAgents = gameState.getNumAgents()
        alpha = -float('inf')
        beta = float('inf')

        maxValue, maxAction = self.AlphaBetaminimax(gameState, agentIndex, curDepth, alpha, beta)  # get the maximum action , maxValue dummy variable
        return maxAction

    def AlphaBetaminimax(self, gameState, agentIndex, curDepth, alpha, beta):
        """Alpha Beta Minimimax handles the cases and calls the appropriate functions"""

        # if terminal state
        if curDepth == self.depth and agentIndex % self.numAgents == 0:
            return self.evaluationFunction(gameState), None

        # if agent 0 return maxValue else return minValue (after increasing agent every time by 1, modulo numAgents gives the agentIndex)
        if agentIndex % self.numAgents == 0:
            return self.maxValue(gameState, agentIndex % self.numAgents, curDepth, alpha, beta)
        else:
            return self.minValue(gameState,agentIndex % self.numAgents, curDepth,alpha, beta)

    def maxValue(self, gameState, agentIndex, curDepth, alpha, beta ):
        """
            Max function that computes the maximum action and returns maximum,maximum action
            Properly prune to reduce the number of states to be generated
        """

        # if terminal state
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), None

        # initialize the value(v) and the action to be returned
        v = -float('inf')
        maxAction = None

        # in order to avoid creating all the successors states at once we generate the legal actions and one by one getting the successors
        # if we perform pruning we don't get any unnecessary successors
        for action in gameState.getLegalActions(agentIndex):

            # generate successor state
            sucState = gameState.generateSuccessor(agentIndex, action)
            value, sucAction = self.AlphaBetaminimax(sucState, agentIndex+1, curDepth+1, alpha, beta)  # increase the agent and depth since we are on a max node again pass alpha and beta, sucAction dummy variable

            # update the max value and keep the action of max value
            if value > v:
                v = value
                maxAction = action

            # pruning
            if v > beta:
                return v, maxAction

            # update the alpha value
            alpha = max(alpha, value)

        return v, maxAction

    def minValue(self, gameState, agentIndex, curDepth, alpha, beta):
        """
            Min function that computes the minimum action and returns minimum,minimum action
            Properly prune to reduce the number of states to be generated
        """

        # if terminal state
        if gameState.isLose() or gameState.isWin():
            # import pdb; pdb.set_trace()
            return self.evaluationFunction(gameState), None

        # initialize the value(v) and the action to be returned

        v = float('inf')
        minAction = None

        # in order to avoid creating all the successors states at once we generate the legal actions and one by one getting the successors
        # if we perform pruning we don't get any unnecessary successors
        for action in gameState.getLegalActions(agentIndex):

            # generate successor state
            sucState = gameState.generateSuccessor(agentIndex,action)
            value, sucAction = self.AlphaBetaminimax(sucState, agentIndex+1, curDepth, alpha, beta)# increase the agent and since we are on a min node don't increase the depth pass alpha and beta, sucAction dummy variable

            # update the min value and keep the action of min value
            if value < v:
                v = value
                minAction = action

            # pruning
            if v < alpha:
                return v,minAction

            # update the beta value
            beta = min(beta, v)

        return v, minAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        curDepth = 0
        agentIndex = 0
        self.numAgents = gameState.getNumAgents()

        maxValue, maxAction = self.expectimax(gameState, agentIndex, curDepth)  # get the maximum action , maxValue dummy variable
        return maxAction

    def expectimax(self, gameState, agentIndex, curDepth):
        """Expectimax function that handles the cases and calls the appropriate function"""

        # if terminal state
        if curDepth == self.depth and agentIndex % self.numAgents == 0:
            return self.evaluationFunction(gameState), None

        # if agent 0 return maxValue else return chanceValue (after increasing agent every time by 1, modulo numAgents gives the agentIndex)
        if agentIndex % self.numAgents == 0 :
            return self.maxValue(gameState, agentIndex % self.numAgents, curDepth)
        else:
            return self.chanceValue(gameState,agentIndex % self.numAgents, curDepth)

    def maxValue(self, gameState, agentIndex, curDepth):
        """Max function that computes the maximum action and returns maximum,maximum action"""

        # if terminal state
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), None

        # initialize the value(v) and the action to be returned
        v = -float('inf')
        maxAction = None

        # create all the successors at once since minimax will expand the whole tree.
        successors = [(gameState.generateSuccessor(agentIndex, action), action) for action in gameState.getLegalActions(agentIndex)]

        for sucState,action in successors:
            value, sucAction = self.expectimax(sucState, agentIndex+1, curDepth+1)  # increase the agent and depth since we are on a max node again, sucAction dummy variable

            # update the max value and keep the action of max value
            if value > v:
                v = value
                maxAction = action

        return v, maxAction

    def chanceValue(self, gameState, agentIndex, curDepth):
        """Chance function that computes the average of all actions based on some probability and returns the value"""

        # if terminal state
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), None

        # initialize the value(vSum)
        vSum = 0

        # create all the successors at once since minimax will expand the whole tree.
        successors = [(gameState.generateSuccessor(agentIndex, action), action) for action in gameState.getLegalActions(agentIndex)]

        # create an equally distributed prob for all successors
        prob = [1.0/float(len(successors)) for i in range(len(successors))]
        for index, (sucState, action) in enumerate(successors):
            value, sucAction = self.expectimax(sucState, agentIndex+1, curDepth)  # increase the agent but not the depth, sucAction dummy variable

            # add the value multiplied with the probability to the sum
            vSum += value*prob[index]
        return vSum, None  # no actions here


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    # if state is win (after the move we get to a win state) return a high number
    # else if its lose return a lower number than win in order to avoid dying in the last move
    if currentGameState.isWin():
        return 10**33
    elif currentGameState.isLose():
        return -10**33

    # get some values of the successor state. Capsules, pacman position, ghost position and food grid
    pacmanPos = currentGameState.getPacmanPosition()
    capsules  = currentGameState.getCapsules()
    GhostsPos = currentGameState.getGhostPositions()
    food      = currentGameState.getFood()

    # get the food count from food grid
    foodCount = 0
    for i, itemI in enumerate(food):
        for j, itemJ in enumerate(itemI):
            if itemJ:
                foodCount += 1

    # get a factor for the capsules based on test-runs(duck typing)
    if capsules:
        capsulesFactor = 5.0/len(capsules)
    else:
        capsulesFactor= 0

    # get a factor for the food count based on test-runs(duck typing)
    if foodCount > 25:
        foodFactor = 50.0/foodCount
    else:
        foodFactor = 25.0/foodCount

    # get a ghost factor based on the number of ghost agents (again the final value was computed bu test-runs)
    if currentGameState.getNumAgents() > 1:
        agentFactor = 1.1/(currentGameState.getNumAgents()-1)
    else:
        agentFactor = 0

    # get the coordinates of the closest food,closest ghost closest capsule and farthest food from pacman
    closefood = closestFood(pacmanPos, food)
    closeghost = closestGhost(pacmanPos, GhostsPos)
    closecapsules = closestCapsule(pacmanPos, capsules)
    farfood = farthestFood(pacmanPos,food)

    # assign the values with the factors and some manipulation for cases of 0 denominator
    x = (foodFactor/(farfood+0.5))
    y = (foodFactor/(closefood+0.2))
    z = (agentFactor/(closeghost+0.2))
    w = (capsulesFactor/(closecapsules+0.2))
    q = foodFactor
    t = capsulesFactor

    # get the usual score
    score = currentGameState.getScore()

    # get the linear combination of those values (the only (true) negative value is the value of the ghost( how close to pacman and its factor multiplied)
    value = q+x+y-z+w+score+t

    return value



def closestFood(pacmanPos,food):
    """
        A function that computes the closest food from pacmans position
        food is a food grid with values True or False

    """
    dist = []
    for i, itemI in enumerate(food):
        for j, itemJ in enumerate(itemI):
            if itemJ:
                dist.append(manhattanDistance(pacmanPos, (i, j))) # manhattan gives better results

    # get the closest food
    dist.sort()
    if dist:
        minitem = dist[0]
    else:
        minitem = 0

    return minitem

def farthestFood(pacmanPos,food):
    """
        A function that computes the farthest food from pacmans position
        food is a food grid with values True or False

    """
    dist = []
    for i, itemI in enumerate(food):
        for j, itemJ in enumerate(itemI):
            if itemJ:
                dist.append(euclideanDistance(pacmanPos, (i, j)))  # euclidean gives better results for some reason

    # get the farthest food
    dist.sort(reverse=True)
    if dist:
        minitem = dist[0]
    else:
        minitem = 0

    return minitem

def closestGhost(pacmanPos,GhostsPos):
    """ A function that finds the closest ghost from pacman's position given a GhostsPos list"""

    dist = []
    for ghost in GhostsPos:
        dist.append(euclideanDistance(pacmanPos, ghost))  # euclidean gives better results for some reason

    # get the closest ghost
    dist.sort()
    if dist:
        minitem = dist[0]
    else:
        minitem = 0
    return minitem

def closestCapsule(pacmanPos,capsules):
    """ A function that finds the closest capsule from pacman's position given a capsules list"""

    dist = []
    for capsule in capsules:
        dist.append(euclideanDistance(pacmanPos, capsule))   # euclidean gives better results for some reason
    dist.sort()
    if dist:
        minitem = dist[0]
    else:
        minitem = 0
    return minitem

def euclideanDistance(xy1,xy2):
    """The Euclidean distance of two points with coordinates xy1(x1,y1) and xy2(x2, y2) """
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5

# Abbreviation
better = betterEvaluationFunction

