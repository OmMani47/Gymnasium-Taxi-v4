import queue
import heapq


def breadthFirstSearch(problem): 
    frontier = queue.Queue()
    frontier.put((problem.start_state(), []))   # (state, path)
    explored = set()
 
    while not frontier.empty():
        state, path = frontier.get()
        if state in explored:
            continue
        explored.add(state)
 
        if problem.goal_test(state):
            return len(path), path, len(explored)
 
        for action, new_state, cost in problem.SuccAndCost(state):
            if new_state not in explored:
                frontier.put((new_state, path + [action]))
 
    return None, None, len(explored)


 
def depthFirstSearch(problem, max_depth=60):
    
   # DFS mkaesuse of a stack. Not optimal, but can find a solution.

    frontier = [(problem.start_state(), [])]
    explored = {problem.start_state()}
 
    while frontier:
        state, path = frontier.pop()            # LIFO
 
        if problem.goal_test(state):
            return len(path), path, len(explored)
 
        if len(path) >= max_depth:
            continue
 
        # reverse so lower actions are tried first
        for action, new_state, cost in reversed(problem.SuccAndCost(state)):
            if new_state not in explored:
                explored.add(new_state)
                frontier.append((new_state, path + [action]))
 
    return None, None, len(explored)
 
 
def astarSearch(problem):
 
   # Heuristic = Manhattan distance from taxi to passenger + Manhattan distance from passenger to destination.
 
    def heuristic(state):
        row, col, passenger, dest = problem.decode(state)
        taxi = (row, col)
        if passenger == 4:          # already in taxi
            target = problem.locations[dest]
            return abs(taxi[0] - target[0]) + abs(taxi[1] - target[1])
        else:
            pass_pos = problem.locations[passenger]
            dest_pos = problem.locations[dest]
            return (abs(taxi[0] - pass_pos[0]) + abs(taxi[1] - pass_pos[1]) +
                    abs(pass_pos[0] - dest_pos[0]) + abs(pass_pos[1] - dest_pos[1]))
 
    # frontier items: (f, g, state, path)
    frontier = []
    start = problem.start_state()
    heapq.heappush(frontier, (heuristic(start), 0, start, []))
    explored = set()
    g_score = {start: 0}
 
    while frontier:
        f, g, state, path = heapq.heappop(frontier)
        if state in explored:
            continue
        explored.add(state)
 
        if problem.goal_test(state):
            return len(path), path, len(explored)
 
        for action, new_state, cost in problem.SuccAndCost(state):
            new_g = g + cost
            if new_state not in g_score or new_g < g_score[new_state]:
                g_score[new_state] = new_g
                f = new_g + heuristic(new_state)
                heapq.heappush(frontier, (f, new_g, new_state, path + [action]))
 
    return None, None, len(explored)
