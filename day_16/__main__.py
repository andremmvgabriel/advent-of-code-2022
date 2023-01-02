"""
Part 2 was giving wrong results with my initial developed solution.

Thanks to the Reddit user Diderikdm, it was possible to develop a solution that provided the correct answer! Many thanks to you!

Reddit post: https://www.reddit.com/r/adventofcode/comments/10n1utt/comment/j68imxl/
"""

from collections import deque

def floyd_warshall_algorithm(graph):
    for k in graph:
        for i in graph:
            for j in graph:
                graph[i][j] = min( graph[i][j], graph[i][k] + graph[k][j] )
    return graph



def main():
    # Read input file contents
    with open("day_16/input.txt", "r") as file:        
        lines = file.read().split("\n")

        valves = tuple([ line.split("; ")[0][6:8] for line in lines ])
        valves_flows = { line.split("; ")[0][6:8]: int(line.split("; ")[0].split("=")[1]) for line in lines }
        valves_connections = { line.split("; ")[0][6:8]: tuple([ v[-2:] for v in line.split("; ")[1][22:].split(",") ]) for line in lines }
    
    # Common
    graph = { v1: { v2: 0 if v1 == v2 else 1 if v2 in valves_connections[v1] else 9999 for v2 in valves } for v1 in valves }
    graph = floyd_warshall_algorithm(graph)

    valves_with_flows = tuple([valve for valve in valves if valves_flows[valve] > 0])

    # Part One algorithms
    NUMBER_MINUTES = 30
    
    INITIAL_STATE = (
        0, "AA", NUMBER_MINUTES,
        tuple(sorted([ valve for valve in valves if valves_flows[valve] <= 0 ]))
    )

    # Actual output
    # > This will cache all the states achieved based on the opened valves and the current valve 
    all_states = { INITIAL_STATE[-1]: INITIAL_STATE[0] }

    # Find the best state
    states = deque( [INITIAL_STATE] )
    while states:
        state_flow, state_valve, state_time_left, state_valves = states.popleft()

        for valve in valves_with_flows:
            # Calculates the time left going to the valve and opening it
            new_time = state_time_left - graph[state_valve][valve] - 1

            # If the previous action reaches the maximum amount of allowed time, cannot go
            if new_time <= 0: continue

            # Do not proceed for the valve if it is already opened
            if valve in state_valves: continue

            # Creates the new state
            new_state = (
                state_flow + new_time * valves_flows[valve],
                valve,
                new_time,
                tuple(sorted(state_valves + (valve,)))
            )

            # Key that will be stored in the all states
            key=new_state[-1] + (valve,)

            # Do not cache the new state if it was already achieved
            if (val:=all_states.get(key)) and val >= new_state[0]: continue

            # Create a new state in the new valve
            states.append(new_state)
            all_states[key] = new_state[0]
    
    # Part One visualization
    print("\n> Part One <")
    print(f"   The best flow that can be achieved in {NUMBER_MINUTES} minutes is {max(all_states.values())}.")



    # Part Two algorithms
    NUMBER_MINUTES = 26
    
    INITIAL_STATE = (
        0,
        ("AA", "AA"), # Player 1 & 2 starting valves
        (NUMBER_MINUTES, NUMBER_MINUTES), # Player 1 & 2 remaining times
        tuple(sorted([ valve for valve in valves if valves_flows[valve] <= 0 ]))
    )

    # Actual output
    # > This will cache all the states achieved based on the opened valves and the current valves of the entities
    all_states = { INITIAL_STATE[-1]: INITIAL_STATE[0] }

    # Find the best state
    states = deque( [INITIAL_STATE] )
    while states:
        state_flow, (state_valve_1, state_valve_2), (state_time_left_1, state_time_left_2), state_valves = states.popleft()

        for valve in valves_with_flows:
            # Calculates the time left going to the valve and opening it (of the first player)
            new_time = state_time_left_1 - graph[state_valve_1][valve] - 1

            # If the previous action reaches the maximum amount of allowed time, cannot go
            if new_time <= 0: continue

            # Do not proceed for the valve if it is already opened
            if valve in state_valves: continue

            # Creates the new state
            new_state = (
                state_flow + new_time * valves_flows[valve],
                (state_valve_2, valve),
                (state_time_left_2, new_time),
                tuple(sorted(state_valves + (valve,)))
            )

            # Key that will be stored in the all states
            # > Adding the current valve move into a sorted list of opened valves was skipping the solution
            # > The pair of current valve positions by each entity (sorted) is added instead.
            # > Cons: ~3x more time.
            key=new_state[-1] + tuple(sorted((state_valve_2, valve)))

            # Do not cache the new state if it was already achieved
            if (val:=all_states.get(key)) and val >= new_state[0]: continue

            # Create a new state in the new valve
            states.append(new_state)
            all_states[key] = new_state[0]

    # Part Two visualization
    print("\n> Part Two <")
    print(f"   The best flow that can be achieved in {NUMBER_MINUTES} minutes is {max(all_states.values())}.")

if __name__ == "__main__":
    main()
