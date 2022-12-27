from collections import deque

def dijkstra_algorithm(grid, start):
    visited = set()
    next_to_analyse = deque([start])
    grid_moves = [ [0 for i in range(len(grid[0]))] for j in range(len(grid)) ]

    while len(next_to_analyse):
        vertex = next_to_analyse.popleft()

        if vertex not in visited:
            visited.add(vertex)
            
            neighbours = [ (vertex[0] + vec[0], vertex[1] + vec[1], ord(grid[vertex[0] + vec[0]][vertex[1] + vec[1]])) for vec in [(-1, 0), (0, 1), (1, 0), (0, -1)] if 0 <= vertex[0] + vec[0] < len(grid) and 0 <= vertex[1] + vec[1] < len(grid[0]) ]

            for neighbour in neighbours:
                if neighbour[2] <= vertex[2] + 1:
                    next_to_analyse.append( neighbour )
                    grid_moves[neighbour[0]][neighbour[1]] = grid_moves[vertex[0]][vertex[1]] + 1

    return grid_moves

def main():
    # Read input file contents
    with open("day_12/input.txt", "r") as file:
        grid = file.read().split("\n")

    # Part One algorithms
    start_pos = (0, 0, ord("a"))
    finish_pos = (0, 0, ord("z"))

    # Find the start and finish positions
    for i, row in enumerate(grid):
        start_pos = (i, row.index("S"), ord("a")) if row.find("S") != -1 else start_pos
        finish_pos = (i, row.index("E"), ord("z")) if row.find("E") != -1 else finish_pos
    
    # Gets the minimum amount of moves for all grid
    grid_moves = dijkstra_algorithm(grid, start_pos)

    # Part One visualization
    print("\n> Part One <")
    print(f"   From S ({start_pos}) to E ({finish_pos}), the best path includes {grid_moves[finish_pos[0]][finish_pos[1]]} moves.")

    # Part Two algorithms
    starts = [start_pos] + [ (i, row.index("a"), ord("a")) for i, row in enumerate(grid) if row.find("a") != -1 ]
    starts_moves = list(filter(lambda x: x!=0, [ dijkstra_algorithm(grid, position)[finish_pos[0]][finish_pos[1]] for position in starts ] ))

    min_moves, min_start_pos = min(zip(starts_moves, starts))

    # Part Two visualization
    print("\n> Part Two <")
    print(f"   The start position with the fewest steps to E ({finish_pos}) is {min_start_pos} with {min_moves} moves.")

if __name__ == "__main__":
    main()
