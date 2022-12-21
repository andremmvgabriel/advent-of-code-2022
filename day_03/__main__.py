# Global variables
A_UCHAR = ord("A")
A_LCHAR = ord("a")
Z_UCHAR = ord("Z")
Z_LCHAR = ord("z")

# QoL functions
def to_ascii(data: list) -> list:
    return [ord(value) for value in data]

def to_priority(data: list) -> list:
    # This function assumes that the input data is already given in ascii values
    return [ (value - A_UCHAR + 1 + 26) if (value >= A_UCHAR and value <= Z_UCHAR) else (value - A_LCHAR + 1) for value in data ]

# Solutions
def main():
    # Read input file contents
    with open("day_03/input.txt", "r") as file:
        rucksacks = file.read().split("\n")

    # Part One algorithms
    compartments = [ [rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:]] for rucksack in rucksacks ]

    duplicates_items = []
    for comp1, comp2 in compartments:
        for item in comp1:
            if item in comp2:
                duplicates_items.append(item)
                break
    duplicates_ascii = to_ascii(duplicates_items)
    duplicates_prior = to_priority(duplicates_ascii)

    priority_total = sum(duplicates_prior)
    
    # Part One visualization
    print("\n> Part One <")
    print(f"  - Total priority: {priority_total}")



    # Part Two algorithms
    rucksacks_groups = [ [rucksacks[0+i*3], rucksacks[1+i*3], rucksacks[2+i*3]] for i in range(len(rucksacks)//3) ]
    
    group_badges_items = []
    for rs1, rs2, rs3 in rucksacks_groups:
        for item in rs1:
            if item in rs2 and item in rs3:
                group_badges_items.append(item)
                break
    group_badges_ascii = to_ascii(group_badges_items)
    group_badges_prior = to_priority(group_badges_ascii)

    priority_total = sum(group_badges_prior)

    # Part Two visualization
    print("\n> Part Two <")
    print(f"  - Total priority: {priority_total}")

if __name__ == "__main__":
    main()
