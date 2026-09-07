class node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class bst:
    def init(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = node(value)
        else:
            self._insert(self.root, value)
                         
    def _insert(self, current_node, value):
        if value < current_node.value:
            if current_node.left is None:
                current_node.left = node(value)
            else:
                self._insert(current_node.left, value)

        elif value > current_node.value:
            if current_node.right is None:
                current_node.right = node(value)
            else:
                self._insert(current_node.right, value)

    def search(self, value):
        return self._search(self.root, value)
    
    def _search(self, current_node, value):
        if current_node is None:
            return False
        if value == current_node.value:
            return True
        elif value < current_node.value:
            return self._search(current_node.left, value)
        else:
            return self._search(current_node.right, value)