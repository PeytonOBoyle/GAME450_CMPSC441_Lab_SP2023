''' 
Lab 12: Beginnings of Reinforcement Learning
We will modularize the code in pygrame_combat.py from lab 11 together.

Then it's your turn!
Create a function called run_episode that takes in two players
and runs a single episode of combat between them. 
As per RL conventions, the function should return a list of tuples
of the form (observation/state, action, reward) for each turn in the episode.
Note that observation/state is a tuple of the form (player1_health, player2_health).
Action is simply the weapon selected by the player.
Reward is the reward for the player for that turn.
'''

#Run turn can be modified
import sys

from pathlib import Path
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab11.pygame_combat import run_pygame_combat
from lab11.agent_environment import get_combat_surface, setup_window
from lab11.sprite import Sprite
from lab2.cities_n_routes import get_randomly_spread_cities

def run_episode():
    actions = run_pygame_combat(combat_surface, screen, player_sprite)

    return actions

if __name__ == "__main__":
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

    actions = run_episode()

    print(actions)