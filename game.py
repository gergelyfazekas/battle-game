
import numpy as np
import random


def simulate(game, n_times):
    """Runs a game n_times and returns winning probabilities and the list of actual winners during the simulation"""
    
    # store initial properties
    team_1_properties = game.team_1.team_properties
    team_1_name = game.team_1.name
    team_2_properties = game.team_2.team_properties
    team_2_name = game.team_2.name
    
    winner_list = []
    for i in range(n_times):
        # reset game in every round using the initial properties
        team_1 = Team(team_1_name, team_1_properties)
        team_2 = Team(team_2_name, team_2_properties)
        game = Game(team_1, team_2)
        
        # play and append
        winner = game.play(verbose=False)
        winner_list.append(winner)
    
    team_1_probability = sum([1 if c.name == team_1_name else 0 for c in winner_list]) / len(winner_list)
    team_2_probability = 1 - team_1_probability
    return team_1_probability, team_2_probability, winner_list

def random_throw(num_dice, num_sides):
    """generates a random number as the sum of the thrown numbers using num_dice with num_sides each"""
    return sum(np.random.randint(1, num_sides + 1, size=num_dice))

class Character:
    def __init__(self, character_properties):
        """A dict of properties is used to set up a new character, currently the below is used in the game"""
        self.character_properties = character_properties
        self.attack_strength = self.character_properties['attack_strength']
        self.defense_strength = self.character_properties['defense_strength']
        self.life = self.character_properties['life']
        self.weapon = self.character_properties['weapon']
        self.id = self.character_properties['id']
        
    def __repr__(self):
        return f"{self.character_properties}"
    
    @property
    def scar(self):
        """deducts life points based on a random throw + weapon strength"""
        weapons = {'spear': 2}
        return random_throw(3,10) + weapons[self.weapon]
    
    @property
    def attack(self):
        return random_throw(2,6) + self.attack_strength
    
    @property
    def defend(self):
        return self.defense_strength
    
class Team:
    def __init__(self, name, team_properties):
        self.character_list = []
        self.team_properties = team_properties
        self.name = name
        for character in list(self.team_properties.keys()):
            self.character_list.append(Character(character_properties = self.team_properties[character]))
            
    def __repr__(self):
        return f"{self.name}"
    
    @property        
    def losing(self):
        one_has_life = np.any([c.life for c in self.character_list])
        if one_has_life:
            # not losing
            return False
        else:
            # losing
            return True
        
    def get_defender(self):
        """currently returns the character with the least amount of life points from the given team"""
        big_number = 1000000
        min_life = min([c.life if c.life > 0 else big_number for c in self.character_list])
        weakest = [c for c in self.character_list if c.life == min_life]
        return weakest[0]
    
    def get_attacker(self):
        """currently returns a random attacker character from the given team"""
        return random.choice(self.character_list)
    

class Game:
    def __init__(self, team_1, team_2):
        self.team_1 = team_1
        self.team_2 = team_2
        
    def get_winner(self):
        if self.team_1.losing:
            return self.team_2
        elif self.team_2.losing:
            return self.team_1
        else:
            raise NotImplementedError("Should not be here: get_winner to be called only when one is losing")
        
    def play(self, verbose=True):
        """plays the game once and returns the winner team"""
        i = 0
        run = True
        while run:
            # set attacker and defender teams
            r = random.choice([1,2])
            attacker_team = self.team_1 if r == 1 else self.team_2
            defender_team = self.team_2 if r == 1 else self.team_1
            
            # choose attacker character from the attacker team
            attacker = attacker_team.get_attacker()
            
            # choose defender character from defender team
            defender = defender_team.get_defender()
            
            # battle
            attack_point = attacker.attack
            defense_point = defender.defend
            scar = attacker.scar
            
            # temporary life -- only for printing when verbose is True
            life_temp = defender.life
            
            # battle
            if attack_point > defense_point:
                if defender.life <= scar:
                    defender.life = 0
                else:
                    defender.life -= scar
                    
            # printing stuff
            if verbose:
                print("--------------------")
                print(f"Round: {i}")
                print(f"attacker: {attacker_team} | {attacker}")
                print(f"defender: {defender_team} | {defender}")
                print(f"attack - defense: {attack_point} | {defense_point}")
                print(f"scar: {scar}")
                print(f"life before - after: {life_temp} | {defender.life}")
                i+=1
                
            # if one team is losing --> run = False
            run = not np.any([self.team_1.losing, self.team_2.losing])
            
        # get, print, return winner
        winner = self.get_winner()
        if verbose:
            print("--------------------")
            print("")
            print("Winner: ", winner)
            print("")
        return winner


if __name__ == '__main__':
    # create teams with dictionaries:
    # keys are arbitrary strings
    # values are dictionaries themselves with fixed key names (see Character.__init__ for supported key names)

    team_A_properties = {
        'character_1': {'id': 1, 'attack_strength': 5, 'defense_strength': 10, 'life': 10, 'weapon': "spear"},
        'character_2': {'id': 2, 'attack_strength': 6, 'defense_strength': 9, 'life': 15, 'weapon': "spear"}
    }

    team_B_properties = {
        'character_1': {'id': 1, 'attack_strength': 4, 'defense_strength': 12, 'life': 11, 'weapon': "spear"},
        'character_2': {'id': 2, 'attack_strength': 8, 'defense_strength': 15, 'life': 16, 'weapon': "spear"}
    }


    # # Example - Play
    #
    # # Initialize the teams: name, property dictionary
    # team_A = Team("team_A", team_A_properties)
    # team_B = Team("team_B", team_B_properties)
    #
    # # Initialize the Game with the two teams
    # game = Game(team_A, team_B)
    #
    # # Play
    # winner = game.play(verbose=True)



    # Example - Simulation

    # Initialize the teams: name, property dictionary
    team_A = Team("team_A", team_A_properties)
    team_B = Team("team_B", team_B_properties)

    # Initialize the Game with the two teams
    game = Game(team_A, team_B)

    # Set number of simulation runs
    sim_num = 100

    # Simulate
    team_A_probability, team_B_probability, winner_list = simulate(game, sim_num)

    print(f"Winning probabilities based on {sim_num} runs: \n",
          f"Team A: {team_A_probability} \n",
          f"Team B: {team_B_probability}")

