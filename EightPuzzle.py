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
    def is_repeat(self,game_state):
        before = len(self.seen_set)
        hashable_state = game_state.tobytes()
        self.seen_set.add(hashable_state)
        after = len(self.seen_set)
        if (after - before) > 0:
            return False
        return True
    
    def get_seen(self):
        return self.seen_set

    def get_seed(self):
        return self.seed
    
    def prepend_move(self,action):
        self.solution = f"{action} -> {self.solution}"

    def push(self,new_node):
        self.frontier_queue.put((new_node.cost,new_node))
        return
    
    def pop(self):
        return self.frontier_queue.get()

def search_2D(val, array):
    for y, _ in enumerate(array):
        for x,_ in enumerate(array):
            if array[y][x] == val:
                return [y,x]
    return -1, -1

class Node:
    def __init__(self, parent, action, game_state, goal):
        self.action = action #how did i get here
        self.parent = parent # parent is a reference to Node / if null, then it is seed
        self.game_state = game_state # game state is a 2D np array
        self.width = len(game_state)
        if parent != 0:
            self.cost = parent.get_cost() + self.a_star_euclidean_distance(goal)
        else:
            self.cost = self.a_star_euclidean_distance(goal)

    def __lt__(self,node):
        return self.cost < node.cost

    def get_cost(self):
        return self.cost

    def expand(self,seen_set):
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

        expand_set = []
        try:
            # test bounds
            temp = self.game_state[i-1][j]
            
            #it is in bounds
            new_game_state = np.array(self.game_state,copy=True)
            new_game_state[i][j] = new_game_state[i-1][j]
            new_game_state[i-1][j] = -1

            if new_game_state.tobytes() not in seen_set:
                expand_set.append((new_game_state,"Up"))
        except:
            pass

        try:
            # test bounds
            temp = self.game_state[i][j+1]
            
            #it is in bounds
            new_game_state = np.array(self.game_state,copy=True)
            new_game_state[i][j] = new_game_state[i][j+1]
            new_game_state[i][j+1] = -1

            if new_game_state.tobytes() not in seen_set:
                expand_set.append((new_game_state,"Right"))
        except:
            pass

        try:
            # test bounds
            temp = self.game_state[i+1][j]
            
            #it is in bounds
            new_game_state = np.array(self.game_state,copy=True)
            new_game_state[i][j] = new_game_state[i+1][j]
            new_game_state[i+1][j] = -1

            if new_game_state.tobytes() not in seen_set:
                expand_set.append((new_game_state,"Down"))
        except:
            pass

        try:
            # test bounds
            temp = self.game_state[i][j-1]
            
            #it is in bounds
            new_game_state = np.array(self.game_state,copy=True)
            new_game_state[i][j] = new_game_state[i][j-1]
            new_game_state[i][j-1] = -1

            if new_game_state.tobytes() not in seen_set:
                expand_set.append((new_game_state,"Left"))
        except:
            pass

        return expand_set #list of nodes with all possible unique movements

    def uniform_cost_search(self):
        cost = 1
        return cost
    
    def a_star_misplaced_type(self, goal):
        #flatten is just iterating through all values of an array and placing them in order
        flat_game_state = np.ndarray.flatten(self.game_state)
        flat_goal = np.ndarray.flatten(goal)
        misplaced_count = 0
        
        for i, tile in enumerate(flat_game_state):
            if flat_game_state[i] != flat_goal[i]:
                misplaced_count += 1

        return misplaced_count - 1
    
    def a_star_euclidean_distance(self, goal):
        #goal.index(value) game_state.index(value) 
        #find distance between these two, x2-x1 ^2 + y2-y1 ^2 sqrted
        cost = 0
        
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
    [-1,7,8]
    ])

# n = int(input("Enter the width of the puzzle grid: "))

# num_inputs = n*n

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

    problem.push(seed)
    cnt = 0
    while (True):
        leaf = problem.pop()[1]
        
        if (str(leaf.game_state) == str(problem.goal)):
            #trace up leaf's parents
            while (str(leaf.game_state) != str(problem.seed.game_state)):
                problem.prepend_move(leaf.action)
                leaf = leaf.parent
            problem.prepend_move(leaf.action)
            problem.solution = f"{problem.solution} Done"
            return problem.solution
        
        if not problem.is_repeat(leaf.game_state):
            new_nodes = leaf.expand(problem.seen_set)
        
        for node in new_nodes:
            new_node = Node(leaf,node[1],node[0],goal)
            problem.push(new_node)
        
        print(cnt)
        cnt += 1

        if problem.frontier_queue.empty():
            break
    return "No solution"

problem = Problem(puzzle, goal)
print(solve(problem))
