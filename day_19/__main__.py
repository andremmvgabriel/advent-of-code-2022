def scenario_next_minute_outcomes(scenario, blueprint):
    # Current scenario amount of rocks and robots
    rocks = scenario[0]
    robots = scenario[1]

    # Actual possible scenarios of outcome
    # > This already caches the possibility of not buying any robot (just extracts the rocks)
    outcomes = [(
        tuple([ have + extracted for have, extracted in zip(rocks, robots) ]),
        tuple([ robot_amount for robot_amount in robots ])
    )]

    for i, robot_cost in enumerate(blueprint[::-1]):
        can_buy_robot = all( [ have >= needed for have, needed in zip(rocks, robot_cost) ] )
        if can_buy_robot:
            # Calculates the new rocks amount for the current outcome
            # > Decreases the amount of rocks that the robot costs
            # > Already increases the amount of rocks extracted by the current robots
            new_rocks_amount = tuple([ have - needed + extracted for have, needed, extracted in zip(rocks, robot_cost, robots) ])
            
            # Updates the amount of robots
            new_robots_amount = tuple([ (have+1) if i==j else have for j, have in enumerate(robots) ])

            # Caches the possible outcome
            outcomes.append( (new_rocks_amount, new_robots_amount) )
    
    return outcomes

def filter_outcomes(scenarios, minute):
    # Just for better understanding, these will be presented individually
    # > Rocks/scenario -> Amount of rocks in each possible scenario
    # > Robots/scenario -> Amount of robots in each possible scenario
    # > Both/scenario -> Amount of rocks + amount or robots in each possible scenario
    rocks_per_scenario = [ scenario[0] for scenario in scenarios ]
    robots_per_scenario = [ scenario[1] for scenario in scenarios ]
    both_per_scenario = [ tuple([x+y for x, y in zip(scenario[0], scenario[1])]) for scenario in scenarios ]

    # The best possible scenarios to have the more extraction are those who have not only the most amount of rocks but also the most robots to target the extraction of the best rocks
    # > Rocks importance: Geode > Obsidian > Clay > Ore
    # > Robots importance: Geode > Obsidian > Clay > Ore
    # > The sorting of best possible scenario will happen as following:
    #   > Sorts by the scenarios which have the most rocks and robots for the most important rocks
    #   > If previous is not enough (a lot of other scenarios with similar amounts), sort these scenarios by those who have the bigger amount of the most important rocks
    #   > If previous is still not enough, sort these scenarios by those who have the bigger amount of robots that target the most important rocks (This does not make sense unless in a scenario some robots appeared by magic).
    # The best way to sort as previous is to make use of Python tuples list sorting. So lets just add these together in a big tuple
    scenarios_big_tuples = [ both + rocks + robots for both, rocks, robots in zip(both_per_scenario, rocks_per_scenario, robots_per_scenario) ]
    sorted_data = sorted(scenarios_big_tuples, reverse=True)[:(minute+1)*75] # This adds 75 more best scenarios by each minute this goes on

    # Recreates the scenarios as a set.
    return set([ (data[4:8], data[8:12]) for data in sorted_data ])

def simulate_blueprint(blueprint, simulation_time):
    initial_inventory = (
        (0,0,0,0),  # Rocks inventory. No rocks
        (0,0,0,1)   # Robots inventory. Ore Robot extractor
    )

    # All generated scenarios in each minute will be added here
    scenarios = set([initial_inventory])

    for minute in range(simulation_time):
        next_scenarios = set()
        for scenario in scenarios:
            next_scenarios.update( scenario_next_minute_outcomes(scenario, blueprint) )

        scenarios = filter_outcomes(next_scenarios, minute)

    return max( [scenario[0][0] for scenario in scenarios] )



def main():
    # Read input file contents
    with open("day_19/input.txt", "r") as file:
        numbers_list = [[int(part) for part in line.replace(":","").split(" ") if part.isnumeric()] for line in file.read().split("\n")]
        blueprints = [ [
            (0,0,0,costs[0]),           # Ore Robot costs
            (0,0,0,costs[1]),           # Clay Robot costs
            (0,0,costs[3],costs[2]),    # Obsidian Robot costs
            (0,costs[5],0,costs[4])     # Geode Robot costs
        ] for id, *costs in numbers_list ]

    # Part One algorithms
    NUMBER_MINUTES = 24

    best_extractions = []
    for id, blueprint in enumerate(blueprints):
        best_extractions.append(simulate_blueprint(blueprint, NUMBER_MINUTES))
    
    result = sum([value * (i+1) for i, value in enumerate(best_extractions)])
    
    # Part One visualization
    print("\n> Part One <")
    print(f"   The total of the best Geode extractions by each blueprint is {result}!")
    print(f"   Individual blueprint results: {best_extractions}")
    
    # Part Two algorithms
    NUMBER_MINUTES = 32

    best_extractions = []
    result = 1
    for id, blueprint in enumerate(blueprints[:3]):
        value = simulate_blueprint(blueprint, NUMBER_MINUTES)
        best_extractions.append(value)
        result *= value

    # Part Two visualization
    print("\n> Part Two <")
    print(f"   The total of the best Geode extractions by each blueprint is {result}!")
    print(f"   Individual blueprint results: {best_extractions}")
    
if __name__ == "__main__":
    main()
