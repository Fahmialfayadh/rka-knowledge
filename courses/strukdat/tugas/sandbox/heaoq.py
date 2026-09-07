import heapq
data = [5, 3, 8, 1, 2]
heapq.heapify(data)
print(data)  # Output: [1, 2, 8, 5, 3]

#soal

import random

def generate_random_numbers(n, lower_bound, upper_bound):
    #gaboleh sama
    numbers = []
    while len(numbers) < n:
        num = random.randint(lower_bound, upper_bound)
        if num not in numbers:
            numbers.append(num)
    return numbers

data = generate_random_numbers(4, 1, 10)
print(data)
heapq.heapify(data)

jawaban = [list(input())]
if jawaban == data:
    print("Jawaban benar!")
else:  
    print("Jawaban salah. Data yang benar adalah:", data)