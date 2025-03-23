# Jakub Głód 417193
# rozpoczęte

class Element:

    def __init__(self, dane, priorytet):
        self.__dane = dane
        self.__priorytet = priorytet

    def __lt__(self, other):
        return self.__priorytet < other.__priorytet

    def __gt__(self, other):
        return self.__priorytet > other.__priorytet

    def __repr__(self):
        return f"{self.__priorytet} : {self.__dane}"


class Heap:

    def __init__(self):
        self.tab = []
        self.heap_size = 0

    def is_empty(self):
        if self.heap_size != 0:
            return False
        else:
            return True

    def peek(self):
        if self.tab[0]:
            return self.tab[0]
        else:
            return None

    def dequeue(self):

        if self.heap_size != 0:
            self.heap_size -= 1
            # zamiana ostatniego z pierwszym
            self.swap(0, self.heap_size)
            self.repair(0)
            return self.tab[self.heap_size]
        else:
            return None

    def enqueue(self, priorytet_nowego):
        # dodanie i aktualizacja wielkości kopca
        if self.heap_size == len(self.tab):
            self.tab.append(priorytet_nowego)

        else:
            self.tab[self.heap_size] = priorytet_nowego
        self.heap_size += 1
        # naprawa kopca poniżej

        # indeks elementu dodawanego do kolejki
        el_idx = self.heap_size - 1
        # indeks jego rodzica
        par_idx = self.parent(el_idx)
        while self.tab[el_idx] > self.tab[par_idx] and el_idx > 0:
            self.swap(el_idx, par_idx)
            el_idx = par_idx
            par_idx = self.parent(el_idx)

    def repair(self, idx):
        right = self.right(idx)     # prawe dziecko
        left = self.left(idx)       # lewe dziecko
        max_idx = idx       # indeks miejsca do naprawy

        # jeśli lewe dziecko ma wyższy priorytet
        if left < self.heap_size and self.tab[left] > self.tab[max_idx]:
            max_idx = left
        # jeśli prawe dziecko ma wyższy priorytet
        if right < self.heap_size and self.tab[right] > self.tab[max_idx]:
            max_idx = right
        # jeśli rodzic nie był większy niż dzieci
        if max_idx != idx:
            # podmień rodzica z większym dzieckiem
            self.swap(idx, max_idx)
            # rozpocznij proces naprawy w tym kolejnym miejscu
            self.repair(max_idx)

    def swap(self, idx1, idx2):
        self.tab[idx1], self.tab[idx2] = self.tab[idx2], self.tab[idx1]

    def print_tab(self):
        print('{', end='')
        print(*self.tab[:self.heap_size], sep=', ', end=' ')
        print('}')

    def print_tree(self, idx=0, lvl=0):
        if idx < self.heap_size:
            self.print_tree(self.right(idx), lvl + 1)
            print(2 * lvl * '  ', self.tab[idx] if self.tab[idx] else None)
            self.print_tree(self.left(idx), lvl + 1)

    @staticmethod
    def left(idx):
        return 2 * (idx + 1) - 1

    @staticmethod
    def right(idx):
        return 2 * (idx + 1)

    @staticmethod
    def parent(idx):
        return (idx - 1) // 2


if __name__ == '__main__':

    heap = Heap()
    prio_list = [7, 5, 1, 2, 5, 3, 4, 8, 9]
    data_list = "GRYMOTYLA"
    for i in range(len(prio_list)):
        heap.enqueue(Element(data_list[i], prio_list[i]))
    heap.print_tree()
    heap.print_tab()
    first = heap.dequeue()
    second = heap.peek()
    print(second)
    heap.print_tab()
    print(first)
    while not heap.is_empty():
        print(heap.dequeue())
    heap.print_tab()
