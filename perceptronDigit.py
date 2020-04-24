# MP4 - perceptronDigit.py:
# Traing weights for each digit class, then
# classify for training.

import sys,random,pickle,math
import readDigitFiles,array2D,plot

# constants
MaxEpoch = 100

# can change these weights:

# initial weight
def initWeight():
	return 0

# initial bias (if any)
def initBias():
	return 0

# weight vectors for each class 
w0 = [[initWeight() for col in range(28)] for col in range(28)]
w1 = [[initWeight() for col in range(28)] for col in range(28)]
w2 = [[initWeight() for col in range(28)] for col in range(28)]
w3 = [[initWeight() for col in range(28)] for col in range(28)]
w4 = [[initWeight() for col in range(28)] for col in range(28)]
w5 = [[initWeight() for col in range(28)] for col in range(28)]
w6 = [[initWeight() for col in range(28)] for col in range(28)]
w7 = [[initWeight() for col in range(28)] for col in range(28)]
w8 = [[initWeight() for col in range(28)] for col in range(28)]
w9 = [[initWeight() for col in range(28)] for col in range(28)]

# add bias
w0[27].append(initBias())
w1[27].append(initBias())
w2[27].append(initBias())
w3[27].append(initBias())
w4[27].append(initBias())
w5[27].append(initBias())
w6[27].append(initBias())
w7[27].append(initBias())
w8[27].append(initBias())
w9[27].append(initBias())

# store in weight list
weights = [w0,w1,w2,w3,w4,w5,w6,w7,w8,w9]

# get training & test data
trainingData = readDigitFiles.getTraining()
tests = readDigitFiles.getTest()
testData = tests[0]
testCounts = tests[1]

# get alpha value based on current epoch, t
def alpha(t):
	return (MaxEpoch / (MaxEpoch + t))

# sigmoid function (for differentiable perceptron)
def sigmoid(x):
  return 1 / (1 + math.exp(-x))

# randomize order of training data
def randomOrder():

	# use randomized swap algorithm to shuffle order of training images
	for i in range(len(trainingData)):

		j = random.randint(0,len(trainingData)-1)
		temp = trainingData[i]
		trainingData[i] = trainingData[j]
		trainingData[j] = temp

# parse data (give each pixel an integer value)
def parseData(data):

	# change all images
	for element in data:
		image = element[0]
		newImage = [[0 for col in range(28)] for row in range(28)]

		# modify pixels
		for row in range(28):
			for col in range(28):

				# if foreground
				if image[row][col] == '#':
					newImage[row][col] += 1

				# if middleground
				elif image[row][col] == '+':
					newImage[row][col] += 1	# change to .5 for ternary values

				else:
					newImage[row][col] += 0

		element[0] = newImage

# update weights for some value (x) of class, c, misclassified as c_prime (cp).... with alpha
def updateWeights(x,w_c,w_cp,alpha):

	# w_c <- w_c + alpha * x
	# w_cp <- w_cp - alpha * x
	for row in range(28):
		for col in range(28):
			w_c[row][col] += alpha * x[row][col] # * sigmoid(w_c[row][col]*x[row][col])*(1-sigmoid(w_c[row][col]*x[row][col]))
			w_cp[row][col] -= alpha * x[row][col] #* sigmoid(w_cp[row][col]*x[row][col])*(1-sigmoid(w_cp[row][col]*x[row][col]))

	# update bias (consider x = 1)
	w_c[27][28] += alpha
	w_cp[27][28] -= alpha

# decision rule for training (c' = argmax(w_c * x + b).... w_c and x are vectors/sums of all)
def decisionRule(x):
	
	# max result... the one that will be selected
	max = -100000
	cur = 0

	# try all classes
	for p in range(len(weights)):

		# get weight vector and bias
		w = weights[p]
		b = w[27][28]
		cur = 0		# current result value for classification

		for row in range(28):
			for col in range(28):
				cur += w[row][col] * x[row][col]

		# add bias
		cur += b

		# make guess
		if cur > max:
			guess = p
			max = cur

	# return classification
	return guess

# train weights for each dight (including the bias)
def learnWeights():
	
	# training errors (for training curve)
	trainingErrors = []

	# test up until limit of epochs
	for t in range(MaxEpoch):
		print(t)

		# try all training images until no misclassifications
		curErrors = 0

		for image in trainingData:
			
			# get value vector (x) and true label (c)
			x = image[0]
			c = int(image[1])

			# make guess (cp)
			cp = decisionRule(x)

			# if incorrect, update weights, count error for current epoch
			if c != cp:
				updateWeights(x,weights[c],weights[cp],alpha(t))
				curErrors += 1

		# add errors of current epoch to overall list
		trainingErrors.append(curErrors)

		# if there were no errors, weight training is done
		if curErrors == 0:
			print("done")
			break
		else:
			print(curErrors)

	# return training errors when done
	return trainingErrors

# classify test data with weight vectors
def classify():

	# confusion matrix
	confusionMatrix = [[0 for predicted in range(10)] for actual in range(10)]

	for image in testData:

		# get value and actual label
		x = image[0]
		actual = int(image[1])

		# guess via decision rule
		predicted = decisionRule(x)

		# add to confusion matrix
		confusionMatrix[actual][predicted] += 1

	# return confusion
	return confusionMatrix


# get rates for confusion matrix (and overall accuracy)
def confusionRates():

	# total test images
	total = sum(testCounts)

	# get total correct guesses
	correct = 0

	for i in range(10):
		correct += confusionMatrix[i][i]

	# get overall accuracy (rounded to two decimals)
	overall = round((correct/total)*100,2)

	# calculate individual accuracies [actual][predicted]
	for i in range(10):
		for j in range(10):

			confusionMatrix[i][j] = round((confusionMatrix[i][j]/testCounts[i])*100,2)

	return overall

# parse training and testing data (give numerical values for pixels)
parseData(trainingData)
parseData(testData)

# randomize order
# randomOrder()	

# learn weights from training set
trainingErrors = learnWeights()

"""
# 'save' weights.... save time for classifying and avoid retraining every time
f = open('store.pckl', 'wb')
pickle.dump([weights,trainingErrors], f)
f.close()

f = open('store.pckl', 'rb')
object = pickle.load(f)
f.close()
weights = object[0]
trainingErrors = object[1]"""

# classify test set
confusionMatrix = classify()

# get accuracies
overallAccuracy = confusionRates()
print(overallAccuracy)

# print confusion matrices [actual][predicted]
array2D.printArray(confusionMatrix)

# graph errors
plot.graphData(trainingErrors,'Epochs','# of Errors')

plot.heatMap(weights[3],28)
