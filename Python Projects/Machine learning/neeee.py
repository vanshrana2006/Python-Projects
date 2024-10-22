def avg(*args):
    return sum(args) / len(args)

import sys

input_data = sys.stdin.read().strip()
if input_data:
    arguments = list(map(int, input_data.split()))
    result = avg(*arguments)
    print("{:.2f}".format(result))  # Do decimal places tak format karega
else:
    print("Error: No input provided. Please enter at least one number.")

    
        