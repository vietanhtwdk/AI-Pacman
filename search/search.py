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

import heapq

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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    Frontier = util.Stack() # theo độ sâu, vào sau ra sau dùng stack
    Visited = []
    Frontier.push( (problem.getStartState(), []) ) # đấy (startstate + mảng rỗng lưu action)=item vào stack 

    while Frontier.isEmpty() == 0: # khi stack không rỗng
        state, actions = Frontier.pop() # loại trạng thái đầu stack 
        
        if state in Visited: # nếu state đã visit bỏ qua đến state tiếp theo
            continue
            
        Visited.append( state ) # đánh dấu state visited
        
        if problem.isGoalState(state): # state hiện tại là goal trả về actions
            return actions 

        for successor, action, stepCost in problem.getSuccessors(state): # loop các successor nếu chưa visit, thêm các unvisited successor vào stack
            if successor not in Visited:
                Frontier.push((successor, actions + [action])) # actions(successor) = actions(predecessor) + action tới nó
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    Frontier = util.Queue() # theo bề ngang, vào trước ra trước dùng queue
    Visited = []
    Frontier.push( (problem.getStartState(), []) ) # đấy startstate + mảng rỗng lưu action vào queue

    while Frontier.isEmpty() == 0: # khi queue không rỗng
        state, actions = Frontier.pop() # loại trạng thái đầu queue 
        
        if state in Visited: # nếu state đã visit bỏ qua đến state tiếp theo
            continue
            
        Visited.append( state ) # đánh dấu state visited
        
        if problem.isGoalState(state): # state hiện tại là goal trả về actions
            return actions 

        for successor, action, stepCost in problem.getSuccessors(state): # loop các successor nếu chưa visit, thêm các unvisited successor vào queue
            if successor not in Visited:
                Frontier.push((successor, actions + [action])) # actions(successor) = actions(predecessor) + action tới nó
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
    #python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
    #python pacman.py -l mediumScaryMaze -p StayWestSearchAgent
            
    # khởi tạo
    Frontier = util.PriorityQueue()
    Visited = []
    Frontier.push( (problem.getStartState(), []), 0 ) # priority startstate = 0

    while Frontier.isEmpty() == 0: # khi Frontier không rỗng
        state, actions = Frontier.pop()

        if state in Visited:
            continue
        
        Visited.append( state )
        
        if problem.isGoalState(state):
            return actions

        for successor, action, stepCost in problem.getSuccessors(state): # loop các successor nếu chưa visit push vào priority queue kèm cost để xếp ưu tiên
            if successor not in Visited:
                Frontier.push((successor, actions + [action]), stepCost + problem.getCostOfActions(actions)) # cost = cost(successor) + cost các action trước đó
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
      #init
    open_set = util.PriorityQueue() 
    close_set = []
    start = problem.getStartState()
    g_values = {}
    f_values = {}
    g_values[start] = 0
    f_values[start] = g_values[start] + heuristic(start, problem)

    # priority of open_set is f_values 
    open_set.push((start, [], g_values[start]), f_values[start])
    
    print(open_set.heap)
    # cost = g()
    position, action, cost = open_set.pop()
    # add to visited list
    close_set.append((position, cost + heuristic(start, problem)))

    while problem.isGoalState(position) is not True: 
        successor_set = problem.getSuccessors(position) 
        for successor in successor_set:
            visited = False
            total_cost = cost + successor[2] # g()
            for (visitedPosition, visitedCost) in close_set:               
                # if the successor in close_set but higher cost than previous
                if (successor[0] == visitedPosition) and (total_cost >= visitedCost): 
                    visited = True
                    break
            # else visited = False 
            if not visited:        
                open_set.push((successor[0], action + [successor[1]], cost + successor[2]),cost + successor[2] + heuristic(successor[0],problem)) 
                close_set.append((successor[0],cost + successor[2])) 

        position, action, cost = open_set.pop()

    print(action)

    return action
    # python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic/euclideanHeuristic/nullHeuristic
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
