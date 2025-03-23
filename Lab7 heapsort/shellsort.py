# Jakub Głód 417193
# sam Shell i heapsort 19.04

import time
import random


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
            for i in range(len(tab)):
                if self.right(i) < len(tab) and self.right(i) < len(tab):
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


def my_shell(tab):
    # początkowa wartość h
    h = len(tab) // 2
    while h > 0:
        for i in range(h, len(tab)):
            temp = tab[i]  # element wyciągany jako pierwszy
            j = i - h  # indeks o h wcześniejszy
            while j - h >= -1 and tab[j] > temp:
                # przesuwanie do przodu większego elementu
                tab[j + h] = tab[j]
                j -= h  # aktualizacja indeksu h
            tab[j + h] = temp
        h = h // 2


def my_shell3(tab):
    # początkowa wartość h
    k = 0
    while (3 ** k - 1) / 2 < len(tab) / 3:
        k += 1

    h = (3 ** k - 1) // 2

    while h > 0:
        for i in range(h, len(tab)):
            temp = tab[i]   # element wyciągany jako pierwszy
            j = i - h   # indeks o h wcześniejszy
            while j - h >= -1 and tab[j] > temp:
                # przesuwanie do przodu większego elementu
                tab[j + h] = tab[j]
                j -= h  # aktualizacja indeksu h
            tab[j + h] = temp
        h = h // 3


def insertion_sort(tab):
    for i in range(1, len(tab)):
        temp = tab[i]
        j = i - 1
        # warunek jest >=, a nie <=, bo chcę uzyskać listę rosnącą
        while j >= 0 and tab[j] >= temp:
            tab[j + 1] = tab[j]
            j = j - 1
        tab[j + 1] = temp


if __name__ == '__main__':
    # DANE DO POSORTOWANIA #
    element_list = [Element(value, key) for key, value in
                    [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'),
                     (2, 'J')]]
    element_list_2 = [el for el in element_list]

    list_to_sort = [random.randint(0, 100) for _ in range(10000)]
    list_to_sort_2 = [el for el in list_to_sort]
    list_to_sort_3 = [el for el in list_to_sort]
    list_to_sort_4 = [el for el in list_to_sort]
    ############ SORTOWANIE SHELLA ############
    my_shell(element_list)

    print(element_list)
    print("Sortowanie Shella nie jest stabilne")



    ############ SORTOWANIE SHELLA ULEPSZONE ############

    insertion_sort(element_list_2)

    print(element_list_2)
    print("Sortowanie przez wstawiania również nie jest stabilne")
    ########### porównanie czasów obliczeń #######################
    t_start_shell = time.perf_counter()
    my_shell(list_to_sort)
    t_stop_shell = time.perf_counter()
    print("Czas obliczeń (shell sort1):", "{:.7f}".format(t_stop_shell - t_start_shell))
    t_start_shell2 = time.perf_counter()
    my_shell3(list_to_sort_2)
    t_stop_shell2 = time.perf_counter()
    print("Czas obliczeń (shell sort2):", "{:.7f}".format(t_stop_shell2 - t_start_shell2))
    t_start_heapsort = time.perf_counter()
    heap_to_sort = Heap(list_to_sort_3)
    while not heap_to_sort.is_empty():
        heap_to_sort.dequeue()
    t_stop_heapsort = time.perf_counter()
    print("Czas obliczeń (heapsort):", "{:.7f}".format(t_stop_heapsort - t_start_heapsort))
    t_start_insert = time.perf_counter()
    insertion_sort(list_to_sort_4)
    t_stop_insert = time.perf_counter()
    print("Czas obliczeń (insert sort):", "{:.7f}".format(t_stop_insert - t_start_insert))

    print("Widać, że czas obliczeń dla sortowania kopcowego jest około dwa razy dłuższy")
