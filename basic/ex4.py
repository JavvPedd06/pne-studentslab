def marks(n):
    if n >= 9:
        result = "A"
    elif n <= 8.9 and n >= 7:
        result = "B"
    elif n <= 6.9 and n >= 5:
        result = "C"
    elif n <= 4.9 and n >= 3:
        result = "D"
    else:
        result = "F"
    return result

print(marks(9.5))
print(marks(7))
print(marks(5.5))
print(marks(3.2))
print(marks(1))
