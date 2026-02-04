def fibosum(n):
    a = 0
    b = 1
    total = 0
    for i in range(n):
        total = total + a

        temp = a
        a = b
        b = temp + b

    return total

print(fibosum(5))
print(fibosum(10))

