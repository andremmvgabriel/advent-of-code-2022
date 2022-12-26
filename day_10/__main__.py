def main():
    # Read input file contents
    with open("day_10/input.txt", "r") as file:
        program = file.read().split("\n")

    # Part One algorithms
    register = 1
    cycles = []

    for i, instruction in enumerate(program):
        # Gets the cycles that the instruction need to complete its execution, and the register value to add to the system register
        inst_cycles, inst_reg = (1, 0) if "noop" == instruction else (2, int(instruction.split(" ")[1]))

        # Registers the Registry value of the current cycle
        for j in range(inst_cycles): cycles.append(register)

        # Increases the instruction register value once the instruction finished
        register += inst_reg
    
    # Calculates the strenght of signal in each cycle
    signals_strenght = [ (value * (i+1)) for i, value in enumerate(cycles) if ((i + 21) % 40 == 0) ]

    # Part One visualization
    print("\n> Part One <")
    print(f"   The signal strenght is {sum(signals_strenght)} (sum of {len(signals_strenght)} signals strength).")

    # Part Two algorithms
    NUMBER_CRT_LINES = 6

    crt_chars = [ "#" if (i % 40 >= value - 1 and i % 40 <= value + 1) else "." for i, value in enumerate(cycles) ]
    crt_display = '\n'.join([ ''.join(crt_chars[i*40:(i+1)*40]) for i in range(NUMBER_CRT_LINES) ])
    
    # Part Two visualization
    print("\n> Part Two <")
    print(crt_display)
    
if __name__ == "__main__":
    main()
