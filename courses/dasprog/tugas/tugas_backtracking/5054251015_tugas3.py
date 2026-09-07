class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        self.ans = [] 
        board = [[0 for _ in range(n)] for _ in range(n)]
        self.rec(board, 0)
        return self.ans

    def is_safe(self, board, row, col):
        n = len(board)
        
        # kolom atas
        for i in range(row):
            if board[i][col] == 1:
                return False
        
        # diagonal kiri atas
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if board[i][j] == 1:
                return False
            i -= 1
            j -= 1
            
        # diaognal kanan atas
        i, j = row - 1, col + 1
        while i >= 0 and j < n:
            if board[i][j] == 1:
                return False
            i -= 1
            j += 1
            
        return True

    def rec(self, board, row):
        n = len(board)
        if row == n:
            current_solution = []
            for r in range(n):
                row_str = ""
                for c in range(n):
                    if board[r][c] == 1:
                        row_str += "Q"
                    else:
                        row_str += "."
                current_solution.append(row_str)
            
            # list jawaban
            self.ans.append(current_solution)
            return

        # rec step
        for col in range(n):
            if self.is_safe(board, row, col):
                board[row][col] = 1    
                self.rec(board, row + 1) 
                board[row][col] = 0     # backtrack ilangin ratu (buat 0)