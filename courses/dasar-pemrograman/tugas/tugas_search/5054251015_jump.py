
def interpolationSearch(arr, lo, hi, x):
    if (lo <= hi and x >= arr[lo] and x <= arr[hi]):
        pos = lo + ((hi - lo) // (arr[hi] - arr[lo]) *
                    (x - arr[lo]))

        if arr[pos] == x:
            return pos
        if arr[pos] < x:
            return interpolationSearch(arr, pos + 1,
                                       hi, x)

        if arr[pos] > x:
            return interpolationSearch(arr, lo,
                                       pos - 1, x)
    return -1

arr = list(map(int, input().split()))
arr.sort()
n = len(arr)

x = int(input())
index = interpolationSearch(arr, 0, n - 1, x)

if index != -1:
    print("ada nih disini =>", index)
else:
    print("Ga nemu wok, coba yg lain")