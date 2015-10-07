# CSCI 3202 - Intro to Artificial Intelligence
# Assignment 5: Markov DEcision Processes
# Brian Salmon

# Recieved online help from: http://www.redblobgames.com/pathfinding/a-star/implementation.html


import sys
import math

GAMMA = 0.9

class Node(object):
	def __init__(self, location, type, reward):
		self.location = location 
		self.type = type # value: empty = 0, mountain =1, wall = 2, snake = 3, barn = 4, and end = 5
		self.reward = reward
		self.utility = 0
		self.direction = '' 
		self.parent = None 
		self.north = None
		self.south = None
		self.east = None
		self.west = None

	# Calculate the utility of the node:
	def utilityCalculator(self):

		if self.type == 'terminal':
			self.utility = self.reward
			self.direction = 'Done'
			return self.utility

		# Determine what values to use in the calculation
		if self.north != None:
			northUtil = self.north.utility
		else:
			northUtil = self.utility
		if self.south != None:
			southUtil = self.south.utility
		else:
			southUtil = self.utility
		if self.east != None:
			eastUtil = self.east.utility
		else:
			eastUtil = self.utility
		if self.west != None:
			westUtil = self.west.utility
		else:
			westUtil = self.utility

		northOption = (0.8 * northUtil) + (0.1 * eastUtil) + (0.1 * westUtil)
		southOption = (0.8 * southUtil) + (0.1 * eastUtil) + (0.1 * westUtil)
		eastOption = (0.8 * eastUtil) + (0.1 * northUtil) + (0.1 * southUtil)
		westOption = (0.8 * westUtil) + (0.1 * northUtil) + (0.1 * southUtil)

		options = ([northOption, 'North', self.north], [southOption, 'South', self.south], 
			[eastOption, 'East', self.east], [westOption, 'West', self.west])
		bestOption = max(options)
		
		self.utility = self.reward + (GAMMA * bestOption[0])
		self.direction = bestOption[1]
		self.parent = bestOption[2]

		return self.utility

def transform(mapString):
	xPos = 0
	yPos = 7
	rows = mapString.split('\n')
	newRows = list()
	nodeList = []

	for k in range(10):
			nodeList.append([])
			for j in range(8):
				nodeList[k].append(None)

	for row in rows:
		if row != '':
			newRows.append(row.split(' '))
	for c in newRows:
		xPos = 0
		for r in c:
			pathType = ''
			reward = 0
			if r == '0':
				pathType = 'path'
			elif r == '1':
				pathType = 'mountain'
				reward = -1.0
			elif r == '2':
				pathType = 'wall'
			elif r == '3':
				pathType = 'snake'
				reward = -2.0
			elif r == '4':
				pathType = 'barn'
				reward = 1.0
			else:
				pathType = 'terminal'
				reward = 50.0
			newNode = Node([xPos, yPos], pathType, reward)
			nodeList[xPos][yPos] = newNode
			xPos = xPos + 1
		yPos = yPos - 1

	return nodeList
	
	
def checkNodes(nodeList):
	xBound = 10
	yBound = 8

	for x in range(10):
		for y in range(8):
			current = nodeList[x][y]
			if current.type != 'wall':
				if x + 1 < xBound and nodeList[x+1][y].type != 'wall':
					current.east = nodeList[x+1][y]
				if x - 1 >= 0 and nodeList[x-1][y].type != 'wall':
					current.west = nodeList[x-1][y]
				if y + 1 < yBound and nodeList[x][y+1].type != 'wall':
					current.north = nodeList[x][y+1]
				if y - 1 >= 0 and nodeList[x][y-1].type != 'wall':
					current.south = nodeList[x][y-1]
	return nodeList
	
def iterateValue(nodeList, minChange):
	maxChangeInCycle = minChange + 1
	iterate = 0
	while maxChangeInCycle > minChange:
		maxChangeInCycle = 0
		iterate = iterate + 1
		for y in range(7, -1, -1):
				for x in range(9, -1, -1):
					if nodeList[x][y].type != 'wall':
						old_utility = nodeList[x][y].utility
						new_utility = nodeList[x][y].utilityCalculator()
						currentChange = abs(old_utility - new_utility)
						if currentChange > maxChangeInCycle:
							maxChangeInCycle = currentChange

	return nodeList
	
	
def printValue(nodeList):
	nodeListFormatted = []

	for k in range(8):
		nodeListFormatted.append([])
		for j in range(10):
			nodeListFormatted[k].append(None)

	for y in range(8):
		for x in range(10):
			if nodeList[x][y].type != 'wall':
				nodeListFormatted[7-y][x] = str(nodeList[x][y].direction)
			else:
				nodeListFormatted[7-y][x] = 'Wall'

	col_width = max(len(word) for row in nodeListFormatted for word in row) + 2
	
	for row in nodeListFormatted:
		print "".join(word.ljust(col_width) for word in row)

def printPath(currentNode, lastNode):
	if currentNode.type == 'terminal':
		print "End: (" + str(currentNode.location[0]) + "," + str(currentNode.location[1]) + ")  Reward:", '%.3f' % currentNode.utility
		return
	elif currentNode.parent == lastNode:
		print "Stuck. Two nodes have best paths to each other."
		print "Final Location:", currentNode.location[0], "," ,currentNode.location[1], "Utility:", '%.3f' % currentNode.utility
		return
	else:
		print "Location: (" + str(currentNode.location[0]) + "," + str(currentNode.location[1]) + ")  Utility:", '%.3f' % currentNode.utility
		return printPath(currentNode.parent, lastNode)

def readFile(fileName):
	mapString = open(fileName, 'r')
	mapString = mapString.read()
	return mapString
	
def inputText():
	if len(sys.argv) < 3:
		print "Not enough arguments given!"
		print "Should be 3."
		return (False, False)
	elif len(sys.argv) > 3:
		print "Too many arguments given!"
		print "Should be 3."
		return (False, False)
	elif sys.argv[1] != "World1MDP.txt":
		print "Can't find world!"
		print "Should be World1MDP.txt"
		return (False, False)
	else:
		return (sys.argv[1], float(sys.argv[2]))
		



if __name__ == "__main__":
	mapFile, eVal = inputText()
	if mapFile != False and eVal != False:
		minChange = (eVal * .1)/.9
		mapString = readFile(mapFile)
		nodeList = transform(mapString)
		nodeList = checkNodes(nodeList)
		nodeList = iterateValue(nodeList, minChange)
		printPath(nodeList[0][0], None)
