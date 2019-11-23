        # maxi= -float('inf')
        # # import pdb; pdb.set_trace()
        # maxAction = None
        # for item in actions :
        #       if item[0]>=maxi:
        #             maxi=item[0]
        #             maxAction=item[1]
        # v = maxi

                # mini = float('inf')
        # minAction = None
        # for item in actions :
        #       if item[0]<=mini:
        #             mini=item[0]
        #             minAction=item[1]
        # v = mini


                #val={'depth':self.depth,'numAgents':gameState.getNumAgents(),'curDepth':0,'ghostIndex':1}
        action = self.minimax(gameState)
        return action
          # util.raiseNotDefined()

    def maxValue(self,gameState):
      # import pdb; pdb.set_trace()
      val=self.val
      val.update({'curDepth':val["curDepth"]+1})
      if val["curDepth"]== val["depth"]:
            return self.evaluationFunction(gameState)

      v = -float('inf')

      for action in gameState.getLegalActions(0):
              v=max(v,self.minValue(gameState.generateSuccessor(0,action)))
              val.update({"curDepth":val["curDepth"]-1})
      return v


    def minValue(self,gameState):
      # import pdb; pdb.set_trace()
      val =self.val
      val.update({"curDepth":val["curDepth"]+1})
      if val["curDepth"]== val["depth"]:
            return self.evaluationFunction(gameState)
      v = float('inf')
      for action in gameState.getLegalActions(val["ghostIndex"]):
              v=min(v,self.maxValue(gameState.generateSuccessor(val["ghostIndex"],action)))
              val.update({"curDepth":val["curDepth"]-1})
      return v

    def minimax(self,gameState):
      self.val={'depth':self.depth,'numAgents':gameState.getNumAgents(),'curDepth':0,'ghostIndex':1}
      val = self.val
      listActions=[]
      for i in range(1, val['numAgents']):
        val.update({'curDepth':0})
        actions = []
        val.update({'ghostIndex':i})
        # import pdb; pdb.set_trace()
        for action in gameState.getLegalActions(0):
                actions.append((self.minValue(gameState.generateSuccessor(0,action)),action ))

        maxi= -float('inf')
        maxAction = None
        for item in actions :
              if item[0]>=maxi:
                    maxi=item[0]
                    maxAction=item[1]
        listActions.append((maxi,maxAction))

      finalMax = -float('inf')
      finalAction=None
      # import pdb; pdb.set_trace()
      for item in listActions:
            if item[0]>finalMax:
                  finalMax=item[0]
                  finalAction=item[1]
      return finalAction
        finalMin = float('inf')
        finalAction=None
        # import pdb; pdb.set_trace()
        for item in listActions:
              if item[0]<=finalMin:
                    finalMin=item[0]
                    finalAction=item[1]
        return finalAction
        dire=['North','South','East','West','Stop']
        l =[item[1] for item in listActions]
        finalMax = -float('inf')
        finalAction=None
        # import pdb; pdb.set_trace()
        for act in dire:
              if l.count(act)>finalMax:
                    finalMax=l.count(act)
                    finalAction = act
        return finalAction

            @staticmethod
            def getFinalAction2(listActions):
                finalMin = float('inf')
                finalAction=None
                # import pdb; pdb.set_trace()
                for item in listActions:
                    if item[0]<=finalMin:
                        finalMin=item[0]
                        finalAction=item[1]
                return finalAction

            @staticmethod
            def getFinalAction3(listActions):
                dire=['North','South','East','West','Stop']
                l =[item[1] for item in listActions]
                finalMax = -float('inf')
                finalAction=None
                # import pdb; pdb.set_trace()
                for act in dire:
                     if l.count(act)>finalMax:
                         finalMax=l.count(act)
                         finalAction = act
                return finalAction
test_cases/q3/2-2b-vary-depth
        for action in gameState.getLegalActions(agentIndex):
            value=(self.minValue(gameState.generateSuccessor(agentIndex,action),curDepth+1,agentIndex+1))
            if value>v:
                v=value
                maxAction=action
            elif value==v:
                if action !='Stop':
                    v=value
                    maxAction=action
            actions.append((v,action))
        # return MinimaxAgent.maxAction(actions)
        return maxAction


        for action in gameState.getLegalActions(agentIndex):
            value=(self.minValue(gameState.generateSuccessor(agentIndex,action),curDepth,agentIndex))
            if value>v:
                v=value
                maxAction=action
            elif value==v:
                if action !='Stop':
                    v=value
                    maxAction=action
            actions.append((v,action))
        # return MinimaxAgent.maxAction(actions)
        return maxAction
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
            if item[0]>maxi:
                maxi=item[0]
                maxAction=item[1]
        return maxAction

  def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))


    if foodCount ==1:
        pass

    x,y,z,w = (float(e)/(ffood+0.1)),(float(b)/(clfood+0.1)),(float(c)/(clghost+0.1)),(float(a)/(clcapsules+0.1))
    value = d+x+y-z+w+score
    return value

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
