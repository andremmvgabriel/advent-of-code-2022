def main():
    # Read input file contents
    with open("day_07/input.txt", "r") as file:
        commands = [ list(filter(lambda a: a!="", command.split("\n"))) for command in file.read().split("$ ")[1:] ]

    # Part One algorithms    
    directories = {"/": 0}
    current_path = ""

    for command in commands:
        if "cd " in command[0]:
            where_to = command[0].split(" ")[-1]

            if where_to == "/":
                current_path = where_to
            elif where_to == "..":
                current_path = "/".join(current_path.split("/")[:-2]) + "/"
            else:
                current_path += f"{where_to}/"
        elif "ls" == command[0]:
            for line_info in command[1:]:
                info1, info2 = line_info.split(" ")

                if info1 == "dir":
                    directories[current_path + f"{info2}/"] = 0
                else:
                    file_size = int(info1)

                    # This size has to be recursively added to all the directories (current and its parents)
                    for i in range(len(current_path.split("/"))-1):
                        update_path = "/".join(current_path.split("/")[:-1-1*i]) + "/"
                        directories[update_path] += file_size
        else:
            print("Invalid command.")
        
    # Part One visualization
    print("\n> Part One <")
    print(f"   The sum of all directories that are at most 100 Kb is: {sum([ value for value in directories.values() if value <= 100000])}")
    
    # Part Two algorithms
    SYSTEM_SIZE = 70000000
    UPDATE_SIZE = 30000000

    available_size = SYSTEM_SIZE - max(directories.values())
    delete_size, delete_path = [ [x, y] for x, y in sorted(zip(directories.values(), directories.keys())) if x >= (UPDATE_SIZE - available_size) ][0]

    # Part Two visualization
    print("\n> Part Two <")
    print(f"   The perfect directory to delete is {delete_path} with size {delete_size} b.")

if __name__ == "__main__":
    main()
