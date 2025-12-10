import math
import sys
import time

PLUS = 0
MULT = 1
op_to_int = {'+': PLUS, '*': MULT}


def method_1(data: list[str]) -> int:
    total = 0

    # first convert the data so that each row is a list of characters, not strings
    diagram = [list(s) for s in data]

    # iterate through the problems
    num_rows = len(diagram)
    num_cols = len(diagram[0])

    for i in range(num_rows):
        count = 0
        for j in range(num_cols):
            # if a cell has a splitter, update the cells before and after with the "|"
            # IF the cell above is a beam
            # Note: this assumes that there is always space to the left and right of the splitter, they aren't on edges
            if diagram[i][j] == '^' and diagram[i-1][j] == '|':
                diagram[i][j-1] = '|'
                diagram[i][j+1] = '|'
                count += 1
            # if the row above has a beam, continue the beam downwards
            elif i > 0 and diagram[i-1][j] in ('|', 'S'):
                diagram[i][j] = '|'
        print(f"{diagram[i]}, count: {count}")
        total += count

    return total


# part 2
def method_2(data: list[str]) -> int:
    # first convert the data so that each row is a list of characters, not strings
    diagram = [list(s) for s in data]

    # iterate through the problems
    num_rows = len(diagram)

    # We're just counting the number of pathways from the top row to the bottom row.  We can do this recursively.
    cache = {}
    def count_paths(row_idx: int, col_idx: int) -> int:
        # terminal case: we've reached the bottom row'
        if row_idx == num_rows - 1:
            # print(f"==> Reached bottom row at {row_idx}, {col_idx}: {diagram[row_idx][col_idx]}")
            return 1

        if (row_idx, col_idx) in cache:
            return cache[(row_idx, col_idx)]

        # now, decide how we proceed in usual cases
        if diagram[row_idx][col_idx] in ('S', '.'):
            # print(f"Continuing beam at {row_idx}, {col_idx}: {diagram[row_idx][col_idx]}")
            # just proceed to the next row, same column
            count = count_paths(row_idx + 1, col_idx)
            # print(f"    Count at {row_idx}, {col_idx}: {count}")
        elif diagram[row_idx][col_idx] == '^':
            # print(f"Found splitter at {row_idx}, {col_idx}: {diagram[row_idx][col_idx]}")
            # split and recurse down each side
            count = count_paths(row_idx + 1, col_idx-1) + count_paths(row_idx + 1, col_idx+1)
            # print(f"    Count at {row_idx}, {col_idx}: {count}")
        else:
            raise RuntimeError(f"Invalid character '{diagram[row_idx][col_idx]}' at row {row_idx}, col {col_idx}")

        cache[(row_idx, col_idx)] = count
        return count

    # first find the starting point, 'S'
    ci = diagram[0].index('S')
    print(f"Starting point: {ci}")
    count = count_paths(0, ci)

    return count


def process_file(filename):
    """
    Read and process lines from a text file.
    Args:
        filename (str): Path to the text file
    """
    diagram: list[str] = []

    try:
        with open(filename, 'r') as file:
            for line in file:
                processed_line = line.strip()
                diagram.append(processed_line)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    return diagram


if __name__ == "__main__":
    # parse command line
    if len(sys.argv) != 3:
        print("Usage: python solve.py <input_file> <method>")
        sys.exit(1)
    file_path = sys.argv[1]
    method = sys.argv[2]

    # read input file
    data = process_file(file_path)

    # process the data, with timing
    start_time = time.time()
    method_fcn = getattr(sys.modules[__name__], f"method_{method}")
    grand_total = method_fcn(data)
    end_time = time.time()

    print(f"Grand total: {grand_total}")
    print(f"Elapsed time {end_time - start_time:.6f} seconds")

