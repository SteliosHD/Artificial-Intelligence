# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class Fringe():
    """
        Custom fringe queue that uses the data structures in util to make
        a universal structure for fringe
    """
    def __init__(self,strategy):
        if strategy == 'dfs':
            self.fringe = util.Stack()
        elif strategy == 'bfs':
            self.fringe = util.Queue()
        elif strategy == 'ucs':
            self.fringe = util.PriorityQueue()
        elif strategy == 'astar':
            pass
        elif strategy == 'nh':
            pass

    def QueuingFn(self, item,):
        if isinstance(self.fringe, util.PriorityQueue):
                self.fringe.push(item,item[2])
        elif isinstance(self.fringe,util.Stack):
                self.fringe.push(item)
        elif isinstance(self.fringe,util.Queue):
                self.fringe.push(item)

    def RemoveFront(self):
        return self.fringe.pop()

    def Empty(self):
        return self.fringe.isEmpty()

    def Expand(self, problem, state):
        if isinstance(self.fringe,util.Stack):
            sucs = problem.getSuccessors(state)
            sucs.reverse()
            return sucs
        else:
            return problem.getSuccessors(state)
        # # # print sucs is None
        # # print sucs.reverse()
        # # print sucs
        # # for ele in sucs:
        # #     print ele
        # # print isinstance(self.fringe, util.PriorityQueue)
        # # print type(sucs)
        # if isinstance(self.fringe, util.PriorityQueue):
        #     for ele in sucs:
        #         self.frige.push(ele,ele[2])
        # elif isinstance(self.fringe,util.Stack):
        #     sucs.reverse()
        #     for ele in sucs:
        #         self.fringe.push(ele)
        # elif isinstance(self.fringe,util.Queue):
        #     for ele in sucs:
        #         self.fringe.push(ele)

class Node:

    def __init__(self, arg, st):
        self.node = arg[0]
        self.parent = st
        self.action = arg[1]
        self.cost = arg[2]

    def getNode(self):
        return self.node

    def getParent(self):
        return self.parent

    def getAction(self):
        return self.action

    def getCost(self):
        return self.cost

def graphSearch(problem,strategy):
    tree = {}
    closed = []
    fringe = Fringe(strategy)
    state = problem.getStartState()
    tree.update({state:Node([state,None,None],None)})
    closed.append(state)
    for child in fringe.Expand(problem, state):
        fringe.QueuingFn(child)
        tree.update({child[0]:Node(child,state)})
    while fringe:
        node = fringe.RemoveFront()
        state = node[0]
        # if state in closed:
        #     sol.pop()
        # print "node is ",node
        # print "state is ",state

        if problem.isGoalState(state):
            # print sol
            sol = []
            while True:
                # print "state is : ",state
                curnode = tree[state]
                # print "curnode is ",curnode
                state = curnode.getParent()
                # print "state now is : ", state
                if state:
                    sol.append(curnode.getAction())
                else:
                    break

            sol.reverse()
            # print sol
            # print len(sol)
            return sol
        # print 'state not in ' ,state not in closed
        if state not in closed  :
            closed.append(state)
            # sucs = []
            # print "print sucs", problem.getSuccessors(state)
            # print sol
            for child in fringe.Expand(problem, state):
                if not child[0] in closed:
                    # sucs.append(child)
                    fringe.QueuingFn(child)
                    tree.update({child[0]:Node(child,state)})
            # print "closed is : ",closed
            # print "sucs list is : ",sucs
            # if not sucs :
            #     sol.pop()
    return None

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    # print "Problem : ", problem
    # print "Start:", problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "the goal is", problem.goal
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())
    # l = [(i,j) for i in range(1,5) for j in range(1,5)]
    # for k in l:
    #     print "node's successors:", problem.getSuccessors(k)[0][0]
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    # print problem.walls[5][5]
    # print problem.getSuccessors(problem.getStartState())
    return graphSearch(problem, 'dfs')

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    # print problem.getSuccessors(problem.getStartState())
    return graphSearch(problem, 'bfs')

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    # print problem.getSuccessors(problem.getStartState())
    return graphSearch(problem, 'ucs')

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
