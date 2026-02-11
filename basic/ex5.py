words = ["Python", "is", "a", "programming", "language"]

def word_processer(lst):
    for ch in lst:
        print(ch, "->", len(ch), "characters")

word_processer((words))