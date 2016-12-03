import copy
import psutil

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
filein = open("input3.txt")
BIGINT = 9999999999
kbCounter = 0

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

# Construct arrays for tracking changes in each iteration of algorithm
allTimes = []
allTimes.append(times)
allStops = []
allStops.append(stops)

# print 0
print "Please note: All values along any diagonal is an edge or path to itself so the values are meaningless and should" \
      " be ignored."
print "Matrix that gives travel times from node (row number, i) to node (column number, j):"
printMatrix(allTimes[0])
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
            kbCounter += 1
            if directPath <= indirectPath:
                nextTime[i][j] = directPath
                nextStop[i][j] = currentStop[i][j]
                kbCounter += 2
            else:
                nextTime[i][j] = indirectPath
                nextStop[i][j] = n-1
                kbCounter += 2

    # print n
    # print "Travel time: "
    # printMatrix(nextTime)
    # print "Next stop: "
    # printMatrix(nextStop)
    allTimes.append(nextTime)
    allStops.append(nextStop)

print "Matrix that gives SHORTEST travel times from node (row number, i) to node (column number, j):"
printMatrix(allTimes[10])

# Create matricies to keep track of paths and flow on each edge
pathMatrix = makeMatrix(numNodes, 0, False)
stopMatrix = allStops[numNodes]
edgeFlowMatrix = makeMatrix(numNodes, 0, False)

# print "Stop Matrix"
# printMatrix(stopMatrix)

# Construct matrix with the paths and edge traffic
for i in range(numNodes):
    for j in range(numNodes):
        if i == j:
            pathMatrix[i][j] = j
            edgeFlowMatrix[i][j] = j
            kbCounter += 1
            continue
        if times[i][j] == BIGINT:
            edgeFlowMatrix[i][j] = BIGINT
            kbCounter += 1

        ii = i
        jj = j
        path = [i]
        kbCounter += 1
        while stopMatrix[ii][jj] != BIGINT:
            path.append(stopMatrix[ii][jj])
            prevstop = ii
            ii = stopMatrix[ii][jj]
            edgeFlowMatrix[prevstop][ii] = edgeFlowMatrix[prevstop][ii] + flows[i][j]
            kbCounter += 1
        pathMatrix[i][j] = path
        kbCounter += 1

print "Matrix that gives amount of flow from node (row number, i) to node (column number, j):"
printMatrix(flows)
print "Matrix of path taken from node (row number, i) to node (column number, j):"
printMatrix(pathMatrix)
print "Matrix that shows the amount of traffic on each edge assuming they take the path in the above matrix:"
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
                kbCounter += 1
                continue
            currentFlow = allFlows[n-1]
            currentStop = allStops2[n-1]

            directPath = currentFlow[i][j]
            indirectPath = currentFlow[i][n-1] + currentFlow[n-1][j]
            kbCounter += 1
            if directPath <= indirectPath:
                nextFlow[i][j] = directPath
                nextStop[i][j] = currentStop[i][j]
                kbCounter += 2
            else:
                nextFlow[i][j] = indirectPath
                nextStop[i][j] = n-1
                kbCounter += 2
    allFlows.append(nextFlow)
    allStops2.append(nextStop)

# print "Matrix for the Sneakiest path between two nodes:"
printMatrix(allFlows[numNodes])

# Construct matrix for path taken
flowPathMatrix = makeMatrix(numNodes, 0, False)
flowStopMatrix = allStops2[numNodes]
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
            kbCounter += 4
            continue

        ii = i
        jj = j
        flowPath = [i]
        while flowStopMatrix[ii][jj] != " ":
            flowPath.append(flowStopMatrix[ii][jj])
            flowprevstop = ii
            ii = flowStopMatrix[ii][jj]
            minPathEdgeMatrix[i][j] = min(minPathEdgeMatrix[i][j], allFlows[numNodes][flowprevstop][ii])
            maxPathEdgeMatrix[i][j] = max(maxPathEdgeMatrix[i][j], allFlows[numNodes][flowprevstop][ii])
            sumPathMatrix[i][j] = sumPathMatrix[i][j] + allFlows[numNodes][flowprevstop][ii]
            kbCounter += 3
        flowPathMatrix[i][j] = flowPath
        hopPathMatrix[i][j] = (len(flowPath)-1)
        avePathMatrix[i][j] = float(sumPathMatrix[i][j]) / (len(flowPath)-1)
        kbCounter += 3

# Output results
print "Matrix of path to take for sneakiest path between two nodes:"
printMatrix(flowPathMatrix)
# print "Matrix of minimum traffic edge on sneaky path:"
# printMatrix(minPathEdgeMatrix)
# print "Matrix of maximum traffic edge on sneaky path:"
# printMatrix(maxPathEdgeMatrix)
# print "Matrix of total traffic on sneaky path:"
# printMatrix(sumPathMatrix)
# print "Matrix of number of edges taken on sneaky path:"
# printMatrix(hopPathMatrix)
# print "Matrix of average traffic for an edge on sneaky path:"
# printMatrix(avePathMatrix)
# print "Number of nodes"
# print numNodes
# print "Number of Key and Basic operations performed"
# print kbCounter
# print "CPU Util"
# print psutil.cpu_percent()
#
print "Sneakiest path from " + str(startNode+1) + " to " + str(endNode+1)
print allFlows[numNodes][startNode][endNode]
print "Path (add 1 to each node)"
print flowPathMatrix[startNode][endNode]