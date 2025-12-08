import sys
import time
from copy import copy


def method_1(line: str) -> int:
    # convert the string into a list of digits
    digits = [int(c) for c in list(line)]

    max_i = max_joltage = 0
    for i in range(len(digits) - 1):
        # if the digits[i] is less than max_i, skip it
        if digits[i] < max_i:
            continue
        else:
            # update max_i and max_joltage
            max_i = digits[i]

        joltage = digits[i] * 10 + max(digits[i + 1:])
        if joltage > max_joltage:
            max_joltage = joltage

    return max_joltage


def method_2(line: str) -> int:
    # brute force search for the maximum joltage
    max_joltage = 0
    NUM_DIGITS = 12
    line_len = len(line)
    for i1 in range(line_len - NUM_DIGITS + 1):
        for i2 in range(i1 + 1, line_len - NUM_DIGITS + 2):
            for i3 in range(i2 + 1, line_len - NUM_DIGITS + 3):
                for i4 in range(i3 + 1, line_len - NUM_DIGITS + 4):
                    for i5 in range(i4 + 1, line_len - NUM_DIGITS + 5):
                        for i6 in range(i5 + 1, line_len - NUM_DIGITS + 6):
                            for i7 in range(i6 + 1, line_len - NUM_DIGITS + 7):
                                for i8 in range(i7 + 1, line_len - NUM_DIGITS + 8):
                                    for i9 in range(i8 + 1, line_len - NUM_DIGITS + 9):
                                        for i10 in range(i9 + 1, line_len - NUM_DIGITS + 10):
                                            for i11 in range(i10 + 1, line_len - NUM_DIGITS + 11):
                                                for i12 in range(i11 + 1, line_len - NUM_DIGITS + 12):
                                                    digits_str = line[i1] + line[i2] + line[i3] + line[i4] + line[i5] + \
                                                                 line[i6] + line[i7] + line[i8] + line[i9] + line[i10] + \
                                                                 line[i11] + line[i12]
                                                    joltage = int(digits_str)
                                                    if joltage > max_joltage:
                                                        max_joltage = joltage

    return max_joltage


# best for large banks (larger than the example)
def method_3(line: str) -> int:
    max_joltage = 0
    NUM_DIGITS = 12
    digits = [int(c) for c in list(line)]

    # recursively search for the maximum joltage
    def find_max_joltage(num_digits_needed: int, digits: list[int]) -> list[int]:
        # terminal case
        if digits == []:
            return []
        if num_digits_needed == 1:
            return [max(digits)]

        # first search through the max digit
        search_digits = copy(digits)
        while True:
            max_digit = max(search_digits)
            i = digits.index(max_digit)
            # now try to find next digit
            candidate_digits = find_max_joltage(num_digits_needed - 1, digits[i + 1:])
            if not candidate_digits:
                search_digits.remove(max_digit)
                if not search_digits:
                    break
            else:
                candidate_digits.insert(0, max_digit)
                return candidate_digits
        return []

    candidate_digits = find_max_joltage(NUM_DIGITS, digits)
    joltage = 0
    for digit in candidate_digits:
        joltage = joltage * 10 + digit
    if joltage > max_joltage:
        max_joltage = joltage

    return max_joltage


def process_file(filename):
    """
    Read and process lines from a text file.
    Args:
        filename (str): Path to the text file
    """
    try:
        with open(filename, 'r') as file:
            total_joltage = 0
            line_count = 0
            start_time = time.time()
            for line in file:
                # Process each line (example: print stripped line)
                processed_line = line.strip()
                method_fcn = getattr(sys.modules[__name__], f"method_{method}")
                max_joltage = method_fcn(processed_line)
                total_joltage += max_joltage
                print(f"{processed_line}: {max_joltage}, total: {total_joltage}")
                line_count += 1
            end_time = time.time()
            print(
                f"Time elapsed: {end_time - start_time:.6f} seconds, average: {(end_time - start_time) / line_count:.6f} seconds per line")

            print(f"Total: {total_joltage}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python solve.py <input_file> <method>")
        sys.exit(1)
    file_path = sys.argv[1]
    method = sys.argv[2]
    process_file(file_path)
