'''
Lab 13: My first AI agent.
In this lab, you will create your first AI agent.
You will use the run_episode function from lab 12 to run a number of episodes
and collect the returns for each state-action pair.
Then you will use the returns to calculate the action values for each state-action pair.
Finally, you will use the action values to calculate the optimal policy.
You will then test the optimal policy to see how well it performs.

Sidebar-
If you reward every action you may end up in a situation where the agent
will always choose the action that gives the highest reward. Ironically,
this may lead to the agent losing the game.
'''
import sys
from pathlib import Path

# line taken from turn_combat.py
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab11.agent_environment import get_combat_surface, setup_window
from lab11.sprite import Sprite
from lab2.cities_n_routes import get_randomly_spread_cities

from lab11.pygame_combat import PyGameComputerCombatPlayer
from lab11.turn_combat import CombatPlayer
from lab12.episode import run_episode

from collections import defaultdict
import random
import numpy as np


class PyGameRandomCombatPlayer(PyGameComputerCombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        self.weapon = random.randint(0, 2)
        return self.weapon


class PyGamePolicyCombatPlayer(CombatPlayer):
    def __init__(self, name, policy):
        super().__init__(name)
        self.policy = policy

    def weapon_selecting_strategy(self):
        print(self.current_env_state)
        self.weapon = self.policy[self.current_env_state]
        return self.weapon


def run_random_episode(player, opponent, combat_surface, screen, player_sprite):
    player.health = random.choice(range(10, 110, 10))
    opponent.health = random.choice(range(10, 110, 10))
    return run_episode(combat_surface, screen, player_sprite, [player, opponent])


def get_history_returns(history):
    total_return = sum([reward for _, _, reward in history])
    returns = {}
    for i, (state, action, reward) in enumerate(history):
        if state not in returns:
            returns[state] = {}
        returns[state][action] = total_return - sum(
            [reward for _, _, reward in history[:i]]
        )
    return returns

# Sword - 0, Arrow - 1, Fire - 2


def run_episodes(n_episodes):
    '''
    Run 'n_episodes' random episodes and return the action values for each state-action pair.
    Action values are calculated as the average return for each state-action pair over the 'n_episodes' episodes.
    Use the get_history_returns function to get the returns for each state-action pair in each episode.
    
    Collect the returns for each state-action pair in a dictionary of dictionaries where the keys are states and
        the values are dictionaries of actions and their returns.
    After all episodes have been run, calculate the average return for each state-action pair.
    Return the action values as a dictionary of dictionaries where the keys are states and 
        the values are dictionaries of actions and their values.
    '''

    #Set variables for game
    size = width, height = 640, 480
    combat_surface = get_combat_surface(size)

    screen = setup_window(width, height, "Game World Gen Practice")

    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]
    cities = get_randomly_spread_cities(size, len(city_names))

    sprite_path = "assets/lego.png"
    player_sprite = Sprite(sprite_path, cities[0])

    #player
    player = PyGameRandomCombatPlayer("Player")
    #opponent
    opponent = PyGameComputerCombatPlayer("Opponent")

    #list history
    history = []

    #For n_episodes
    for episode in range(n_episodes):
        #run_random_episode
        new_episode = run_random_episode(player, opponent, combat_surface, screen, player_sprite)
        #add entry from run_random_episode to list
        history.append(new_episode)

    #returns_dict
    returns_dict = {}

    """
    #Print dictionary entries (Delete after)
    for episode in range(n_episodes):
        returns = get_history_returns(history[episode])
        
        returns_dict[episode] = returns
    
    print(returns_dict)
    """

    #Compile info
    for episode in range(n_episodes):
        #Get the returns
        returns = get_history_returns(history[episode])
        
        for state, action in returns.items():
            #If the state does not exist in our returns_dict, add it
            if state not in returns_dict:
                #Add new state and the action and reward related to it
                returns_dict[state] = {0: [], 1: [], 2: []}

                if (0 in action.keys()):
                    returns_dict[state].get(0).append(action.get(0))
                elif (1 in action.keys()):
                    returns_dict[state].get(1).append(action.get(1))
                else:
                    returns_dict[state].get(2).append(action.get(2))

            #If the state exists in our returns_dict, add its reward to the entry
            else:
                #This state exists, so determine if the action has been performed before
                if (0 in action.keys()):
                    returns_dict[state].get(0).append(action.get(0))
                elif (1 in action.keys()):
                    returns_dict[state].get(1).append(action.get(1))
                else:
                    returns_dict[state].get(2).append(action.get(2))
    print("Swag")
    print(returns_dict[(100, 100)])
    
    #Information is now compiled in a format like this
    #{
    # (100, 20): {0: [7,4,1,0,], 1: [33], 2: [1]}}

    #{
    # state: {move: list of cumilitive rewads}
    #}

    #Now go through each state and find the average of each of the actions
    action_values = {}

    for state, action in returns_dict.items():
        #Put the state into the action_values
        #action_values[state] = {0: -1, 1: -1, 2: -1}
        action_values[state] = {}

        if (returns_dict[state].get(0)):
            action_values[state][0] = sum(returns_dict[state].get(0)) / len(returns_dict[state].get(0))
        
        if (returns_dict[state].get(1)):
            action_values[state][1] = sum(returns_dict[state].get(1)) / len(returns_dict[state].get(1))
        
        if (returns_dict[state].get(2)):
            action_values[state][2] = sum(returns_dict[state].get(2)) / len(returns_dict[state].get(2))

    print(action_values)

    return action_values


def get_optimal_policy(action_values):
    optimal_policy = defaultdict(int)
    for state in action_values:
        optimal_policy[state] = max(action_values[state], key=action_values[state].get)
    return optimal_policy


def test_policy(policy):
    #Set variables for game
    size = width, height = 640, 480
    combat_surface = get_combat_surface(size)

    screen = setup_window(width, height, "Game World Gen Practice")

    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]
    cities = get_randomly_spread_cities(size, len(city_names))

    sprite_path = "assets/lego.png"
    player_sprite = Sprite(sprite_path, cities[0])

    names = ["Legolas", "Saruman"]
    total_reward = 0
    for _ in range(100):
        player1 = PyGamePolicyCombatPlayer(names[0], policy)
        player2 = PyGameComputerCombatPlayer(names[1])
        players = [player1, player2]
        total_reward += sum(
            [reward for _, _, reward in run_episode(combat_surface, screen, player_sprite, players)]
        )
    return total_reward / 100


if __name__ == "__main__":
    action_values = run_episodes(15000)
    print(action_values)
    optimal_policy = get_optimal_policy(action_values)
    print(optimal_policy)
    print(test_policy(optimal_policy))

    #print("またね")
    #print(action_values)
    #print(optimal_policy)
