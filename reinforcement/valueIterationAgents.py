# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # assigning the counter dict to a temporary variable
        temp = util.Counter()

        # getting the mdp states
        states = mdp.getStates()

        for i in range(iterations):
            # copying the values into the dictionary temp
            temp = self.values.copy()

            # looping through the each state
            for state in states:
                # collect all possible actions for the given state
                actions = mdp.getPossibleActions(state)

                # initalizing list for transitions and values
                transitions = []
                values = []

                # if it is in the terminal state then the value is zero
                if mdp.isTerminal(state):
                    self.values[state] = 0

                else:
                    for action in actions:
                        # get the transitions for the state and action
                        transitions = mdp.getTransitionStatesAndProbs(state, action)
                        value = 0

                        for transition in transitions:
                            # saving the action available into the x
                            x = transition[1]
                            # saving the state value into the y
                            y = transition[0]
                            # reward for the particular action at that state
                            reward = mdp.getReward(state, action, y)
                            value += x * ( reward + discount * temp[y])

                        # adding the values into the list
                        values.append(value)

                    # selecting the max value from the list of values and assigning it to the state
                    self.values[state] = max(values)


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # intializing the value to zero
        value = 0.0

        # collecting all the possible transitions for the particular state and action
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)

        for transition in transitions:
            # saving the action available into the x
            x = transition[1]
            # saving the state value into the y
            y = transition[0]
            # computing the q_value
            value += x * (self.mdp.getReward(state, action, y) + self.discount * self.values[y])

        return value

        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        # collecting all the possible actions for a particular state
        actions = self.mdp.getPossibleActions(state)

        # initially set up legal_action to be None
        legal_action = None

        # initalizing the reward value to negative infinity
        value = float("-inf")

        for action in actions:
            # computing the Q - values to all actions available
            qValue = self.computeQValueFromValues(state, action)

            # for the highest q-value of an action we choose that as the legal action for that state
            if qValue > value:
                value = qValue
                legal_action = action

        return legal_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
