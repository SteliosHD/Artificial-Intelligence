#   trivial 2/5 score
    dist = len(foodGrid.asList())
    # print dist
    return dist
#   max manhattanDistance from remaning food 3/5 score
    current = position
    foods = foodGrid.asList()
    if foods==0: return 0
    distance=[]
    for food in foods:
        distance.append(util.manhattanDistance(food,current))
    if not distance:return 0
    furtherIndex = distance.index(max(distance))
    # print corners[closestIndex],min(distance)
    foodNode,dist=foods[furtherIndex],max(distance)
    return dist
