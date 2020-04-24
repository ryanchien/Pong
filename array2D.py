#prints 2D array

from prettytable import PrettyTable

def printArray(array):

	p = PrettyTable()
	for row in array:
	    p.add_row(row)

	print (p.get_string(header=False, border=False))
