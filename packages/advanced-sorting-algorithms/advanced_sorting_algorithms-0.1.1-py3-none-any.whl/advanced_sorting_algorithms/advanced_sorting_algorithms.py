import random as rn
import time
# import timeit
from math import factorial


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
