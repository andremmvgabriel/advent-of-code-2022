from collections import deque

def adjacent_cubes(cube):
    return set([
        (cube[0] - 1, cube[1], cube[2]), (cube[0] + 1, cube[1], cube[2]), # -/+ x
        (cube[0], cube[1] - 1, cube[2]), (cube[0], cube[1] + 1, cube[2]), # -/+ y
        (cube[0], cube[1], cube[2] - 1), (cube[0], cube[1], cube[2] + 1), # -/+ z
    ])

def calculate_surface_area(cubes):
    surface_area = 0
    for cube in cubes:
        # For each missing adjacent cube, a surface area is not covered.
        surface_area += [0 if adj in cubes else 1 for adj in adjacent_cubes(cube)].count(1)
    return surface_area



def main():
    # Read input file contents
    with open("day_18/input.txt", "r") as file:
        cubes = set([ eval(line) for line in file.read().split("\n") ])

    # Part One algorithms    
    surface_area = calculate_surface_area(cubes)
    
    # Part One visualization
    print("\n> Part One <")
    print(f"   The surface are of the scanned lava droplet is {surface_area}.")



    # Part Two algorithms

    # For this part, consider the following:
    # > "box" is the volume on which its limits are defined by the placed cubes
    # > "bbox" is the same volume as "box" but with a margin of 1 on all its sides. "b" stands for "bigger" :D

    # Box ranges
    box_range = { key: ( min([cube[i] for cube in cubes]), max([cube[i] for cube in cubes]) ) for i, key in enumerate(["x", "y", "z"]) }

    # BBox range (gives 1 margin for all directions)
    bbox_range = { key: (value[0] - 1, value[1] + 1) for key, value in box_range.items() }

    # Just some utility functions
    def inside_bbox_x(value): return bbox_range["x"][0] <= value <= bbox_range["x"][1]
    def inside_bbox_y(value): return bbox_range["y"][0] <= value <= bbox_range["y"][1]
    def inside_bbox_z(value): return bbox_range["z"][0] <= value <= bbox_range["z"][1]
    def inside_bbox(cube): return inside_bbox_x(cube[0]) and inside_bbox_y(cube[1]) and inside_bbox_z(cube[2])

    # Starting point for analysis
    initial_point = ( bbox_range["x"][0], bbox_range["y"][0], bbox_range["z"][0] )
    points = deque( [(initial_point)] )

    # Search for all the empty spaces on which the water could reach from outside the grid
    water_cubes = set()
    while points:
        point = points.popleft()
        if point in water_cubes: continue
        water_cubes.add(point)
        points.extend([ adj for adj in adjacent_cubes(point) if adj not in cubes and inside_bbox(adj) ])

    # All the other points should be lava cubes
    lava_cubes = set([point for x in range(bbox_range["x"][0], bbox_range["x"][1] + 1) for y in range(bbox_range["y"][0], bbox_range["y"][1] + 1) for z in range(bbox_range["z"][0], bbox_range["z"][1] + 1) if (point := (x, y, z)) not in water_cubes])

    # Same puzzle solving as part I
    surface_area = calculate_surface_area(lava_cubes)

    # Part Two visualization
    print("\n> Part Two <")
    print(f"   The surface are of the scanned lava droplet is {surface_area}.")


if __name__ == "__main__":
    main()
