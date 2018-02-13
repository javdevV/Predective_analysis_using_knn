import csv
import random
import math
import operator

# 1 LOAD DATA
def loadDataset(filename, split, trainingSet=[],testSet=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset)-1):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[y])


# 2 SIMILARITY (GET DISTANCE BETWEEN TOW VECTORS)
def eucDistance(instance1, instance2, lenghth):
    distance = 0
    for x in range(lenghth):
        distance += pow(instance1[x]-instance2[x],2)
        return math.sqrt(distance)

data1 = [4,4,4,'a']
data2 = [4,4,4,'b']


# 3 GET NEAREST NEIGHBOR
def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = eucDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors
    
# 4 RESPONSE 
def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        # print('response =' + repr(response))
        if response in classVotes:
            classVotes[response]+=1
        else:
            classVotes[response]=1
    sortedVotes = sorted(classVotes.iteritems(),key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


# 5 Accuracy 
def getAccuracy(testSet, predictions):
    corret=0
    for x in range(len(testSet)):
        if testSet[x][-1] is predictions[x]:
            corret+=1
    return (corret/float(len(testSet))) *100.0
# 6 main

def main():
	# prepare data
	trainingSet=[]
	testSet=[]
	split = 0.67
	loadDataset('data.csv', split, trainingSet, testSet)
	print 'Train set: ' + repr(len(trainingSet))
	print 'Test set: ' + repr(len(testSet))
	# generate predictions
	predictions=[]
	k = 3
	for x in range(len(testSet)):
		neighbors = getNeighbors(trainingSet, testSet[x], k)
		result = getResponse(neighbors)
		predictions.append(result)
		print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: ' + repr(accuracy) + '%')
	
main()