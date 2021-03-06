import numpy as np
import abc
import util
from game import Agent, Action


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """

        # Useful information you can extract from a GameState (game_state.py)

        successor_game_state = current_game_state.generate_successor(action=action)
        board = successor_game_state.board
        max_tile = successor_game_state.max_tile
        score = successor_game_state.score
        emptyCells=successor_game_state.get_empty_tiles()[0].size

        sum = 0
        for row in board:
            for col in range(4):
                sum += row[col]
        #
        #for col in range(4):
        #    for row in range(3):
        #        sum += abs(board[row][col]-board[row+1][col])
        #return sum
        #if board[0][0] == max_tile:
        return sum + emptyCells *10 + max_tile*100
        #return  sum +emptyCells*10


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """

        return self.maxChild(game_state,self.depth)[1]

    def maxChild(self,Current_state,depth):
        if depth==0:
            return (self.evaluation_function(Current_state),Action.STOP)
        legalActions=Current_state.get_legal_actions(0)

        maxScore=-float("inf")
        maxAction=Action.STOP
        for action in legalActions:
            minStep=self.minChild(Current_state.generate_successor(0, action), depth)[0]
            if minStep>maxScore:
                maxAction=action
                maxScore=minStep
        return (maxScore,maxAction)
    def minChild(self,Current_state,depth):
        if depth==0:
            return (self.evaluation_function(Current_state),Action.STOP)
        legalActions=Current_state.get_legal_actions(1)
        "get maxScore to inifity"
        minScore = float("inf")
        minAction = Action.STOP
        for action in legalActions:
            maxStep = self.maxChild(Current_state.generate_successor(1, action), depth - 1)[0]
            if maxStep < minScore:
                minAction = action
                minScore = maxStep
        return (minScore, minAction)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.alphabeta(game_state,self.depth,-float("inf"),float("inf"),0)[1]

    def alphabeta(self,game_State,depth,alpha,beta,playerIndex):
        if depth==0 or len(game_State.get_legal_actions(playerIndex))==0:
            return (self.evaluation_function(game_State),Action.STOP)

        if playerIndex == 0 : #max player is our player
            #alpha=-inifity
            score = -float("inf")
            currentBest=Action.STOP
            for action in game_State.get_legal_actions(0):
                currentScore = self.alphabeta(game_State.generate_successor(0, action),depth,alpha,beta,1)
                if currentScore[0] > score:
                    score=currentScore[0]
                    currentBest=action
                alpha= max(alpha,score)
                if beta <=alpha:
                    break
            return (score,currentBest)
        else: # computer player
            score = float("inf")
            currentBest=Action.STOP
            for action in game_State.get_legal_actions(1):
                currentScore = self.alphabeta(game_State.generate_successor(1, action), depth - 1, alpha, beta, 0)
                if currentScore[0] < score:
                    score = currentScore[0]
                    currentBest = action
                alpha = max(alpha, score)

                if beta <= alpha:
                    break
            return (score,currentBest)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        return self.maxChild(game_state,self.depth)[1]

    def maxChild(self,Current_state,depth):
        if depth==0 or len(Current_state.get_legal_actions(0))==0:
            return (self.evaluation_function(Current_state),Action.STOP)
        legalActions=Current_state.get_legal_actions(0)

        maxScore=-float("inf")
        maxAction=Action.STOP
        for action in legalActions:
            maxStep=self.expectedNode(Current_state.generate_successor(0, action), depth)
            if maxStep>maxScore:
                maxAction=action
                maxScore=maxStep
        return (maxScore,maxAction)
    def expectedNode(self,Current_state,depth):
        legalActions=Current_state.get_legal_actions(1)
        average=0
        counter=0
        for action in legalActions:
            average += self.maxChild(Current_state.generate_successor(1, action), depth - 1)[0]
            counter +=1
        return average/counter



def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    Weights= [1,10,15]

    board = current_game_state.board
    max_tile = current_game_state.max_tile
    emptyCells = current_game_state.get_empty_tiles()[0].size

    sum = 0
    for row in board:
        for col in range(4):
            sum += row[col]

    return sum * Weights[0]\
        + emptyCells * Weights[1]\
        + max_tile * Weights[2]\
        + bonusPoints(board,max_tile)

    # return  sum +emptyCells*10
def bonusPoints(Given_board,maxTile):
    board =[row[:] for row in Given_board] #copy the given board so we can change it
    if board[0][0]==maxTile: # first line top left corner
        NextCell = board[0][0]
        for col in range(4):
            if NextCell >= np.max(board):
                NextCell=board[0][col]
                board[0][col]=0
            else: return (col+1)*1000
        return 10000
    elif board[0][-1]==maxTile: # first line top left corner
        NextCell=board[0][-1]
        for col in reversed(range(4)):
            if NextCell >= np.max(board):
                NextCell=board[0][col]
                board[0][col]=0
            else: return (col+1)*900
        return 8000
    elif board[-1][0] == maxTile:  # first line top left corner
        NextCell = board[-1][0]
        for col in range(4):
            if NextCell >= np.max(board):
                NextCell = board[-1][col]
                board[-1][col] = 0
            else:
                return (col + 1) * 900
        return 8000
    elif board[-1][-1]==maxTile: # first line top left corner
        NextCell=board[-1][-1]
        for col in reversed(range(4)):
            if NextCell >= np.max(board):
                NextCell=board[-1][col]
                board[-1][col]=0
            else: return (col+1)*900
        return 8000
    return 0

# Abbreviation
better = better_evaluation_function
