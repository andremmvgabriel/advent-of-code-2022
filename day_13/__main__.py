from functools import cmp_to_key

def main():
    # Read input file contents
    with open("day_13/input.txt", "r") as file:
        data = file.read()
        packet_pairs = [ packet.split("\n") for packet in data.split("\n\n") ]
        packets = [ eval(packet) for packet in data.split("\n") if packet != "" ]
    
    # Relevant for both parts
    def compare(left, right):
        # Compare the left and right values if both are integers
        if type(left) == type(right) == int:
            return (left > right) - (left < right)
        
        # Compare the left and right values if both are lists
        if type(left) == type(right) == list:
            # Recursively compare the list values as long as there are values to be compared
            if len(left) and len(right):
                result = compare(left[0], right[0])
                return result if result else compare(left[1:], right[1:])

            # Compare which list is empty
            return compare(len(left), len(right))
        
        # If one of the values is not a list, put it as so and compare again
        return compare(left if type(left) == list else [left], right if type(right) == list else [right])

    # Part One algorithms
    results = [ (i+1) if compare(eval(pair[0]), eval(pair[1])) == -1 else 0 for i, pair in enumerate(packet_pairs) ]

    # Part One visualization
    print("\n> Part One <")
    print(f"   There are {len(results) - results.count(0)} incorrect packets, making a total sum value of {sum(results)}.")

    # Part Two algorithms
    packets += [[[2]]] + [[[6]]]
    packets = sorted(packets, key=cmp_to_key(compare))

    # Part Two visualization
    print("\n> Part Two <")
    print(f"    The multiplication between the [[2]] and [[6]] indexes is {(packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)}.")
    print(f"     > [[2]] position: {packets.index([[2]]) + 1}")
    print(f"     > [[6]] position: {packets.index([[6]]) + 1}")


if __name__ == "__main__":
    main()
