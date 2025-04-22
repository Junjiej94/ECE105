import numpy as np
import random
import string

"""
Junjie Jiang
14583901

ASSIGNMENT: COMPLETE function fwia() below
"""

"""
ECE 105: Programming for Engineers 2
Created September 4, 2020
Steven Weber

Modified April 5, 2023 
Naga Kandasamy 

Word Search Solution

This code creates and solves a word search

Variable convention:
l: list or tuple
nr: number of rows
nc: number of columns
l_min: minimum list length
l_max: maximum list length
a: 2d-array with nr rows and nc columns
nw: number of words (to be found)
w: a word to be found
wl: a list of words to be found
i,j: a row, column index (from a)
wp: a word position (row/column, r/c index, start/stop index)
wpl: a list of word positions (one for each word)
"""

# return a numpy 2d-array with nr rows, nc columns,
# and each entry drawn uniformly at random from tuple l
def genRandMatrix(l, nr, nc):
	return np.array([random.choices(l, k=nc) for _ in range(nr)])

# rwil: return a random word from a list l
# the random word should have length between l_min and l_max
def rwil(l, l_min, l_max):
	# si: random starting index for the word
	si = random.choice(range(len(l) - l_min))
	# sf: random stopping index for the word
	sf = random.choice(range(si+l_min, min(len(l),si+l_max+1)))
	# at random, return word either forwards (f) or backwards (b)
	if random.choice(['f','b']) == 'f':
		return l[si:sf]
	else:
		return l[si:sf][::-1]

# rrca: return a random row or column from a 2d-array a
def rrca(a):
	# at random, choose to return a row or a column
	if random.choice(['r','c']) == 'r':
		# at random, return one of the rows from a
		return a[random.choice(range(a.shape[0])),:]
	else:
		# at random, return one of the columns from a
		return a[:,random.choice(range(a.shape[1]))]

# grwlim: generate random word list from a 2d-array a
# there should be nw words, each of length between l_min, l_max
def grwlim(a, nw, l_min, l_max):
	# get a random row or column by calling rrca()
	# then get a random word from that list by calling rwil()
	return [rwil(rrca(a), l_min, l_max) for _ in range(nw)]

# return whether or not word w is in list l
def bwil(l, w):
	return ''.join(w) in ''.join(l)

# return the starting and ending position of word w in list l
def pwil(l, w):
	# iterate over the starting index (si) in list l
	for si in range(len(l)):
		# return start index (si) and stopping index (si+len(w))
		if list(l[si:si+len(w)]) == list(w):
			return si, si+len(w)

"""
COMPLETE:
fwia takes 2d-array a and word w, and returns position of w in a
1. make use of helper functions bwil and pwil:
bwil(l, w) returns True/False if word w is/not in list l
pwil(l, w) returns the start/stop positions of word w in list l
2. iterate over all rows and columns in a
3. for each row/column, check the list in both "forward" and reversed direction
RECALL: if l is a list then l[::-1] is the list reversed
4. return 4 items: rc, rci, si, ei
i) rc = 'r' if w is in a row of a, else rc = 'c' if w is in a column of a
ii) rci is the row/column index of a containing w
iii) si: the starting index of the word (always less than ei)
iv) ei: the ending index of the word (always greater than si)
"""
# find word w in 2d-array a
def fwia(a, w):
    rc = ''
    rci = si = ei = -1

    # iterate over row indices i
    for i in range(a.shape[0]):
        row = a[i, :]
		# if word w is found in the "forward" list:
        if bwil(row, w):
            rc = 'r'
            rci = i
            si, ei = pwil(row, w)
		# else, if word w is found in "reversed" list:
        elif bwil(row[::-1], w):
            rc = 'r'
            rci = i
            si, ei = pwil(row[::-1], w)
            # adjust indices for reversed row
            si, ei = len(row) - ei, len(row) - si

    # iterate over column indices j
    for j in range(a.shape[1]):
        col = a[:, j]
		# if word w is found in the "forward" list:
        if bwil(col, w):
            rc = 'c'
            rci = j
            si, ei = pwil(col, w)
		# else, if word w is found in "reversed" list:
        elif bwil(col[::-1], w):
            rc = 'c'
            rci = j
            si, ei = pwil(col[::-1], w)
            # adjust indices for reversed column
            si, ei = len(col) - ei, len(col) - si
	# return 4 components of location:
    return rc, rci, si, ei


# faw: find all words in word list wl in 2d-array a
def faw(a, wl):
	# call fwia(a,w) to find each word w in word list wl
	return [fwia(a, w) for w in wl]

# print 2d-array a
def printArray(a):
	# print each row r in 2d-array a, joined into a string
	[print("{}".format(' '.join(r))) for r in a]

# piwp: indicate whether position (i,j) is in word position wp
# N.B.: wp has the four components returned from function fwia()
def piwp(i, j, wp):
	# if wp is row, and wp's row is i, and wp's indices contain j
	if wp[0] == 'r' and wp[1] == i and wp[2] <= j and j < wp[3]:
		return True
	# if wp is col, and wp's col is j, and wp's indices contain i
	if wp[0] == 'c' and wp[1] == j and wp[2] <= i and i < wp[3]:
		return True
	# else, position (i,j) is not contained in word position wp
	return False

# piwpl: return whether position (i,j) in word position list wpl
def piwpl(i, j, wpl):
	# return True if any word position wp in wpl holds pos. (i,j)
	return any([piwp(i,j,wp) for wp in wpl])

# print subset of 2d-array a matching word position list wpl
def printWL(a, wpl):
	# iterate over all row indices i in 2d-array a
	for i in range(a.shape[0]):
		# iterate over all column indices j in 2d-array a
		for j in range(a.shape[1]):
			# if pos. (i,j) in wpl: print the letter
			if piwpl(i, j, wpl): print("{} ".format(a[i,j]), end='')
			# else, pos(i,j) NOT in wpl: print a "."
			else: print(". ", end='')
		print("")

# Main program 
if __name__ == "__main__":
	# create the list l of characters for word search: a,b,...,z
	l = list(string.ascii_lowercase)
	# number of rows and number of columns in 2d-array a
	nr, nc = 20, 20
	# create 2d-array a by calling genRandMatrix()
	a = genRandMatrix(l, nr, nc)
	# print the 2d-array a
	print("Word search array")
	printArray(a)

	# number of words (nw), range of word lengths (l_min, l_max)
	nw, l_min, l_max = 10, 5, 10
	# generate the random list of words wl from 2d-array a:
	wl = grwlim(a, nw, l_min, l_max)
	# print the target word list
	print("\nTarget word list:")
	printArray(wl)

	# find the word position list for the word list wl in array a
	wpl = faw(a,wl)
	# print the word position list wpl as subset of a
	print("\nSolution:")
	printWL(a, wpl)
