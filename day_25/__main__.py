def main():
    # Read input file contents
    with open("day_25/input.txt", "r") as file:
        snafu_words = file.read().strip().split("\n")

    # Part One algorithms

    # "Translation" dictionaries
    snafu2dec = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
    dec2snafu = { value: key for key, value in snafu2dec.items() }

    # Convertion functions
    def SNAFU_to_DECIMAL(word):
        if not word: return 0
        return SNAFU_to_DECIMAL(word[:-1]) * 5 + snafu2dec[word[-1]]
    
    def DECIMAL_to_SNAFU(value):
        if not value: return ""
        return DECIMAL_to_SNAFU((value+2)//5) + dec2snafu[(value+2)%5-2]
    
    decimal_result = sum([ SNAFU_to_DECIMAL(word) for word in snafu_words ])
    snafu_result = DECIMAL_to_SNAFU(decimal_result)
    
    # Part One visualization
    print("\n> Part One <")
    print(f"   Decimal result from SNAFU words: {decimal_result}")
    print(f"   Decimal result converted to SNAFU: {snafu_result}")
    
    # Part Two algorithms

    # Part Two visualization
    print("\n> Part Two <")
    
if __name__ == "__main__":
    main()
