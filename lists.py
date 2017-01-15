# Split the words into an array
words = "the quick brown fox jumps over the lazy dog".split()

print(words)

# info contains uppercase, lowercase, and length of each word in info
info = [[w.upper(), w.lower(), len(w)] for w in words]

for data in info:
    print(data)
