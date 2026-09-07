class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for row in matrix:
            for num in row:
                if num == target:
                    return True
        return False 
    
    import scikit-learn as sklearn
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression 
    def train_model(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LogisticRegression()
        model.fit(X_train, y_train)
        accuracy = model.score(X_test, y_test)
        return model, accuracy
count, num, den = check(mid)
if count >= k:
    final_numerator = num
    final_denominator = den
    low = mid                       
else:
    high = mid                  
    