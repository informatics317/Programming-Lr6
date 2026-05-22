# AVL-дерево
class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def _height(self, node):
        return node.height if node else 0

    def _balance(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        # Делаем поворот
        x.right = y
        y.left = T2

        # Обновляем высоты
        y.height = max(self._height(y.left), self._height(y.right)) + 1
        x.height = max(self._height(x.left), self._height(x.right)) + 1

        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left

        # Делаем поворот
        y.left = x
        x.right = T2

        # Обновляем высоты
        x.height = max(self._height(x.left), self._height(x.right)) + 1
        y.height = max(self._height(y.left), self._height(y.right)) + 1

        return y

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if node is None:
            return AVLNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            return node

        node.height = max(self._height(node.left), self._height(node.right)) + 1

        balance = self._balance(node)

        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)

        if balance < -1 and value > node.right.value:
            return self._rotate_left(node)

        if balance > 1 and value > node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    # Удаление значения из дерева
    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _min_value_node(self, node):
        # Найти узел с минимальным значением в поддереве
        current = node
        while current.left:
            current = current.left
        return current

    def _delete(self, node, value):
        if node is None:
            return node

        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right

            if node.right is None:
                return node.left

            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete(node.right, temp.value)

        if node is None:
            return node

        node.height = max(self._height(node.left), self._height(node.right)) + 1

        balance = self._balance(node)

        if balance > 1 and self._balance(node.left) >= 0:
            return self._rotate_right(node)

        if balance > 1 and self._balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and self._balance(node.right) <= 0:
            return self._rotate_left(node)

        if balance < -1 and self._balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def search(self, value):
        return self._search(self.root, value)

    def _search(self, node, value):
        if node is None or node.value == value:
            return node is not None
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)


# Красно-черное дерево
class RBNode:
    def __init__(self, value, color='RED'):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.color = color


class RedBlackTree:
    def __init__(self):
        self.root = None
    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, value):
        new_node = RBNode(value, 'RED')
        if self.root is None:
            self.root = new_node
            self.root.color = 'BLACK'
            return

        current = self.root
        parent = None

        while current:
            parent = current
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return

        new_node.parent = parent
        if value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        self._fix_insert(new_node)

    def _fix_insert(self, node):
        while node != self.root and node.parent.color == 'RED':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right

                if uncle and uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._rotate_left(node)

                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left

                if uncle and uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_right(node)

                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self._rotate_left(node.parent.parent)

        self.root.color = 'BLACK'

    def delete(self, value):
        node = self._find_node(value)
        if node:
            self._delete_node(node)

    def _find_node(self, value):
        current = self.root
        while current:
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return None

    def _min_node(self, node):
        while node.left:
            node = node.left
        return node

    def _delete_node(self, node):
        if node.left is None or node.right is None:
            self._delete_one_child(node)
        else:
            successor = self._min_node(node.right)
            node.value = successor.value
            self._delete_one_child(successor)

    def _delete_one_child(self, node):
        child = node.left if node.left else node.right
        if node.parent is None:
            self.root = child
            if child:
                child.parent = None
                child.color = 'BLACK'
            return
        if node == node.parent.left:
            node.parent.left = child
        else:
            node.parent.right = child

        if child:
            child.parent = node.parent

        if node.color == 'BLACK':
            self._fix_delete(child, node.parent)

    def _fix_delete(self, node, parent):
        while node != self.root and (node is None or node.color == 'BLACK'):
            if node == parent.left:
                sibling = parent.right

                if sibling and sibling.color == 'RED':
                    sibling.color = 'BLACK'
                    parent.color = 'RED'
                    self._rotate_left(parent)
                    sibling = parent.right

                if (sibling is None or sibling.left is None or sibling.left.color == 'BLACK') and \
                        (sibling is None or sibling.right is None or sibling.right.color == 'BLACK'):
                    if sibling:
                        sibling.color = 'RED'
                    node = parent
                    parent = node.parent
                else:
                    if sibling.right is None or sibling.right.color == 'BLACK':
                        if sibling.left:
                            sibling.left.color = 'BLACK'
                        sibling.color = 'RED'
                        self._rotate_right(sibling)
                        sibling = parent.right

                    if sibling:
                        sibling.color = parent.color
                    parent.color = 'BLACK'
                    if sibling and sibling.right:
                        sibling.right.color = 'BLACK'
                    self._rotate_left(parent)
                    node = self.root
                    break
            else:
                sibling = parent.left

                if sibling and sibling.color == 'RED':
                    sibling.color = 'BLACK'
                    parent.color = 'RED'
                    self._rotate_right(parent)
                    sibling = parent.left

                if (sibling is None or sibling.left is None or sibling.left.color == 'BLACK') and \
                        (sibling is None or sibling.right is None or sibling.right.color == 'BLACK'):
                    if sibling:
                        sibling.color = 'RED'
                    node = parent
                    parent = node.parent
                else:
                    if sibling.left is None or sibling.left.color == 'BLACK':
                        if sibling.right:
                            sibling.right.color = 'BLACK'
                        sibling.color = 'RED'
                        self._rotate_left(sibling)
                        sibling = parent.left

                    if sibling:
                        sibling.color = parent.color
                    parent.color = 'BLACK'
                    if sibling and sibling.left:
                        sibling.left.color = 'BLACK'
                    self._rotate_right(parent)
                    node = self.root
                    break

        if node:
            node.color = 'BLACK'

    def search(self, value):
        return self._find_node(value) is not None

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)


# Тестирование

print('Тестирование AVL-дерева:')
avl = AVLTree()
print('\nВставка чисел: 10, 20, 30, 40, 50, 25')
for val in [10, 20, 30, 40, 50, 25]:
    avl.insert(val)
    print(f'После вставки {val}: {avl.inorder()}')

print('\nУдаление 40')
avl.delete(40)
print(f'После удаления: {avl.inorder()}')

print('\nУдаление 30')
avl.delete(30)
print(f'После удаления: {avl.inorder()}')

print('\nПоиск 20:', 'Найден' if avl.search(20) else 'Не найден')
print('Поиск 100:', "Найден" if avl.search(100) else 'Не найден')


print('\nТестирование красно-черного дерева:')
rbt = RedBlackTree()
print('\nВставка чисел: 7, 3, 18, 10, 22, 8, 11, 26')
for val in [7, 3, 18, 10, 22, 8, 11, 26]:
    rbt.insert(val)
    print(f'После вставки {val}: {rbt.inorder()}')

print('\nУдаление 18')
rbt.delete(18)
print(f'После удаления: {rbt.inorder()}')

print('\nУдаление 7')
rbt.delete(7)
print(f'После удаления: {rbt.inorder()}')

print('\nПоиск 10:', 'Найден' if rbt.search(10) else 'Не найден')
print('Поиск 100:', 'Найден' if rbt.search(100) else 'Не найден')
