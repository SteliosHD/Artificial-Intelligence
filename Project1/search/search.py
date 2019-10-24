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
        a universal structure for fringe.
        Strategy that supports : dfs,bfs,ucs
    """
    def __init__(self,strategy):
        """ Create the fringe according the given strategy"""
        if strategy == 'dfs':
            self.structure = 'Stack'
            self.fringe = util.Stack()
        elif strategy == 'bfs':
            self.structure = 'Queue'
            self.fringe = util.Queue()
        elif strategy == 'ucs':
            self.structure = 'PriorityQueue'
            self.fringe = util.PriorityQueue()

    def QueuingFn(self, item):
        """ Use the appropriate push method if PriorityQueue is used cost is the PathCost"""
        if self.structure == 'PriorityQueue':
            self.fringe.push(item,item.getPathCost())
        elif self.structure == 'Stack': # wasn't nessesary to be distinct but better seperated
            self.fringe.push(item)
        elif self.structure == 'Queue': # wasn't nessesary to be distinct but better seperated
            self.fringe.push(item)
        elif self.structure == 'PriorityQueueWithFunction': # wasn't nessesary to be distinct but better seperated
            self.fringe.push(item)

    def RemoveFront(self):
        """ Universal remove (pop)"""
        return self.fringe.pop()

    def Empty(self):
        return self.fringe.isEmpty()

    def Expand(self, problem, state):
        """ Expand the children of the node get succesors """
        if self.structure == 'Stack':
            sucs = problem.getSuccessors(state)
            # sucs.reverse() # reverse method returns false but reverses list so not direct return
            return sucs
        else:
            return problem.getSuccessors(state)


    def GetList(self):
        """ Gets a list of the fringe in it's current state"""
        if self.structure == 'PriorityQueue' or self.structure == 'PriorityQueueWithFunction':
            return self.fringe.heap
        else:
            return self.fringe.list

class FringeHeur(Fringe):

    def __init__(self, problem, heuristic, strategy ='astar'):
        self.fringe = util.PriorityQueueWithFunction(self.priorityFn)
        self.problem = problem
        self.heurisic = heuristic
        self.strategy = strategy
        self.structure = 'PriorityQueueWithFunction'

    def priorityFn(self,item):
        return self.heurisic(item.getState(),self.problem) + item.getPathCost()



#
# class PriorityQueueFn(util.PriorityQueue):
#     """
#     Implements a priority queue with the same push/pop signature of the
#     Queue and the Stack classes. This is designed for drop-in replacement for
#     those two classes. The caller has to provide a priority function, which
#     extracts each item's priority.
#     """
#     def  __init__(self, priorityFunction):
#         "priorityFunction (item) -> priority"
#         self.priorityFunction = priorityFunction      # store the priority function
#         util.PriorityQueue.__init__(self)        # super-class initializer
#
#     def push(self, item, problem = None):
#         "Adds an item to the queue with priority from the priority function"
#         util.PriorityQueue.push(self, item, self.costFunc(item, problem))
#
#     def costFunc(self,item, problem):
#         return item.getPathCost() + self.priorityFunction(item.getState(), problem)






class Tree:
    """
        This is a simple tree structure implemented with a dictionary
        Each element has a distinct key-name (node name or state ) and the
        value of that key is a node object from the node class
        Methods: addNode,getNode
    """
    def __init__(self,root):
        """Create the root of the tree"""
        self.root = root
        self.node = Node(self.root,None, None, None)
        self.tree = {root:self.node}

    def addNode(self, itemNode):
        """ Takes a node as an argument and adds it in the tree"""
        self.tree.update({itemNode.getState():itemNode})

    def getNode(self, state ):
        """ Returns the node with key = state from the tree"""
        return self.tree[state]


class Node:
    """
        Node class that creates nodes (to be stored in the Tree). Every node has
        a state(e.g. name) an action (e.g. 'West') a cost(e.g. 1)(the cost from
        the parent node till this node) and a parent Node(node object).
        Methods: getState, getAction, getCost,getParent. getPathCost, getDepth, getPathAction
    """

    def __init__(self, state, action, cost , parent):
        """Creates a node with a state, an action, a cost, an a parent Node"""
        self.state  = state
        self.action = action
        self.cost   = cost
        self.parent = parent

    def getState(self):
        return self.state

    def getAction(self):
        return self.action

    def getCost(self):
        return self.cost

    def getParent(self):
        return self.parent

    def getPathCost(self):
        """ Gets the path cost from the root till the Node"""
        PathCost = self.cost
        node = self.parent
        while True:
            if not node.parent: break
            PathCost += node.cost
            node = node.parent
        return PathCost

    def getDepth(self):
        """ Gets the depth of the Node"""
        depth = 1
        node = self.parent
        while True:
            if not node.parent: break
            depth += 1
            node = node.parent
        return depth

    def getPathAction(self):
        """ Gets the path(actions to get to the Node) from the root"""
        path = [self.action]
        node = self.parent
        while True:
            if not node.parent: break
            path.append(node.action)
            node = node.parent
        path.reverse()
        return path



def graphSearch(problem,strategy,priorityFn = None):
    """
        Impemantation of graph search using a tree structure with nodes. The
        input is the problem and a strategy("dfs", "bfs", "ucs"). Depending
        on the strategy a universal fringe is created using an assisting class
        called Fringe that impements the appropriate data structure(stack, queue,
        priority queue).
    """

    #initialization phase create tree(root and root children) and fringe.
    if strategy == 'astar':
        fringe = FringeHeur(problem,priorityFn,strategy)
    else:
        fringe = Fringe(strategy)
    state = problem.getStartState()
    explored = Tree(state)
    if problem.isGoalState(state):return []
    for child in fringe.Expand(problem, explored.getNode(state).getState()):
        childnode = Node(child[0],child[1],child[2],explored.getNode(state))
        fringe.QueuingFn(childnode)
    #loop until solution is find or fringe is empty
    while True:
        if not fringe.GetList(): return False
        currentNode = fringe.RemoveFront()
        # if goal state get the path actions
        if problem.isGoalState(currentNode.getState()):
            return currentNode.getPathAction()
        # check if node is in explored
        if not currentNode.getState() in explored.tree.keys()  :
            explored.addNode(currentNode)
            for child in fringe.Expand(problem, currentNode.getState()):
                childnode = Node(child[0],child[1],child[2],currentNode)
                # if child is has not been explored or is not in the fringe addNode in the Fringe
                if  not childnode.getState() in explored.tree.keys() or childnode in fringe.GetList():
                    fringe.QueuingFn(childnode)


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
    # util.raiseNotDefined()
    # print "the goal is", problem.goal
    return graphSearch(problem, 'astar', heuristic)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
