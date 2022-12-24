def main():
    # Read input file contents
    with open("day_09/input.txt", "r") as file:
        moves = file.read().split("\n")
    
    # Relevant variables for both parts
    direction_vecs = {
        "R": [ 1, 0],
        "L": [-1, 0],
        "U": [ 0, 1],
        "D": [ 0,-1]
    }
    
    # Part One algorithms
    starting_pos = [0, 0]
    head_pos = starting_pos.copy()
    tail_pos = starting_pos.copy()

    tail_visited_positions = set([f"{tail_pos}"])

    for i, move in enumerate(moves):
        direction, amount = move.split(" ")

        for j in range(int(amount)):
            # Updates the head position based on the direction to move
            head_pos[0] += direction_vecs[direction][0]
            head_pos[1] += direction_vecs[direction][1]

            # Calculates distance between the head and tail in each axis
            x_diff = head_pos[0] - tail_pos[0]
            y_diff = head_pos[1] - tail_pos[1]

            # Checks if the tail is too distant from the head in any of the axis
            if abs(x_diff) > 1 or abs(y_diff) > 1:
                # Updates the tail position
                tail_pos[0] += x_diff / abs(x_diff) if x_diff else 0
                tail_pos[1] += y_diff / abs(y_diff) if y_diff else 0

                # Adds a new visited position to the set
                tail_visited_positions.add(f"{tail_pos}")
                
    # Part One visualization
    print("\n> Part One <")
    print(f"   The tail of the rope has been in {len(tail_visited_positions)} different positions.")

    # Part Two algorithms
    NUMBER_KNOTS = 10 # H + 1-9
    rope_knots = [ starting_pos.copy() for i in range(NUMBER_KNOTS) ]

    tail_visited_positions = set([f"{rope_knots[-1]}"])

    for i, move in enumerate(moves):
        direction, amount = move.split(" ")

        for j in range(int(amount)):
            # Updates the head position based on the direction to move
            rope_knots[0][0] += direction_vecs[direction][0]
            rope_knots[0][1] += direction_vecs[direction][1]

            # Updates all the rope nots
            for n, knot in enumerate(rope_knots[1:]):
                # Calculates distance between the current knot and its head knot
                x_diff = rope_knots[n][0] - rope_knots[n+1][0]
                y_diff = rope_knots[n][1] - rope_knots[n+1][1]

                # Checks if the knot is too distant from the its parent knot in any of the axis
                if abs(x_diff) > 1 or abs(y_diff) > 1:
                    # Updates the knot position
                    rope_knots[n+1][0] += (x_diff // abs(x_diff)) if x_diff else 0
                    rope_knots[n+1][1] += (y_diff // abs(y_diff)) if y_diff else 0

                    # Checks if it is the tail
                    if n+2 == NUMBER_KNOTS:
                        # Adds a new visited position to the set
                        tail_visited_positions.add(f"{rope_knots[-1]}")
                else: break # If knot did not move, all next knots will remain the same as well            
    
    print("\n> Part Two <")
    print(f"   The tail of the rope has been in {len(tail_visited_positions)} different positions.")
    
if __name__ == "__main__":
    main()
