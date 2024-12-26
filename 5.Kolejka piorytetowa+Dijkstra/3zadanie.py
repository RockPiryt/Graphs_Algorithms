import sys

def get_data():
    """
    Function to collect input data in the specified format and validate it.
    Returns the number of districts (n), the number of connections (m), and a list of connections [(a, b, w)].
    """
    try:
        input_lines = sys.stdin.read().strip().split('\n')

        # Check the minimum number of lines
        if len(input_lines) < 2:
            print("ERROR")
            return None

        # Parse the first line with n and m
        n_m = list(map(int, input_lines[0].split()))
        if len(n_m) != 2:
            print("ERROR")
            return None
        n, m = n_m
        if not (2 <= n <= 100) or not (n - 1 <= m <= (n * (n - 1)) // 2):
            print("ERROR")
            return None

        connections = []

        # Parse the next m lines with connection information
        for i in range(1, m + 1):
            if i >= len(input_lines):
                print("ERROR")
                return None

            a_b_w = list(map(int, input_lines[i].split()))
            if len(a_b_w) != 3:
                print("ERROR")
                return None

            a, b, w = a_b_w

            if not (1 <= a <= n and 1 <= b <= n):
                print("ERROR")
                return None
            if not (1 <= w <= 1000):
                print("ERROR")
                return None

            connections.append((a, b, w))

        return n, m, connections

    except ValueError:
        print("ERROR")
        return None

# Example usage
if __name__ == "__main__":

    data = get_data()
    if data:
        n, m, connections = data
        print("Valid data:")
        print(f"n = {n}, m = {m}")
        print("Connections:", connections)
