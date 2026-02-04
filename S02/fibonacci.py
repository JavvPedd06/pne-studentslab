
a, b = 0, 1
result = str(a)
for i in range(10):
    result += " " + str(b)
    a, b = b, a + b
print(result)