class Beacon(object):
    def __init__(self, data: str):
        self._location = eval(data[23:data.index(",")+1] + data[data.index(",")+4:])
    
    @property
    def location(self) -> tuple: return self._location

class Sensor(Beacon):
    def __init__(self, data: str, beacon: Beacon):
        self._location = eval(data[12:data.index(",")+1] + data[data.index(",")+4:])
        self._beacon = beacon
        self._range_x_lims, self._range_y_lims = self._discover_range()

    @property
    def beacon(self): return self._beacon

    @property
    def range_x_lims(self): return self._range_x_lims

    @property
    def range_y_lims(self): return self._range_y_lims

    def _discover_range(self):
        # Calculates the x and y differences between the sensor and its respective beacon
        delta_x = abs(self.location[0] - self._beacon.location[0])
        delta_y = abs(self.location[1] - self._beacon.location[1])

        # Calculates the x and y ranges
        range_x_lims = [ self.location[0] - delta_x - delta_y, self.location[0] + delta_x + delta_y ]
        range_y_lims = [ self.location[1] - delta_x - delta_y, self.location[1] + delta_x + delta_y ]

        return (range_x_lims, range_y_lims)
    
    def get_range_in_row(self, row: int):
        if self._range_y_lims[0] > row or row > self._range_y_lims[1]: return []

        length = self._range_y_lims[1] - row if self.location[1] < row else row - self._range_y_lims[0]

        return [self.location[0] - length, self.location[0] + length]


def main():
    # Read input file contents
    with open("day_15/input.txt", "r") as file:
        data = [ [pair for pair in line.split(": ")] for line in file.read().split("\n") ]
        beacons = [ Beacon(beacon) for _, beacon in data ]
        sensors = [ Sensor(sensor, beacon) for (sensor, _), beacon in zip(data, beacons) ]

    # Part One algorithms
    TARGET_ROW = 2000000

    # The covered positions for the target row (actual output)
    target_row_range = set()

    # Searches and adds the range of all the sensors in the target row
    for _, sensor in enumerate(sensors):
        row_range = sensor.get_range_in_row(TARGET_ROW)
        if not row_range: continue
        target_row_range.update([val for val in range(row_range[0],row_range[1] + 1)])

    # Removes the beacons that are in the target row that are already contain in the range
    target_row_range.difference_update([beacon.location[0] for beacon in beacons if beacon.location[1] == TARGET_ROW])

    # Part One visualization
    print("\n> Part One <")
    print(f"   In the row {TARGET_ROW} there are {len(target_row_range)} positions that cannot contain a beacon.")



    # Part Two algorithms
    SCAN_LIMITS = [0, 4000000]

    for y in range(SCAN_LIMITS[0], SCAN_LIMITS[1] + 1):
        line_ranges = []

        # Gets all the ranges of the sensors for the y row
        for sensor in sensors:
            if not (range_x := sensor.get_range_in_row(y)): continue
            if range_x[0] > SCAN_LIMITS[1]: continue
            if range_x[1] < SCAN_LIMITS[0]: continue
            if range_x[0] < SCAN_LIMITS[0]: range_x[0] = SCAN_LIMITS[0]
            if range_x[1] > SCAN_LIMITS[1]: range_x[1] = SCAN_LIMITS[1]
            line_ranges.append(range_x)

        line_ranges = sorted( line_ranges , key=lambda x: x[0])

        # Searches for a gap in the ranges
        ria = line_ranges[0]
        has_gap = False
        for j in range(len(line_ranges) - 1):
            cur_range = line_ranges[j+1]
            if ria[1] < cur_range[0]: has_gap = True; break
            if ria[1] < cur_range[1]: ria = cur_range
        
        # Saves the target point
        if has_gap: target_point = (ria[1] + 1, y); break

    # Part Two visualization
    print("\n> Part Two <")
    print(f"   The only position available is: {target_point}.")
    print(f"   Result = x * 4000000 + y = {target_point[0] * 4000000 + target_point[1]}")
    
if __name__ == "__main__":
    main()
