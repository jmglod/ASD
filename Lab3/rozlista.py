# JAKUB GŁÓD 417193
class Node:
    def __init__(self, size=6):
        self.tab = [None for x in range(size)]
        self.fill = 0
        self.next = None
        self.maxsize = size

class ULL:
    def __init__(self):
        self.head = None

    def get(self, index):
        current = self.head
        while current:
            if index < current.fill:
                return current.tab[index]
            index -= current.fill
            current = current.next
        return None

    def insert(self, index, data):
        # tworzy pierwszy węzeł jeśli go nie ma
        if self.head == None:
            self.head = Node()
            self.head.tab[0] = data
            self.head.fill = 1
            return
            # gotowe, bo indeks był większy niż liczba elementów

        current = self.head
        prev = None
        # dopóki nie okaże się, że indeks jest większy niż
        while current:
            # jeśli zapisujemy do tego elementu
            if index <= current.fill:
                # jeśli w elemencie jest miejsce
                if current.fill < current.maxsize:
                    # przesuwamy w prawo to co po prawo od indeksu i na nim
                    current.tab.insert(index, data)
                    current.tab = current.tab[:-1]
                    current.fill += 1
                    return
                # jeśli w tym elemencie nie ma miejsca - czyli jest pełny
                else:
                    # tworzę nowy element
                    new_node = Node()
                    current.next = new_node
                    prev = current
                    current = current.next
                    # połowa elementów idzie do nowego elementu
                    current.tab[:3] = prev.tab[3:]
                    current.fill = 3
                    prev.tab[3:] = [None for _ in range(3)]
                    prev.fill = 3
                    # listy mają teraz po 3 elementy
                    if index <= 3:
                        # przesuwamy w prawo to co po prawo od indeksu i na nim
                        prev.tab.insert(index, data)
                        prev.tab = prev.tab[:-1]
                        prev.fill += 1
                        return
                    else:
                        index -= 3
                        current.tab.insert(index, data)
                        current.tab = current.tab[:-1]
                        current.fill += 1
                        return
            # zmniejsz indeks o ilość elementów listy
            index -= current.fill
            prev = current
            current = current.next
        # jak indeks za duży
        prev.tab[prev.fill] = data
        prev.fill += 1

    def delete(self, index):
        current = self.head
        prev = None
        while current:
            if index < current.fill:
                current.tab.pop(index)
                current.tab.append(None)
                current.fill -= 1

                if current.fill < 3 and current.next:
                    # Przenieś pierwszy z kolejnego
                    following = current.next
                    temp = following.tab.pop(0)
                    following.tab.append(None)
                    following.fill -= 1
                    current.tab[current.fill] = temp
                    current.fill += 1

                    # Jeśli nie ma już więcej elementów w następnym węźle, usuń go
                    if following.fill == 0:
                        current.next = following.next
                    else:
                        # Jeśli w następnym jest mniej niż połowa
                        if following.fill < 3:
                            while following.fill:
                                temp = following.tab.pop(0)
                                following.tab.append(None)
                                following.fill -= 1
                                current.tab[current.fill] = temp
                                current.fill += 1
                            current.next = following.next
                return

            index -= current.fill
            prev = current
            current = current.next

        raise IndexError("Indeks spoza zakresu")

    def __str__(self):
        elements = []
        current = self.head
        while current:
            elements.extend(current.tab[:current.fill])
            current = current.next
        return "[" + ", ".join(str(elem) for elem in elements) + "]"

if __name__ == "__main__":
    ull = ULL()

    for i in range(1, 10):
        ull.insert(i - 1, i)
    print(ull.get(4))

    ull.insert(1, 10)
    ull.insert(8, 11)
    print(ull)
    ull.delete(1)
    ull.delete(2)
    print(ull)
