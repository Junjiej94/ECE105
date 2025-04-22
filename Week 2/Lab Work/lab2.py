import numpy as np
import random

"""
Junjie Jiang
14583901

ASSIGNMENT: COMPLETE randomPlay and randomGame functions below
"""

"""a
ECE 105: Programming for Engineers 2
Created September 3, 2020
Steven Weber

Modified April 4, 2023
Naga Kandasamy

Connect4 Starter Code

This code plays a random game of Connect 4 and checks for a win condition
The __main__ method will repeatedly play until a game with no winner is found

Variable convention:
nr: number of rows
nc: number of columns
b: board (6 rows, 7 columns)
c: column (1 of 7)
r: row (1 of 6)
p: player index (1 or 2)
"""

# Create the board with the initial state
def initBoard(nr, nc):
	# Create board as numpy 2D array, initialized to hold zeros
	return np.zeros((nr, nc), dtype=int)

# Find the row when placing a piece in a given column
def findRow(b, c):
	# get the number of rows
	nr = b.shape[0]
	# get the columnn from the board, convert to list
	col = list(b[:,c])
	# reverse the list (start from bottom)
	rev_col = col[::-1]
	# get the (row) index of the first 0 in the reversed list
	rri = rev_col.index(0)
	# return this position in the original list
	return nr - 1 - rri

# Get list of all open (non-full) columns in board
def openCols(b):
	open_cols = []
	# iterate over column indices j
	for j in range(b.shape[1]):
		# add j to open_cols if it contains a 0
		if 0 in b[:,j]: open_cols.append(j)
	return open_cols

"""
COMPLETE:
randomPlay takes board b and player p
1. open_cols: get list of open column indices
2. c: choose column index at random from open_cols
3. call findrow(b,c) to get row index for that column
4. b[r,c]: assign b[r,c] with player index p
5. b: return the board
"""
# Make a random play for player p
def randomPlay(b, p):
	# 1. open_cols: get list of open column indices
	open_cols = openCols(b)
	# 2. c: choose column index at random from open_cols
	c = random.choice(open_cols)
	# 3. r: call findrow(b,c) to get row index for that column
	r = findRow(b, c)
	# 4. b[r,c]: assign b[r,c] with player index p
	b[r, c] = p
	# 5. b: return the board
	return b

# Check if the board is full
def boardFull(b):
	# board is full iff there are no open columns
	return False if openCols(b) else True

"""
COMPLETE:
randomGame takes board b and repeatedly calls randomPlay:
1. stopping criterion is that the board is not full
2. get an updated board by calling randomPlay
3. check the updated board to see if a player has won, if yes, return board
4. update the player index (from 1 to 2, or from 2 to 1)
"""
# Play a random game
def randomGame(b):
	p = 1 # player 1 goes first
	# continue to play until board is full
	# replace True with stopping criterion using boardFull(b)
	while not boardFull(b):
		# make a random play
		b = randomPlay(b, p)
		# check for a win
		if ckWin(b) in ['w1', 'w2']:
			continue
		# toggle player
		if p == 1:
			p = 2
		if p == 2:
			p = 1
	# board is full
	return b

# Check board to see if either player has won the game
def ckWin(b):
	if b == []:
		return True
	# w1 is True if player 1 wins, w2 is True if player 2 wins
	w1 = any([ckRows(b,1), ckCols(b,1), ckDiagsFor(b,1), ckDiagsRev(b,1)])
	w2 = any([ckRows(b,2), ckCols(b,2), ckDiagsFor(b,2), ckDiagsRev(b,2)])
	return w1 or w2

# Check each row for a win for player p
def ckRows(b, p):
	# check each row r in b
	return any([ckArray(r,p) for r in b])

# Check each column for a win for player p
def ckCols(b, p):
	# check each column c in b
	return any([ckArray(c,p) for c in b.T])

# Check each forward diagonal for a win for player p
def ckDiagsFor(b, p):
	# offset indices for the diagonals of length 4 or more
	dMin, dMax = -2, 4
	# check each diagonal in b by specifying the offset d
	return any([ckArray(np.diagonal(b,d),p) for d in range(dMin, dMax)])

# Check each reverse diagonal for a win for player p
def ckDiagsRev(b, p):
	# reverse the board: reverse diags in b are forward diags in bf
	bf = np.fliplr(b)
	# offset indices for the diagonals of length 4 or more
	dMin, dMax = -2, 4
	# check each diagonal in bf by specifying the offset d
	return any([ckArray(np.diagonal(bf,d),p) for d in range(dMin, dMax)])

# Check if winning pattern is in array (converted to strings)
def ckArray(a, p):
	# convert the numpy 1-dim array a to a string s (no spaces)
	s = np.array2string(a, separator='')[1:-1]
	# construct the winning pattern for the given player ass ws
	ws = '1111' if p == 1 else '2222'
	# check for the winning pattern (ws) in the array string (s)
	return True if ws in s else False

# Main program 
if __name__ == "__main__":
	# Connect4 board has 6 rows and 7 columns
	nr, nc = 6, 7

	# Repeatedly play a random game until there is no winner
	n, b = 0, []
	while b == [] or ckWin(b): # ckWin(b) is True if there is a winner
		b = randomGame(initBoard(nr, nc)) # random game board
		n += 1 # number of games played

	# Print board, # attempts, and win status of board
	print(b)
	print(n)
	print(ckWin(b))