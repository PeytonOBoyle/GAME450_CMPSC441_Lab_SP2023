'''
Lab 4: Rock-Paper-Scissor AI Agent

In this lab you will build one AI agent for the game of Rock-Paper-Scissors, that can defeat a few different kinds of 
computer players.

You will update the AI agent class to create your first AI agent for this course.
Use the precept sequence to find out which opponent agent you are facing, 
so that it can beat these three opponent agents:

    Agent Single:  this agent picks a weapon at random at the start, 
                   and always plays that weapon.  
                   For example: 2,2,2,2,2,2,2,.....

    Agent Switch:  this agent picks a weapon at random at the start,
                   and randomly picks a weapon once every 10 rounds.  
                   For example:  2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,...

    Agent Mimic:  this agent picks a weapon at random in the first round, 
                  and then always does what you did the previous round.  
                  For example:  if you played 1,2,0,1,2,0,1,2,0,...  
                   then this agent would play 0,1,2,0,1,2,0,1,2,...

Discussions in lab:  You don't know ahead of time which opponent you will be facing, 
so the first few rounds will be used to figure this out.   How?

Once you've figured out the opponent, apply rules against that opponent. 
A model-based reflex agent uses rules (determined by its human creator) to decide which action to take.

If your AI is totally random, you should be expected to win about 33% of the time, so here is the requirement:  
In 100 rounds, you should consistently win at least 85 rounds to be considered a winner.

You get a 1 point for beating the single agent, 2 points for beating the switch agent, 
and 2 points for beating the mimic agent.

'''

from rock_paper_scissor import Player
from rock_paper_scissor import run_game
from rock_paper_scissor import random_weapon_select

class AiPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.initial_weapon = random_weapon_select()
    
    def check_single(self):
        #Check last five moves. If all of them are the same, we are most likely fighting a single or a switch that has yet to change
        five_moves_ago = self.opponent_choices[-5]

        for x in range(-4, 0):
            if x != five_moves_ago:
                return(False)

        return(True)
    
    def check_switch(self):
        #Check last five moves. If it is two volleys of the same move in a row, such as 0, 0, 0, 1, 1, then it is most likely a switch statement
        five_moves_ago = self.opponent_choices[-5]

        #new_move is set to 3 right now, but will be set to a real move if the sequence changes in the for loop
        new_move = 3

        for x in range(-4, 0):
            #Continue if the sequence has not changed yet
            if self.opponent_choices[x] == five_moves_ago:
                continue
            
            #If the sequence changes, register that as the new move
            if self.opponent_choices[x] != five_moves_ago and new_move == 3:
                new_move = self.opponent_choices[x]
                continue

            #If the sequence changess a third time, then this cannot be a switch statement
            if self.opponent_choices[x] != new_move:
                return False

        return True


    def weapon_selecting_strategy(self):
        #Initial move is chosen a random
        if len(self.opponent_choices) == 0:
            return  self.initial_weapon
        
        #Check last five moves
        #If the opponent consistently uses a certain number, it is most likely a single or a switch, such as 0, 0, 0, 0, 0
        elif len(self.opponent_choices) > 4 and self.check_single():
            return(self.opponent_choices[-1]+1)%3

        #If the opponent consistently uses one move followed by another, it is most likely a switch, such as 0, 0, 0, 1, 1
        elif len(self.opponent_choices) > 4 and self.check_switch():
            return(self.opponent_choices[-1]+1)%3

        #If it is none of these, then the opponent is most likely a mimic

        #Check if the thrown hand has changed
        #elif len(self.opponent_choices) > 4:
        elif self.opponent_choices[0] != self.opponent_choices[-1] and len(self.opponent_choices) >= 2:
            return(self.my_choices[-1]+1)%3

        #For the first four turns, we are just gathering data, so we can use the function below to guarentee wins against the first two enemy types and at least stall the mimics
        else:
            return(self.opponent_choices[-1]+1)%3

    

    #HIGHER THAN 95 - 1 point credit


if __name__ == '__main__':
    final_tally = [0]*3
    for agent in range(3):
        #Change the 10s to 100 after this lab
        for i in range(10):
            tally = [score for _, score in run_game(AiPlayer("AI"), 10, agent)]
            if sum(tally) == 0:
                final_tally[agent] = 0
            else:
                final_tally[agent] += tally[0]/sum(tally)

    print("Final tally: ", final_tally)  