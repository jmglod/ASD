# Jakub Głód 417193
# skonczone 21.04

class BNode:

    # Konstruktor pustego węzła o maksymalnej liczbie dzieci
    def __init__(self, max_child):
        self.keys = []
        self.children = []
        self.max_child = max_child

    # prosta metoda do sprawdzenia, czy jest liściem
    def is_leaf(self):
        return True if self.children == [] else False

    # wypisanie drzewa
    # inna implementacja niż w poleceniu, bo zdecydowałem się na puste listy, a nie wypełnione None
    def print_tree(self, lvl):
        if not self.is_leaf():
            # Wypisywanie węzła z dziećmi
            for j in range(len(self.keys)):
                # Wypisz dzieci mniejsze niż obecny klucz o jedno wcięcie dalej
                self.children[j].print_tree(lvl + 1)
                # wypisz ten klucz
                print("    " * lvl + str(self.keys[j]))

            # Wypisz ostatnie dziecko
            self.children[-1].print_tree(lvl + 1)

        else:
            # Wypisywanie liścia
            for j in range(len(self.keys)):
                # wypisz same klucze po wcięciach
                print("    " * lvl + str(self.keys[j]))

    # Podział węzła, zwraca środkową wartość (do wpisania do rodzica) oraz nowo utworzony węzeł
    def split(self):
        """
        Funkcja, która realizuje jedynie podział węzła, nie dodaje nowego klucza
        :return: (środkowa wartość dla rodzica, nowo utworzony węzeł do podpięcia w rodzicu jako dziecko)
        """
        # indeks podziału węzła
        split_index = self.max_child // 2 - 1
        # środkowa wartość (która pójdzie do rodzica)
        split_value = self.keys[split_index]

        # Nowy węzeł zawiera klucze prawej połowy
        new_node = BNode(self.max_child)
        new_node.keys = self.keys[split_index + 1:]
        # ograniczamy klucze starego węzła do lewej połowy
        self.keys = self.keys[:split_index]
        # powyżej należy zauważyć, że self.keys[split_index] nie ma nigdzie, bo pójdzie to do rodzica

        # jeśli węzeł miał dzieci
        if not self.is_leaf():
            # dzieci z prawej strony (większe) do nowego węzła
            new_node.children = self.children[split_index + 1:]
            # dzieci z lewej do starego węzła
            self.children = self.children[:split_index + 1]

        return split_value, new_node

    def insert(self, new_key):
        # zmienna na ewentualną informację, czy doszło do podziału (w szczególności korzenia),
        # wówczas jest to krotka ze środkowym indeksem i nowym węzłem
        split_tuple = None

        # odnalezienie indeksu w którym "powinien" znaleźć się nowy klucz
        idx = 0
        while idx < len(self.keys) and new_key > self.keys[idx]:
            idx += 1

        if not self.is_leaf():
            # funkcja woła samą siebie na odpowiednim dziecku
            split_tuple = self.children[idx].insert(new_key)

            # jeśli doszło do podziału dziecka
            if split_tuple is not None:
                # jeśli jest miejsce w węźle
                if len(self.keys) < self.max_child - 1:
                    # dodajemy do kluczy klucz z podziału
                    self.keys.append(split_tuple[0])
                    # dodajemy do dzieci dziecko z podziału
                    self.children.append(split_tuple[1])
                    # i dalej już tematu nie ma, czyli wyżej nie idzie już żaden podział
                    split_tuple = None
                # jeśli nie ma miejsca w węźle
                else:
                    # analogicznie dodajemy
                    self.keys.insert(idx, split_tuple[0])
                    self.children.insert(idx + 1, split_tuple[1])
                    # ale tym razem dokonujemy jeszcze na końcu podziału węzła
                    split_tuple = self.split()
        # jeśli dodajemy do liścia
        else:
            # po prostu dodajemy do listy kluczy
            self.keys.insert(idx, new_key)

            # Jeśli węzeł jest przepełniony, czyli zawiera
            # więcej kluczy o 1 niż może, czyli tyle kluczy ile max. ilość dzieci
            if len(self.keys) == self.max_child:
                split_tuple = self.split()

        # zwracamy informację o ewentualnym podziale węzła niżej w hierarchii
        return split_tuple

    def nowy_korzen(self, val, newEntry):
        # inicjalizacja nowego korzenia
        new_root = BNode(self.max_child)
        # węzeł ma tylko jedną wartość (środkową, z podziału starego korzenia)
        new_root.keys.append(val)
        # jako dzieci nowego korzenia zostaje obcięty już stary korzeń i węzeł utworzony z jego podziału
        new_root.children.append(self)
        new_root.children.append(newEntry)

        return new_root


class BTree:
    # konstruktor inicjujący korzeń pustym węzłem
    def __init__(self, max_child):
        self.root = BNode(max_child)
        self.max_child = max_child

    # Insert new key
    def insert(self, key):
        split_tuple = self.root.insert(key)

        # Jeśli nastąpił podział korzenia:
        if split_tuple is not None:
            self.root = self.root.nowy_korzen(split_tuple[0], split_tuple[1])

    # wyświetlanie drzewa
    def print_tree(self):
        print("==============")
        self.root.print_tree(0)
        print("==============")


if __name__ == '__main__':
    # drzewo z listy, 4 potomkowie
    tree = BTree(4)
    for i in [5, 17, 2, 14, 7, 4, 12, 1, 16, 8, 11, 9, 6, 13, 0, 3, 18 , 15, 10, 19]:
        tree.insert(i)
    tree.print_tree()
    # drzewo 0-19, 4 potomkowie
    tree2 = BTree(4)
    for i in range(20):
        tree2.insert(i)
    # drzewo 0-199, 4 potomkowie
    tree2.print_tree()
    for i in range(20, 200):
        tree2.insert(i)
    tree2.print_tree()
    # drzewo 0-199, 6 potomków
    tree3 = BTree(6)
    for i in range(200):
        tree3.insert(i)
    tree3.print_tree()
