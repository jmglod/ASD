# Jakub Głód 417193
import random
import time


class Element:

    def __init__(self, dane, priorytet):
        self.__dane = dane
        self.__priorytet = priorytet

    def __lt__(self, other):
        return self.__priorytet < other.__priorytet

    def __gt__(self, other):
        return self.__priorytet > other.__priorytet

    def __le__(self, other):
        return self.__priorytet <= other.__priorytet

    def __ge__(self, other):
        return self.__priorytet >= other.__priorytet

    def __repr__(self):
        return f"{self.__priorytet} : {self.__dane}"


class Heap:

    def __init__(self, tab=None):
        if tab is None:
            self.tab = []
            self.heap_size = 0
        else:
            self.tab = tab
            self.heap_size = len(tab)
            for i in range(len(tab) // 2 - 1, -1, -1):
                self.repair(i)

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

    # metoda naprawiająca, o której mowa
    def repair(self, idx):
        right = self.right(idx)  # prawe dziecko
        left = self.left(idx)  # lewe dziecko
        max_idx = idx  # indeks miejsca do naprawy

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
        print(*self.tab[:self.heap_size], sep=', ', end='')
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


# funkcja realizująca sortowanie przez wybieranie
def wybieranie_swap(tab):
    for i in range(len(tab)):
        m = i
        for j in range(i + 1, len(tab)):
            if tab[j] < tab[m]:
                m = j
        tab[i], tab[m] = tab[m], tab[i]


def wybieranie_shift(tab):
    for i in range(len(tab)):
        m = i
        for j in range(i + 1, len(tab)):
            if tab[j] < tab[m]:
                m = j
        temp = tab.pop(m)
        tab.insert(i, temp)


if __name__ == '__main__':
    # DANE DO POSORTOWANIA #
    element_list = [Element(value, key) for key, value in
                    [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'),
                     (2, 'J')]]
    element_list_swap = [el for el in element_list]
    element_list_shift = [el for el in element_list]

    list_to_sort = [random.randint(0, 100) for _ in range(10000)]
    list_to_sort_swap = [el for el in list_to_sort]
    list_to_sort_shift = [el for el in list_to_sort]
    ########################
    # SORTOWANIE KOPCOWE
    heap = Heap(element_list)
    heap.print_tab()
    heap.print_tree()
    # sortowanie
    while not heap.is_empty():
        heap.dequeue()

    print(element_list)
    print("Sortowanie kopcowe nie jest stabilne (elementy w złej kolejności A, E, H, B)")

    t_start = time.perf_counter()

    heap = Heap(list_to_sort)
    while not heap.is_empty():
        heap.dequeue()

    t_stop = time.perf_counter()
    print(list_to_sort)
    print("Czas obliczeń (heapsort):", "{:.7f}".format(t_stop - t_start))
    print("### sortowanie przez wybieranie poniżej ###")

    # SORTOWANIE SWAP
    wybieranie_swap(element_list_swap)

    print(element_list_swap)
    print("Sotowanie przez wybieranie z zamienianiem nie jest stabilne")

    t_start_swap = time.perf_counter()
    wybieranie_swap(list_to_sort_swap)
    t_stop_swap = time.perf_counter()
    print("Czas obliczeń (swap):", "{:.7f}".format(t_stop_swap - t_start_swap))

    # SORTOWANIE SHIFT
    wybieranie_shift(element_list_shift)

    print(element_list_shift)
    print("Sotowanie przez wybieranie z przesuwaniem jest stabilne")

    t_start_shift = time.perf_counter()
    wybieranie_shift(list_to_sort_shift)
    t_stop_shift = time.perf_counter()
    print("Czas obliczeń (shift):", "{:.7f}".format(t_stop_shift - t_start_shift))
