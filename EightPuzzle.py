import sys
import numpy as np
import queue

class Problem:
    def __init__(self, game_state, goal):
        self.seen_set = set()
        self.seed = Node(0,"Begin",game_state,goal)
        self.goal = goal
        self.solution = "" #will be replaced with solution trace i think
        self.frontier_queue = queue.PriorityQueue()

    #returns False if game state is new, True if game state is seen before
    def is_repeat(game_state, self):
        before = len(self.seen_set)
        self.seen_set.add(game_state)
        after = len(self.seen_set)
        if (after - before) > 0:
            return False
        return True
    
    def get_seen(self):
        return self.seen_set

    def get_seed(self):
        return self.seed
    
    def prepend_move(action, self):
        self.solution = f"{action} -> {self.solution}"

    def push(new_node, self):
        self.frontier_queue.put((new_node.get_cost(),new_node))
        return
    
    def pop(self):
        return self.frontier_queue.get()

def search_2D(val, array):
    for y in array:
        for x in array:
            if array[y][x] == val:
                return [y,x]
    return -1, -1

class Node:
    def __init__(self, parent, action, game_state, goal):
        self.action = action #how did i get here
        if parent != 0:
            self.cost = parent.get_cost() + self.a_star_euclidean_distance(goal)
        else:
            print("DEBUG GOAL")
            print(goal)
            self.cost = self.a_star_euclidean_distance(goal)
        self.parent = parent # parent is a reference to Node / if null, then it is seed
        self.game_state = game_state # game state is a 2D np array
        self.width = np.sqrt(len(game_state))

    def get_cost(self):
        return self.cost

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

        return expand_set #list of nodes with all possible unique movements

    def uniform_cost_search(self):
        cost = 1
        return cost
    
    def a_star_misplaced_type(goal, self):
        #flatten is just iterating through all values of an array and placing them in order
        flat_game_state = np.ndarray.flatten(self.game_state)
        flat_goal = np.ndarray.flatten(goal)
        misplaced_count = 0
        
        for i, tile in enumerate(flat_game_state):
            if flat_game_state[i] != flat_goal[i]:
                misplaced_count += 1

        return misplaced_count - 1
    
    def a_star_euclidean_distance(goal, self):
        #goal.index(value) game_state.index(value) 
        #find distance between these two, x2-x1 ^2 + y2-y1 ^2 sqrted
        cost = 0
        
        print(type(goal))
        for i, row in enumerate(goal):
            for j, val in enumerate(row):
                game_state_index = search_2D(val,self.game_state)
                goal_index = [i,j]

                cost += pow(pow(goal_index[0]-game_state_index[0], 2) + pow(goal_index[1]-game_state_index[1],2),.5)
        
        return cost



#import initial state in order left to right top down
fakePuzzle = np.array([
    [1,2,3],
    [4,5,6],
    [7,-1,8]
    ])

n = int(input("Enter the width of the puzzle grid: "))

num_inputs = n*n

puzzle = fakePuzzle #use for inputs: np.arange(num_inputs).reshape(n,n)

goal = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,-1]
]) #puzzle

# print("Begin inputting puzzle configuration with unique values, and inputting -1 for an empty space")
# for i in range(n):
#     print(f"Row {i+1} inputs: ")
#     print()
#     for j in range(n):
#         puzzle[i][j] = input(f"Enter item {j+1} for row {i+1}: ")
#     print()

print("Given puzzle: ")
print(puzzle)
print()

# print("Begin inputting goal configuration with unique values, and inputting -1 for an empty space")
# for i in range(n):
#     print(f"Row {i+1} inputs: ")
#     print()
#     for j in range(n):
#         goal[i][j] = input(f"Enter item {j+1} for row {i+1}: ")
#     print()

print("Given goal: ")
print(goal)
print()

def solve(problem):

    seed = problem.get_seed() #seed is the base of the tree

    problem.frontier_queue.push(seed.get_seed())
    while (True):
        if problem.frontier_queue.empty():
            break
        
        leaf = problem.pop()
        if (leaf.game_state == goal):
            return problem.solution
        
        if not problem.is_repeat(leaf.game_state):
            new_nodes = leaf.expand(problem.seen_set)
        for node in new_nodes:
            problem.push(node)
    return "No solution"

problem = Problem(puzzle, goal)
solve(problem)
