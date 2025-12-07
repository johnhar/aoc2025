import sys


class Dial:
    # the dial has positions from 0 to 99.
    # We can use modulo and div to quickly find the position after a rotation and
    # count the # of times the dial points to zero at the end of the rotation.
    def __init__(self, number: int = 50, method: int = 1):
        self.number = number
        self.count_zeros = 0
        self.method = method

    def rotate(self, r: str) -> int:
        """
        Rotate the dial by the direction and clicks.
        E.g. "L10" would rotate the dial 10 left (decrement).
        E.g. "R68" would rotate the dial 68 right (increment).
        :param r: the rotation string
        :return: how much the count of zeros changed
        """
        # convert the rotation string into an integer number of clicks (+/-)
        clicks = int(r[1:])
        dir = -1 if r[0] == 'L' else 1
        count_of_zeros_before = self.count_zeros

        # Method 1: day 1 part 1
        if self.method == 1:
            # update the dial position, and mod it to keep it between 0 and 99
            self.number = (self.number + dir * clicks) % 100

            # add to the count of zeros if it landed on a zero
            if self.number == 0:
                self.count_zeros += 1

        # Method 2: day 1 part 2, optimized
        elif self.method == 2:
            # in the new method, count any time the dial lands on zero, even during the rotation.
            # first, count the full rotations (which will hit zero once per full rotation)
            self.count_zeros += clicks // 100
            # next, see if we pass zero during the partial rotations
            partial_rotations = clicks % 100
            if partial_rotations:
                new_number = self.number + dir * partial_rotations
                # corner case: if number is already at zero, don't count it.  Else, check if it rotates around
                if self.number:
                    if new_number <= 0 or new_number >= 100:
                        self.count_zeros += 1
                # save the new position
                self.number = new_number % 100

        # Method 3: day 1, part 2, brute force
        elif self.method == 3:
            # the brute force method, just count the zeros after each click
            for _ in range(clicks):
                self.number = (self.number + dir) % 100
                if self.number == 0:
                    self.count_zeros += 1

        return self.count_zeros - count_of_zeros_before


def process_file(filename, dial: Dial, dial2: Dial = None):
    """
    Read and process lines from a text file.
    Args:
        filename (str): Path to the text file
        dial (Dial): The dial to use for processing
    """
    try:
        with open(filename, 'r') as file:
            line_number = 1
            for line in file:
                # Process each line (example: print stripped line)
                processed_line = line.strip()

                new_zeros1 = dial.rotate(processed_line)
                new_zeros2 = dial2.rotate(processed_line)
                msg = f"{line_number}: {processed_line} -> {dial.number:2} {dial.count_zeros}"
                if new_zeros1 != new_zeros2:
                    msg += f"{'<<< should be '+str(dial2.count_zeros)}"
                print(msg)

                line_number += 1

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error processing file: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python solve.py <method: 1, 2 or 3> <input file>")
        sys.exit(1)
    method = int(sys.argv[1])
    file_path = sys.argv[2]
    dial = Dial(method=method)
    dial2 = Dial(method=3)
    process_file(file_path, dial, dial2)
