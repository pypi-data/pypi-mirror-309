import random as rn
import time
# import timeit
from math import factorial
from typing import Callable

# Copyright (c) 2024 Hryharovich Daniil
# MIT License

random = rn.SystemRandom()
arr = [5, 22222, 54, 8, 6, 9]


def bubble_sort(arr: list) -> list:
    arr_len = len(arr)

    if arr_len <= 1:
        return arr

    for i in range(arr_len):
        # Флаг для оптимизации: если за проход не было обменов, массив отсортирован
        swapped = False
        for j in range(arr_len - 1 - i):  # Уменьшаем диапазон, так как последние элементы уже отсортированы
            first = arr[j]
            second = arr[j + 1]
            if first > second:
                arr[j] = second
                arr[j + 1] = first
                swapped = True
        # Если не было обменов, выходим из цикла
        if not swapped:
            break

    return arr


def is_sorted(arr: list) -> bool:
    if arr:
        arr_copy = arr.copy()
        arr_copy.sort()

        return arr_copy == arr

    return False


def bogo_sort(arr: list) -> list:
    ans_arr = []
    arr_copy = arr.copy()

    if len(arr) <= 1:
        return arr

    while True:
        if is_sorted(ans_arr):
            break

        random.shuffle(arr_copy)
        ans_arr = arr_copy

    return ans_arr


def merge_sort(arr: list) -> Callable:
    # Базовый случай: если массив состоит из одного элемента, он уже отсортирован
    if len(arr) <= 1:
        return arr

    # Разделяем массив на две половины
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])   # Рекурсивно сортируем левую половину
    right_half = merge_sort(arr[mid:])  # Рекурсивно сортируем правую половину

    # Сливаем отсортированные половины
    return merge(left_half, right_half)


def merge(left: list, right: list) -> list:
    sorted_array = []
    i = j = 0

    # Сравниваем элементы двух половин и добавляем меньший в отсортированный массив
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_array.append(left[i])
            i += 1
        else:
            sorted_array.append(right[j])
            j += 1

    # Добавляем оставшиеся элементы из левой половины, если они есть
    while i < len(left):
        sorted_array.append(left[i])
        i += 1

    # Добавляем оставшиеся элементы из правой половины, если они есть
    while j < len(right):
        sorted_array.append(right[j])
        j += 1

    return sorted_array


# if __name__ == '__main__':  # bogo sort test
#    try:
#        print(f"""\tBogo sort is O(n!) or O({len(arr)}!) or O({factorial(len(arr))}),
#        approximately in seconds: {factorial(len(arr)) * 0.000008:0.9f}""")
#        start = time.time()
#        print(bogo_sort(arr))
#        end = time.time()
#        print(f"Time: {end-start}")

#    except KeyboardInterrupt:
#        print("Program terminated")
