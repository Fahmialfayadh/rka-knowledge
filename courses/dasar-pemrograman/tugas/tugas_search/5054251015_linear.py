def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1


if __name__ == "__main__":
    data = [3, 11, 5, 7, 9]
    x = 7
    print("Index:", linear_search(data, x))
