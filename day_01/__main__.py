def main():
    # Read input file contents
    with open("day_01/input.txt", "r") as file:
        elfs_lists = [list(map(int, elf.split("\n"))) for elf in file.read().split("\n\n")]
        calories_per_elf = [sum(list) for list in elfs_lists]

    # Part One algorithms
    top_1_cal = max(calories_per_elf)
    top_1_pos = calories_per_elf.index(top_1_cal)

    # Part One visualization
    print("\n> Part One <")
    print(f"   The elf with the most calories is {top_1_pos} with {top_1_cal} calories!")
    

    
    # Part Two algorithms
    top_3_cal = sorted(calories_per_elf, reverse=True)[:3]
    top_3_pos = [calories_per_elf.index(cal) for cal in top_3_cal]
    top_3_total = sum(top_3_cal)

    # Part Two visualization
    podium = """
         {:^5}          | #1: Elf number {}. Calories: {}
         @---@          |
    {:^5}| @ |          | #2: Elf number {}. Calories: {}
    @---@| | |          |
    | @ || | |{:^5}     | #3: Elf number {}. Calories: {}
    | | || | |@---@     |
    | | || | || @ |     | Total calories: {} """

    print("\n> Part Two <")
    print(podium.format(
        top_3_pos[0], top_3_pos[0], top_3_cal[0],
        top_3_pos[1], top_3_pos[1], top_3_cal[1],
        top_3_pos[2], top_3_pos[2], top_3_cal[2],
        top_3_total
    ))

if __name__ == "__main__":
    main()
