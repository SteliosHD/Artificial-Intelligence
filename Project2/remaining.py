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
