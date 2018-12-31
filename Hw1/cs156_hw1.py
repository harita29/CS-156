#!/usr/bin/python
import heapq
import math
import sys

# Constants for the NARIO program.
TEST_CASE_FILE = sys.argv[1]
USER_HEURISTIC = sys.argv[2]
HEURISTIC_EUCLIDEAN = "euclidean"
HEURISTIC_MANHATTAN = "manhattan"
HEURISTIC_MADEUP = "my_own"

# Cost for 1 move.
COST_VALUE = 1

# Node object indexes.
NODE_X = 0
NODE_Y = 1
NODE_C = 2
NODE_H = 3

# Board Constants.
NARIO = '@'
DOT_PATH = '.'
OBSTACLE = '='
DESTINATION = '#'


def load_test_case_file():
    """
    Reads test case file and returns the information.
    :return: List containing maze lines, maze height, maze width.
    """
    maze_file = open(TEST_CASE_FILE, "r")
    maze_line_list = []
    for line in maze_file:
        # Strip trailing new lines, white spaces or tabs
        maze_line_list.append(line.strip(' \t\n\r'))
    maze_file.close()
    local_maze_height = len(maze_line_list)
    # The width has to account for new line character.
    local_maze_width = len(maze_line_list[0])
    return maze_line_list, local_maze_height, local_maze_width


def locate_nario(blank=False):
    """
    Finds the X and Y position of agent in given board.
    :param blank: True if blank board without agent should be saved,
                  False otherwise.
    :return: X axis and Y axis of NARIO.
    """
    global maze_lines
    pos_y = 0
    for line in maze_lines:
        pos_x = line.find(NARIO)
        if pos_x != -1:
            if blank:
                maze_lines[pos_y] = line.replace(NARIO, DOT_PATH)
            return pos_x, pos_y
        else:
            pos_y += 1
    if pos_x == -1:
        print ("NARIO is MISSING!!")
        sys.exit(0)


def get_destination_axes():
    """
    Location of Destination
    :return: X axis and Y axis of destination.
    """
    pos_y = 0
    pos_x = 0
    return pos_x, pos_y


def is_node_in_frontier_list(frontier_list, node):
    """
    Determines if given node's state exists in the frontier list.
    :param frontier_list: Frontier list.
    :param node: Current node.
    :return: Index of node in frontier, - 1 if Do not exist.
    """
    for index in range(0, len(frontier_list)):
        if frontier_list[index][1] == node:
            return index
    return -1


def is_a_possible_move(x, y):
    """
    Determines if maze character denotes a valid move.
    :param x: X-axis.
    :param y: Y-axis.
    :return: True if valid move, False otherwise.
    """
    global maze_lines, maze_height, maze_width
    if (0 <= x < maze_width and 0 <= y < maze_height
            and maze_lines[y][x] != OBSTACLE):
        return True
    else:
        return False


def is_a_neighbor_node(node1, node2):
    """
    Determines if two nodes are neighbors.
    :param node1: First node.
    :param node2: Second node.
    :return: True if neighbor nodes, False otherwise.
    """
    if (node1[NODE_X] == node2[NODE_X] and
            (node1[NODE_Y] == node2[NODE_Y] - 1 or
                     node1[NODE_Y] == node2[NODE_Y] + 1)) \
        or (node1[NODE_Y] == node2[NODE_Y] and
            (node1[NODE_X] == node2[NODE_X] - 1 or
                     node1[NODE_X] == node2[NODE_X] + 1)):
        return True
    elif node1[NODE_Y] == node2[NODE_Y] and \
            ((node1[NODE_X] == 0 and node2[NODE_X] == maze_width-1) or
                 (node2[NODE_X] == 0 and node1[NODE_X] == maze_width-1)):
        return True
    else:
        return False


def explore_valid_actions(node):
    """
    Explore all valid actions from provided node.
    :param node: Current node.
    :return: List of possible action nodes.
    """
    global destination
    possible_action_list = []
    if node[NODE_X] == 0:
        if is_a_possible_move(maze_width-1, node[NODE_Y]):
            possible_action_list.append(create_a_node(maze_width - 1,
                                                      node[NODE_Y],
                                                      COST_VALUE))
    if node[NODE_X] == maze_width-1:
        if is_a_possible_move(0, node[NODE_Y]):
            possible_action_list.append(create_a_node(0, node[NODE_Y],
                                                      COST_VALUE))
    # Validate UP move.
    if is_a_possible_move(node[NODE_X], node[NODE_Y] - 1):
        possible_action_list.append(create_a_node(node[NODE_X],
                                                  node[NODE_Y] - 1,
                                                  COST_VALUE))
    # Validate RIGHT move.
    if is_a_possible_move(node[NODE_X] + 1, node[NODE_Y]):
        possible_action_list.append(create_a_node(node[NODE_X] + 1,
                                                  node[NODE_Y],
                                                  COST_VALUE))
    # Validate DOWN move.
    if is_a_possible_move(node[NODE_X], node[NODE_Y] + 1):
        possible_action_list.append(create_a_node(node[NODE_X],
                                                  node[NODE_Y] + 1,
                                                  COST_VALUE))
    # Validate LEFT move.
    if is_a_possible_move(node[NODE_X] - 1, node[NODE_Y]):
        possible_action_list.append(create_a_node(node[NODE_X] - 1,
                                                  node[NODE_Y],
                                                  COST_VALUE))
    return possible_action_list


def create_a_node(x_axis, y_axis, node_cost):
    """
    Builds a node object. A node is defined by a tuple containing:
      X position (X), Y position (Y), cost (C), and heuristic (H).
    :param x_axis: Node X-axis.
    :param y_axis: Node Y-axis.
    :param node_cost: Node cost.
    :return: Node object, form of tuple.
    """
    global destination
    return x_axis, y_axis, node_cost, heuristic(x_axis, y_axis,
                                                destination[NODE_X],
                                                destination[NODE_Y])


def euclidean_distance(x1, y1, x2, y2):
    """
    Calculates the Euclidean distance between two points.
    :param x1: X axis of Point 1.
    :param y1: Y axis of Point 1.
    :param x2: X axis of Point 2.
    :param y2: Y axis of Point 2.
    :return: Euclidean distance.
    """
    return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


def manhattan_distance(x1, y1, x2, y2):
    """
    Calculates the Manhattan distance between two points.
    :param x1: X axis of Point 1.
    :param y1: Y axis of Point 1.
    :param x2: X axis of Point 2.
    :param y2: Y axis of Point 2.
    :return: Manhattan distance.
    """
    return math.fabs(x2 - x1) + math.fabs(y2 - y1)


def my_own_distance(x1, y1, x2, y2):
    """
    Calculates the average of Euclidean and Manhattan.
    :param x1: X axis of Point 1.
    :param y1: Y axis of Point 1.
    :param x2: X axis of Point 2.
    :param y2: Y axis of Point 2.
    :return: Distance.
    """
    return ((math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2)))
            + (math.fabs(x2 - x1) + math.fabs(y2 - y1))) / 2


def output_solution(explored_list):
    """
    This function is called once the solution is found
      to format and print the steps taken.
    :param explored_list: Explored list.
    """
    global nario_position
    solution_list = []
    # Remove goal node.
    previous = explored_list[len(explored_list) - 1]
    solution_list.append(previous)
    # Loop through explored list and generate solution list.
    while (previous[NODE_X] != nario_position[NODE_X]
           or previous[NODE_Y] != nario_position[NODE_Y]):
        # Get first node that is adjacent to previous node.
        for node in explored_list:
            if is_a_neighbor_node(previous, node):
                previous = node
                solution_list.append(previous)
                break
    # Get solution in start-to-finish order.
    solution_list.reverse()
    # Format and print steps to solution state.
    for index in range(0, len(solution_list)):
        if index != 0:
            print_solution("Step " + str(index) + ":",
                           solution_list[index][NODE_X],
                           solution_list[index][NODE_Y])
        else:
            print_solution("Initial:",
                           solution_list[index][NODE_X],
                           solution_list[index][NODE_Y])
    print "PATH Found! NARIO reached the destination"


def print_solution(text, pos_x, pos_y):
    """
    Prints the board with specified header text and agent position.
    :param text: Header text.
    :param pos_x: X axis of agent.
    :param pos_y: Y axis of agent.
    """
    global maze_lines
    print "\n" + text
    for index in range(0, len(maze_lines)):
        line = maze_lines[index]
        if index == pos_y:
            print line[:pos_x] + NARIO + line[pos_x + 1:]
        else:
            print line

# Load board data.
maze_lines, maze_height, maze_width = load_test_case_file()

# Load heuristic.
if USER_HEURISTIC == HEURISTIC_EUCLIDEAN:
    heuristic = euclidean_distance
elif USER_HEURISTIC == HEURISTIC_MANHATTAN:
    heuristic = manhattan_distance
elif USER_HEURISTIC == HEURISTIC_MADEUP:
    heuristic = my_own_distance
else:
    print ("Invalid heuristic choice!")
    sys.exit(0)

# Get nario and destination position.
nario_position = locate_nario(True)
destination = get_destination_axes()

# ------ BEGIN A* ALGORITHM ------ #

# Current node is problem's initial state.
currentNode = (nario_position[NODE_X], nario_position[NODE_Y], 0,
               heuristic(nario_position[NODE_X], nario_position[NODE_Y],
                         destination[NODE_X], destination[NODE_Y]))
# Frontier list contains tuples of the total cost and node tuple.
frontierList = []
heapq.heappush(frontierList, (currentNode[NODE_C] + currentNode[NODE_H],
                              currentNode))
# Explored list is initially empty.
exploredList = []

# A* Algorithm
while True:
    # No solution if frontier list is empty.
    if len(frontierList) == 0:
        print "NO PATH"
        sys.exit(0)
    # Pop lowest f-value node in frontier,
    #   index 1 to get actual node, not (f+node) tuple.
    currentNode = heapq.heappop(frontierList)[1]
    # Perform goal test.
    if (currentNode[NODE_X] == destination[NODE_X]
            and currentNode[NODE_Y] == destination[NODE_Y]):
        exploredList.append(currentNode)
        output_solution(exploredList)
        sys.exit(0)
    # Add current node to explored list.
    exploredList.append(currentNode)
    actionList = explore_valid_actions(currentNode)
    # For every possible child/action, check to add to frontier.
    for childNode in actionList:
        frontierIndexOfChild = is_node_in_frontier_list(frontierList,
                                                        childNode)
        # Add to frontier if node not in explored or frontier list.
        if childNode not in exploredList and frontierIndexOfChild < 0:
            heapq.heappush(frontierList,
                           (childNode[NODE_C] + childNode[NODE_H], childNode))
        # Update frontier if node is in explored and new f-value is smaller
        elif (frontierIndexOfChild >= 0
                and frontierList[frontierIndexOfChild][0] >
                        (childNode[NODE_C] + childNode[NODE_H])):
            frontierList[frontierIndexOfChild] = (
                    childNode[NODE_C] + childNode[NODE_H], childNode)
            # Maintain the priority queue invariant if node f-value is changed.
            heapq.heapify(frontierList)
