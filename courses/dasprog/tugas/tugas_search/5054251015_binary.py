def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
            
    return -1

arr = list(map(int, input().split()))
target = int(input("Enter target value: "))
result = binary_search(arr, target)
if result != -1:
    print(f" Ada disini wok {result}")
else:
    print("Ga nemu wok, coba yg lain")