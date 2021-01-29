# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    fringe_dfs = util.Stack()   # Fringe is used to store the nodes and their paths
    explored_nodes = set([])    # Set to maintain all the visited nodes
    fringe_dfs.push((problem.getStartState(), {}))
    while 1:
        if fringe_dfs.isEmpty():
            return 'Empty Fringe \n'
        searchNextNode = fringe_dfs.pop()
        if problem.isGoalState(searchNextNode[0]):  # Exit on encountering goal node
            return searchNextNode[1]
        if not searchNextNode[0] in explored_nodes:     # Check for visited nodes
            explored_nodes.add(searchNextNode[0])   # Adding new nodes to the visited nodes
            succ = problem.getSuccessors(searchNextNode[0])
            for node in range(len(succ)):
                path = list(searchNextNode[1])
                path.append(succ[node][1])
                fringe_dfs.push((succ[node][0], path))  # Pushing (node and path from state to child node) to the fringe

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()  # Fringe is used to store the nodes and their paths
    visited = []           #List to maintain all the visited nodes
    fringe.push((problem.getStartState(), [])) # Pushing node and path from start to node, into the fringe
    while True:
        node, node_path = fringe.pop()
        if problem.isGoalState(node):  # Exit on encountering goal node
            break
        else:
            if node not in visited:  # Check for visited nodes
                visited.append(node)  # Adding newly encountered nodes to the set of visited nodes
                successors = problem.getSuccessors(node)
                for successor in successors:
                    node_1 = successor[0]
                    path_1 = successor[1]
                    fringe.push((node_1, node_path + [path_1]))  # Pushing ('state', Path from state to child node) to the fringe

    return node_path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()   # Fringe is used to store the nodes and their paths
    visited = []                    #List to maintain all the visited nodes
    '''Pushing Node, Path, total cost till 'Node') to the fringe. 
    Culmulative backward cost is used as a factor based on which priority is decided.'''
    fringe.push((problem.getStartState(), [], 0), 0)
    while True:
        node, path_till_node,cost_till_node = fringe.pop()
        if problem.isGoalState(node):  # Exit on encountering goal node
            break
        else:
            if node not in visited:  # Check for visited nodes
                visited.append(node)  # Adding newly encountered nodes to the set of visited nodes
                successors = problem.getSuccessors(node)
                for successor in successors:
                    node_1 = successor[0]
                    path_1 = successor[1]
                    cost = successor[2]
                    # Pushing (state,total path, and the cost to the fringe
                    fringe.push((node_1, path_till_node + [path_1],cost_till_node + cost), cost_till_node + cost)

    return path_till_node

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe_astar = util.PriorityQueue()     # Fringe is used to store the nodes and their paths
    explored_nodes = set([])                #Set to maintain all the visited nodes
    startState = (problem.getStartState(), {})  # assign problem start state as it develops
    startEstCost = heuristic(problem.getStartState(), problem)  # heuristic cost uptil the node
    fringe_astar.push(startState, problem.getCostOfActions(startState[1]) + startEstCost)   # push heuristic, cost and initial state to the fringe

    while 1:
        if fringe_astar.isEmpty():
            return 'Empty Fringe'
        searchNextNode = fringe_astar.pop()
        if problem.isGoalState(searchNextNode[0]):
            return searchNextNode[1]
        # next node is not present in visited nodes then add it
        if not searchNextNode[0] in explored_nodes:
            explored_nodes.add(searchNextNode[0])
            # retrieve successor to the node
            succ = problem.getSuccessors(searchNextNode[0])
            for node in range(len(succ)):
                path = list(searchNextNode[1])
                path.append(succ[node][1])
                fringe_astar.push((succ[node][0], path), problem.getCostOfActions(path)
                                  + heuristic(succ[node][0], problem))

    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch