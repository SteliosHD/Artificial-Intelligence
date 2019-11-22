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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        # get some values
        food =currentGameState.getFood()
        pos = currentGameState.getPacmanPosition()
        ghostPos = currentGameState.getGhostPosition(1)
        newGhostPos = successorGameState.getGhostPosition(1)
        newScore = successorGameState.getScore()

        # find the manhattanDistance of the new pacman position and the available food
        dist1 = []
        for i, itemI in enumerate(food):
            for j, itemJ in enumerate(itemI):
                if itemJ:
                    dist1.append(manhattanDistance(newPos, (i, j)))

        # get the closest food
        dist1.sort()
        if dist1:
            minitem = dist1[0]
        else:
            minitem = 0

        # add some weights to the values that generates the score value if foodWeigh > ghostWeigh
        # pacman risks more and rushes for food else pacman tries first to stay alive
        # if these values are relative close pacman is balanced
        foodWeigh = 100
        ghostWeigh = 120

        # calculate the val where states closer to food are important but also avoid ghosts
        val = (foodWeigh/(minitem + 0.1))-(ghostWeigh/(manhattanDistance(newPos, ghostPos) + 0.1))

        return val


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

        # if agent 0 return maxValue else return minValue (after increasing agent every time modulo numAgents gives the agentIndex)
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
        successors = [(gameState.generateSuccessor(agentIndex, action),action ) for action in gameState.getLegalActions(agentIndex)]

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
        successors = [(gameState.generateSuccessor(agentIndex, action),action ) for action in gameState.getLegalActions(agentIndex)]
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

        # if agent 0 return maxValue else return minValue (after increasing agent every time modulo numAgents gives the agentIndex)
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
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:

            # generate successor state
            sucState = gameState.generateSuccessor(agentIndex,action)
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
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
