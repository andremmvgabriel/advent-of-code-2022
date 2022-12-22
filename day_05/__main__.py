def main():
    # Read input file contents
    with open("day_05/input.txt", "r") as file:
        drawing, moves_list = file.read().split("\n\n")
    
    # Relevant for both parts
    *cargo_layers, numbers_layer = drawing.split("\n")
    n_stacks = len(list(filter(lambda a: a!="", numbers_layer.split(" "))))
    instructions = [list(map(int,filter(lambda a: a!="", move.replace("move", "").replace("from", "").replace("to", "").split(" ")))) for move in moves_list.split("\n")]
    
    # > Range filtering explanation: (of cargo_stacks)
    #
    # [A]     [B]
    # [C] [D] [E]
    # | | | | | |
    # 0 2 4 6 8 10 (indices)
    # 
    # > 4*i + 1 : 4*i + 2  ->  This solution just contains the letters
    # 1. The wanted range is (knowing that before ':' is inclusive and after exclusive):
    # 2. Every before value and after value differs by 4, which can be written in a iterative way
    #       1:2     |     5:6     |     9:10       (1)
    #   4*0+1:2+4*0 | 4*1+1:2+4*1 | 4*2+1:2+4*2    (2)
    # 
    # R: 4*i+1:4*i+2
    #
    # > 4*i : 4*i + 3  ->  This solution preserves the crate symbolism ("[]")
    # 1. Simply include one more character by each side of the previous response
    # 
    #   4*i+1-1:4*i+2+1
    #
    # R: 4*i:4*i+3

    # Part One algorithms
    cargo_stacks_1 = [list(filter(lambda a: a!= " ", [line[4*i+1:4*i+2] for line in cargo_layers[::-1]])) for i in range(n_stacks)]

    for move in instructions:
        i_amount = move[0]
        i_from = move[1]-1
        i_to = move[2]-1

        cargo_stacks_1[i_to] += cargo_stacks_1[i_from][-i_amount:][::-1]
        cargo_stacks_1[i_from] = cargo_stacks_1[i_from][:-i_amount]

    # Part One visualization
    print("\n> Part One <")
    print(f"   The creates on top of each stack are: {''.join(stack[-1] for stack in cargo_stacks_1)}")

    # Part One a more beautiful visualization :D
    print()
    drawing_results_1 = "\t"
    for i in range(max([len(stack) for stack in cargo_stacks_1]))[::-1]:
        for stack in cargo_stacks_1:
            if len(stack) >= i + 1: drawing_results_1 += f"[{stack[i]}]"
            else:                   drawing_results_1 += "   "
            drawing_results_1 += " "
        drawing_results_1 += "\n\t"
    for i in range(n_stacks):
        drawing_results_1 += f" {i+1} "
        drawing_results_1 += f" "
    print(drawing_results_1)



    # Part Two algorithms
    cargo_stacks_2 = [list(filter(lambda a: a!= " ", [line[4*i+1:4*i+2] for line in cargo_layers[::-1]])) for i in range(n_stacks)]

    for move in instructions:
        i_amount = move[0]
        i_from = move[1]-1
        i_to = move[2]-1

        cargo_stacks_2[i_to] += cargo_stacks_2[i_from][-i_amount:]
        cargo_stacks_2[i_from] = cargo_stacks_2[i_from][:-i_amount]

    # Part Two visualization
    print("\n> Part Two <")
    print(f"   The creates on top of each stack are: {''.join(stack[-1] for stack in cargo_stacks_2)}")

    # Part Two a more beautiful visualization :D
    print()
    drawing_results_1 = "\t"
    for i in range(max([len(stack) for stack in cargo_stacks_2]))[::-1]:
        for stack in cargo_stacks_2:
            if len(stack) >= i + 1: drawing_results_1 += f"[{stack[i]}]"
            else:                   drawing_results_1 += "   "
            drawing_results_1 += " "
        drawing_results_1 += "\n\t"
    for i in range(n_stacks):
        drawing_results_1 += f" {i+1} "
        drawing_results_1 += f" "
    print(drawing_results_1)

if __name__ == "__main__":
    main()
