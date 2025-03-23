# skonczone 15.03 Jakub Głód 417193

def realloc(tab, size):
    oldSize = len(tab)
    return [tab[i] if i < oldSize else None for i in range(size)]


class Queue:

    def __init__(self, size=5):
        self._tab = [None for _ in range(size)]
        self._size = size
        self._reader = 0
        self._saver = 0

    def is_empty(self):
        return True if self._saver == self._reader else False

    def peek(self):
        if self._saver == self._reader:
            return None
        else:
            return self._tab[self._reader]

    def dequeue(self):
        if self._saver == self._reader:
            return None
        else:
            temp = self._tab[self._reader]
            self._tab[self._reader] = None
            self._reader += 1
            if self._reader >= self._size:
                self._reader = 0

            return temp

    def enqueue(self, data):
        self._tab[self._saver] = data
        self._saver += 1

        if self._saver == self._size:
            self._saver = 0

        if self._saver == self._reader:
            temp = self._size
            self._tab = realloc(self._tab, self._size * 2)
            self._size *= 2
            for i in range(self._reader, temp):
                self._tab[i + temp] = self._tab[i]
                self._tab[i] = None
            self._reader += temp

    def __str__(self):
        tab_str = "["
        if self._reader == self._saver:
            return "[]"
        elif self._reader <= self._saver:
            for i in self._tab[self._reader:self._saver]:
                tab_str += str(i)
                tab_str += " ,"
        else:
            for i in self._tab[self._reader:] + self._tab[:self._saver]:
                tab_str += str(i)
                tab_str += " ,"
        tab_str = tab_str[:-2]
        return tab_str + "]"

    def wypisz(self):
        tab_str = "["
        for i in self._tab:
            tab_str += str(i)
            tab_str += ", "
        tab_str = tab_str[:-2]
        tab_str += "]"
        print(tab_str)


if __name__ == "__main__":
    kolejka = Queue()
    for i in range(1, 5):
        kolejka.enqueue(i)
    print(kolejka.dequeue())
    print(kolejka.peek())
    print(kolejka)
    for i in range(5, 9):
        kolejka.enqueue(i)
    kolejka.wypisz()
    while kolejka.peek():
        print(kolejka.dequeue())
    print(kolejka)

# JAKUB GŁÓD 417193
