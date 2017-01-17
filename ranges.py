def main():
    myNums = range(10) #specify a range of ten
    # Range between 0 and 1
    print(myNums) # output: range(0, 10)

    myNums2 = list(range(10)) # Same range as a list, max num is 9
    print(myNums2)

    # Ranges can be separated by values other than one
    myNums3 = list(range(10, 20, 2))
    print(myNums3) # [10, 12, 14, 16, 18] does not include upper bound

    # If no specifications are given for beginning values, assuption is that it
    # begins as zero.
    # If no specifications are given for ending values, it is argument - 1


main()
