class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = []
        
        def backtrack(start, path):
            if len(path) == k:
                res.append(path[:]) # copy path
                return
    
            need = k - len(path)
            remain = n - start + 1
            
            # kalau sisa angka gak cukup, gak usah lanjut loop
            if remain < need:
                return
                
            limit = n - need + 2 
            
            for i in range(start, limit):
                path.append(i)
                backtrack(i + 1, path)
                path.pop()
        
        backtrack(1, [])
        return res