def main():
    # Read input file contents
    with open("day_08/input.txt", "r") as file:
        rows = file.read().split("\n")
    
    cols = ["" for i in range(len(rows[0]))]
    for i, row in enumerate(rows):
        for j, char in enumerate(row):
            cols[j] += char
    
    # Part One algorithms
    visible_trees = set()

    # Rows check!
    for i, row in enumerate(rows):
        highest_tree = max(row)

        # Viewing from left to right
        left_visible_trees_heights = set( [ max(row[:j+1]) for j in range(row.index(highest_tree)+1) ] )
        left_visible_trees = [ f"{i},{row.index(height)}" for height in left_visible_trees_heights ]

        # Viewing from right to left
        right_visible_trees_heights = set( [ max(row[::-1][:j+1]) for j in range(row[::-1].index(highest_tree)+1) ] )
        right_visible_trees = [ f"{i},{len(row) - row[::-1].index(height) - 1}" for height in right_visible_trees_heights ]

        # Updates the set of visible trees coordinates
        visible_trees.update(left_visible_trees)
        visible_trees.update(right_visible_trees)

    # Columns check!    
    for i, col in enumerate(cols):
        highest_tree = max(col)

        # Viewing from top to bottom
        top_visible_trees_height = set( [ max(col[:j+1]) for j in range(col.index(highest_tree)+1) ] )
        top_visible_trees = [ f"{col.index(height)},{i}" for height in top_visible_trees_height ]

        # Viewing from bottom to top
        bottom_visible_trees_heights = set( [ max(col[::-1][:j+1]) for j in range(col[::-1].index(highest_tree)+1) ] )
        bottom_visible_trees = [ f"{len(col) - col[::-1].index(height) - 1},{i}" for height in bottom_visible_trees_heights ]

        # Updates the set of visible trees coordinates
        visible_trees.update(top_visible_trees)
        visible_trees.update(bottom_visible_trees)
    
    # Part One visualization
    print("\n> Part One <")
    print(f"   There are {len(visible_trees)} visible trees within the tree grid.")

    # Part Two algorithms
    scenic_scores = {}

    # Rows check!
    for i, row in enumerate(rows):
        for j, tree in enumerate(row):
            # Looking to the left
            left_visible_trees = [ True if tree > other else False for other in row[:j] ]
            left_visible_trees_counter = (left_visible_trees[::-1].index(False) + 1) if left_visible_trees.count(False) else (len(left_visible_trees) if left_visible_trees else 0)

            # Looking to the right
            right_visible_trees = [ True if tree > other else False for other in row[j+1:] ]
            right_visible_trees_counter = (right_visible_trees.index(False) + 1) if right_visible_trees.count(False) else (len(right_visible_trees) if right_visible_trees else 0)

            # Registers the scenic score of the tree
            scenic_scores[f"{i},{j}"] = left_visible_trees_counter * right_visible_trees_counter

    # Cols checks!
    for i, col in enumerate(cols):
        for j, tree in enumerate(col):
            # Looking to the top
            top_visible_trees = [ True if tree > other else False for other in col[:j] ]
            top_visible_trees_counter = (top_visible_trees[::-1].index(False) + 1) if top_visible_trees.count(False) else (len(top_visible_trees) if top_visible_trees else 0)

            # Looking to the bottom
            bottom_visible_trees = [ True if tree > other else False for other in col[j+1:] ]
            bottom_visible_trees_counter = (bottom_visible_trees.index(False) + 1) if bottom_visible_trees.count(False) else (len(bottom_visible_trees) if bottom_visible_trees else 0)

            # Updates the scenic score of the tree
            scenic_scores[f"{j},{i}"] *= top_visible_trees_counter * bottom_visible_trees_counter

    # Result
    scenic_score, best_tree = max(zip(scenic_scores.values(), scenic_scores.keys()))

    # Part Two visualization
    print("\n> Part Two <")
    print(f"   The tree with the best scenic score is located at {best_tree} with a score of {scenic_score}!")

if __name__ == "__main__":
    main()
