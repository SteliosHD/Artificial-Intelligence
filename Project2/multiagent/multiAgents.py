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
        food =currentGameState.getFood()
        pos = currentGameState.getPacmanPosition()
        ghostPos = currentGameState.getGhostPosition(1)
        newGhostPos = successorGameState.getGhostPosition(1)
        newScore = successorGameState.getScore()

        dist1=[]
        for i,itemI in enumerate(food):
              for j,itemJ in enumerate(itemI):
                    if itemJ:
                          dist1.append(manhattanDistance(newPos,(i,j)))

        dist1.sort()
        if dist1:
            minitem=dist1[0]
        else:
            minitem=0

        val =(100/(minitem+0.1))-(120/(manhattanDistance(newPos,ghostPos)+0.1))

        return val
       # return successorGameState.getScore()

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
        return self.minimax(gameState)

    def minimax(self, gameState):
        # import pdb; pdb.set_trace()
        curDepth = 0
        agentIndex = 0
        self.numAgents = gameState.getNumAgents()
        actions = []
        for action in gameState.getLegalActions(agentIndex):
            actions.append((self.minValue(gameState.generateSuccessor(agentIndex,action),curDepth+1,agentIndex+1),action))
        return MinimaxAgent.maxAction(actions)

    def maxValue(self, gameState, curDepth, agentIndex):
        # import pdb; pdb.set_trace()
        if curDepth == self.depth or curDepth == self.depth+1 or gameState.isLose() or gameState.isWin():
            # import pdb; pdb.set_trace()
            return self.evaluationFunction(gameState)
        agentIndexRe = agentIndex % self.numAgents
        if agentIndexRe == 0:
            v = -float('inf')
            for action in gameState.getLegalActions(agentIndexRe):
                v=max(v,self.minValue(gameState.generateSuccessor(agentIndexRe,action),curDepth+1,agentIndexRe+1))
            return v
        else:
            v = -float('inf')
            for action in gameState.getLegalActions(agentIndexRe):
                v=max(v,self.maxValue(gameState.generateSuccessor(agentIndexRe,action),curDepth,agentIndexRe+1))
            return v


    def minValue(self, gameState, curDepth, agentIndex):
        # import pdb; pdb.set_trace()
        if curDepth==self.depth+1 or gameState.isLose() or gameState.isWin():
            # import pdb; pdb.set_trace()
            return self.evaluationFunction(gameState)
        agentIndexRe = agentIndex % self.numAgents
        if agentIndexRe == self.numAgents-1:
            v = float('inf')
            for action in gameState.getLegalActions(agentIndexRe):
                v=min(v,self.maxValue(gameState.generateSuccessor(agentIndexRe,action),curDepth,agentIndexRe+1))
            return v
        else:
            v = float('inf')
            for action in gameState.getLegalActions(agentIndexRe):
                v=min(v,self.minValue(gameState.generateSuccessor(agentIndexRe,action),curDepth,agentIndexRe+1))
            return v

 #*******************************
 #       Static methods         *
 #*******************************
    @staticmethod
    def getFinalAction1(listActions):
        finalMax = -float('inf')
        finalAction=None
        # import pdb; pdb.set_trace()
        for item in listActions:
            if item[0]>finalMax:
                finalMax=item[0]
                finalAction=item[1]
        return finalAction

    @staticmethod
    def maxAction(actions):
        maxi= -float('inf')
        maxAction = None
        for item in actions :
            if item[0]>=maxi:
                maxi=item[0]
                maxAction=item[1]
        return maxAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.AlphaBetaminimax(gameState)

    def AlphaBetaminimax(self, gameState):
        # import pdb; pdb.set_trace()
        curDepth = 0
        agentIndex = 0
        self.numAgents = gameState.getNumAgents()
        actions = []
        alpha = -float('inf')
        beta  =  float('inf')
        for action in gameState.getLegalActions(agentIndex):

            value,alpha= (self.minValue(gameState.generateSuccessor(agentIndex,action),curDepth+1,agentIndex+1,alpha,beta))
            actions.append((value,action))
        return AlphaBetaAgent.maxAction(actions)

    def maxValue(self, gameState, curDepth, agentIndex,alpha,beta):
        # import pdb; pdb.set_trace()
        if curDepth == self.depth or curDepth == self.depth+1 or gameState.isLose() or gameState.isWin():
            # import pdb; pdb.set_trace()
            return self.evaluationFunction(gameState),alpha
        agentIndexRe = agentIndex % self.numAgents
        if agentIndexRe == 0:
            v = -float('inf')
            for action in gameState.getLegalActions(agentIndexRe):
                value,beta=self.minValue(gameState.generateSuccessor(agentIndexRe,action),curDepth+1,agentIndexRe+1,alpha,beta)
                v = max(v, value)
                if v > beta :
                    return v,alpha
                alpha = max(alpha,v)
            return v,alpha
        else:
            v = -float('inf')
            for action in gameState.getLegalActions(agentIndexRe):
                value,alpha= self.maxValue(gameState.generateSuccessor(agentIndexRe,action),curDepth,agentIndexRe+1,alpha,beta)
                v=max(v,value)
                if v > beta :
                    return v,alpha
                alpha = max(alpha,v)
            return v,alpha

    def minValue(self, gameState, curDepth, agentIndex,alpha,beta):
        # import pdb; pdb.set_trace()
        if curDepth==self.depth+1 or gameState.isLose() or gameState.isWin():
            # import pdb; pdb.set_trace()
            return self.evaluationFunction(gameState),beta
        agentIndexRe = agentIndex % self.numAgents
        if agentIndexRe == self.numAgents-1:
            v = float('inf')
            for action in gameState.getLegalActions(agentIndexRe):
                value,alpha= self.maxValue(gameState.generateSuccessor(agentIndexRe,action),curDepth,agentIndexRe+1,alpha,beta)
                v=min(v,value)
                if v<alpha :
                    return v,beta
                beta = min(beta,v)
            return v,beta
        else:
            v = float('inf')
            for action in gameState.getLegalActions(agentIndexRe):
                value,beta= self.minValue(gameState.generateSuccessor(agentIndexRe,action),curDepth,agentIndexRe+1,alpha,beta)
                v=min(v,value)
                if v<alpha :
                    return v,beta
                beta = min(beta,v)
            return v,beta

 #*******************************
 #       Static methods         *
 #*******************************
    @staticmethod
    def getFinalAction1(listActions):
        finalMax = -float('inf')
        finalAction=None
        # import pdb; pdb.set_trace()
        for item in listActions:
            if item[0]>finalMax:
                finalMax=item[0]
                finalAction=item[1]
        return finalAction

    @staticmethod
    def maxAction(actions):
        maxi= -float('inf')
        maxAction = None
        for item in actions :
            if item[0]>=maxi:
                maxi=item[0]
                maxAction=item[1]
        return maxAction


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
