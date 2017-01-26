def main():

    # Print an array in sorted order
    myNumArr = [1, 4, 9, 8, 5, 6]
    print(sorted(myNumArr))

    print(sorted(['a', 'g', 'z', 'k', 'v', 'd']))

    items = ['bread', 'cheese', 'milk', 'eggs']
    print(items.sort()) # comes up empty because no values are assigned to items
    # Sorted doesnt work because it is not associated with items
    print(sorted(items)) # Works

    ## Sorting Functions
    print(myNumArr.sort()) # works
main()
