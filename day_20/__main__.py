def mix_data(data, sequence):
    for value in sequence:
        # Gets its previous position in the sequence
        old_index = data.index(value)

        # Removes the value from the sequence
        data.remove(value)

        # Calculates its new index position
        new_index = (old_index + value[1]) % len(data)

        # Adds the value to its new position
        data.insert(new_index, value)
    
    return data

def grove_coords(data, number):
    num_pos = data.index(number)
    return [ data[(num_pos + i) % len(data)][1] for i in [1000, 2000, 3000] ]



def main():
    # Read input file contents
    with open("day_20/input.txt", "r") as file:
        original_data = [int(value) for value in file.read().split("\n")]

    # Part One algorithms
    encrypted_data = [value for value in enumerate(original_data)] # Needed due to multiple occurrence of the same value
    sequence = encrypted_data.copy()
    zero = (original_data.index(0), 0)

    # Mixing and final result
    encrypted_data = mix_data(encrypted_data, sequence)
    result = sum( grove_coords(encrypted_data, zero) )

    # Part One visualization
    print("\n> Part One <")
    print(f"   The 1000th, 2000th and 3000th position values after the 0 value occurrence give a total of {result} summed.")
    


    # Part Two algorithms
    DECRYPTION_KEY = 811589153
    NUMBER_ROUNDS = 10

    encrypted_data = [ (i, value * DECRYPTION_KEY) for i, value in enumerate(original_data) ]
    sequence = encrypted_data.copy()
    zero = (original_data.index(0), 0)

    # Mixing and final result
    for _ in range(NUMBER_ROUNDS):
        encrypted_data = mix_data(encrypted_data, sequence)
    result = sum( grove_coords(encrypted_data, zero) )

    # # Part Two visualization
    print("\n> Part Two <")
    print(f"   The 1000th, 2000th and 3000th position values after the 0 value occurrence give a total of {result} summed.")

if __name__ == "__main__":
    main()
