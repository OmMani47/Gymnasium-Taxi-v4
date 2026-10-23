import gymnasium as gym
import time
from taxi_problem import TaxiProblem
from search_algorithms import breadthFirstSearch, depthFirstSearch, astarSearch

ALGORITHMS = {
    "bfs": breadthFirstSearch,
    "dfs": depthFirstSearch,
    "astar": astarSearch,
}


def run_episode(env, algorithm="astar", delay=0.5, render=True):
    
# run one ep search and follow the path
    
    
    state, _ = env.reset()    #resets the env
    problem = TaxiProblem(state)

    start_time = time.time()    # start timerfor search
    cost, path, explored = ALGORITHMS.get(algorithm, astarSearch)(problem)
    elapsed = time.time() - start_time

    if path is None:
        print("No solution found for this starting state.")
        return 0, 0, explored, elapsed

    total_reward = 0
    for action in path:                              
        state, reward, terminated, truncated, _ = env.step(action)
        total_reward += reward
        if render:
            env.render()
            time.sleep(delay)              # delay to see whats going on
        if terminated or truncated:
            break

    return total_reward, cost, explored, elapsed


def compare_algorithms(env):
  
   # doing atsk 3 runming all three algorithms on the same starting state and compare

    state, _ = env.reset()

    print("  Comparing search algorithms on the same starting state")

    print(f"{'Algorithm':<10}{'Path length':<14}{'Explored':<12}{'Time (s)':<10}")

    for name, algorithm in ALGORITHMS.items():
        problem = TaxiProblem(state)
        start_time = time.time()
        cost, path, explored = algorithm(problem)
        elapsed = time.time() - start_time
        length = cost if path is not None else "no solution"
        print(f"{name:<10}{str(length):<14}{explored:<12}{elapsed:<10.5f}")


def evaluate_algorithms(num_episodes=100):
    # runs all three algorithms on the set of random start for 100 times
    
    env = gym.make("Taxi-v4").unwrapped
    seeds = [env.reset(seed=s)[0] for s in range(num_episodes)]

    print(f"\n  Evaluating {num_episodes} episodes per algorithm")
    print(f"{'Algorithm':<10}{'AvgLength':<12}{'AvgExplored':<14}{'AvgTime(s)':<12}{'AvgReward':<10}")

    for name, algorithm in ALGORITHMS.items():
        totals = [0, 0, 0, 0]  # length, explored, time, reward

        for start_state in seeds:
            t0 = time.time()
            cost, path, explored = algorithm(TaxiProblem(start_state))
            elapsed = time.time() - t0

            env.s = start_state
            reward = sum(env.step(a)[1] for a in path)    #calc reward for the algorithm

            totals[0] += cost
            totals[1] += explored
            totals[2] += elapsed
            totals[3] += reward

        avg = [t / num_episodes for t in totals]
        print(f"{name:<10}{avg[0]:<12.2f}{avg[1]:<14.1f}{avg[2]:<12.5f}{avg[3]:<10.2f}")

    env.close()


def main():

    print("  ICT203 Assignment 1 Taxi-v4 Search Agent")
    print("Om Mani Tamang Student Id = 35349382")
    print("Available algorithms: bfs, dfs, astar")
    algo = input("Select search algorithm: ").strip().lower()
    if algo not in ALGORITHMS:
        algo = "astar"                   # astar is set to default algorithm incase of invalid input by user

    try:
        loops = int(input("How many episodes to run : ") or "1")
    except ValueError:
        loops = 1                 # if invalid input the loop runs for one time

    compare = input("Also compare all 3 algorithms on one state? [y/N]: ").strip().lower() == "y"
    run_eval = input("Run full 100-episode evaluation across all algorithms? [y/N]: ").strip().lower() == "y"

    if run_eval:
        evaluate_algorithms(num_episodes=100)

    env = gym.make("Taxi-v4", render_mode="human")

    if compare:
        compare_algorithms(env)

    results = []
    for i in range(loops):
        print(f"\nEpisode {i + 1} ")
        reward, length, explored, t = run_episode(env, algorithm=algo)
        print(f"Algorithm used  : {algo}")
        print(f"Path length     : {length}")
        print(f"States explored : {explored}")
        print(f"Time taken      : {t:.4f} seconds")
        print(f"Total reward    : {reward}")
        results.append((length, explored, t, reward))
        time.sleep(0.8)                #aading break for betweee eps

    env.close()

    if results:
       
        print("  Summary")
       
        n = len(results)
        print(f"Average path length     : {sum(r[0] for r in results) / n:.1f}")

        print(f"Average states explored : {sum(r[1] for r in results) / n:.1f}")
        print(f"Average time            : {sum(r[2] for r in results) / n:.4f} s")
        print(f"Average reward          : {sum(r[3] for r in results) / n:.1f}")


if __name__ == "__main__":
    main()