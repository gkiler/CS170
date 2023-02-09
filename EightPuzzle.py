import sys
import numpy as np

class Node:
    def __init__(self, val, parent, game_state):
        self.value = val #
        self.parent = parent # parent is a reference to Node / if null, then it is seed
        self.game_state = game_state # game state is a 2D np array
        self.width = np.sqrt(len(game_state))

    def expand(seen_set, self):
        # i - 1, i - 1
        # i - 1, i + 1
        # i + 1, i + 1
        # i + 1, i - 1
        i = -1
        j = -1
        for x in range(self.width):
            for y in range(self.width):
                if self.game_state[x][y] == -1:
                    i = x
                    j = y
                    break
            break

        expand_set = []
        try:
            # test bounds
            temp = self.game_state[i-1][j-1]
            
            #it is in bounds
            new_game_state = self.game_state
            new_game_state[i][j] = new_game_state[i-1][j-1]
            new_game_state[i-1][j-1] = -1

            if new_game_state not in seen_set:
                expand_set.append(new_game_state)
        except:
            pass

        try:
            # test bounds
            temp = self.game_state[i-1][j+1]
            
            #it is in bounds
            new_game_state = self.game_state
            new_game_state[i][j] = new_game_state[i-1][j+1]
            new_game_state[i-1][j+1] = -1

            if new_game_state not in seen_set:
                expand_set.append(new_game_state)
        except:
            pass

        try:
            # test bounds
            temp = self.game_state[i+1][j-1]
            
            #it is in bounds
            new_game_state = self.game_state
            new_game_state[i][j] = new_game_state[i+1][j-1]
            new_game_state[i+1][j-1] = -1

            if new_game_state not in seen_set:
                expand_set.append(new_game_state)
        except:
            pass

        try:
            # test bounds
            temp = self.game_state[i+1][j+1]
            
            #it is in bounds
            new_game_state = self.game_state
            new_game_state[i][j] = new_game_state[i+1][j+1]
            new_game_state[i+1][j+1] = -1

            if new_game_state not in seen_set:
                expand_set.append(new_game_state)
        except:
            pass

        return expand_set #array of nodes with all possible unique movements

    def uniform_cost_search(self):
        cost = 0
        return cost
    
    def a_star_misplaced_type(self):
        
        return
    
    def a_star_euclidean_distance(self):
        return
    
class Node:
    def __init__(self, val, parent):
        #cost of self?
        self.value = val

        #parent is null or Node object i think? or separate if i need
        self.parent = parent



#import initial state in order left to right top down
fakePuzzle = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,-1]
    ])

n = input("Enter the width of the puzzle grid: ")

num_inputs = n*n-1



#pick empty space
#calculate costs by manhattan distance from correct location
#its fastest to store this in a 1D array, but that has to translate easily
#nxn puzzle has nxn slots