# nieskończone
# JAKUB GŁÓD 417193

class Element:

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        string = f'{self.key}:{self.value}'
        return string


class Hash:

    def __init__(self, size, c1, c2):
        self.tab = [None for _ in range(size)]
        self.size = size
        self.c1 = c1
        self.c2 = c2

    def mix(self, key):
        temp = key
        if isinstance(temp, str):
            temp = 0
            for char in key:
                temp += ord(char)
        index = temp % self.size
        return index

    def solve_collision(self, key):
        bad_idx = self.mix(key)
        for i in range(1, self.size + 1):
            index = ((bad_idx + (self.c1 * i) + (self.c2 * i ** 2))) % self.size
            if self.tab[index] is None or self.tab[index].key == key or self.tab[index].key is None:
                return index
        return None

    def search(self, key):
        index = self.mix(key)
        if self.tab[index]:
            if self.tab[index].key == key:
                return self.tab[index].value
        else:
            for i in range(1, self.size):
                new_index = (self.mix(key) + self.c1 * i + self.c2 * (i ** 2)) % self.size
                if self.tab[new_index]:
                    if self.tab[new_index].key == key:
                        return self.tab[new_index].value
        # Jestem świadomy, że zwracanie stringa w przypadku nie odnalezienia elementu
        # w normalnych zastosowaniach byłoby tragicznym pomysłem, lecz robię (zamiast zwracać None)
        # aby "None" nie wypisywało się do konsoli, skoro i tak obsługuję taki wyjątek
            return "Nie znaleziono elementu!"
        return "Nie znaleziono elementu!"

    def insert(self, key, value):
        index = self.mix(key)
        if self.tab[index] is None or self.tab[index].key == key:
            self.tab[index] = Element(key, value)
        else:
            new_index = self.solve_collision(key)
            if new_index is not None:
                if self.tab[new_index] is None:
                    self.tab[new_index] = Element(key, value)
                    return
            print(f"Brak miejsca dla {key}:{value}")

    def remove(self, key):
        index = self.mix(key)
        if self.tab[index]:
            if self.tab[index].key == key:
                self.tab[index] = None
        else:
            for i in range(1, self.size):
                new_index = (self.mix(key) + self.c1 * i + self.c2 * (i ** 2)) % self.size
                if self.tab[new_index].key == key:
                    self.tab[new_index] = None
                    return
            print("Brak danej")

    def __str__(self):
        string = '{'
        for element in self.tab:
            if element:
                keyval = f'{element.key}:{element.value}'
                string += keyval
                string += ", "
            else:
                string += 'None, '
        string = string[:-2]
        string += '}'
        return string


def procedure1(size, c1, c2):
    hash_tab = Hash(size, c1, c2)
    keys = [1, 2, 3, 4, 5,
            18, 31, 8, 9, 10,
            11, 12, 13, 14, 15]
    values = ['A', 'B', 'C', 'D', 'E',
              'F', 'G', 'H', 'I', 'J',
              'K', 'L', 'M', 'N', 'O']
    for i in range(12):
        hash_tab.insert(keys[i], values[i])
    print(hash_tab)
    print(hash_tab.search(5))
    print(hash_tab.search(14))
    hash_tab.insert(5, 'Z')
    print(hash_tab.search(5))
    hash_tab.remove(5)
    print(hash_tab)
    print(hash_tab.search(31))


def procedure2(size, c1, c2):
    hash_tab = Hash(size, c1, c2)
    keys = [13 * i for i in range(1, 16)]
    values = ['A', 'B', 'C', 'D', 'E',
              'F', 'G', 'H', 'I', 'J',
              'K', 'L', 'M', 'N', 'O']
    for i in range(15):
        hash_tab.insert(keys[i], values[i])
    print(hash_tab)


if __name__ == '__main__':
    procedure1(13, 1, 0)
    procedure2(13, 1, 0)
    procedure2(13, 0, 1)
    procedure1(13, 0, 1)
