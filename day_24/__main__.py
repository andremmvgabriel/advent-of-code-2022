def main():
    # Read input file contents
    with open("day_24/input.txt", "r") as file:
        lines = file.read().split("\n")

    # Grid size - Ignores the walls
    grid_size = ( len(lines[0][1:-1]), len(lines[1:-1]) ) # x, y

    # Start and Finish positions - These are out of grid bounds
    start_pos = (lines[0].index(".") - 1, -1)
    finish_pos = (lines[-1].index(".") - 1, grid_size[1])

    # Creates a dictionary with all the blizzards, separated by each direction
    blizzards = {
        ">": set([ (j, i) for i, line in enumerate(lines[1:-1]) for j, char in enumerate(line[1:-1]) if char == ">" ]),
        "<": set([ (j, i) for i, line in enumerate(lines[1:-1]) for j, char in enumerate(line[1:-1]) if char == "<" ]),
        "^": set([ (j, i) for i, line in enumerate(lines[1:-1]) for j, char in enumerate(line[1:-1]) if char == "^" ]),
        "v": set([ (j, i) for i, line in enumerate(lines[1:-1]) for j, char in enumerate(line[1:-1]) if char == "v" ])
    }

    reverse_move = { # m = minute
        ">": lambda pos, m: ((pos[0] - m) % grid_size[0], pos[1]),
        "<": lambda pos, m: ((pos[0] + m) % grid_size[0], pos[1]),
        "^": lambda pos, m: (pos[0], (pos[1] + m) % grid_size[1]),
        "v": lambda pos, m: (pos[0], (pos[1] - m) % grid_size[1])
    }

    def get_move_options(pos):
        return [
            pos, # Same position
            (pos[0] - 1, pos[1]), # Left
            (pos[0] + 1, pos[1]), # Right
            (pos[0], pos[1] - 1), # Top
            (pos[0], pos[1] + 1), # Bottom
        ]

    def crossing_time(start_pos, finish_pos, initial_time):
        # Actual output
        minutes = initial_time

        check_positions = [start_pos]

        while True:
            next_checks_positions = set()
            for pos in check_positions:
                for move in get_move_options(pos):
                    # Checks if the move is the finish
                    if move == finish_pos: return minutes

                    # Checks if the position is inside the grid
                    if move[0] < 0 or move[0] >= grid_size[0]: continue
                    if move[1] < 0 or move[1] >= grid_size[1]: continue

                    # Checks if a blizzard is in the position
                    if reverse_move[">"](move, minutes) in blizzards[">"]: continue
                    if reverse_move["<"](move, minutes) in blizzards["<"]: continue
                    if reverse_move["^"](move, minutes) in blizzards["^"]: continue
                    if reverse_move["v"](move, minutes) in blizzards["v"]: continue

                    # Adds the position to the next minute checks
                    next_checks_positions.add( move )

            # If no new possible positions to check were found, it would be better to not move all along. Restart over.
            if not next_checks_positions: next_checks_positions.add(start_pos)

            # Caches the next positions to check
            check_positions = list(next_checks_positions)

            minutes += 1

            if minutes >= 1000000 + initial_time: return -1 # Invalid time

    # Part One algorithms
    time_to_cross = crossing_time(start_pos, finish_pos, 1)

    # Part One visualization
    print("\n> Part One <")
    print(f"   The fastest time to reach the goal is {time_to_cross} minutes.")
    
    # Part Two algorithms
    trip_2_time = crossing_time(finish_pos, start_pos, time_to_cross)
    trip_3_time = crossing_time(start_pos, finish_pos, trip_2_time)

    # Part Two visualization
    print("\n> Part Two <")
    print(f"   The first trip took {time_to_cross} minutes, going back took {trip_2_time - time_to_cross} minutes, the last trip took {trip_3_time - trip_2_time} minutes.")
    print(f"   The whole trip took {trip_3_time} minutes.")
    
if __name__ == "__main__":
    main()
