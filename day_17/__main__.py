class Rock(object):
    TYPES = {
        0: [(0,0), (1,0), (2,0), (3,0)],
        1: [(1,0), (0,1), (1,1), (2,1), (1,2)],
        2: [(0,0), (1,0), (2,0), (2,1), (2,2)],
        3: [(0,0), (0,1), (0,2), (0,3)],
        4: [(0,0), (1,0), (0,1), (1,1)]
    }

    def __init__(self, rock_type, spawn_position):
        self._rest = False
        self._blocks = set([ (coord[0] + spawn_position[0], coord[1] + spawn_position[1]) for coord in Rock.TYPES[rock_type] ])
    
    def _move(self, increment):
        self._blocks = set([ (block[0] + increment[0],block[1] + increment[1]) for block in self._blocks ])

    def move(self, increment, obstacles):
        # test = [ True if (block[0] + increment[0], block[1] + increment[1]) not in obstacles else False for block in self._blocks ]
        can_move = all([ True if (block[0] + increment[0], block[1] + increment[1]) not in obstacles else False for block in self._blocks ])
        if can_move: self._move(increment)
        return can_move

    def fall(self, obstacles):
        can_move = self.move( (0, -1), obstacles )
        if not can_move: self._rest = True

    @property
    def rest(self): return self._rest

    @property
    def height(self): return max([y for _, y in self._blocks])

    @property
    def blocks(self): return self._blocks

class Tower(object):
    JETS = { "<": (-1, 0), ">": (1, 0) }
    SPAWN_OFFSETS = (3, 4)

    class PatternFinder(object):
        def __init__(self) -> None:
            self._registry = {}
            self._found = False
            self._pattern = None
        
        def add_state(self, state, state_height, state_rocks):
            if self._found: return # We dont care about adding more states if pattern already found

            if state not in self._registry:
                self._registry[state] = [(state_height, state_rocks)]
            else:
                self._registry[state].append((state_height, state_rocks))
            
            # We need a 3rd repetition of the state before flagging as pattern found
            # > To calculate an accurate pattern height we need to see the height difference in an actual pattern repetion.
            # > This "real" pattern repetition only occurs upon the 3rd repetition of the state.
            if len(self._registry[state]) == 3:
                self._pattern = self._registry[state]
                self._found = True
        
        def get_pattern(self):
            return ( self._pattern[2][0]-self._pattern[1][0], self._pattern[2][1]-self._pattern[1][1] )
        
        def calculate_repetitions(self, number_rocks):
            return (number_rocks - self._pattern[2][1]) // self.get_pattern()[1]
        
        @property
        def found(self): return self._found

    def __init__(self, width, jets_pattern) -> None:
        self._height = 0
        self._width = width
        self._jets = jets_pattern
        self._blocks = set([(i,0) for i in range(self._width)])
    
    def _spawn_position(self):
        return (Tower.SPAWN_OFFSETS[0], Tower.SPAWN_OFFSETS[1] + self._height)

    def drop_rocks(self, number_rocks):
        pattern_used = False
        pattern_finder = Tower.PatternFinder()

        rocks_counter = 0
        moves_counter = 0
        while rocks_counter < number_rocks:
            if not pattern_used:
                # Calculates the current iteration state and sends it to the pattern finder
                state = (rocks_counter % len(Rock.TYPES), moves_counter % len(self._jets))
                pattern_finder.add_state(state, self._height, rocks_counter)

                if pattern_finder.found:
                    # Gets the pattern height and the pattern amount of rocks
                    delta_height, delta_rocks = pattern_finder.get_pattern()

                    # Calculates how many times can the pattern still repeat
                    repetitions = pattern_finder.calculate_repetitions(number_rocks)

                    if repetitions > 0:
                        # Updates the rocks counter and the tower height up to the last pattern repetition
                        rocks_counter += delta_rocks * repetitions
                        self._height += delta_height * repetitions

                        # Updates the tower blocks to match the updated tower height
                        # >   This does not add all the placed blocks so far. It just shifts all the current placed blocks all
                        #   the way up to the new height instead.
                        self._blocks = set([(x, y + delta_height*repetitions) for x,y in self._blocks])
                    
                    # Updates the control flag of the pattern usage. It proceeds to continue to the next while cycle.
                    # > This is needed due to the fact that the last deployed rock from the pattern could be last allowed rock to be dropped.
                    pattern_used = True
                    continue
            
            # Deploy rock
            rock = Rock( rocks_counter % len(Rock.TYPES), self._spawn_position() )

            # Increases the height of the tower walls
            self._blocks.update([ (0, i+1) for i in range(self._height, rock.height) ])
            self._blocks.update([ (self._width-1, i+1) for i in range(self._height, rock.height) ])

            # Move the rock until it reaches a rest position
            while not rock.rest:
                # Current jet direction
                jet = self._jets[moves_counter % len(self._jets)]
                moves_counter += 1

                # Move the rock by jet direction
                rock.move(Tower.JETS[jet], self._blocks)

                # Move the rock by gravity
                rock.fall(self._blocks)

            # Updates the tower height and tower blocks
            self._height = max(self._height, rock.height)
            self._blocks.update(rock.blocks)
            rocks_counter += 1 

    @property
    def height(self): return self._height



def main():
    # Read input file contents
    with open("day_17/input.txt", "r") as file:
        jets = file.read().strip()

    # Part One algorithms
    NUMBER_ROCKS = 2022

    tower = Tower(9, jets)
    tower.drop_rocks(NUMBER_ROCKS)

    # Part One visualization
    print("\n> Part One <")
    print(f"   After {NUMBER_ROCKS} dropped, the tower has {tower.height} of height.")
    
    # Part Two algorithms
    NUMBER_ROCKS = 1000000000000
    
    tower2 = Tower(9, jets)
    tower2.drop_rocks(NUMBER_ROCKS)

    # # Part Two visualization
    print("\n> Part Two <")
    print(f"   After {NUMBER_ROCKS} dropped, the tower has {tower2.height} of height.")


    
if __name__ == "__main__":
    main()
