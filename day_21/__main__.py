operations = {
    "+": lambda a,b: a + b,
    "-": lambda a,b: a - b,
    "*": lambda a,b: a * b,
    "/": lambda a,b: a / b
}

reverse_equation = {
    "+": lambda res,a,b,match: [res, "-", b] if not match else [res, "-", a],
    "-": lambda res,a,b,match: [res, "+", b] if not match else [a, "-", res],
    "*": lambda res,a,b,match: [res, "/", b] if not match else [res, "/", a],
    "/": lambda res,a,b,match: [res, "*", b] if not match else [a, "/", res]
}

def monkey_number(equations, name):
    value = equations.get(name)
    
    # If this key is in the dict, we need to search an equation with it and reverse it
    if value is None: return reverse_search(equations, name)

    return int(value[0]) if len(value) == 1 else int(operations[value[1]]( monkey_number(equations, value[0]), monkey_number(equations, value[2]) ))

def reverse_search(equations, name):
    # Searches for an equation if the target name
    for key, equation in equations.items():
        if name in equation:
            original_key = key
            reversed_equation = reverse_equation[equation[1]](
                key,
                equation[0],
                equation[2],
                equation.index(name)
            )
            break
    
    # If the root key is found, this equation should be overritten with a 0
    if original_key == "root":
        equations[original_key] = "0"
    # Otherwise remove the original equation from the equations map
    else:
        equations.pop(original_key)
    
    # Add the new equation to the map
    equations[name] = reversed_equation

    return monkey_number(equations, name)



def main():
    # Read input file contents
    with open("day_21/input.txt", "r") as file:
        # for line in file.read().split("\n"):
        equations = dict([[line.split(": ")[0], line.split(": ")[1].split(" ")] for line in file.read().split("\n")])

    # Part One algorithms
    TARGET_MONKEY = "root"
    
    result = monkey_number(equations, TARGET_MONKEY)
    
    # Part One visualization
    print("\n> Part One <")
    print(f"   The monkey with name \"root\" has a value of {result}.")

    # Part Two algorithms
    TARGET_MONKEY = "humn" # Me :D

    # Prepares the equations map (accordingly to the instructions)
    equations["root"][1] = "-"
    equations.pop("humn")

    result = monkey_number(equations, TARGET_MONKEY)
    
    # Part Two visualization
    print("\n> Part Two <")
    print(f"   I should yell the number {result}!")
    
if __name__ == "__main__":
    main()
