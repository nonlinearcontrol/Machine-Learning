########## guess_maze_path.py ##########

'''

- This script implements an attempt to solve a maze path by minimizing f costs

'''

#########
# imports
#########

from math import sqrt

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
start_g = 0.0; start_h = 0.0; start_f = 0.0 # initialize A* parameters
population_size = 1 # define how many initial guesses at paths that the algorithm will take
elite_size = 1 # define how many paths from the population will automatically make the next generation
mutation_rate = 0.01 # define the chance to remove the path and create a new one
generations = 1 # define how many generations of paths the algorithm will analyze

######################
# define the algorithm
######################

def create_node(position, g, h, f):
	'''
	create a node as a location on the maze with corresponding g, h, and f values
	'''
	return [position, g, h, f]

# test
# node = create_node(start_node, start_g, start_h, start_f)
# print(node)

def create_path(maze, start_node, end_node, start_g, start_h, start_f):
	'''
	create a path around the maze from start to finish (steals concepts from A* but actually doesn't implement A* completely - as the path is random)
	'''
	on_path = [] # define which full nodes are already in the path
	path = [] # define the node x,y positions the algorithm takes to solve the maze
	current_node = create_node(start_node, start_g, start_h, start_f) # define the current node of the path as the start_node
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
			new_node = create_node(node_position, start_g, start_h, start_f) # if this potnential next position is on the maze and not blocked, create a node for it
			next_moves.append(new_node) # add the node we just created to a list of potential moves we can make next in the maze
		for node in next_moves:
			if node[0] in path: # check if the potential node is on the path already
				continue # if this node is already in the path, skip it (avoid cycling b/w the same nodes over and over again)
			# create g, h, f values for each potential node
			if node[0][0] == current_node[0][0] or node[0][1] == current_node[0][1]:
				node[1] = current_node[1] + 1
			else:
				node[1] = current_node[1] + sqrt(2)
			node[2] = (node[0][0] - end_node[0])**2 + (node[0][1] - end_node[1])**2 # h = the distance b/w the current node and the end_node
			node[3] = node[1] + node[2] # f = g + h
		# delete potential nodes that are already in the path (https://stackoverflow.com/questions/1207406/how-to-remove-items-from-a-list-while-iterating)
		next_moves = [node for node in next_moves if not node[1] == 0]
		if not next_moves: # check if there are no potential next moves (the path is stuck in the maze and has failed)
			break # break the while loop. the path is stuck and didn't reach the end_goal, resulting in an epic fail
		next_moves.sort(key=lambda x: x[-1])
		best_next_move = next_moves[0]
		on_path.append(best_next_move) # append the on_path list to include the new random position
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

path = create_path(maze, start_node, end_node, start_g, start_h, start_f)
print(path)
visualize_path(maze, path)


