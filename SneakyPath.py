import copy

# Function for making nodes x nodes size matrix filled with 'default'
def makeMatrix(nodes, default, diagonal):
    alist = []
    for i in range(nodes):
        insert = []
        for j in range(nodes):
            insert.append(default)
        if diagonal: # fill diagonal with -1's
            insert[i] = -1
        alist.append(insert)
    return alist

# function for printing a 2d array/matrix
def printMatrix(matrix):
    for row in matrix:
        for entry in row:
            print("{:<20.13s}".format(str(entry))),
        print
    print

# function for printing 3d array/matrix
def print3DMatrix(m3):
    i = 0
    for matrix in m3:
        print i
        printMatrix(matrix)
        i += 1

# parameters: filein = input, BIGINT ~ INFINITI for this exercise
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

# Construct arrays for tracking changes in each iteraton of algorithm
allTimes = []
allTimes.append(times)
allStops = []
allStops.append(stops)

# print 0
# printMatrix(allTimes[0])
# printMatrix(allStops[0])

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

    # print n
    # print "Travel time: "
    # printMatrix(nextTime)
    # print "Next stop: "
    # printMatrix(nextStop)
    allTimes.append(nextTime)
    allStops.append(nextStop)

# Create matricies to keep track of paths and flow on each edge
pathMatrix = makeMatrix(numNodes, 0, False)
stopMatrix = allStops[6]
edgeFlowMatrix = makeMatrix(numNodes, 0, False)

print "Stop Matrix"
printMatrix(stopMatrix)
print "times"
printMatrix(times)

# Construct matrix with the paths and edge traffic
for i in range(numNodes):
    for j in range(numNodes):
        if i == j:
            pathMatrix[i][j] = j
            continue
        if times[i][j] == BIGINT:
            edgeFlowMatrix[i][j] = BIGINT

        ii = i
        jj = j
        path = [i]
        while stopMatrix[ii][jj] != BIGINT:
            path.append(stopMatrix[ii][jj])
            prevstop = ii
            ii = stopMatrix[ii][jj]
            edgeFlowMatrix[prevstop][ii] = edgeFlowMatrix[prevstop][ii] + flows[i][j]
        pathMatrix[i][j] = path

# Any un-used edge (typically non existent paths) need large flow value
for i in range(numNodes):
    for j in range(numNodes):
        if edgeFlowMatrix[i][j] == 0:
            edgeFlowMatrix[i][j] = BIGINT

print "Path matrix:"
printMatrix(pathMatrix)
print "Flows:"
printMatrix(flows)
print "Edge Flows"
printMatrix(edgeFlowMatrix)

allFlows = []
allFlows.append(edgeFlowMatrix)
allStops2 = []
allStops2.append(stops)


# Apply Floyd-Warshall on flow matrix
for n in range(1, numNodes+1):
    nextFlow = makeMatrix(numNodes, BIGINT, False)
    nextStop = makeMatrix(numNodes, BIGINT, False)
    for i in range(numNodes):
        for j in range(numNodes):
            if i == j:
                # nextFlow[i][j] = 0
                nextStop[i][j] = " "
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
    allFlows.append(nextFlow)
    allStops2.append(nextStop)

print "Final Flows:"
printMatrix(allFlows[6])

# Construct matrix for path taken
flowPathMatrix = makeMatrix(numNodes, 0, False)
flowStopMatrix = allStops2[6]
sumPathMatrix = makeMatrix(numNodes, 0, False)
hopPathMatrix = makeMatrix(numNodes, 0, False)
avePathMatrix = makeMatrix(numNodes, 0, False)
maxPathEdgeMatrix = makeMatrix(numNodes, 0, False)
minPathEdgeMatrix = makeMatrix(numNodes, BIGINT, False)

for i in range(numNodes):
    for j in range(numNodes):
        if i == j:
            flowPathMatrix[i][j] = j
            maxPathEdgeMatrix[i][j] = " "
            sumPathMatrix[i][j] = " "
            minPathEdgeMatrix[i][j] = " "
            continue

        ii = i
        jj = j
        flowPath = [i]
        while flowStopMatrix[ii][jj] != " ":
            flowPath.append(flowStopMatrix[ii][jj])
            flowprevstop = ii
            ii = flowStopMatrix[ii][jj]
            minPathEdgeMatrix[i][j] = min(minPathEdgeMatrix[i][j], allFlows[6][flowprevstop][ii])
            maxPathEdgeMatrix[i][j] = max(maxPathEdgeMatrix[i][j], allFlows[6][flowprevstop][ii])
            sumPathMatrix[i][j] = sumPathMatrix[i][j] + allFlows[6][flowprevstop][ii]
        flowPathMatrix[i][j] = flowPath
        hopPathMatrix[i][j] = (len(flowPath)-1)
        avePathMatrix[i][j] = float(sumPathMatrix[i][j]) / (len(flowPath)-1)

# Output results
print "Flow Path Matrix"
printMatrix(flowPathMatrix)
print "Min edge Matrix"
printMatrix(minPathEdgeMatrix)
print "Max edge matrix"
printMatrix(maxPathEdgeMatrix)
print "Sum Matrix"
printMatrix(sumPathMatrix)
print "Hop Matrix"
printMatrix(hopPathMatrix)
print "Ave Matrix"
printMatrix(avePathMatrix)