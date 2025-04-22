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

# Play a random game
def randomGame(b):
	p = 1  # player 1 goes first
	# continue to play until board is full
	while not boardFull(b):
		# make a random play
		b = randomPlay(b, p)
		# check for a win
		if ckWin(b):
			return b
		# toggle player
		p = 2 if p == 1 else 1
	# board is full
	return b
