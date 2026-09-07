n = int(input())
dp = [0] * (n + 1)
dp[0] = 1
def tangga1(n):
    i = 0
    while i <= n:
        dp[i] = dp[i - 1] + 1
        i += 1
    return dp[n]
def tangga2(n):
    i = 0
    while i >=2 and i <= n:
        dp[i] = dp[i - 2] + 1
        i += 1
    return dp[n]

print(tangga1(n) + tangga2(n))