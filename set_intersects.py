import collections
from numbers import Number
import re
# a = [1,2,3,2,1,5,6,5,5,5]
# print [item for item, count in collections.Counter(a).items() if count > 1]

input_file = "list.txt"
input_file_IO = open(input_file, 'r')
data = input_file_IO.readlines()
responsible_count = 0
responsible_master_list = []
responsible = ""

for index, elem in enumerate(data):
    elem = elem.strip()
    if re.search('[a-zA-Z]', elem):
        new_elem_list = []
        # Start a new list
        new_elem_list.append(elem)
        responsible_master_list.append(new_elem_list)
        responsible_count += 1
    else:
        new_elem_list.append(elem)
i = 0
# for sublist in responsible_master_list:
while i < len(responsible_master_list):
    # Find intersection of common elements
    result = set(responsible_master_list[i])
    for s in responsible_master_list[i+1:]:
        result.intersection_update(s)
    i += 1
print(result)
