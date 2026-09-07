def interpolationSearch(arr, lo, hi, x):

    # Since array is sorted, an element present
    # in array must be in range defined by corner
    if (lo <= hi and x >= arr[lo] and x <= arr[hi]):

        # Probing the position with keeping
        # uniform distribution in mind.
        pos = lo + ((hi - lo) // (arr[hi] - arr[lo]) *
                    (x - arr[lo]))

        # Condition of target found
        if arr[pos] == x:
            return pos

        # If x is larger, x is in right subarray
        if arr[pos] < x:
            return interpolationSearch(arr, pos + 1,
                                       hi, x)

        # If x is smaller, x is in left subarray
        if arr[pos] > x:
            return interpolationSearch(arr, lo,
                                       pos - 1, x)
    return -1

arr = list(map(int, input().split()))
arr.sort()
n = len(arr)

# Element to be searched
x = int(input())
index = interpolationSearch(arr, 0, n - 1, x)

if index != -1:
    print("ada nih disini =>", index)
else:
    print("Ga nemu wok, coba yg lain")