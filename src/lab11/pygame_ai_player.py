import pygame
from lab11.turn_combat import CombatPlayer

""" Create PyGameAIPlayer class here"""

#As for now, the AI Player will move from locations 1-9 in sequential order
class PyGameAIPlayer:
    def __init__(self) -> None:
        #Start at 0, no cities visited
        self.next_city = 0

    def selectAction(self, state):
        #If we are not travelling, move to the next city
        if (state.travelling == False):
            self.next_city += 1
            print(self.next_city)
            return ord(str(self.next_city))
        
        #Otherwise, continue on our path to the next city
        return ord(str(state.current_city))
        


""" Create PyGameAICombatPlayer class here"""

#As for now, fight the Enemy by using the fastest combination against them (Arrow on turns 1-6 8-10 and sword on turn 7)
class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)
        #Count turns to counter AI pattern
        self.turn = 0

    def weapon_selecting_strategy(self):
        #Use Arrow when it isn't turn 7
        if self.turn < 5:
            self.weapon = 1
        #Switch to Sword
        else:
            self.weapon = 2
        
        self.turn += 1

        return self.weapon
