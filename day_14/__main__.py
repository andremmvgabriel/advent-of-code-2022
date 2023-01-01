def deploy_sand(grid, start):
    while True:
        sand_pos = [start[0], start[1]]
        voided = False

        while True:
            # Straight down
            if sand_pos[0] + 1 > len(grid): # Void check
                voided=True
                break
            if grid[sand_pos[0]+1][sand_pos[1]] == 0:
                sand_pos[0] += 1
                continue

            # Left diagonal
            if sand_pos[1] - 1 < 0: # Void check
                voided=True
                break
            if grid[sand_pos[0]+1][sand_pos[1]-1] == 0:
                sand_pos[0] += 1
                sand_pos[1] -= 1
                continue

            # Right diagonal
            if sand_pos[1] + 1 >= len(grid[0]): # Void check
                voided=True
                break
            if grid[sand_pos[0]+1][sand_pos[1]+1] == 0:
                sand_pos[0] += 1
                sand_pos[1] += 1
                continue

            # Rest position
            grid[sand_pos[0]][sand_pos[1]] = 2
            break

        # Stop if the sand block went to void
        if voided: break

        # Stop if the last rest block is located at the starting point (cannot deploy more sand)
        if grid[start[0]][start[1]] == 2: break
    
    return grid

def main():
    # Read input file contents
    with open("day_14/input.txt", "r") as file:
        rock_platforms_orig = [ [eval(coord)[::-1] for coord in line.split(" -> ")] for line in file.read().split("\n")]
        
    # Part One algorithms
    sand_machine = (0, 500)

    # Rocks points limits
    rocks_min = (0, min(set([vertice[1] for platform in rock_platforms_orig for vertice in platform])))
    rocks_max = (max(set([vertice[0] for platform in rock_platforms_orig for vertice in platform])), max(set([vertice[1] for platform in rock_platforms_orig for vertice in platform])))

    # Put the start point and the rock platforms coordinates in the grid limits
    start_point = (sand_machine[0] - rocks_min[0], sand_machine[1] - rocks_min[1])
    rock_platforms = [[(coord[0]-rocks_min[0], coord[1]-rocks_min[1]) for coord in platform] for platform in rock_platforms_orig]

    # Constructing the 2D grid
    grid = [ [ 0 for j in range(rocks_min[1], rocks_max[1]+1) ] for i in range(rocks_min[0], rocks_max[0]+1) ]
    
    # Placing the rocks in the grid
    for i, platform in enumerate(rock_platforms):
        for j in range(len(platform)-1):
            for y in range(min(platform[j][0], platform[j+1][0]), max(platform[j][0], platform[j+1][0]) + 1):
                for x in range(min(platform[j][1], platform[j+1][1]), max(platform[j][1], platform[j+1][1]) + 1):
                    grid[y][x] = 1
    
    # Deploying the sand
    grid = deploy_sand(grid, start_point)

    # Part One visualization
    print("\n> Part One <")
    print(f"   There are {sum([line.count(2) for line in grid])} resting blocks of sand.")



    # Part Two algorithms
    
    # Calculates the new min and max values of the rocks
    rocks_max = (rocks_max[0] + 2, sand_machine[1] + (rocks_max[0] + 2))
    rocks_min = (rocks_min[0]    , sand_machine[1] - (rocks_max[0] + 2))

    # Creates the ground rock platform
    rock_platforms_orig.append([(rocks_max[0], rocks_min[1]), (rocks_max[0], rocks_max[1])])

    # Put the start point and the rock platforms coordinates in the new grid limits
    start_point = (sand_machine[0] - rocks_min[0], sand_machine[1] - rocks_min[1])
    rock_platforms = [[(coord[0]-rocks_min[0], coord[1]-rocks_min[1]) for coord in platform] for platform in rock_platforms_orig]

    # Constructing the 2D grid
    grid = [ [ 0 for j in range(rocks_min[1], rocks_max[1]+1) ] for i in range(rocks_min[0], rocks_max[0]+1) ]
    
    # Placing the rocks in the grid
    for i, platform in enumerate(rock_platforms):
        for j in range(len(platform)-1):
            for y in range(min(platform[j][0], platform[j+1][0]), max(platform[j][0], platform[j+1][0]) + 1):
                for x in range(min(platform[j][1], platform[j+1][1]), max(platform[j][1], platform[j+1][1]) + 1):
                    grid[y][x] = 1
    
    # Deploying the sand
    grid = deploy_sand(grid, start_point)

    # Part Two visualization
    print("\n> Part Two <")
    print(f"   There are {sum([line.count(2) for line in grid])} resting blocks of sand.")

if __name__ == "__main__":
    main()
