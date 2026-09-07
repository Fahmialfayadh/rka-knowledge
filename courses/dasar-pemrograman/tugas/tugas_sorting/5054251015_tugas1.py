n = int(input())
lst = list(map(int, input().split()))

# (1) sort dulu
lst.sort()

# (2) hitung distinct setelah sort
count = 1 if n > 0 else 0
for i in range(1, n):
    if lst[i] != lst[i-1]:
        count += 1

print(count)
