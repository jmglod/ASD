# Jakub Głód 417193
# skończone


class Node:

    def __init__(self, key, value, right=None, left=None, height=1):
        self.key = key
        self.value = value
        self.right = right
        self.left = left
        self.height = height


class AVL:

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
        # jeśli klucz jest większy / mniejszy:
        elif node.key < key:
            return self.__rec_search(node.right, key)
        elif node.key > key:
            return self.__rec_search(node.left, key)
        # jeśli znaleziono
        else:
            return node.value

    # metoda wywołująca rekurencję od korzenia
    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            self.root = self.__rec_insert(self.root, key, value)

    def __rec_insert(self, node, key, value):
        if node is None:
            # tworzy nowy węzeł
            return Node(key, value)
        # zwykłe wpisanie jak w BST
        if key < node.key:
            # jeśli klucz mniejszy, rekurencja przechodzi do mniejszego dziecka
            node.left = self.__rec_insert(node.left, key, value)
        elif key > node.key:
            # jeśli większy, analogicznie do większego
            node.right = self.__rec_insert(node.right, key, value)
        else:
            # po wszystkich przejściach klucz jest równy obecnemu i go nadpisuje
            node.value = value

        # wszystko, co poniżej w tej metodzie dzieje się w ramach rekurencji ogonowej, podczas cofania #

        # zaktualizowanie wysokości (węzeł plus większe poddrzewo)
        node.height = 1 + max(self.__get_height(node.left), self.__get_height(node.right))
        # uzyskanie balansu węzła oraz prawego/lewego dziecka
        balance = self.__get_balance(node)
        balance_left = self.__get_balance(node.left)
        balance_right = self.__get_balance(node.right)
        # sprawdzenie czterech warunków i ewentualne serie rotacji
        if balance == -2 and balance_left <= 0:
            return self.prawa_rotacja(node)

        if balance == -2 and balance_left > 0:
            node.left = self.lewa_rotacja(node.left)
            return self.prawa_rotacja(node)

        if balance == 2 and balance_right >= 0:
            return self.lewa_rotacja(node)

        if balance == 2 and balance_right < 0:
            node.right = self.prawa_rotacja(node.right)
            return self.lewa_rotacja(node)

        return node

    def delete(self, key):
        # rozpoczęcie rekurencji od korzenia
        self.root = self.__rec_delete(self.root, key)

    def __rec_delete(self, node, key):
        if node is None:
            # w pustym nic nie znajdziemy
            print("Nie znaleziono danej do usunięcia")
            # przerwanie działania
            return
        # pierwsze dwa warunki to nic innego jak rekurencyjne szukanie węzła
        if key < node.key:
            node.left = self.__rec_delete(node.left, key)
        elif key > node.key:
            node.right = self.__rec_delete(node.right, key)
        else:
            # w tym momencie znaleźliśmy już węzeł i obsługuję te same 4 przypadki
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                # tak samo, jak w zadaniu podstawowym nie wiem, czy konieczne jest dopisanie node = None
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            # znalezienie węzła o minimalnym kluczu w prawym poddrzewie
            child = node.right
            while child.left:
                child = child.left
            # zamiana klucza i wartości usuwanego węzła z kluczem następnika
            node.key = child.key
            node.value = child.value
            # lewa gałąź zostaje taka sama
            node.right = self.__rec_delete(node.right, child.key)

        # ten sam balans i aktualizacja co w funkcji insert,
        # wszystko już się dzieje przy cofaniu rekurencji

        node.height = 1 + max(self.__get_height(node.left), self.__get_height(node.right))
        balance = self.__get_balance(node)
        balance_left = self.__get_balance(node.left)
        balance_right = self.__get_balance(node.right)

        if balance == -2 and balance_left <= 0:
            return self.prawa_rotacja(node)

        if balance == -2 and balance_left > 0:
            node.left = self.lewa_rotacja(node.left)
            return self.prawa_rotacja(node)

        if balance == 2 and balance_right >= 0:
            return self.lewa_rotacja(node)

        if balance == 2 and balance_right < 0:
            node.right = self.prawa_rotacja(node.right)
            return self.lewa_rotacja(node)

        return node

    def __str__(self):
        res = ""
        if self.root is None:
            res += "Drzewo jest puste"
        else:
            res += self.__str_rec(self.root)
        return res

    def __str_rec(self, node):
        A, B, C = "", "", ""
        if node:
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

    # Proste metody pomocnicze do pozyskania wysokości, współczynnika balansu.
    # PyCharm mi powiedział, że powinny/mogą być statyczne.
    # Nie odwołuję się wprost to node.height, bo może być None i wywali błąd, lub musiałbym tworzyć warunek
    @staticmethod
    def __get_height(node):
        if node is None:
            return 0
        return node.height

    @staticmethod
    def __get_balance(node):
        if node is None:
            return 0
        return AVL.__get_height(node.right) - AVL.__get_height(node.left)

    def prawa_rotacja(self, A):
        # umieszczenie problemu w pamięci
        B = A.left
        C = B.right
        # przeprowadzenie właściwej rotacji
        B.right = A
        A.left = C
        # aktualizacja wysokości "od dołu"
        A.height = 1 + max(self.__get_height(A.left), self.__get_height(A.right))
        B.height = 1 + max(self.__get_height(B.left), self.__get_height(B.right))
        # zwracanie "korzenia" poddrzewa
        return B

    def lewa_rotacja(self, A):
        B = A.right
        C = B.left

        B.left = A
        A.right = C

        A.height = 1 + max(self.__get_height(A.left), self.__get_height(A.right))
        B.height = 1 + max(self.__get_height(B.left), self.__get_height(B.right))

        return B


if __name__ == '__main__':
    avl = AVL()
    insert_list = {50: 'A', 15: 'B', 62: 'C', 5: 'D', 2: 'E', 1: 'F', 11: 'G', 100: 'H', 7: 'I', 6: 'J', 55: 'K',
                   52: 'L', 51: 'M', 57: 'N', 8: 'O', 9: 'P', 10: 'R', 99: 'S', 12: 'T'}

    for key, value in insert_list.items():
        avl.insert(key, value)

    avl.print_tree()
    print(avl)
    print(avl.search(10))
    avl.delete(50)
    avl.delete(52)
    avl.delete(11)
    avl.delete(57)
    avl.delete(1)
    avl.delete(12)
    avl.insert(3, 'AA')
    avl.insert(4, 'BB')
    avl.delete(7)
    avl.delete(8)

    avl.print_tree()
    print(avl)
