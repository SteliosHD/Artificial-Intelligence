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
        """ Use the appropriate push method if PriorityQueue is used cost is the PathCost"""
        if isinstance(self.fringe, util.PriorityQueue):
                self.fringe.push(item,item.getPathCost())
        elif isinstance(self.fringe,util.Stack):
                self.fringe.push(item)
        elif isinstance(self.fringe,util.Queue):
                self.fringe.push(item)

    def RemoveFront(self):
        """ Universal remove (pop)"""
        return self.fringe.pop()

    def Empty(self):
        return self.fringe.isEmpty()

    def Expand(self, problem, state):
        """ Expand the children of the node get succesors """
        if isinstance(self.fringe,util.Stack):
            sucs = problem.getSuccessors(state)
            sucs
            return sucs
        else:
            return problem.getSuccessors(state)

    def Get(self):
        """ Gets a list of the fringe in it's current state"""
        if isinstance(self.fringe,util.PriorityQueue):
            return self.fringe.heap
        else:
            return self.fringe.list

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

    def addNode(self, args, parent):
        """
            Takes a list as a first argument (not to be confused with *args)
            with the following form [<state>, <action>, <cost>] then creates
            a node with this list. The second argument is the parent node.
        """
        self.tree.update({args[0]:Node(args[0], args[1], args[2], parent)})

    def getNode(self, state ):
        """ Returns the node with key = state from the tree"""
        return self.tree[state]


class Node:
    """
        Node class that creates nodes to be stored in the Tree. Every node has
        a state(e.g name) an action (e.g. 'West') a cost(e.g. 1)(the cost from
        the parent node till this node) and a parent Node.
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



def graphSearch(problem,strategy):
    """
        Impemantation of graph search using a tree structure with nodes. The
        input is the problem and a strategy("dfs", "bfs", "ucs"). Depending
        on the strategy a universal fringe is created using an assisting class
        called Fringe that impements the appropriate data structure(stack, queue,
        priority queue).
    """

    closed = []
    #initialization phase create tree(root and root children) and fringe.
    fringe = Fringe(strategy)
    state = problem.getStartState()
    tree = Tree(state)
    closed.append(state)
    for child in fringe.Expand(problem, tree.getNode(state).getState()):
        tree.addNode(child,tree.getNode(state))
        fringe.QueuingFn(tree.getNode(child[0]))
    #loop until solution is find or fringe is empty
    while fringe:
        node = fringe.RemoveFront()
        state = node.getState()
        # if goal state get the path actions
        if problem.isGoalState(state):
            sol = node.getPathAction()
            return sol
        # check if node is in explored
        if not state in closed  :
            closed.append(state)
            for child in fringe.Expand(problem, tree.getNode(state).getState()):
                childstate = child[0]
                fls = fringe.Get()
                # if child is has not been explored or is not in the fringe addNode in the Fringe
                if  not childstate in closed or childstate in fls:
                    tree.addNode(child,node)
                    fringe.QueuingFn(tree.getNode(child[0]))
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
