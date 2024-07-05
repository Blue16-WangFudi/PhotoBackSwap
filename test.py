def round_to_multiple_of_four(n):
    remainder = n % 4
    if remainder == 0:
        return n
    if remainder >= 2:
        return n + (4 - remainder)
    else:
        return n - remainder

print(round_to_multiple_of_four(1706))