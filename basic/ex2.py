text = "  Hello, World! Welcome to Python Programming.  "

text_stripped = text.strip()
text_separated = text_stripped.split()
joined_sentence = " - ".join(text.split())

print(text_stripped)
print(len(text_separated))
print(text_stripped.title())
print(text_stripped.startswith("Hello"))
print(text_stripped.endswith("ing."))
print(text_stripped.find("Python"))
print(joined_sentence)

