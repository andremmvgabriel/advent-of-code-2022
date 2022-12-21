def print_results(table_title, outcomes, player1_points, player2_points, player1_choices, player2_choices):
    show_results = """
    > {} <
               +---------+---------++---------+---------+---------++---------+---------+---------+
               | Results | Points  ||  Wins   | Losses  |  Draws  ||  Rock   |  Paper  | Scissor |
    +----------+---------+---------++---------+---------+---------++---------+---------+---------+
    | Player 1 |  {:^5}  |  {:^5}  ||  {:^5}  |  {:^5}  |  {:^5}  ||  {:^5}  |  {:^5}  |  {:^5}  |
    +----------+---------+---------++---------+---------+---------++---------+---------+---------+
    | Player 2 |  {:^5}  |  {:^5}  ||  {:^5}  |  {:^5}  |  {:^5}  ||  {:^5}  |  {:^5}  |  {:^5}  |
    +----------+---------+---------++---------+---------+---------++---------+---------+---------+
    """
    print(show_results.format(
        table_title,
        # Player 1
        "win" if player1_points > player2_points else "-", player1_points,
        outcomes.count(1), outcomes.count(2), outcomes.count(0),
        player1_choices.count("A"), player1_choices.count("B"), player1_choices.count("C"),
        # Player 2
        "win" if player1_points < player2_points else "-", player2_points,
        outcomes.count(2), outcomes.count(1), outcomes.count(0),
        player2_choices.count("X"), player2_choices.count("Y"), player2_choices.count("Z")
    ))

def main():
    # Read input file contents
    with open("day_02/input.txt", "r") as file:
        rounds = file.read().split("\n")
        player1_choices = [round.split(" ")[0] for round in rounds]
        player2_choices = [round.split(" ")[1] for round in rounds]
    
    # Relevant variables for both solutions
    choice_scoring = {
        "A": 1, "X": 1, # 1 -> Rock
        "B": 2, "Y": 2, # 2 -> Paper
        "C": 3, "Z": 3  # 3 -> Scissor
    }

    # Part One relevant variables
    round_outcomes = {
        "A X": 0, "B Y": 0, "C Z": 0, # 0 -> Draw
        "A Z": 1, "B X": 1, "C Y": 1, # 1 -> Player 1 wins
        "A Y": 2, "B Z": 2, "C X": 2  # 2 -> Player 2 wins
    }

    # Part One algorithms
    outcomes = [ round_outcomes[round] for round in rounds ]

    player1_points = outcomes.count(1) * 6 + outcomes.count(0) * 3 + sum([choice_scoring[choice] for choice in player1_choices])
    player2_points = outcomes.count(2) * 6 + outcomes.count(0) * 3 + sum([choice_scoring[choice] for choice in player2_choices])
    
    # Part One visualization
    print_results("Part One", outcomes, player1_points, player2_points, player1_choices, player2_choices)

    

    # Part Two relevant variables
    round_outcomes = {
        "A Y": 0, "B Y": 0, "C Y": 0, # 0 -> Draw
        "A X": 1, "B X": 1, "C X": 1, # 1 -> Player 1 wins
        "A Z": 2, "B Z": 2, "C Z": 2  # 2 -> Player 2 wins
    }

    # Part Two algorithms
    outcomes = [ round_outcomes[round] for round in rounds ]

    def find_choice(result, player1_choice):
        player2_win  = {"A": "Y", "B": "Z", "C": "X"}
        player2_draw = {"A": "X", "B": "Y", "C": "Z"}
        player2_lose = {"A": "Z", "B": "X", "C": "Y"}

        if result == 0: return player2_draw[player1_choice]
        if result == 1: return player2_lose[player1_choice]
        if result == 2: return player2_win[player1_choice]

    player2_choices = [ find_choice(result, player1_choice) for result, player1_choice in zip(outcomes, player1_choices) ]

    player1_points = outcomes.count(1) * 6 + outcomes.count(0) * 3 + sum([choice_scoring[choice] for choice in player1_choices])
    player2_points = outcomes.count(2) * 6 + outcomes.count(0) * 3 + sum([choice_scoring[choice] for choice in player2_choices])

    # Part Two visualization
    print_results("Part Two", outcomes, player1_points, player2_points, player1_choices, player2_choices)

if __name__ == "__main__":
    main()
