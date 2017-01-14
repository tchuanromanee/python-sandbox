def main():

    data = "This is where I want to break"
    for char in data:
        if char == 'b': break ## Need to specify that we want to break
    print(char, end='') ## Print the next char where it breaks


main()