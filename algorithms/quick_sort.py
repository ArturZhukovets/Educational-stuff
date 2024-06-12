import random
random_elements = [random.randint(0, 1000) for _ in range(100)]
set1 = set(random_elements)
set2 = set(random_elements)

print(set1)
print(set2)
# print(set3)
# print(random_elements)
# print(set(random_elements))

def quick_sort(array: list[int]) -> list[int]:
    if len(array) < 2:
        return array
    elif len(array) == 2:
        return array if array[0] <= array[1] else array[::-1]
    element = array.pop(0)
    lt_array = []
    gt_array = []
    for el in array:
        if element > el:
            lt_array.append(el)
        else:
            gt_array.append(el)
    res = quick_sort(lt_array) + [element] + quick_sort(gt_array)
    return res

# res = quick_sort(random_elements)
# print(res)