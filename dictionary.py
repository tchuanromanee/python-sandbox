# Has to open with curly braces
# Has to have a colon between
students = {'name':'alex', 'age':'12', 'grade':'6'}

print('name ', students['name']) ## prints 'Alex
print('age ', students['age']) ## prints age
print('grade ', students['grade']) # prints grade

# Create a simple dictionary
dictionary1 = {'one': 1, 'two': 2, 'three': 3}
# type(d) is to ask python what type it is.
# In this case it is a dictionary

# x is a dictionary. Assign values
x = dict(four = 4, five = 5, six = 6)

print(x) # Prints out the dictionary in sorted order

# Makes a new dictionary out of new elements and includes elements from dictionary x
dictionary2 = dict(one = 1, two = 2, three = 3, **x)
print(dictionary2)

# Checking if there are elements in a dictionary
if ('four' in x): # If there is a 4 in dictionary x
    print("There is a 4 in dictionary x")

if ('three' in x): # If there is a 3 in dictionary x
    print("Three is in dictionary x")
else:
    print("Three is not in dictionary x")

# Iterating through elements in a dictionary
print("Iterate through elements in a dictionary")
for k in dictionary2: # for each element k in dictionary dictionary2
    print(k)

# Iterate through each key/value pair in dictionary2
print("Iterate through key/value pairs in a dictionary")
for k, v in dictionary2.items():
    print(k, v)

# Get the value stored in key 'three' in dictionary2
print(dictionary2.get('three'))
# Get the value stored in key 'three' in dictinoary x
# If not found, print out 'not found'
print(x.get('three', 'not found'))

# Pop key 'five' out of x
# Pop removes the specified key if there is an argument and returns
# its value
print(x.pop('five'))

print(x) # 'five' should not be in x anymore

## Updating Dictionary Elements ##
# Use student dictionary created in the beginning of the file
students['name'] = 'alex whiteman' # Change student name
print('name: ', students['name']) # Print the new name

## Deleting Dictionary Elements ##
wumboDict = {'name': 'Wumbo', 'symbol': 'W for Wumbo', 'major': 'Wumbology', 'comments': 'The study of WUMBO'}
print('comments: ', wumboDict['comments'])
# Remove the key 'commets'
del wumboDict['comments']
if 'comments' in wumboDict:
    print("Deletion unsuccessful. How???")
else:
    print("Deletion succesful.")

# Clear a dictionary
students.clear() # Removes everything from a dictionary
#  The line "del students" does the same thing
