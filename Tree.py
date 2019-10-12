

class Tree:
        def __init__(self,root):
            self.root = root
            self.node = Node(self.root)
            self.tree = {root:self.node}

        def addNode(self, args, parent):
            self.tree.update({args[0]:Node(args[0], args[1], args[2], parent)})

        def getNode(self, state ):
            return self.tree[state]


class Node():

    def __init__(self, state, action=None, cost=None,parent = None):
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

    def getPathCost(self):
        PathCost = self.getCost()
        node = self.getParent()
        while node.getAction():
            PathCost += node.getCost()
            node = node.getParent()
        return PathCost

    def getDepth(self):
        depth = 1
        node = self.getParent()
        while node.getAction():
            depth += 1
            node = node.getParent()
        return depth

    def getPathAction(self):
        path = [self.action]
        node = self.getParent()
        while node.getParent():
            path.append(node.getAction())
            node = node.getParent()
        path.reverse()
        return path

    def getParent(self):
        return self.parent


if __name__ == '__main__':
    t = Tree((5,5))
    t.addNode([(5,4),'West',4],t.getNode((5,5)))
    t.addNode([(5,3),'South',10],t.getNode((5,4)))
    t.addNode([(4,3),'North',12],t.getNode((5,4)))
    t.addNode([(4,2),'West',15],t.getNode((4,3)))
    node = t.getNode((4,2))
    print node.getPathCost()
    print node.getDepth()
    print node.getPathAction()
