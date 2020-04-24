# prints thermo graphic of image and pixel likelihood
import matplotlib.pyplot as plt

# heatmap of 2D array
def heatMap(array,size):

	# make array for data of given size
	data = [[0 for i in range(size)] for j in range(size)]

	for i in range(size):
		for j in range(size):
			data[i][j] = int(array[i][j])

	fig, ax = plt.subplots()

	cax = ax.imshow(data, interpolation='nearest', cmap='jet')

	# Add colorbar, make sure to specify tick locations to match desired ticklabels
	cbar = fig.colorbar(cax, ticks=[-30,0,30])
	cbar.ax.set_yticklabels(['-', '0', '+'])  # vertically oriented colorbar

	plt.show()

# graph list of data
def graphData(list,x_axis,y_axis):
	plt.plot(list)
	plt.xlabel(x_axis)
	plt.ylabel(y_axis)
	plt.title('Training Curve')
	plt.show()