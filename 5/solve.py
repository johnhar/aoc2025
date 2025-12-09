import sys
import time
from copy import copy, deepcopy


def method_1(fresh_list: list[list[int]], available_ingredients: list[int]) -> int:
    count = 0

    # iterate through the list of available ingredients
    for ingredient in available_ingredients:
        for fresh_range in fresh_list:
            if fresh_range[0] <= ingredient <= fresh_range[1]:
                count += 1
                break

    return count


# part 2: this is the straight forward approach, but it's slow.
def method_2(fresh_list: list[list[int]], available_ingredients: list[int]) -> int:
    count = 0

    # this time, we're only counting how many ingredients are in the fresh ranges, deduping for overlaps.
    fresh_set = set()
    for fresh_range in fresh_list:
        fresh_set.update(range(fresh_range[0], fresh_range[1] + 1))

    return len(fresh_set)


# faster method
def method_3(fresh_list: list[list[int]], available_ingredients: list[int]) -> int:
    count = 0

    # create a sorted copy of the fresh list, so we can merge ranges
    fresh_list = deepcopy(fresh_list)
    fresh_list.sort(key=lambda x: x[0])

    # repeatedly try merging adjacent ranges until there are no more merges possible
    i = 0
    while i < len(fresh_list) - 1:
        curr_range = fresh_list[i]
        next_range = fresh_list[i + 1]
        print(f"i {i}: current range {curr_range}, next range {next_range}")
        # current and next ranges overlap
        if curr_range[1] >= next_range[0]:
            # merge them
            fresh_list[i] = [min(curr_range[0], next_range[0]), max(curr_range[1], next_range[1])]
            del fresh_list[i + 1]
            print(f"    merged {fresh_list[i]}")
            # keep i at the same place, since we updated it and need to check the next range (after the deleted range)
            continue

        # current and next ranges don't overlap, so check the next pair
        else:
            i += 1

    # fresh_list is now non-overlapping and sorted ranges.  Count the number of ingredients in the fresh ranges.
    print(f"Final list: {fresh_list}")
    count = sum([r[1] - r[0] + 1 for r in fresh_list])

    return count


def process_file(filename):
    """
    Read and process lines from a text file.
    Args:
        filename (str): Path to the text file
    """
    fresh_list = []
    available_ingredients = []
    try:
        with open(filename, 'r') as file:
            parsing = 'fresh'
            for line in file:
                # Process each line (example: print stripped line)
                processed_line = line.strip()
                if processed_line == "":
                    parsing = 'available'
                    continue

                if parsing == 'fresh':
                    fresh_range = processed_line.split('-')
                    print(fresh_range)
                    fresh_list.append([int(fresh_range[0]), int(fresh_range[1])])
                else:
                    available_ingredients.append(int(processed_line))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

    start_time = time.time()
    method_fcn = getattr(sys.modules[__name__], f"method_{method}")
    count_fresh = method_fcn(fresh_list, available_ingredients)
    end_time = time.time()

    print(f"Count of fresh ingredients: {count_fresh}")
    print(
        f"Elapsed time {end_time - start_time:.6f} seconds, {len(available_ingredients) / (end_time - start_time):.6f} ingredients/second")
    return


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python solve.py <input_file> <method>")
        sys.exit(1)
    file_path = sys.argv[1]
    method = sys.argv[2]
    process_file(file_path)
