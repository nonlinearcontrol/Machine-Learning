########## guess_maze_path.py ##########

'''

- This script guesses the path around a maze

'''

#########
# imports
#########

from random import choice

####################
# initial conditions
####################

maze = [[0, 0, 0, 0, 1, 0], 
		[0, 0, 1, 1, 1, 0],
		[0, 1, 0, 0, 1, 0],
		[0, 1, 0, 0, 1, 0],
		[0, 0, 1, 1, 1, 0],
		[0, 0, 0, 0, 0, 0]]
start_node = [2, 3] # define where the maze starts
end_node = [0, 5] # define where the maze ends

######################
# define the algorithm
######################

def create_node(position):
	'''
	create a node as a location on the maze
	'''
	return [position]

def create_path(maze, start_node, end_node):
	'''
	create a random path around the maze
	'''
	on_path = [] # define which full nodes are already in the path
	path = [] # define the node x,y positions the algorithm takes to solve the maze
	current_node = create_node(start_node) # define the current node of the path as the start_node
	on_path.append(current_node) # add the start_node to the on_path list
	path.append(current_node[0]) # add the start_node x,y position to the path
	# define the path through the maze
	while current_node[0] != end_node: # break the loop if the path finds the end of the maze
		next_moves = [] # define a list of potential next moves the path could take
		for new_position in [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]: # the path can either go up/down, left/right, or in any of the 4 diagonal directions
			node_position = [current_node[0][0] + new_position[0], current_node[0][1] + new_position[1]] # this is full list of potential possible next moves in the path
			# check if moving to this position puts the path off the maze
			if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
				continue # if moving to this position puts us off the maze, skip it
			# check if moving to this position is blocked
			if maze[node_position[0]][node_position[1]] != 0:
				continue # if moving to this position is blocked, skip it
			new_node = create_node(node_position) # if this potnential next position is on the maze and not blocked, create a node for it
			next_moves.append(new_node) # add the node we just created to a list of potential moves we can make next in the maze
		random_next_move = choice(next_moves) # make a random guess on where to move next along the path in the maze -> not implementing A* b/c we are randomly moving forward instead of moving forward in the optimal way
		on_path.append(random_next_move) # append the on_path list to include the new random position
		current_node = on_path[-1] # update the current node to the last node in the path
		path.append(current_node[0]) # update the path with the new node's x,y position
	return path

def visualize_path(maze, path):
	'''
	visualize the maze path by printing the path to the screen
	'''
	for node in path:
		maze[node[0]][node[1]] = '>' # use the ge character to show the path 
	for i in maze:
		print(*i) # print the maze showing the path we took

########################
# visualize the solution
########################

path = create_path(maze, start_node, end_node)
print(path)
visualize_path(maze, path)

