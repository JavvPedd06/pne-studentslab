temperatures = [15.5, 17.2, 14.8, 16.0, 18.3, 20.1, 19.5]


def highest_and_lowest(lista, n):

    value = lista[0]


    if n == "max":

        for e in lista:
            if e < value:
                value = e
    elif n == "min":

        for e in lista:
            if e > value:
                value = e

    return value

def mean(lst):
    c = 0
    t = 0
    for ch in lst:
        t = t + ch
        c = c + 1

    return round(t/c , 1)

def above_value(lst, n):
    c = 0
    for ch in lst:
        if ch >= n:
            c = c + 1
    return c

print(temperatures[2])
print("The max value is: ", highest_and_lowest(temperatures, "max"))
print("The min value is: ", highest_and_lowest(temperatures, "min"))
print("The mean value is:", mean(temperatures))
n = 17
print("The number of values over", n, "are:", above_value(temperatures, n))
temperatures.sort(reverse=False)
print(temperatures)

