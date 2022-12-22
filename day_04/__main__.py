def main():
    # Read input file contents
    with open("day_04/input.txt", "r") as file:
        assignment_pairs = [ assignment.split(",") for assignment in file.read().split("\n") ]

    # Part One algorithms
    full_overlap_counter = 0
    for pair in assignment_pairs:
        p1_min, p1_max = map(int, pair[0].split("-"))
        p2_min, p2_max = map(int, pair[1].split("-"))

        full_range = f"{min(p1_min, p2_min)}-{max(p1_max, p2_max)}"

        # It can only be fully overlapping if the full range is equal to one of the pairs
        if full_range == pair[0] or full_range == pair[1]:
            full_overlap_counter += 1

    # Part One visualization
    print("\n> Part One <")
    print(f"   Full overlapping groups: {full_overlap_counter}")



    # Part Two algorithms
    overlap_counter = 0
    for pair in assignment_pairs:
        p1_min, p1_max = map(int, pair[0].split("-"))
        p2_min, p2_max = map(int, pair[1].split("-"))

        if max(p1_min, p2_min) <= min(p1_max, p2_max):
            overlap_counter += 1
    
    # Part Two visualization
    print("\n> Part Two <")
    print(f"   Overlapping groups: {overlap_counter}")

if __name__ == "__main__":
    main()
