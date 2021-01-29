# multiAgents.py
# --------------
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

# C:\Python27\python.exe

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        # considering all the food as a list
        food_list = newFood.asList()

        # initializing the food distance, to save the food points from pacman
        foodDist = []

        # finding the distance of all the food from the pacman
        # we use the manhattan distance formula to calculate the food distances
        for food in food_list:
            foodDist.append(util.manhattanDistance(food, newPos))

        # finding the number of foods available for the pacman
        food_len = len(foodDist)

        # when there is no food for the pacman then return
        if food_len == 0:
            return float("inf")

        sum2 = 10000 / food_len

        # when the pacman position remains the same in the peresnt and the next state
        if currentGameState.getPacmanPosition() == newPos:
            return float("-inf")

        # finding the distance of all the ghosts from the pacman and checking if they are in
        # close proximity to the pacman
        for ghost in successorGameState.getGhostPositions():
            if (util.manhattanDistance(ghost, newPos) < 1):
                return float("-inf")

        sum1 = 1000 / sum(foodDist)

        # returning the evaluated values from the above conditions for the pacman to direct
        return sum1 + sum2

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        # max agent is used for evaluating the best direction for the pacman
        def max_value(gameState, depth):

            # first intialize the value and the action to be performed by the pacman (at the root node)
            maxval = float("-inf")
            max_action = None

            # checking the different states the pacman can be found
            # if the pacman has reached a certain depth or if the game is won/lost or when no legal actions
            if len(gameState.getLegalActions(0)) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState), None)

            # calculating the next action values available from the game state at a certain depth
            # if the successor values are greater then replace maxval and maxaction with the present action
            for present_action in gameState.getLegalActions(0):

                successor = min_value(gameState.generateSuccessor(0, present_action), 1, depth)[0]
                if (successor > maxval):
                    maxval, max_action = successor, present_action

            return (maxval, max_action)

        # min agent is used for evaluation the worst case direction for the ghost to perform
        def min_value(gameState, index, depth):

            # first intialize the value and the action to be performed by the ghost (at the root node)
            minval = float("inf")
            min_action = None

            # checking the different states the pacman can be found
            # if the pacman has no legal actions to perform
            if len(gameState.getLegalActions(index)) == 0:
                return (self.evaluationFunction(gameState), None)

            # calculating the next action values available from the game state at a certain depth and that index
            # if the successor values is minimum, then replace minval and min_action with the present action
            for presnt_action in gameState.getLegalActions(index):

                agent_count = gameState.getNumAgents()
                if (index == agent_count - 1):
                    d = depth + 1
                    successor = max_value(gameState.generateSuccessor(index, presnt_action), d)[0]
                else:
                    i = index + 1
                    successor = min_value(gameState.generateSuccessor(index, presnt_action), i, depth)[0]

                # comparing the successor value and the minvalue
                if (successor < minval):
                    minval, min_action = successor, presnt_action

            return (minval, min_action)

        score = max_value(gameState, 0)[1]

        return score

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        # max agent is used for evaluating the best direction for the pacman
        def max_value(gameState, depth):

            # first intialize the value and the action to be performed by the pacman (at the root node)
            maxval = float("-inf")
            max_action = None

            # checking the different states the pacman can be found
            # if the pacman has reached a certain depth or if the game is won/lost or when no legal actions
            if len(gameState.getLegalActions(0)) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState), None)

            # calculating the next action values available from the game state at a certain depth
            # if the successor values is maximum, then replace maxval and max_action with the present action
            for current_action in gameState.getLegalActions(0):
                successor = exp_value(gameState.generateSuccessor(0, current_action), 1, depth)[0]

                if (maxval < successor):
                    maxval, max_action = successor, current_action

            return (maxval, max_action)

        # expect agent
        def exp_value(gameState, index, depth):

            # initializing the expected value and the corresponding action
            expval = 0
            exp_action = None

            # checking the different states the pacman can be found
            # if the pacman has no legal actions to perform
            if len(gameState.getLegalActions(index)) == 0:
                return (self.evaluationFunction(gameState), None)

            for current_action in gameState.getLegalActions(index):

                if (index == gameState.getNumAgents() - 1):
                    d = depth + 1
                    successor = max_value(gameState.generateSuccessor(index, current_action), d)[0]
                else:
                    i = index + 1
                    successor = exp_value(gameState.generateSuccessor(index, current_action), i, depth)[0]

                # calculating the probability
                probability = successor / len(gameState.getLegalActions(index))

                # add the calculated probability to the expval
                expval += probability

            return (expval, exp_action)

        score = max_value(gameState, 0)[1]
        return score


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
