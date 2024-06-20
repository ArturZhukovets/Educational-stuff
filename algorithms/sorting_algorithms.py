import random

numbers_array = [random.randint(0, 1000) for _ in range(100)]

# ============================== QUICK SORT ==============================
# Выбирается опорный элемент (в нашем случае это первый элемент массива)
# В два списка скалдываем соответсвенно элементы меньшие опорного элемента и большие опорного элемента.
# После вызываем рекурсивно функцию quick_sort для списка с меньшими элементами и для списка с большими элементами.
# Резульатом будет сумма результата рекурсии для левого списка, опорный элемент, результат рекурсии правого списка.
# `res = quick_sort(lt_array) + [element] + quick_sort(gt_array)`
# ========================================================================
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


# ============================== SORTING BY SELECTION ==============================
# Проходим по массиву каждый раз в поиске минимального значения.
# После каждой итерации обхода минимальное значение меняется с текущим элементом, стоящим по индексу i.
# Соответсвенно каждая новая итерация обхода начинается не с 0, а с текущего указателя i.
# ==================================================================================
def selection_sort(array: list[int]) -> list[int]:
    for i in range(len(array) - 1):
        current_min = array[i]
        current_min_index = i

        for j in range(i, len(array)):
            if array[j] < current_min:
                current_min = array[j]
                current_min_index = j

        if current_min_index != i:
            # then swap elements
            array[i], array[current_min_index] = array[current_min_index], array[i]
    return array


# ============================== SORTING BY SELECTION ==============================
# Внутри каждой run_iteration мы проходим циклом по массиву, сравнивая соседние элементы.
# По окончанию такого прохода в конце массива остаётся самый большой элемент (всплывающий пузырёк)
# На следющей итерации этот элемент (пузырёк с прошлой итерации) уже проверять нет смысла,
# поэтому `for i in range(len(array) - 1 - run_iteration)`
# ==================================================================================

def bubble_sort(array: list[int]) -> list[int]:
    for run_iteration in range(len(array) - 1):
        for i in range(len(array) - 1 - run_iteration):
            if array[i] > array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]
    return array

