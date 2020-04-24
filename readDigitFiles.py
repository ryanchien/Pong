# readDigitFiles.py

# Read entire training and test sets (plus their labels)

import sys

# function for grouping all 28 lines from file of each image and returns it
def groupLines(file,start):
	# check for NULL
	if file == None:
		print("Error")
		return

	# add lines to image
	image = []
	for l in range(28):
		image.append(file[start+l])

	# return "image" (list)
	return image

# get training data (return list of images and labels)
def getTraining():

	# load training images and sets
	f1 = open("digitdata/trainingimages")
	set = f1.read().splitlines()

	f2 = open("digitdata/traininglabels")
	labels = f2.read().splitlines()

	# put all images and labels in list
	training = []
	l = 0

	for start in range(0,len(set),28):
		item = (groupLines(set,start),labels[l])
		training.append(list(item))
		l += 1

	return training

# get test data (return list of images and labels)
def getTest():

	# load test images and sets
	f1 = open("digitdata/testimages")
	set = f1.read().splitlines()

	f2 = open("digitdata/testlabels")
	labels = f2.read().splitlines()

	# put all images and labels in list
	test = []
	l = 0

	# get counts of tests
	counts = [0]*10

	for start in range(0,len(set),28):
		item = (groupLines(set,start),labels[l])
		counts[int(labels[l])] += 1
		test.append(list(item))
		l += 1

	return (test,counts)
