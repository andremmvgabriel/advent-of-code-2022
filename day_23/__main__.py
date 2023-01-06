move_directions = [
    # N move position
    lambda pos: (pos[0], pos[1]-1),
    # S move position
    lambda pos: (pos[0], pos[1]+1),
    # W move position
    lambda pos: (pos[0]-1, pos[1]),
    # E move position
    lambda pos: (pos[0]+1, pos[1])
]

scan_directions = [
    # N, NE, and NW position checks
    lambda pos, collection: any(collection.intersection( {(pos[0], pos[1]-1), (pos[0]-1, pos[1]-1), (pos[0]+1, pos[1]-1)} )),
    # S, SE, and SW position checks
    lambda pos, collection: any(collection.intersection( {(pos[0], pos[1]+1), (pos[0]-1, pos[1]+1), (pos[0]+1, pos[1]+1)} )),
    # W, NW, ans SW position checks
    lambda pos, collection: any(collection.intersection( {(pos[0]-1, pos[1]), (pos[0]-1, pos[1]-1), (pos[0]-1, pos[1]+1)} )),
    # E, NE, and SE position checks
    lambda pos, collection: any(collection.intersection( {(pos[0]+1, pos[1]), (pos[0]+1, pos[1]-1), (pos[0]+1, pos[1]+1)} ))
]

def find_elves_positions(elves_positions, rounds=None):
    r = 0 # Rounds counter
    while True:
        proposed_movements = {}
        proposed_positions = set()
        rejected_positions = set()
        for elf in elves_positions:
            # Analyses its surroundings (already puts the analysis in the correct scan order)
            surroundings = [ scan_directions[(r+i)%4](elf, elves_positions) for i in range(4) ]
            # Only proposes a move if there is at least an elf in its surroundings
            if any(surroundings):
                # Only proposes a move if there is an empty direction without an elf
                if (i:=surroundings.index(False) if False in surroundings else -1) != -1:
                    # Proposed move
                    move = move_directions[(r+i)%4](elf)

                    # Registers the elf movement proposition (To have a from-to info)
                    proposed_movements[elf] = move

                    # Adds the move to a rejected list if the proposition was already made by another elf
                    rejected_positions.update( proposed_positions.intersection({move}) )

                    # Adds the move to the list of proposed positions
                    proposed_positions.add(move)
                else: # Keeps its current position if can not propose
                    proposed_movements[elf] = elf
                    proposed_positions.add(elf)
            else: # Keeps its current position if can not propose
                proposed_movements[elf] = elf
                proposed_positions.add(elf)
        
        # Increase the number of rounds
        r += 1
        
        # Checks if no elf moved and stops the simulation if so
        if elves_positions == proposed_positions: break
        
        # Updates the new elfs positions
        accepted_positions = proposed_positions.difference(rejected_positions) # Unique proposed positions
        accepted_positions.update([ key for key, value in proposed_movements.items() if value in rejected_positions ]) 
        elves_positions = accepted_positions

        if rounds and r >= rounds: break # Stops the simulation if a number of rounds was specified     
    
    return elves_positions, r


def main():
    # Read input file contents
    with open("day_23/input.txt", "r") as file:
        elves = set([ (col, row) for row, line in enumerate(file.read().split("\n")) for col, char in enumerate(line) if char == "#" ])

    # Part One algorithms
    NUMBER_ROUNDS = 10

    elves_positions, _ = find_elves_positions(elves.copy(), NUMBER_ROUNDS)
    
    region_width = max([ x for x,_ in elves_positions ]) - min([ x for x,_ in elves_positions ]) + 1
    region_height = max([ y for _,y in elves_positions ]) - min([ y for _,y in elves_positions ]) + 1
    total_area = region_width*region_height
    empty_area = total_area - len(elves)

    # Part One visualization
    print("\n> Part One <")
    print(f"   The area has a total of {total_area} squares (x: {region_width}, y: {region_height})")
    print(f"   Within this area, only {empty_area} squares are not occupied by elves.")
    
    # Part Two algorithms
    _, result = find_elves_positions(elves.copy())

    # Part Two visualization
    print("\n> Part Two <")
    print(f"   No elf moved after round {result}.")
    
if __name__ == "__main__":
    main()   
