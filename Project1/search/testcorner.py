import util
def corners(state):
    print state[1]
    print state [0]
    corners = ((1,6),(6,1),(6,6),(1,1))
    actives = []
    node = state[0]
    for i,corn in enumerate(state[1]):
        if corn:
            activeCorner = corners[i]
            actives.append(activeCorner)
    if not actives: return 0
    # distance =[]
    # for activeCorn in actives:
    #     distance.append(util.manhattanDistance(activeCorn,node))
    #
    # distance.sort()
    # numActives = len(actives)
    # print actives
    d=[]
    cornersList = list(corners)
    for corn in corners:
        temp=[]
        for i in corners:
            if not corn==i:
                temp.append(i)
        d.append(findClosest(temp,corn)[1])

    print "minimum ", min(d)

    closest,distance = findClosest(actives,node)
    # print distance
    actives.remove(closest)
    sumRemaining = cornersDistance(actives,closest)
    return distance+sumRemaining
    # return 0 # Default to trivial solution

def cornersDistance(corners,closest):
    cornersList=list(corners)
    current=closest
    sum = 0
    while cornersList:
        corn,distance = findClosest(cornersList,current)
        sum+=distance
        cornersList.remove(corn)

    return sum

def findFurthest(corners,current):
    distance=[]
    for corn in corners:
        distance.append(util.manhattanDistance(corn,current))
    furtherIndex = distance.index(max(distance))
    # print corners[closestIndex],min(distance)
    return corners[furtherIndex],max(distance)

def Euclidean(xy1,xy2):
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

if __name__ == '__main__':
    testState1=((2,2),(1,1,1,1))
    testState2=((2,2),(1,0,1,0))
    testState3=((2,2),(0,0,0,0))
    testState4=((1,3),(0,0,0,1))
    print corners(testState1)
    print corners(testState2)
    print corners(testState3)
    print corners(testState4)
