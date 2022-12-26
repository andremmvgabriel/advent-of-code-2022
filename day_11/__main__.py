from collections import deque

operations = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b
}

class Monkey(object):
    def __init__(self, data) -> None:
        self._items = deque([ int(item) for item in data[0].split(": ")[1].split(", ") ])
        self._value1, self._operator, self._value2 = data[1].split(" = ")[1].split(" ")
        self._div_value = int(data[2].split(" by ")[1])
        self._who_to_pass = [ int(data[4].split(" ")[-1]), int(data[3].split(" ")[-1]) ]
        self._inspections = 0
    
    @property
    def inspections(self) -> int: return self._inspections

    @property
    def div_value(self) -> int: return self._div_value
    
    def has_items(self) -> bool: return bool(len(self._items))

    def toss_item(self, worry_reducer) -> tuple:
        self._inspections += 1
        item = self._items.pop()

        new_value = operations[self._operator](
            int(self._value1) if self._value1 != "old" else item,
            int(self._value2) if self._value2 != "old" else item
        )

        return (new_value, self._who_to_pass[int(new_value % self._div_value == 0)])
    
    def catch_item(self, item) -> None: self._items.append(item)



def main():
    # Read input file contents
    with open("day_11/input.txt", "r") as file:
        monkeys_data = file.read().split("\n\n")

    # Part One algorithms
    NUMBER_ROUNDS = 20

    # Monkey class for Part 1. This overrides the parent algorithm to toss the item to divide the item worry level by 3.
    class MonkeyPart1(Monkey):
        def toss_item(self, worry_reducer) -> tuple:
            new_value, target = super().toss_item(worry_reducer)
            return (new_value // worry_reducer, target)

    monkeys = [ MonkeyPart1(data.split("\n")[1:]) for data in monkeys_data ]

    for i in range(NUMBER_ROUNDS):
        for j, monkey in enumerate(monkeys):
            while monkey.has_items():
                item, target = monkey.toss_item(3)
                monkeys[target].catch_item(item)

    result = operations["*"](*sorted([monkey.inspections for monkey in monkeys], reverse=True)[:2])
    
    # Part One visualization
    print("\n> Part One <")
    print(f"   The two monkey with the most inspected items achieve the following result: {result}")
    
    # Part Two algorithms
    NUMBER_ROUNDS = 10000

    # Monkey class for Part 1. This overrides the parent algorithm to toss the item to module the item worry level by a value.
    class MonkeyPart2(Monkey):
        def toss_item(self, worry_reducer) -> tuple:
            new_value, target = super().toss_item(worry_reducer)
            return (new_value % worry_reducer, target)

    monkeys = [ MonkeyPart2(data.split("\n")[1:]) for data in monkeys_data ]

    # Calculates the module value of all the monkeys div value.
    # > The resulting value is dividable by each one of the monkeys div value
    # > The item worry level will now be limited to be between [0, (items_mod - 1)]
    items_mod = 1
    for value in [monkey.div_value for monkey in monkeys]: items_mod *= value

    for i in range(NUMBER_ROUNDS):
        for j, monkey in enumerate(monkeys):
            while monkey.has_items():
                item, target = monkey.toss_item(items_mod)
                monkeys[target].catch_item(item)

    result = operations["*"](*sorted([monkey.inspections for monkey in monkeys], reverse=True)[:2])
    
    # Part Two visualization
    print("\n> Part Two <")
    print(f"   The two monkey with the most inspected items achieve the following result: {result}")
    
if __name__ == "__main__":
    main()
