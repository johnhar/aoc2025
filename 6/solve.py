import math
import sys
import time

PLUS = 0
MULT = 1
op_to_int = {'+': PLUS, '*': MULT}


def method_1(worksheet: list[list[int]]) -> int:
    total = 0

    # iterate through the problems
    num_problems = len(worksheet[0])
    num_numbers = len(worksheet) - 1
    print(f"Processing {num_problems} problems with {num_numbers} numbers each.")

    for i in range(num_problems):
        numbers = [worksheet[ri][i] for ri in range(num_numbers)]
        op = worksheet[num_numbers][i]
        if op == PLUS:
            answer = sum(numbers)
        else:
            answer = math.prod(numbers)
        print(f"Problem {i}: {numbers} {'+' if op == PLUS else '*'} = {answer}")
        total += answer

    return total


# part 2: this is the straight forward approach, but it's slow.
def method_2(worksheet: list[str]) -> int:
    total = 0

    # reparse the worksheet by columns and operate on it along the way
    num_rows = len(worksheet)

    this_problem_op = ''
    numbers = []
    for i in range(len(worksheet[0])):
        # get the number in this column
        number_list = [worksheet[r][i] for r in range(num_rows-1)]
        number_str = ''.join(number_list).strip()
        print(number_str)
        if number_str:
            number = int(number_str)
            numbers.append(number)
        else:   # no number in this column, so it's the end of this problem
            answer = sum(numbers) if this_problem_op == '+' else math.prod(numbers)
            print(f"Problem: {numbers} {'+' if this_problem_op == '+' else '*'} = {answer}")
            total += answer
            numbers = []

        # get the operators in this column, if any
        try:
            op = worksheet[num_rows-1][i]
            if op in ('+', '*'):
                this_problem_op = op
        except:
            pass


    return total


def process_file(filename):
    """
    Read and process lines from a text file.
    Args:
        filename (str): Path to the text file
    """
    # worksheet for method 1/part 1 is a list[list[int]], where each inner list represents
    # a row of numbers or operator code (PLUS or MULT)
    # worksheet for part 2 is the list of strings exactly as read from the file.  We need to retain whitespace
    # and parse within the method.
    worksheet = []

    try:
        with open(filename, 'r') as file:
            for line in file:
                if method == '1':
                    # Process each line (example: print stripped line)
                    processed_line = line.strip().split()
                    # print(processed_line)
                    # are we processing numbers or operands?
                    if processed_line[0] in ('+', '*'):
                        worksheet.append([op_to_int[op] for op in processed_line])
                    else:
                        worksheet.append([int(num) for num in processed_line])
                else:
                    # read in every line as is
                    worksheet.append(line)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    # print(worksheet)
    start_time = time.time()
    method_fcn = getattr(sys.modules[__name__], f"method_{method}")
    grand_total = method_fcn(worksheet)
    end_time = time.time()

    print(f"Grand total: {grand_total}")
    print(
        f"Elapsed time {end_time - start_time:.6f} seconds, {len(worksheet[0]) / (end_time - start_time):.6f} problems/second")
    return


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python solve.py <input_file> <method>")
        sys.exit(1)
    file_path = sys.argv[1]
    method = sys.argv[2]
    process_file(file_path)
