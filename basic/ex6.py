
def is_even(n):
    return n % 2 == 0

print(is_even(4))
print(is_even(7))
print(is_even(0))
print(is_even(-3))
print(is_even(10))

def triangles(a, b, c):
    if a == b and a == c and b == c:
        result = "Equilateral"
    elif a != b and a != c and b != c:
        result = "Scalene"
    else:
        result = "Isosceles"

    return result

print(triangles(5,5,5))
print(triangles(5,5,3))
print(triangles(5,2,3))






