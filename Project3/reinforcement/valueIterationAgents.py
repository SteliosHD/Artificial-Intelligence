# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp,util,copy
from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()
        self.legalActions ={}


    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        self.epsilon  = 0.05
        self.actions = {}
        self.valuesKminusOne = util.Counter()
        for state in self.mdp.getStates():
            self.actions.update({state: None})
            self.values.update({state: 0})
        # import pdb; pdb.set_trace()
        for i in range(self.iterations):
            for state in self.mdp.getStates():
                max, maxAction = self.maxValue(state)
                nextState = self.nxt(state, maxAction)
                self.values.update({state:self.mdp.getReward(state, maxAction, nextState)+self.discount*max})
                self.actions.update({state:maxAction})
            self.valuesKminusOne = copy.deepcopy(self.values)
        # import pdb; pdb.set_trace()


    def maxValue(self, state):
        if state == 'TERMINAL_STATE':
            return 0,None
        max = None
        maxAction = None
        for action in self.mdp.getPossibleActions(state):
            sumAction = sum([self.valuesKminusOne[x[0]]*x[1] for x in self.mdp.getTransitionStatesAndProbs(state, action)])
            if  max == None:
                max = sumAction
                maxAction = action
            elif sumAction > max:
                max = sumAction
                maxAction = action

        return max, maxAction

    @staticmethod
    def nxt(state, action):
        if state == 'TERMINAL_STATE':
            return 'exit'
        if action == 'north':
            return(state[0],state[1]+1)
        elif action == 'east':
            return(state[0]+1,state[1])
        elif action == 'south':
            return(state[0],state[1]-1)
        else :
            return(state[0]-1,state[1])







    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #
        if  'exit' in self.mdp.getPossibleActions(state):
            # import pdb; pdb.set_trace()
            return self.mdp.getReward(state,None,'exit')
        if action == 'north':
            newState = (state[0], state[1] + 1)
        elif action == 'east':
            newState = (state[0] + 1, state[1])
        elif action == 'south':
            newState = (state[0], state[1] - 1)
        elif action == 'west':
            newState = (state[0] - 1, state[1])
        else:
            newState = 'TERMINAL_STATE'
        possibleStates = [x for x in self.mdp.getTransitionStatesAndProbs(state, action)]
        # import pdb; pdb.set_trace()
        prob = 0
        if not possibleStates:
            prob=1
        for states in possibleStates:
            if newState == states[0]:
                prob = states[1]
                break
        # import pdb; pdb.set_trace()
        if prob==0:
            newState = state
            prob = 1
        return self.discount*prob*self.values[newState]
        print(new)
        # util.raiseNotDefined()


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        if state=='TERMINAL_STATE':
            return None
        else:
            return self.actions[state]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
