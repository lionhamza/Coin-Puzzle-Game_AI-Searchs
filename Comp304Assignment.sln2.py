import copy
from collections import deque

class State:
    def __init__(self, stack_E, stack_A, stack_B, stack_C, stack_D, heuristicValue=8, path=[]):
        self.stack_E = stack_E
        self.stack_A = stack_A
        self.stack_B = stack_B
        self.stack_C = stack_C
        self.stack_D = stack_D
        self.heuristicValue = heuristicValue
        self.path = path.copy()  # Ensure the path is copied correctly

    def __str__(self):
        return f"{self.stack_E} {self.stack_A} {self.stack_B} {self.stack_C} {self.stack_D} {self.heuristicValue}"

    # Method to convert the state to a tuple for hashing in a set
    def to_tuple(self):
        return (tuple(self.stack_E), tuple(self.stack_A), tuple(self.stack_B), tuple(self.stack_C), tuple(self.stack_D), self.heuristicValue)

    # Checks if the current state is the goal
    def is_Goal(self):
        return len(self.stack_E) == 0

class Problems:
    def __init__(self, initialState):
        self.initialState = initialState
  
    # Move checking if the next move is valid or not
    def move(self, from_stack, to_stack):
        if len(from_stack) != 0:  # Ensure there is something in the 'from_stack'
            from_circle = from_stack[-1]  # Get the top of the 'from_stack'
            if len(to_stack) == 0 or (from_circle % 2 == to_stack[-1] % 2 and from_circle < to_stack[-1]):
                return True
        return False

    # Heuristic function
    def gethueristic(self, state):
        hueristicE = state[0]
        count = 1
        x = 0
        y = 1
        while y <= len(hueristicE) - 1 and (hueristicE[x] - hueristicE[y]) == 1:
            count += 1
            x += 1
            y += 1
        if len(hueristicE) == 0:
            count = 0
        return count

    # Generate all possible states and add them to the list
    def getGenerateStates(self, initialstate):
        allStates = []
        state = [initialstate.stack_E, initialstate.stack_A, initialstate.stack_B, initialstate.stack_C, initialstate.stack_D, initialstate.heuristicValue, initialstate.path]
        
        for i in range(5):  # Loop through stacks
            for j in range(5):
                if i != j and self.move(state[i], state[j]):
                    copiedState = copy.deepcopy(state)
                    current = copiedState[i].pop()
                    copiedState[j].append(current)
                    copiedState[5] = self.gethueristic(copiedState)  # Update heuristic value
                    copiedState[6] = state[6] + [current]  # Update the path
                    allStates.append(copiedState)
        return allStates  # Returns all possible states


#### Depth-First Search (DFS) #######
def DFS(problem):
    stack = []
    stack.append(problem.initialState)
    explored_nodes = set()  # Set to store visited nodes
    explored_nodes.add(problem.initialState.to_tuple())  # Mark initial state as visited
    count = 0
    
    while len(stack) != 0:
        node = stack.pop()
        count += 1
        print(f"Expanded Node: {node}")
        
        if node.is_Goal():
            print("Goal found:", node)
            print("Number of nodes explored:", count)
            return node.path  # Return the path if goal is found

        node_tuple = node.to_tuple()
        
        # Generate new states and explore
        for new_state in problem.getGenerateStates(node):
            new_node = State(*new_state)  # Create a new State object from the generated state
            new_node_tuple = new_node.to_tuple()
            
            # Only add the state if it hasn't been visited
            if new_node_tuple not in explored_nodes:
                stack.append(new_node)
                explored_nodes.add(new_node_tuple)  # Mark this state as visited

    print("No solution found.")
    return []


#### Breadth-First Search (BFS) #######
def BFS(problem):
    queue = deque([problem.initialState])
    visitedNodes = set()
    count = 0   
    while len(queue) != 0:
        current = queue.popleft()
        count += 1
        print("Expanded Node:", current)
        print("Number of Nodes explored:", count)

        if current.is_Goal():
            print("Goal Found", current)
            return current.path

        node_tuple = current.to_tuple()  # Convert state to tuple
        if node_tuple not in visitedNodes:
            visitedNodes.add(node_tuple)
            new_states = problem.getGenerateStates(current)
            
            for new_state in new_states:
                new_node = State(*new_state)
                new_node_tuple = new_node.to_tuple()
                
                if new_node_tuple not in visitedNodes:
                    queue.append(new_node)

    print("No solution found.")
    return []


#### Best-First Search #######
def BestFirstSearch(problem):
    queue = deque([problem.initialState])
    visitedNodes = set()
    count = 0
    while len(queue) != 0:
        current = queue.popleft()
        count += 1
        print("Expanded Node:", current)
        print("Number of nodes explored:", count)
        
        if current.is_Goal():
            print("Goal Found:", current)
            return current.path

        node_tuple = current.to_tuple()  # Convert state to tuple
        if node_tuple not in visitedNodes:
            visitedNodes.add(node_tuple)
            new_states = problem.getGenerateStates(current)
            
            for new_state in new_states:
                new_node = State(*new_state)
                new_node_tuple = new_node.to_tuple()
                
                if new_node_tuple not in visitedNodes:
                    queue.append(new_node)
            # Sort the queue based on heuristic value
            queue = deque(sorted(queue, key=lambda state: state.heuristicValue))

    print("No solution found.")
    return []
#### A_Star #######
def A_Star(problem):
    queue = deque([problem.initialState])
    visitedNodes = set()
    count = 0   
    while len(queue) != 0:
        current = queue.popleft()
        count += 1
        print("Expanded Node:", current)
        print("Number of Nodes explored:", count)

        if current.is_Goal():
            print("Goal Found", current)
            return current.path

        node_tuple = current.to_tuple()  # Convert state to tuple
        if node_tuple not in visitedNodes:
            visitedNodes.add(node_tuple)
            new_states = problem.getGenerateStates(current)
            
            for new_state in new_states:
                new_node = State(*new_state)
                new_node_tuple = new_node.to_tuple()
                
                if new_node_tuple not in visitedNodes:
                    queue.append(new_node)

    print("No solution found.")
    return []

def main():
    initial_game_state = State(
        stack_E=[8, 7, 6, 5, 4, 3, 2, 1],
        stack_A=[],
        stack_B=[],
        stack_C=[],
        stack_D=[]
    )
    problem1 = Problems(initial_game_state)
    
    # Uncomment one of the following search algorithms to test:
    name=input("Enter the search you want,dfs,bfs,astar,bestfs:")
    if(name=="dfs"):
        path = BFS(problem1)
    elif(name=="bfs"):
        path = BFS(problem1)
    elif(name=="astar"):
        path=A_Star(problem1)
    elif(name=="bestfs"):
        path = BestFirstSearch(problem1)
     
    if path:
        print("Solution Path:", path)

if __name__ == "__main__":
    main()
