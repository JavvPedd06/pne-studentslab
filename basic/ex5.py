words = ["Python", "is", "a", "programming", "language"]

def word_processer(lst):
    for ch in lst:
        print(ch, "->", len(ch), "characters")

n = 1
while n <= 1000:
    print(n)
    n = n * 2
print(n)

word_processer((words))

