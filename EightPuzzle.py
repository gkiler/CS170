import sys
import numpy as np
import queue

class Problem:
    def __init__(self, game_state, goal,alg):
        self.seen_set = set()
        self.seed = Node(0,"Begin",game_state,goal,alg)
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
    def __init__(self, parent, action, game_state, goal, alg):
        self.action = action #how did i get here
        self.parent = parent # parent is a reference to Node / if null, then it is seed
        self.game_state = game_state # game state is a 2D np array
        self.width = len(game_state)
        if alg == 1:
            if parent != 0:
                self.cost = parent.get_cost() + self.uniform_cost_search(goal)
                self.depth = parent.depth + 1
            else:
                self.cost = self.uniform_cost_search(goal)
                self.depth = 1
        elif alg == 2:
            if parent != 0:
                self.cost = parent.get_cost() + self.a_star_misplaced_type(goal)
                self.depth = parent.depth + 1
            else:
                self.cost = self.a_star_misplaced_type(goal)
                self.depth = 1
        else:
            if parent != 0:
                self.cost = parent.get_cost() + self.a_star_euclidean_distance(goal)
                self.depth = parent.depth + 1
            else:
                self.cost = self.a_star_euclidean_distance(goal)
                self.depth = 1
        
        

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
            if i == 0:
                raise Exception
            # temp = self.game_state[i-1][j]
            
            #it is in bounds
            new_game_state = np.array(self.game_state,copy=True)
            new_game_state[i][j] = new_game_state[i-1][j]
            new_game_state[i-1][j] = -1

            if new_game_state.tobytes() not in seen_set:
                expand_set.append((new_game_state,f"{new_game_state[i][j]} Down"))
        except:
            pass

        try:
            # test bounds
            if j == 2:
                raise Exception
            # temp = self.game_state[i][j+1]
            
            #it is in bounds
            new_game_state = np.array(self.game_state,copy=True)
            new_game_state[i][j] = new_game_state[i][j+1]
            new_game_state[i][j+1] = -1

            if new_game_state.tobytes() not in seen_set:
                expand_set.append((new_game_state,f"{new_game_state[i][j]} Left"))
        except:
            pass

        try:
            # test bounds
            if i == 2:
                raise Exception
            # temp = self.game_state[i+1][j]
            
            #it is in bounds
            new_game_state = np.array(self.game_state,copy=True)
            new_game_state[i][j] = new_game_state[i+1][j]
            new_game_state[i+1][j] = -1

            if new_game_state.tobytes() not in seen_set:
                expand_set.append((new_game_state,f"{new_game_state[i][j]} Up"))
        except:
            pass

        try:
            # test bounds
            if j == 0:
                raise Exception
            # temp = self.game_state[i][j-1]
            # print(temp)
            #it is in bounds
            new_game_state = np.array(self.game_state,copy=True)
            new_game_state[i][j] = new_game_state[i][j-1]
            new_game_state[i][j-1] = -1

            if new_game_state.tobytes() not in seen_set:
                expand_set.append((new_game_state,f"{new_game_state[i][j]} Right"))
        except:
            pass

        return expand_set #list of nodes with all possible unique movements

    def uniform_cost_search(self,goal):
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
trivial = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,-1]
    ])

easy = np.array([
    [1,2,-1],
    [4,5,3],
    [7,8,6]
    ])

very_easy = np.array([
    [1,2,3],
    [4,5,6],
    [7,-1,8]
    ])
    
doable = np.array([
    [-1,1,2],
    [4,5,3],
    [7,8,6]
    ])

ohBoy = np.array([
    [8,7,1],
    [6,-1,2],
    [5,4,3]
    ])

impossible = np.array([
    [1,2,3],
    [4,5,6],
    [8,7,-1]
    ]) 

def solve(problem,alg):
    seed = problem.get_seed() #seed is the base of the tree

    problem.push(seed)
    cnt = 0
    expansions = 0
    max_queue_size = 0
    while (True):
        leaf = problem.pop()[1]
        print(f'The best state to expand with g(n) = {leaf.depth} and h(n) = {leaf.cost}')
        if (str(leaf.game_state) == str(problem.goal)):
            #trace up leaf's parents
            while (str(leaf.game_state) != str(problem.seed.game_state)):
                problem.prepend_move(leaf.action)
                leaf = leaf.parent
            problem.prepend_move(leaf.action)
            problem.solution = f"{problem.solution} Done"
            print(f"Max Queue Size: {max_queue_size} | Nodes expanded: {expansions}")
            return problem.solution
        
        if not problem.is_repeat(leaf.game_state):
            expansions += 1
            new_nodes = leaf.expand(problem.seen_set)
            print(f"Expanding state \n {leaf.game_state}")
        
        for node in new_nodes:
            new_node = Node(leaf,node[1],node[0],goal,alg)
            problem.push(new_node)
        
        max_queue_size = max(max_queue_size,problem.frontier_queue.qsize())
        # print(cnt)
        # cnt += 1
        # if cnt % 10000 == 0:
        #     print(f"Iterations: {cnt} | Unique States Seen: {len(problem.seen_set)}")
        if problem.frontier_queue.empty():
            break
    print(f"Max Queue Size: {max_queue_size} | Nodes expanded: {expansions}")
    return f"No solution in {cnt} iterations"
# hardest = np.array([
#     [8,6,7],
#     [2,5,4],
#     [3,-1,1]
# ])

n = int(input("Enter the width of the puzzle grid: "))

num_inputs = n*n

puzzle = np.arange(num_inputs).reshape(n,n)

goal = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,-1]
]) #puzzle
print("Welcome to 862208140 8 Puzzle Solver")
puzzlechoice = int(input("Type 1 for default puzzle or 2 for entering your own puzzle:"))
if puzzlechoice == 2:
    print("Begin inputting puzzle configuration with unique values, and inputting -1 for an empty space")
    for i in range(n):
        print(f"Row {i+1} inputs: ")
        print()
        for j in range(n):
            puzzle[i][j] = input(f"Enter item {j+1} for row {i+1}: ")
        print()

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

    

    

    alg = int(input("Enter your choice of algorithm: \nUniform Cost Search\nA* Misplaced Tile Heuristic\nA* Euclidean Distance Heuristic\n"))
    problem = Problem(puzzle, goal,alg)
    if alg == 1:
        print(f'Solution with Uniform Cost Search for given puzzle: {solve(problem,alg)}')
    elif alg == 2:
        print(f'Solution with Misplaced Tile Heuristic for given puzzle: {solve(problem,alg)}')
    elif alg == 3:
        print(f'Solution with Euclidean Distance Heuristic for given puzzle: {solve(problem,alg)}')

# print(f'Euclidean Distance for given puzzle: {solve(problem)}')
else:
    alg = int(input("Enter your choice of algorithm: \nUniform Cost Search\nA* Misplaced Tile Heuristic\nA* Euclidean Distance Heuristic\n"))
    #trivial
    trivial = Problem(trivial,goal,alg)
    #easy 
    very_easy = Problem(very_easy,goal,alg)
    #very_easy
    doable = Problem(doable,goal,alg)
    #doable
    ohBoy = Problem(ohBoy,goal,alg)
    #ohBoy
    impossible = Problem(impossible,goal,alg)
    #impossible

    # print(solve(problem))

    # i have to manually change heuristics bc i was lazy but its only like two lines
    print(f'trivial: \n{solve(trivial)}')
    print(f'very_easy: \n{solve(very_easy)}')
    print(f'easy: \n{solve(easy)}')
    print(f'doable: \n{solve(doable)}')
    print(f'ohBoy: \n{solve(ohBoy)}')
    print(f'impossible: \n{solve(impossible)}')