import sys
import pygame
import random
from sprite import Sprite
from pygame_combat import run_pygame_combat
from pygame_human_player import PyGameHumanPlayer
from landscape import get_landscape, get_combat_bg
from pygame_ai_player import PyGameAIPlayer

from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab2.cities_n_routes import get_randomly_spread_cities, get_routes

#Stuff I added :)
from lab5.landscape import elevation_to_rgba
from lab5.landscape import get_elevation
from lab7.ga_cities import game_fitness, setup_GA, solution_to_cities, show_cities

import numpy as np
import array as array
import matplotlib.pyplot as plt

import re
from transformers import pipeline, set_seed, GPT2Tokenizer, GPT2LMHeadModel, GenerationConfig
#https://huggingface.co/tasks/text-generation


pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)


def get_landscape_surface(size):
    landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def get_combat_surface(size):
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def setup_window(width, height, caption):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def displayCityNames(city_locations, city_names):
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])


class State:
    def __init__(
        self,
        current_city,
        destination_city,
        travelling,
        encounter_event,
        cities,
        routes,
        gold
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes
        self.gold = 30


if __name__ == "__main__":
    size = width, height = 640, 480
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_path = "assets/lego.png"
    sprite_speed = 1

    screen = setup_window(width, height, "Game World Gen Practice")

    #landscape_surface = get_landscape_surface(size)
    combat_surface = get_combat_surface(size)
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

    elevation = []
    #initialize elevation here from previous code
    elevation = get_elevation(size)

    # normalize landscape
    elevation = np.array(elevation)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())
    landscape_pic = elevation_to_rgba(elevation)

    # setup fitness function and GA
    fitness = lambda cities, idx: game_fitness(
        cities, idx, elevation=elevation, size=size
    )

    fitness_function, ga_instance = setup_GA(fitness, len(city_names), size)

    # Show one of the initial solutions.
    cities = ga_instance.initial_population[0]
    cities = solution_to_cities(cities, size)

    # Run the GA to optimize the parameters of the function.
    ga_instance.run()
    ga_instance.plot_fitness()

    # Show the best solution after the GA finishes running.
    cities = ga_instance.best_solution()[0]
    cities_t = solution_to_cities(cities, size)
    cities = cities_t

    #Recreate routes
    routes = get_routes(cities)

    #Create landscape_surface
    landscape_surface = pygame.surfarray.make_surface(landscape_pic)

    random.shuffle(routes)
    routes = routes[:10]

    player_sprite = Sprite(sprite_path, cities[start_city])

    player = PyGameHumanPlayer()

    """ Add a line below that will reset the player variable to 
    a new object of PyGameAIPlayer class."""

    #player = PyGameAIPlayer()

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
        gold = 30
    )

    #Text generator
    generator = pipeline('text-generation', model = 'gpt2')
    
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

    #Generate an output here so the warning is not in the way of the game
    output = generator("Getting warning here", max_new_tokens = 10, num_return_sequences = 1, pad_token_id = tokenizer.eos_token_id)

    #Tracks which journal entry this is
    entry_num = 1

    while True:
        action = player.selectAction(state)
        if 0 <= int(chr(action)) <= 9:
            #Added check to see if there is route leading from current_city to chosen city
            if int(chr(action)) != state.current_city and not state.travelling and ( any(np.array_equal((np.asarray(cities[state.current_city]), np.asarray(cities[int(chr(action))])), route) for route in routes) or any(np.array_equal((np.asarray(cities[int(chr(action))]), np.asarray(cities[state.current_city])), route) for route in routes)):
                start = cities[state.current_city]
                state.destination_city = int(chr(action))
                destination = cities[state.destination_city]
                player_sprite.set_location(cities[state.current_city])
                state.travelling = True
                print(
                    "Travelling from", state.current_city, "to", state.destination_city
                )

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        displayCityNames(cities, city_names)
        if state.travelling:
            #Make temp_speed that we pass into move_sprite instead of sprite_speed
            #temp_speed = sprite_speed - 2*|elevation - 0.5|
            #If we are travelling at a mid range height, we will travel fast, otherwise we will travel slow
            temp_speed = sprite_speed - 2 * abs(elevation.item(int(player_sprite.sprite_pos[0]), int(player_sprite.sprite_pos[1])) - 0.5)

            state.travelling = player_sprite.move_sprite(destination, temp_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print('Arrived at', state.destination_city)
                #AI generated journal entry summarizing the town visit
                context = "Ollie is a young elf living in a fantasy world, travelling from town to town."
                prompt = f"{context} Once he arrived in {city_names[state.destination_city]} with {state.gold} gold, Ollie "
                #do_sample = False for more generic text (repeats itself)
                output = generator(prompt, max_new_tokens = 130, num_return_sequences = 1, pad_token_id = tokenizer.eos_token_id)
                while not output[0]['generated_text'].endswith("."):
                    output[0]['generated_text'] = output[0]['generated_text'][:-1]
                print("---------------------------------------")
                print(f"Entry # {entry_num}")
                print(output[0]['generated_text'])
                print("---------------------------------------")

                entry_num = entry_num + 1

        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city

        if state.encounter_event:
            #0 Player lost 1 Player Won 2 Draw
            winValue = run_pygame_combat(combat_surface, screen, player_sprite)
            #If player lost, remove 50 gold
            if winValue == 0:
                state.gold -= 50
                #If player is now out of gold, game over
                if state.gold < 1:
                    print("---------------------------------------")
                    print('You have no remaining gold - Game Over!')
                    print("---------------------------------------")
                    break
                else:
                    print("---------------------------------------")
                    print("Lost 50 gold... Current gold: " + str(state.gold))
                    print("---------------------------------------")
            #If player won, get 10 gold
            elif winValue == 1:
                state.gold += 10
                print("---------------------------------------")
                print("Got 10 gold! Current gold: " + str(state.gold))
                print("---------------------------------------")
            
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()
        if state.current_city == end_city:
            print('You have reached the end of the game!')
            break
