import copy

def makeMatrix(nodes, default, diagonal):
    alist = []
    for i in range(nodes):
        insert = []
        for j in range(nodes):
            insert.append(default)
        if diagonal:
            insert[i] = -1
        alist.append(insert)
    return alist

def printMatrix(matrix):
    for row in matrix:
        for entry in row:
            print str(entry) + "\t\t\t",
        print
    print

def print3DMatrix(m3):
    i = 0
    for matrix in m3:
        print i
        printMatrix(matrix)
        i += 1

filein = open("input.txt")
BIGINT = 999

# Consturct the matricies from input file
for line in filein:
    if line.strip() != "":
        linearray = line.strip().split(',')
        if linearray[0] == 'E':
            i = int(linearray[1]) - 1
            j = int(linearray[2]) - 1
            weight = int(linearray[3])
            times[i][j] = weight
            stops[i][j] = j
        elif linearray[0] == 'F':
            i = int(linearray[1]) - 1
            j = int(linearray[2]) - 1
            weight = int(linearray[3])
            flows[i][j] = weight
            stops[i][j] = j
        else:
            numNodes = int(linearray[0])
            startNode = int(linearray[1])-1
            endNode = int(linearray[2])-1
            times = makeMatrix(numNodes, BIGINT, False)
            flows = makeMatrix(numNodes, BIGINT, False)
            stops = makeMatrix(numNodes, BIGINT, False)

filein.close()

allTimes = []
allTimes.append(times)
allStops = []
allStops.append(stops)

print 0
printMatrix(allTimes[0])
printMatrix(allStops[0])

# Apply Floyd-Warshall on travel times matrix
for n in range(1, numNodes+1):
    nextTime = makeMatrix(numNodes, BIGINT, False)
    nextStop = makeMatrix(numNodes, BIGINT, False)
    for i in range(numNodes):
        for j in range(numNodes):
            if i == j:
                continue
            currentTime = allTimes[n-1]
            currentStop = allStops[n-1]

            directPath = currentTime[i][j]
            indirectPath = currentTime[i][n-1] + currentTime[n-1][j]
            if directPath <= indirectPath:
                nextTime[i][j] = directPath
                nextStop[i][j] = currentStop[i][j]
            else:
                nextTime[i][j] = indirectPath
                nextStop[i][j] = n-1

    print n
    print "Travel time: "
    printMatrix(nextTime)
    print "Next stop: "
    printMatrix(nextStop)
    allTimes.append(nextTime)
    allStops.append(nextStop)

# Construct matrix with the paths and edge traffic
pathMatrix = makeMatrix(numNodes, 0, False)
stopMatrix = allStops[6]
edgeFlowMatrix = makeMatrix(numNodes, 0, False)

for i in range(numNodes):
    for j in range(numNodes):
        if i == j:
            pathMatrix[i][j] = j
            continue
        if times[i][j] == BIGINT:
            edgeFlowMatrix[i][j] = BIGINT
            continue

        ii = i
        jj = j
        path = [i]
        while stopMatrix[ii][jj] != BIGINT:
            path.append(stopMatrix[ii][jj])
            prevstop = ii
            ii = stopMatrix[ii][jj]
            edgeFlowMatrix[prevstop][ii] = edgeFlowMatrix[prevstop][ii] + flows[i][j]
        pathMatrix[i][j] = path

printMatrix(pathMatrix)
printMatrix(edgeFlowMatrix)

allFlows = []
allFlows.append(edgeFlowMatrix)
allStops2 = []
allStops2.append(stops)

print 0
printMatrix(allTimes[0])
printMatrix(allStops[0])

# Apply Floyd-Warshall on flow matrix
for n in range(1, numNodes+1):
    nextFlow = makeMatrix(numNodes, BIGINT, False)
    nextStop = makeMatrix(numNodes, BIGINT, False)
    for i in range(numNodes):
        for j in range(numNodes):
            if i == j:
                nextFlow[i][j] = 0
                nextStop[i][j] = 0
                continue
            currentFlow = allFlows[n-1]
            currentStop = allStops2[n-1]

            directPath = currentFlow[i][j]
            indirectPath = currentFlow[i][n-1] + currentFlow[n-1][j]
            if directPath <= indirectPath:
                nextFlow[i][j] = directPath
                nextStop[i][j] = currentStop[i][j]
            else:
                nextFlow[i][j] = indirectPath
                nextStop[i][j] = n-1

    print n
    print "Flows: "
    printMatrix(nextFlow)
    print "Next stop: "
    printMatrix(nextStop)
    allFlows.append(nextFlow)
    allStops2.append(nextStop)