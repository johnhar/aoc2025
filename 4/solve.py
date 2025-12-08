import sys
import time
from copy import copy


def method_1(floor: list[list[str]]) -> int:
    count_movable_rolls = 0

    def count_surrounding_rolls(ri, ci) -> int:
        count = 0
        for r in range(ri - 1, ri + 1 + 1):
            # make sure the coordinates are within the map
            if not (0 <= r < len(floor)):
                continue
            for c in range(ci - 1, ci + 1 + 1):
                # make sure the coordinates are within the map
                if not (0 <= c < len(floor[0])):
                    continue
                # make sure not to count the current space
                if r == ri and c == ci:
                    continue
                if floor[r][c] != '.':
                    count += 1
        return count

    # iterate through the floor map, checking for movable rolls
    row_len = len(floor[0])
    for ri in range(len(floor)):
        for ci in range(row_len):
            # if there is a roll at this space, check if it's movable
            if floor[ri][ci] != '.':
                count = count_surrounding_rolls(ri, ci)
                if count < 4:
                    floor[ri][ci] = 'x'
                    count_movable_rolls += 1
    return count_movable_rolls


# part 2
def method_2(floor: list[list[str]]) -> int:
    count_removable_rolls = 0

    # iterate through the floor map, checking for and removing movable rolls
    while True:
        # use method 1 for each pass
        count_movable_rolls = method_1(floor)
        if count_movable_rolls == 0:
            break
        print_floor(floor, f"Remove {count_movable_rolls} rolls of paper:")
        count_removable_rolls += count_movable_rolls
        # now remove them from the floor map
        for ri in range(len(floor)):
            for ci in range(len(floor[0])):
                if floor[ri][ci] == 'x':
                    floor[ri][ci] = '.'
    return count_removable_rolls


def print_floor(floor: list[list[str]], title: str = "") -> None:
    print(title)
    for line in floor:
        print("".join(line))
    print("")


def process_file(filename):
    """
    Read and process lines from a text file.
    Args:
        filename (str): Path to the text file
    """
    floor_map: list[list[str]] = []
    try:
        with open(filename, 'r') as file:
            total_joltage = 0
            line_count = 0
            for line in file:
                # Process each line (example: print stripped line)
                processed_line = line.strip()
                floor_map.append([c for c in processed_line])
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

    print_floor(floor_map, "Initial floor map")

    start_time = time.time()
    method_fcn = getattr(sys.modules[__name__], f"method_{method}")
    count_movable_rolls = method_fcn(floor_map)
    end_time = time.time()

    print_floor(floor_map, "Final floor map")
    floor_size = len(floor_map) * len(floor_map[0])
    print(f"{count_movable_rolls} rolls of {floor_size}")
    print(f"Elapsed time {end_time - start_time:.6f} seconds, {floor_size / (end_time - start_time):.6f} spaces/second")
    return


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python solve.py <input_file> <method>")
        sys.exit(1)
    file_path = sys.argv[1]
    method = sys.argv[2]
    process_file(file_path)
