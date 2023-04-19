# Dice Game

## Introduction
In this assignment the Markov Decision Process (MVP) has been used to determine the optimal policy for playing a dice game. The optimal policy is a mapping of states to actions, giving the optimal action which should be taken when in each state to give the maximum score.

## Method
The method used in this code to determine the optimal policy is value iteration. This was chosen because it is guaranteed to converge and was found to achieve a policy which scored highly within a short time frame, given the best values for gamma and theta. The method works by using the one-step look-ahead approach with rewards for each action that can be taken.

A version of the Bellman optimal equation is used, altered slightly to create an update equation. This equation, given an arbitrary starting value, calculates the expected value for a given a state, an action, a reward, the discount value (gamma), the next state and the probability of transitioning to that state. For each state in the dice game, which is each distinct combination of dice, each action is looped through to calculate the expected value, summing up for each next state and probability. Then, for each state the optimal action is chosen and the expected value of that action stored. Once there is an expected value for each state, the states are looped through again, this time using the updated expected value in the update equation. This iteration is continued until the change in the expected value from one loop to the next (delta) is below a limit called theta (named deltaLim in the code).

Once complete the game can be played and for each current state in the game, the update equation is ran once more for each to determine the next best action to play.

## Code
In the code the class MyAgent is used which is a subclass of DiceGameAgent, with the two methods __init__ (the constructor) and __play__ (used to play each turn of the game).

In the constructor the initial one-step look-ahead loop with convergence is used to determine the optimal policy before the game has begun. It starts by setting the values for gamma and theta and initialising lists for the expected values and next expected values. Two lists are used so as not to override values before they have been used in the current loop.

A while loop is then stated which ends when delta drops below the theta value. From this point each action for each state is looped through as mention previously, summing up the values for each action and picking the maximum to return as the expected value for that action. Expected are calculated using the probablity-weighted average of its values, *probablity(reward+gamma(Vs'))*. As the action (0,1,2) gives a terminal state, None is returned as the next state from __get_next_states__, therefor the current state is used.

After each states new expected value is calculated, the delta is calculated and once all states are re-calculated, this is checked against theta to determine if to continue or not.


By the end, the expected values have converged and a map is created between the states and the optimal actions.

In the __play__ method as mention previously, the update equation is ran once more to determine the best action given the optimal expected values already calculated. This equation is the same as the one used in the loop. Addition, when a maximum expected value is found, the values for the actions are searched to see if there is more than one action equalling that maximum value. If there is more than one instance of the maximum value then the choice between those actions which produced the maximum is done at random. Lastly, the optimal action is returned.

## Gamma and Theta
Once the value iteration functionality was completed, the values for gamma and theta can be varied to try to produce the best output. For different applications the best values for these variables will differ. In this case, a gamma of 0.935 and a theta of 0.1 gave the best results without optimising them to several decimal points.

A low gamma value represents a bias to a short-term strategy, meaning the agent will decide to end the game earlier by sticking with all dice rather then continuing for a potentially better score, and for high gamma values a long-term strategy, where more actions are taken per game to try to find a better score than the instant reward of the early dice.

The theta value, which is always positive determines the criteria for convergence, how close the previous and current expected values should be before stopping the initial iteration. The lower the value the longer the iteration lasts.

Testing for the optimal values was done with 10,000 tests at which point the average score had little variation. In table 1 the results can be seen for varying gamme at a fixed theta of 0.001.


<center>

|Gamma|Construction_Time(s)|Avg_Score|
|:-:|:-:|:-:|
|0.900|11.41|13.06|
|0.905|12.11|13.09|
|0.910|12.66|13.19|
|0.915|13.55|13.32|
|0.920|14.36|13.32|
|0.925|15.31|13.33|
|0.930|16.59|13.36|
|0.935|17.92|13.36|
|0.940|19.31|13.35|
|0.945|21.22|13.33|
*Table 1: Optimal Gamma Testing at 0.001 Theta*

</center>

Lower values of gamma were manually tested to find a rough best score and this automated test was used to find the a higher precision value.

After testing the theta value was manually varied and the findings were that above a certain value there was a drop off in average score. However, a higher value gave a shorter construction time. Decreasing the value gave a higher score up until a point when the score did not vary significantly, however continuing to increase theta increased the contruction time because more iterations were carried out. The final value for theta was decided to be 0.1 as this gave a high average score without unnecessarily increasing the construction time.

## Conclusion
The MDP worked well as an agent for determining the best next action as can be determine by its average score which beat the only hold and perfectionist agents and also beating the theoritical average score of 10.5 given by the proability-weighted average score of the dice in each state. The gamma and theta values were critical to the performance of the agent in terms of both average score and contruction time. Automated testing of both of these values can generate a clear understanding of what the optimal values for these variables are. Continuing from this, a policy iteration strategy could be attempted which also guarantees convergence but can reduce the construction time.



