def main():
    # Read input file contents
    with open("day_06/input.txt", "r") as file:
        buffer = file.read()
    
    # Relevant variables for both parts
    unique_chars = set()
    received_signal = ""

    # Part One algorithms
    packet_marker = ""
    packet_marker_start = 0

    # The instructions say "receive one at a time". As so, the buffer will be iterated
    for i, character in enumerate(buffer):
        received_signal += character
        if character in unique_chars:
            last_4 = received_signal[-4:]
            if len(set(last_4)) == 4:
                packet_marker = last_4
                packet_marker_start = i + 1
                break
        unique_chars.add(character)

    # Part One visualization
    print("\n> Part One <")
    print(f"   Found packet marker after receiving character {packet_marker_start}! Result: {packet_marker}")

    # Part Two algorithms
    message_marker = ""
    message_marker_start = 0

    # The instructions say "receive one at a time". As so, the buffer will be iterated
    for i, character in enumerate(buffer[packet_marker_start:]): # No way the message marker is achieved without achieving the packet marker. As so, lets start iterate from the packet marker character.
        received_signal += character
        if character in unique_chars:
            last_14 = received_signal[-14:]
            if len(set(last_14)) == 14:
                message_marker = last_14
                message_marker_start = i + packet_marker_start + 1
                break
        unique_chars.add(character)
    
    # Part Two visualization
    print("\n> Part Two <")
    print(f"   Found message marker after receiving character {message_marker_start}! Result: {message_marker}")

if __name__ == "__main__":
    main()
