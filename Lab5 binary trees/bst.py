# Jakub Głód 417193
# skończone

class Node:

    def __init__(self, key, value, right=None, left=None):
        self.key = key
        self.value = value
        self.right = right
        self.left = left


class BST:

    def __init__(self):
        self.root = None

    def search(self, key):
        # tworzy rekurencję od korzenia
        return self.__rec_search(self.root, key)

    def __rec_search(self, node, key):
        # jeśli każe szukać w pustym węźle
        if node is None:
            print("Nie znaleziono")
            return None
        # jeśli klucz jest większy / mniejszy, dalsza rekurencja:
        elif node.key < key:
            return self.__rec_search(node.right, key)
        elif node.key > key:
            return self.__rec_search(node.left, key)
        # jeśli znaleziono klucz, zwraca wartość
        else:
            return node.value

    # metoda rekurencyjna samodzielna z dodatkowym parametrem domyślnie None
    def insert(self, key, value, node=None):
        # jeśli nie podano parametru, to tworzy wywołanie rekurencyjne od korzenia
        # lub oczywiście tworzy korzeń w razie pustego drzewa
        if node is None:
            if self.root is None:
                self.root = Node(key, value)
            else:
                self.insert(key, value, self.root)
        # jeśli znaleziono węzeł o takim kluczu, to go nadpisujemy
        elif key == node.key:
            node.value = value
        # jeśli klucz mniejszy, to
        elif key < node.key:
            # albo wstaw dziecko
            if node.left is None:
                node.left = Node(key, value)
            # albo rekurencyjne wywołanie do mniejszego dziecka
            else:
                self.insert(key, value, node.left)
        # analogicznie dla większego klucza
        else:
            if node.right is None:
                node.right = Node(key, value)
            else:
                self.insert(key, value, node.right)

    def delete(self, key):
        # rozpoczęcie rekurencji od korzenia
        return self.__delete(self.root, key)

    def __delete(self, node, key):
        if node is None:
            print("Nie znaleziono danej do usunięcia")
        # szukanie węzła do usunięcia
        if key < node.key:
            # jeśli mniejszy klucz, to przechodzimy w lewo
            node.left = self.__delete(node.left, key)
        elif key > node.key:
            # jeśli większy, to przechodzimy w prawo
            node.right = self.__delete(node.right, key)
        # gdy węzeł node jest do usunięcia
        else:
            # gdy nie ma dzieci
            if node.left is None and node.right is None:
                # zwróci None, który cofając rekurencję nadpisze ten węzeł jako pusty
                return None
            # jedno dziecko z prawej
            elif node.left is None:
                # nadpisuje węzeł prawym dzieckiem
                temp = node.right
                node = None
                return temp
            # jedno dziecko z lewej
            elif node.right is None:
                # nadpisuje węzeł lewym dzieckiem
                temp = node.left
                node = None
                return temp
            # dwoje dzieci
            else:
                # znalezienie węzła o minimalnym kluczu w prawym poddrzewie
                child = node.right
                while child.left:
                    child = child.left
                # zamiana klucza i wartości usuwanego węzła z kluczem następnika
                node.key = child.key
                node.value = child.value
                # lewa gałąź zostaje taka sama
                node.right = self.__delete(node.right, child.key)
        return node

    def __str__(self):
        res = ""
        if self.root is None:
            res += "Drzewo jest puste"
        else:
            res += self.__str_rec(self.root)
        return res

    def __str_rec(self, node):
        if node:
            A, B, C = "", "", ""
            if node.left:
                A = self.__str_rec(node.left)
            B = f"{node.key} {node.value},"
            if node.right:
                C = self.__str_rec(node.right)
        return A + B + C

    def height(self):
        # Najdłuższą ścieżkę rozumiem jako liczbę wierzchołków, które obejmuje.
        # Dla liczby krawędzi należałoby dopisać "-1"
        return self.__rec_height(self.root)

    def __rec_height(self, node):
        if node is None:
            return 0
        else:
            left_height = self.__rec_height(node.left)
            right_height = self.__rec_height(node.right)
            return max(left_height, right_height) + 1

    # funkcje z polecenia
    def print_tree(self):
        print("==============")
        self.__print_tree(self.root, 0)
        print("==============")

    def __print_tree(self, node, lvl):
        if node is not None:
            self.__print_tree(node.right, lvl + 5)

            print()
            print(lvl * " ", node.key, node.value)

            self.__print_tree(node.left, lvl + 5)


if __name__ == '__main__':
    drzewko = BST()
    insert_list = {50: 'A', 15: 'B', 62: 'C', 5: 'D', 20: 'E', 58: 'F', 91: 'G', 3: 'H', 8: 'I', 37: 'J', 60: 'K',
                   24: 'L'}
    for key, value in insert_list.items():
        drzewko.insert(key, value)
    drzewko.print_tree()
    print(drzewko)
    print(drzewko.search(24))
    drzewko.insert(20, "AA")
    drzewko.insert(6, "M")
    drzewko.delete(62)
    drzewko.insert(59, "N")
    drzewko.insert(100, "P")
    drzewko.delete(8)
    drzewko.delete(15)
    drzewko.insert(55, "R")
    drzewko.delete(50)
    drzewko.delete(5)
    drzewko.delete(24)
    print(drzewko.height())
    print(drzewko)
    drzewko.print_tree()
