########## astar_maze_path_plot.py ##########

'''

- This script implements the A* path finding algorithm and plots the result

'''

#########
# imports
#########

from math import sqrt
import matplotlib.pyplot as plt
from operator import itemgetter

####################
# initial conditions
####################

edge_min = 0
edge_max = 8
maze_edges = [[edge_min, edge_min], [edge_min, edge_max], [edge_max, edge_max], [edge_max, edge_min]]
barriers = [(2, 4), (2, 5), (2, 6), (3, 6), (4, 6), (5, 6), (5, 5), (5, 4), (5, 3), (5, 2), (4, 2), (3, 2)]
start = (7, 7)
end = (4, 5)

######################
# create the algorithm
######################


def plot_maze(maze_edges, barriers):
	'''
	- plot the maze board as defined by the maze edges and barriers
	'''
	# plot the board
	i = 0
	j = 1
	while j < len(maze_edges):
		plt.plot([maze_edges[i][0], maze_edges[j][0]], [maze_edges[i][1], maze_edges[j][1]], 'k-')
		i += 1
		j += 1
	plt.plot([maze_edges[-1][0], maze_edges[0][0]], [maze_edges[-1][1], maze_edges[0][1]], 'k-')
	# plot the barriers
	i = 0
	j = 1
	while j < len(barriers):
		plt.plot([barriers[i][0], barriers[j][0]], [barriers[i][1], barriers[j][1]], 'k-')
		i += 1
		j += 1

def create_g(current_node, child):
	'''
	- define the g cost for the A* algorithm
	'''
	if child[0] == current_node[0] or child[1] == current_node[1]:
		g = 1			
	else:
		g = sqrt(2)
	return g


def create_h(start, end):
	'''
	- define the h cost for the A* algorithm
	'''
	distx = abs(start[0] - end[0])
	disty = abs(start[1] - end[1])
	if distx > disty:
		h = sqrt(2)*disty + (distx - disty)
	else:
		h = sqrt(2)*distx + (disty - distx)
	return h

def create_children(current_node, edge_min, edge_max, barriers):
	'''
	- create the children of a parent node
	'''
	children = []
	for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
		node_position = (current_node[0] + new_position[0], current_node[1] + new_position[1])
		# check if moving to this position puts the path off the map
		if node_position[0] == edge_max or node_position[0] == edge_min or node_position[1] == edge_max or node_position[1] == edge_min:
			continue
		# check if moving to this position is blocked
		blocked = False
		for barrier in barriers:
			if node_position == barrier:
				blocked = True
				break
		if blocked:
			continue
		children.append(node_position)
	return children

def astar(start, end):
	g = {}
	f = {}
	g[start] = 0
	f[start] = create_h(start, end)
	closed_list = set()
	open_list = set([start])
	parent = {}
	while len(open_list) > 0:
		# get the child in the open list with the lowest f cost
		current_node = None
		current_f = None
		for node in open_list:
			if current_node is None or f[node] < current_f:
				current_f = f[node]
				current_node = node
		# check if the maze is complete
		if current_node == end:
			# retrace our steps
			path = [current_node]
			while current_node in parent:
				current_node = parent[current_node]
				path.append(current_node)
			path.reverse()
			return path
		# mark the current parent as closed
		open_list.remove(current_node)
		closed_list.add(current_node)
		# update the costs for each child of the parent
		children = create_children(current_node, edge_min, edge_max, barriers)
		for child in children:
			if child in closed_list:
				continue # we already processed this node
			candidates_g = g[current_node] + create_g(current_node, child)
			if child not in open_list:
				open_list.add(child)
			elif candidates_g >= g[current_node]:
				continue # this g score is worse than previously found
			# adopt this g score
			parent[child] = current_node
			g[child] = candidates_g
			h = create_h(child, end)
			f[child] = g[child] + h

#########
# testing
#########
maze = plot_maze(maze_edges, barriers)
path = astar(start, end)
plt.plot([i[0] for i in path], [i[1] for i in path])
plt.show()


















# def create_node(position, parent, g, h, f):
# 	'''
# 	- create a noce as defined by its position, its parent, and its g, h, and f costs
# 	'''
# 	return [position, parent, g, h, f]

# def create_children(current_node, edge_min, edge_max, barriers):
# 	'''
# 	- create the children of a parent node
# 	'''
	# children = []
	# for new_position in [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]:
	# 	node_position = [current_node[0][0] + new_position[0], current_node[0][1] + new_position[1]]
	# 	# check if moving to this position puts the path off the map
	# 	if node_position[0] == edge_max or node_position[0] == edge_min or node_position[1] == edge_max or node_position[1] == edge_min:
	# 		continue
	# 	# check if moving to this position is blocked
	# 	blocked = False
	# 	for barrier in barriers:
	# 		if node_position == barrier:
	# 			blocked = True
	# 			break
	# 	if blocked:
	# 		continue
	# 	new_node = create_node(node_position, start_parent, start_g, start_h, start_f)
	# 	children.append(new_node)
# 	return children
# 	# loop through the children
# 	# for child in children:
# 	# 	# create parent, g, h, f values for the children
# 	# 	child[1] = [[current_node[0]], [current_node[1]], [current_node[2]], [current_node[3]]]
# 	# 	if child[0][0] == current_node[0][0] or child[0][1] == current_node[0][1]:
# 	# 		child[2] = current_node[2] + 1
# 	# 	else:
# 	# 		child[2] = current_node[2] + sqrt(2)
# 	# 	distx = abs(child[0][1] - end_node[1])
# 	# 	disty = abs(child[0][0] - end_node[0])
# 	# 	if distx > disty:
# 	# 		child[3] = sqrt(2)*disty + (distx - disty)
# 	# 	else:
# 	# 		child[3] = sqrt(2)*distx + (disty - distx)
# 	# 	child[4] = child[2] + child[3]
# 	# return children


# def astar():















# 	open_list = []
# 	closed_list = []
# 	start = create_node(start_node, start_parent, start_g, start_h, start_f)
# 	target = create_node(end_node, start_parent, start_g, start_h, start_f)
# 	open_list.append(start)
# 	while len(open_list) > 0:
# 		open_list = sorted(open_list, key = itemgetter(-1))
# 		current_node = open_list[0]
# 		open_list.remove(current_node)
# 		closed_list.append(current_node)
# 		if current_node[0] == target[0]:
# 			path = []
# 			current = current_node
# 			while current[0] != start[0]:
# 				path.append(current)
# 				current = current[1]
# 			path.append(start)
# 			path = path[::-1]
# 			best_path = []
# 			for node in path:
# 				best_path.append(node[0])
# 			return best_path
# 			break
# 		children = create_children(current_node, edge_min, edge_max, barriers)
# 		for child in children:
# 			if child in closed_list:
# 				continue
# 			if child not in open_list:
# 				child[1] = current_node
# 				if child not in open_list:
# 					open_list.append(child)



# # maze_plot = plot_maze(maze_edges, barriers)
# # current_node = create_node([5, 1], start_parent, start_g, start_h, start_f)
# # plt.plot(current_node[0][0], current_node[0][1], 'ro')
# # children = create_children(current_node, edge_min, edge_max, barriers)
# # print(children)
# # plt.gca().set_aspect('equal')
# # plt.show()

# path = astar()
# print(path)