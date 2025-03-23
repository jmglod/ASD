# Jakub Głód 417193

import random


# funkcja zewnętrzna nadająca liczbę poziomów węzłowi (podana w poleceniu)
def randomLevel(p, maxLevel):
    lvl = 1
    while random.random() < p and lvl < maxLevel:
        lvl = lvl + 1
    return lvl


# klasa reprezentująca węzeł
class Node:

    def __init__(self, key, value, max_level, level):
        # klucz, wartość, maksymalna liczba poziomów, tablica 'wskaźników'
        # wskazująca na tyle kolejnych ile wynosi liczba poziomów
        self.key = key
        self.value = value
        self.max_level = max_level
        self.next = [None for _ in range(level)]
        # dodaję również pole 'level' gdybym potrzebował tej wartości później
        self.level = level

    # metody ułatwiające reprezentację w postaci klucz : wartość
    def __str__(self):
        return f"{self.key} : {self.value}"


class SkipList:
    # konstruktor tworzący pustą listę
    def __init__(self, max_level):
        self.max_level = max_level
        self.head = Node("head_key", "head_value", max_level, max_level)

    # szukanie elementu po kluczu
    def search(self, key):
        # możnaby dodać dodatkowy parametr dzięki któremu metoda zwracała by również
        # tablicę wskaźników poprzednika - wówczas nie trzeba by było pisać tego samego
        # w metodzie insert oraz remove, tylko użyć tego.
        current = self.head
        # zaczynamy przeszukiwanie od najwyższych poziomów
        for i in range(self.max_level - 1, -1, -1):
            # dopóki jest następca:
            while current.next[i]:
                # jeśli następca jest mniejszy, lub równy to przejdź do niego
                if current.next[i].key <= key:
                    current = current.next[i]
                else:
                    # w przeciwnym wypadku przerwij i zejdź niżej
                    break
        # po przejściu pętli jesteśmy tuż na tym, którego ewentualnie szukamy
        # zwróć poprawnie znaleziony
        if current is not None:
            if current.key == key:
                return current
        # jeśli nie znaleziono lub znaleziono zły
        return None

    def insert(self, key, value):
        # jeśli istnieje już element z takim kluczem, to go nadpisz i tyle
        this_node = self.search(key)
        if this_node is not None:
            this_node.value = value
            return
        # tablica tego na co pokazywał poprzedni względem dodawanego
        previous_pointers = [None for _ in range(self.max_level)]

        current = self.head
        # Znajdź miejsce wstawienia węzła na najniższym poziomie
        for i in range(self.max_level - 1, -1, -1):
            while current.next[i]:
                if current.next[i].key < key:
                    current = current.next[i]
                else:
                    break
            previous_pointers[i] = current

        # Stwórz nowy węzeł (klucz, wartość, losowanie poziomu)
        new = Node(key, value, self.max_level, randomLevel(0.5, self.max_level))

        # Aktualizuj wskaźniki na poprzednich i następne węzły dla poziomów nowego węzła
        for i in range(new.level):
            # nowy pokazuje tam gdzie stary pokazywał
            new.next[i] = previous_pointers[i].next[i]
            # stary pokazuje na nowego
            previous_pointers[i].next[i] = new

    def remove(self, key):
        # tablica tego na co pokazywał poprzedni względem usuwanego
        previous = [None for _ in range(self.max_level)]
        current = self.head
        # w pętli znajdź
        for i in range(self.max_level - 1, -1, -1):
            while current.next[i]:
                if current.next[i].key < key:
                    current = current.next[i]
                else:
                    break
            previous[i] = current

        current = current.next[0]
        # current jest do usunięcia
        if current and current.key == key:
            for i in range(self.max_level):
                if previous[i].next[i] == current:
                    # przepisz wskaźniki poprzedniego na to co pokazywał usuwany
                    previous[i].next[i] = current.next[i]
        else:
            print('Nie znaleziono elementu do usunięcia')

    def __str__(self):
        # metoda do printowania
        current = self.head
        result = ""
        while current:
            result += f"{str(current)}, "
            current = current.next[0]
        return f"[{result[:-2]}]"

    # tej metody nie komentuję, gdyż została podana w poleceniu
    def displayList_(self):
        node = self.head.next[0]  # pierwszy element na poziomie 0
        keys = []  # lista kluczy na tym poziomie
        while node is not None:
            keys.append(node.key)
            node = node.next[0]

        for lvl in range(self.max_level - 1, -1, -1):
            print(f"{lvl}  ", end=" ")
            node = self.head.next[lvl]
            idx = 0
            while node is not None:
                while node.key > keys[idx]:
                    print(end=5 * " ")
                    idx += 1
                idx += 1
                print(f"{node.key:2d}:{node.value:2s}", end="")
                node = node.next[lvl]
            print()


if __name__ == '__main__':
    random.seed(42)
    skipper = SkipList(6)
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    for i in range(15):
        skipper.insert(i + 1, letters[i])
    skipper.displayList_()
    print(skipper.search(2))
    skipper.insert(2, "Z")
    print(skipper.search(2))
    skipper.remove(5)
    skipper.remove(6)
    skipper.remove(7)
    print(skipper)
    skipper.insert(6, "W")
    print(skipper)
