from abc import ABC, abstractmethod
from dice_game import DiceGame
import numpy as np
import time
import math

class DiceGameAgent(ABC):
    def __init__(self, game):
        self.game = game
    
    @abstractmethod
    def play(self, state):
        pass

class AlwaysHoldAgent(DiceGameAgent):
    def play(self, state):
        return (0, 1, 2)


class PerfectionistAgent(DiceGameAgent):
    def play(self, state):
        if state == (1, 1, 1) or state == (1, 1, 6):
            return (0, 1, 2)
        else:
            return ()


class MyAgent(DiceGameAgent):
    def __init__(self, game):
        """
        if your code does any pre-processing on the game, you can do it here
        
        e.g. you could do the value iteration algorithm here once, store the policy, 
        and then use it in the play method
        
        you can always access the game with self.game
        """
        # this calls the superclass constructor (does self.game = game)
        super().__init__(game)
        
        self.gamma = 0.935
        deltaLim = 0.1
        startValue = int(0)
        self.expectedValue = [startValue] * len(self.game.states)
        nextExpectedValue = [startValue] * len(self.game.states)
        delta = 1

        while delta > deltaLim:
            stateCount = 0
            delta = 0
            for state in self.game.states:
                count = 0
                potentialExpectedValues = []
                temp = self.expectedValue[stateCount]
                for action in self.game.actions:
                    states, _, reward, probabilities = self.game.get_next_states(action, state)
                    value = 0
                    for nextState, probability in zip(states, probabilities):
                        if nextState is None:
                            vs = self.expectedValue[stateCount]
                            value = probability * (reward + self.gamma * vs)
                        else:
                            vs = self.expectedValue[self.game.states.index(nextState)]
                            value += probability * (reward + self.gamma * vs)
                    potentialExpectedValues.append((value, action, reward))
                    count += 1
                    
                nextExpectedValue[stateCount] = (max(potentialExpectedValues, key=lambda tup: tup[0]))[0]
                
                nextDelta = temp - nextExpectedValue[stateCount]
                delta = max(delta, abs(nextDelta))
                
                stateCount += 1

            self.expectedValue = nextExpectedValue.copy()
        
    def play(self, state):
        """
        given a state, return the chosen action for this state
        at minimum you must support the basic rules: three six-sided fair dice
        
        if you want to support more rules, use the values inside self.game, e.g.
            the input state will be one of self.game.states
            you must return one of self.game.actions
        
        read the code in dicegame.py to learn more
        """
        pi = []
        for action in self.game.actions:
            states, _, reward, probabilities = self.game.get_next_states(action, state)
            value = 0
            for nextState, probability in zip(states, probabilities):
                if nextState == None:
                    value = probability * (reward + self.gamma * self.expectedValue[self.game.states.index(state)])
                else:
                    value += probability * (reward + self.gamma * self.expectedValue[self.game.states.index(nextState)])
            pi.append((value, action, reward))
            
        maxValue = (max(pi, key=lambda tup: tup[0]))[0]
        maxValues = []
        for a in range(len(self.game.actions)):
            if pi[a][0] == maxValue:
                maxValues.append(a)
        actionToTake = np.random.choice(maxValues)
        
        return self.game.actions[actionToTake]



def play_game_with_agent(agent, game, verbose=True):
    state = game.reset()
    
    if(verbose): print(f"Testing agent: \n\t{type(agent).__name__}")
    if(verbose): print(f"Starting dice: \n\t{state}\n")
    
    game_over = False
    actions = 0
    while not game_over:
        action = agent.play(state)
        actions += 1
        
        if(verbose): print(f"Action {actions}: \t{action}")
        _, state, game_over = game.roll(action)
        if(verbose and not game_over): print(f"Dice: \t\t{state}")

    if(verbose): print(f"\nFinal dice: {state}, score: {game.score}")
        
    return game.score


SKIP_TESTS = False

def tests():
    import time

    total_score = 0
    total_time = 0
    n = 10000

    np.random.seed()

    print("Testing basic rules.")
    print()

    game = DiceGame()

    start_time = time.process_time()
    test_agent = MyAgent(game)
    total_time += time.process_time() - start_time

    for i in range(n):
        start_time = time.process_time()
        score = play_game_with_agent(test_agent, game)
        total_time += time.process_time() - start_time

        print(f"Game {i} score: {score}")
        total_score += score

    print()
    print(f"Average score: {total_score/n}")
    print(f"Constuction time: {total_time:.4f} seconds")
    print(f"Average time: {total_time/n:.5f} seconds")
    
if not SKIP_TESTS:
    tests()
    time.sleep(2)
    
TEST_EXTENDED_RULES = False

def extended_tests():
    total_score = 0
    total_time = 0
    n = 1000

    print("Testing extended rules – two three-sided dice.")
    print()

    game = DiceGame(dice=2, sides=3)#DiceGame(dice=4, sides=3, values=[1, 2, 6], bias=[0.1, 0.1, 0.8], penalty=2)

    start_time = time.process_time()
    test_agent = MyAgent(game)
    total_time += time.process_time() - start_time

    for i in range(n):
        start_time = time.process_time()
        score = play_game_with_agent(test_agent, game)
        total_time += time.process_time() - start_time

        print(f"Game {i} score: {score}")
        total_score += score

    print()
    print(f"Average score: {total_score/n}")
    print(f"Total time: {total_time:.4f} seconds")
    print(f"Average time: {total_time/n:.5f} seconds")

if not SKIP_TESTS and TEST_EXTENDED_RULES:
    extended_tests()