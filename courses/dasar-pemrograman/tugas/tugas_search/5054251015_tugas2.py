import sys

# fpb
def fpb(a, b):
    while b:
        a, b = b, a % b
    return a

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    current_index = 0
    
    # main variables
    N = int(input_data[current_index]); current_index += 1
    M = int(input_data[current_index]); current_index += 1
    A = int(input_data[current_index]); current_index += 1
    B = int(input_data[current_index]); current_index += 1
    Q = int(input_data[current_index]); current_index += 1
    
    queries = []
    for _ in range(Q):
        queries.append(int(input_data[current_index]))
        current_index += 1

    def check(value):
        count = 0
        best_numerator = -1
        best_denominator = 1
        
        for row in range(1, N + 1):
            calculated_limit = value * (A + row) - B
            max_column = int(calculated_limit)
            
            if max_column > M:
                max_column = M
            
            if max_column >= 1:
                count += max_column
                
                # kolom paling kanan adalah max_column 
                current_numerator = B + max_column
                current_denominator = A + row
                
                # compare pecahan menggunakan perkalian silang
                # current > best jika: current_num * best_den > best_num * current_den
                if current_numerator * best_denominator > best_numerator * current_denominator:
                    best_numerator = current_numerator
                    best_denominator = current_denominator
                    
        return count, best_numerator, best_denominator
    
    # prosess each query
    for k in queries:
        low = 0.0
        high = (B + M) / (A + 1) + 1.0
        
        final_numerator = 1
        final_denominator = 1
        
        # binary search for 70 iterations
        for _ in range(70):
            mid = (low + high) / 2
            count_result, candidate_numerator, candidate_denominator = check(mid)
            
            if count_result >= k:
                final_numerator = candidate_numerator
                final_denominator = candidate_denominator
                high = mid
            else:
                low = mid
        
        # sederhanakan hasil [pake pecahan]
        divisor = fpb(final_numerator, final_denominator)
        print(f"{final_numerator // divisor}/{final_denominator // divisor}")

if __name__ == '__main__':
    solve()