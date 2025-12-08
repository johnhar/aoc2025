import sys


def process_range(start, end) -> list[int]:
    def is_invalid(n: int):
        # simple string-based method
        nstr = str(n)
        num_chars = len(nstr)
        # even number of digits, so it's possible to split it into two equal halves
        if num_chars and num_chars % 2 == 0:
            return nstr[:num_chars // 2] == nstr[num_chars // 2:]
        else:
            return False

    def is_invalid2(n: int):
        def is_invalid_for_m_times(n: int, m: int):
            nstr = str(n)
            # first check if n can be split into m equal parts
            num_chars = len(nstr)
            if num_chars % m != 0:
                return False

            # next check that all parts are equal
            part_int = 0
            part_len = num_chars // m
            for i in range(m):
                if i == 0:
                    part_int = int(nstr[0:part_len])
                else:
                    if part_int != int(nstr[i * part_len:(i + 1) * part_len]):
                        return False

            return True

        # For the number n, check if it's invalid for 2, 3, ... len(n) times
        for m in range(2, len(str(n)) + 1):
            if is_invalid_for_m_times(n, m):
                return True
        return False

    if method == 1:
        invalids = []
        for i in range(start, end + 1):
            # check if the number is an invalid, i.e. a number sequence repeated twice
            if is_invalid(i):
                invalids.append(i)
        return invalids
    else:
        invalids = []
        for i in range(start, end + 1):
            # check if the number is an invalid, i.e. a number sequence repeated twice
            if is_invalid2(i):
                invalids.append(i)
        return invalids


def process_file(filename):
    """
    Read and process lines from a text file.
    Args:
        filename (str): Path to the text file
    """
    sum_invalids = 0
    try:
        with open(filename, 'r') as file:
            line = file.readline()
            ranges = line.split(',')
            for r in ranges:
                # convert the range
                start, end = r.split('-')
                start, end = int(start), int(end)
                invalids = process_range(start, end)
                count = len(invalids) if invalids else 0
                print(f"{r}: {count} invalid(s){' <<< ' + str(invalids) if invalids else ''}")
                sum_invalids += sum(invalids)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error processing file: {e}")

    print(f"Total sum of invalid numbers: {sum_invalids}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python solve.py <method> <input_file>")
        sys.exit(1)
    method = int(sys.argv[1])
    file_path = sys.argv[2]
    process_file(file_path)
