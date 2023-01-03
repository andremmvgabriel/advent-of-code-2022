from collections import deque

# Movement increments based of orientation
orientation_increment = [
    (1, 0), # Move right
    (0, 1), # Move bottom
    (-1, 0),# Move left
    (0, -1) # Move up
]

# Rotation increments for L (Left) and R (Right)
rotation = { "L": -1, "R": 1 }

# Function to parse the path steps
# > This returns a list as [ int, str, int, (...), int, str, int ]
# > int: These are the amount of steps that has to be done
# > str: These are the orientation rotations
def parse_path(path: str):
    moves = []
    counter = -1
    while True:
        counter += 1
        if len(path) <= counter: break
        if not path[counter].isnumeric():
            moves.append(int(path[:counter]))
            moves.append(path[counter])
            path = path[counter+1:]
            counter = 0
    
    moves.append(int(path))
    return moves

class Board(object):
    def __init__(self, data) -> None:
        self._data = data

    def _move(self, position, orientation):
        # Gets the step increment based on the movement direction & calculates its new position
        increment = orientation_increment[orientation % 4]
        new_position = (
            (position[0] + increment[0]) % len(self._data[0]),
            (position[1] + increment[1]) % len(self._data)
        )

        new_char = self._data[new_position[1]][new_position[0]]

        return (new_position, new_char)

    def follow_path(self, position, orientation, path):
        # Caches the current position and orientation of the movement
        cur_position, cur_orientation = position, orientation

        for step in path:
            if step in ["L","R"]:
                # Rotates the movement
                cur_orientation += rotation[step]
                continue

            # Each step has an amount of movements
            for i in range(step):
                # Increments a movement. Keep incrementing if the movement is going into an empty space
                next_pos = cur_position
                while True:
                    next_pos, next_char = self._move(next_pos, cur_orientation)
                    if next_char != " ": break # Stop incrementing if a valid position was reached
                
                # This is a wall, can't move in such direction!
                # > Stop the rest of the needed movements in the step.
                # > Does not update the current position
                if next_char == "#": break

                # Update the current position
                cur_position = next_pos
        
        return (cur_position, cur_orientation)

class Cube(object):
    # The following are the base patterns of each one of the cube faces
    # > Naming: T(Top), F(Front), R(Right), L(Left), B(Bottom), b(back)
    # > Rotations (degrees): 0 (0 clockwise), 1 (90 clockwise), 2 (180 clockwise), 3 (270 clockwise)
    # > Directions: Top (0, -1), Bottom (0, 1), Right (1, 0), Left (-1, 0) 
    FACES_PATTERNS = {
        "F": { (0, -1): ("T", 0), (1, 0): ("R", 0), (0, 1): ("B", 0), (-1, 0): ("L", 0) },
        "B": { (0, -1): ("F", 0), (1, 0): ("R", 1), (0, 1): ("b", 0), (-1, 0): ("L", 3) },
        "b": { (0, -1): ("B", 0), (1, 0): ("R", 2), (0, 1): ("T", 0), (-1, 0): ("L", 2) },
        "T": { (0, -1): ("b", 0), (1, 0): ("R", 3), (0, 1): ("F", 0), (-1, 0): ("L", 1) },
        "L": { (0, -1): ("T", 3), (1, 0): ("F", 0), (0, 1): ("B", 1), (-1, 0): ("b", 2) },
        "R": { (0, -1): ("T", 1), (1, 0): ("b", 2), (0, 1): ("B", 3), (-1, 0): ("F", 0) }
    }

    def __init__(self, size, data) -> None:
        # Just some verification checks
        if len(data) % size != 0: raise RuntimeError("Invalid cube size for y board size.")
        if len(data[0]) % size != 0: raise RuntimeError("Invalid cube size for x board size.")

        # Caches the input data
        self._size = size
        self._data = data

        # Find where are the cube faces located
        self._locate_cube_faces()
    
    def _rotate_pattern(self, face, rotation):
        # Gets the current face pattern (This is the face pattern at 0, no rotation)
        pattern = Cube.FACES_PATTERNS[face]

        # Caches the current adjacent faces
        adjacent_faces = [ adj for adj in pattern.values() ]

        # QoL function
        # > From each direction i (0 to 3, which is Top, Right, Bottom, Left, respectively), find its adjacent face considering the rotation
        # > (i-rotation) % 4 -> Gives the face position index that should be in a given "i" (directions list) assuming the rotation
        # > adjacent_faces[(i-rotation) % 4][0] -> Gives the face name of the previous face position index
        # > adjacent_faces[(i-rotation) % 4][1] + rotation) % 4 -> Calculates the new rotation of the face
        rotate_adjacent = lambda i, rotation: (adjacent_faces[(i-rotation)%4][0], (adjacent_faces[(i-rotation)%4][1] + rotation)%4)

        # Rotates the adjacent faces to their "new" position
        return { key: rotate_adjacent(i, rotation) for i, key in enumerate(pattern.keys()) }
    
    def crop_face(self, face_info):
        # Calculates the x0, x1, y0, and y1 (on the real board data) that contains the face data
        x0 = self._size * face_info["point"][0]
        x1 = self._size * (face_info["point"][0] + 1)
        y0 = self._size * face_info["point"][1]
        y1 = self._size * (face_info["point"][1] + 1)

        # Crops the data from the board data
        data = [[char for char in line[x0:x1]] for line in self._data[y0:y1]]

        # Also caches the real board position of each one of the data characters
        # > Each face has its own referential from 0 to square size
        # > We need to keep track of the real position of each of the data characters
        real_positions = [[(self._size*face_info["point"][0] + i, self._size*face_info["point"][1] + j) for i in range(len(data[0]))] for j in range(len(data)) ]

        return { "rotation": face_info["rotation"], "data": data, "real_positions": real_positions, }

    def _locate_cube_faces(self):
        # Creates the smallest version possible of the cube, where can only exist empty spaces or "."
        simplified_cube = [ [ char if char != "#" else "." for i, char in enumerate(line) if i % self._size == 0 ] for j, line in enumerate(self._data) if j % self._size == 0 ]

        # The first face to be found will always be the F face with no rotation
        # > Finds the position of the F face
        F_face = { "rotation": 0, "point": (simplified_cube[0].index("."), 0) }

        # This will cache all the found faces along the search
        # > F face is already found
        found_faces = { "F": F_face }

        # As the faces are being found, it is needed to search for their adjacent faces
        next_to_check = deque([("F", F_face)])

        # Searching...
        while next_to_check:
            # Current face being analysed
            face, face_info = next_to_check.popleft()

            # Rotates its base pattern (depending on the face info rotation on which was found)
            pattern = self._rotate_pattern( face, face_info["rotation"] )

            # Searches all directions
            for direction in [ (0, -1), (1, 0), (0, 1), (-1, 0) ]:
                # Exits the current direction if the search is going our of bounds/limits
                if face_info["point"][0] + direction[0] < 0 or face_info["point"][0] + direction[0] >= len(simplified_cube[0]): continue
                if face_info["point"][1] + direction[1] < 0 or face_info["point"][1] + direction[1] >= len(simplified_cube): continue

                # Exits if the current direction has an empty character (no face found)
                if simplified_cube[face_info["point"][1] + direction[1]][face_info["point"][0] + direction[0]] == " ": continue

                # Gets the face name and its rotation for the current direction search
                dir_face, dir_face_rotation = pattern[direction]

                # Exits if the found face was previously found
                if dir_face in found_faces: continue

                # Caches the found face and adds it to the next face to check
                dir_face_info = { "rotation": dir_face_rotation, "point": (face_info["point"][0] + direction[0], face_info["point"][1] + direction[1]), }
                found_faces[dir_face] = dir_face_info
                next_to_check.append( (dir_face, dir_face_info) )

        # Cuts and caches each one of the found cube faces
        self._faces = {
            "F": self.crop_face(found_faces["F"]),
            "b": self.crop_face(found_faces["b"]),
            "R": self.crop_face(found_faces["R"]),
            "L": self.crop_face(found_faces["L"]),
            "T": self.crop_face(found_faces["T"]),
            "B": self.crop_face(found_faces["B"])
        }

    def _move(self, position, orientation, face):
        # Gets the step increment based on the movement direction & calculates its new position
        increment = orientation_increment[orientation % 4]
        position = ( (position[0] + increment[0]), (position[1] + increment[1]) ) # This can go out-of-bounds

        # The movement went to another face!
        if not 0 <= position[0] < self._size or not 0 <= position[1] < self._size:
            # The following is based on the face where the movement is coming from, and the expected face on which the movement will be
            # > Expected face: face (and its rotation) that is expected to be adjacent on the current face in the movement direction
            # > Target face: same face as expected, but this is what is cached in the cube faces that was found in the faces search. It can have different rotation than expected.
            expected_face = self._rotate_pattern(face, self._faces[face]["rotation"])[increment]
            target_face = (expected_face[0], self._faces[expected_face[0]]["rotation"])

            # Calculates the rotation delta between the target Vs expected
            delta_orientation = target_face[1] - expected_face[1]
            mod_delta_orientation = (delta_orientation + 4) % 4 # Module of the delta

            # Makes the rotation of the point
            # > Rotation of any point (relative to a (0,0) origin)
            # > Rotation: (x', y') = (x.cos(teta) - y.sin(teta), x.sin(teta) + y.cos(teta))
            #   > Teta is always 90 degrees for each rotation
            #   > Rotation: (x', y') = (-y, x)
            # > Since the origin of all the faces is located at top left corner (0,0):
            #   > A point translation is needed to reposition the origin at the center of the face
            #   > Apply the rotation
            #   > Apply an inverted translation to reposition the origin at its expected point (top left)
            position = (position[0] - float(self._size - 1) / 2, position[1] - float(self._size - 1) / 2)
            for i in range(mod_delta_orientation):
                position = (-position[1], position[0])
            position = (int(position[0] + float(self._size - 1) / 2), int(position[1] + float(self._size - 1) / 2))
            
            # Swaps the face on which the next movement will occur on
            face = target_face[0]

            # Updates the movement orientation based on the face swap
            orientation = (orientation + delta_orientation) % 4
        
        # Modulates the position and orientation
        position = ( position[0] % self._size, position[1] % self._size )
        orientation = (orientation + 4) % 4

        char = self._faces[face]["data"][position[1]][position[0]]
        
        return (position, char, face, orientation)
    
    def _get_real_point(self, face_pos, face):
        # Returns the face point position in the whole board data
        return self._faces[face]["real_positions"][face_pos[1]][face_pos[0]]

    def follow_path(self, orientation, path):
        # Caches the current position, orientation, and face of the movement
        cur_position, cur_orientation, cur_face = (0, 0), orientation, "F" # Always start at Front face in its (0, 0) position

        for step in path:
            if step in ["L","R"]:
                # Rotates the movement
                cur_orientation += rotation[step]
                continue

            # Each step has an amount of movements
            for i in range(step):
                # Increments a movement
                next_pos, next_char, next_face, next_orientation = self._move(cur_position, cur_orientation, cur_face)

                # This is a wall, can't move in such direction!
                # > Stop the rest of the needed movements in the step.
                # > Does not update the current position, orientation, and face
                if next_char == "#": break

                # Updates the current position, orientation, and face
                cur_position, cur_orientation, cur_face = next_pos, next_orientation, next_face
        
        return (self._get_real_point(cur_position, cur_face), cur_orientation)



def main():
    # Read input file contents
    with open("day_22/input.txt", "r") as file:
        board, path = file.read().split("\n\n")
        board_grid = [[char for char in line] for line in board.split("\n")]
        
        # Adds empty spaces to the lines that do not have the needed length
        max_line = max(len(line) for line in board_grid)
        for i in range(len(board_grid)):
            while len(board_grid[i]) < max_line:
                board_grid[i].append(" ")

        path_steps = tuple(parse_path(path))
    
    # Part One algorithms
    START_POINT = (board_grid[0].index("."), 0)
    START_ORIEN = 0

    board = Board(board_grid)
    final_point, final_orien = board.follow_path(START_POINT, START_ORIEN, path_steps)
    
    result = 1000 * (final_point[1]+1) + 4 * (final_point[0]+1) + (final_orien % 4)

    # Part One visualization
    print("\n> Part One <")
    print(f"   The final password is: {result}")
    
    # Part Two algorithms
    CUBE_SIZE = 50
    START_ORIEN = 0

    cube = Cube(CUBE_SIZE, board_grid)
    final_point, final_orien = cube.follow_path(START_ORIEN, path_steps)

    result = 1000 * (final_point[1]+1) + 4 * (final_point[0]+1) + (final_orien % 4)

    # Part Two visualization
    print("\n> Part Two <")
    print(f"   The final password is: {result}")
    
if __name__ == "__main__":
    main()
