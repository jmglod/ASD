# Jakub Głód 417193
# skonczone 10.06
# W mojej implementacji drzewa skompresowanego zdecydowałem się
# osobne węzły na znaki końca suffixu '\0' w celu łatwiejszego liczenia
# liści w poddrzewie


class SuffixTrieNode:
    def __init__(self):
        self.children = []  # Lista par (char, SuffixTrieNode)
        # char reprezentuje krawędź drzewa pomiędzy węzłem nadrzędnym,
        # a dzieckiem

    # wyszukuje w węźle dziecko sparowane z daną krawędzią
    def get_child(self, char):
        for c, node in self.children:
            if c == char:
                return node
        # jeśli takiego nie ma, zwraca None
        return None

    # dodaje dziecko do węzła
    def add_child(self, char):
        new_node = SuffixTrieNode()
        self.children.append((char, new_node))
        return new_node


# klasa Trie posiłkująca się elementami SuffixTrieNode
class SuffixTrie:

    def __init__(self):
        self.root = SuffixTrieNode()

    # Metoda dodająca suffix
    def insert_suffix(self, suffix):
        node = self.root
        # Dla każdego znaku w suffixie
        for c in suffix:
            # Znajdź 'dziecko-literę' taką samą jak c
            child_node = node.get_child(c)
            # Jeśli nie znalazłeś, to dodaj takie nowe dziecko
            if not child_node:
                child_node = node.add_child(c)
            # Przejdź do tego dziecka dalej (znalezionego lub stworzonego)
            node = child_node

    def build_suffix_trie(self, text):
        # dodaję znak \0 na końcu tekstu (zamiast robić to w 'main')
        text = text + '\0'
        # dodaję każdy suffix do drzewa
        for i in range(len(text)):
            self.insert_suffix(text[i:])

    # Metoda licząca liście w poddrzewie (zarówno skompresowanym, jak i pełnej wielkości)
    @staticmethod
    def _count_leaves_universal(node):
        # dodaje na stos węzeł
        stack = [node]
        count = 0
        # dopóki są węzły na stosie
        while stack:
            # przechodzi po stosie (przez całe poddrzewo)
            current_node = stack.pop()
            for char, child in current_node.children:
                # zlicza liście
                if char[-1] == '\0':
                    count += 1
                # dodaje kolejne elementy poddrzewa
                else:
                    stack.append(child)
        return count

    # Metoda szukająca wzorca w drzewie nieskompresowanym
    def search(self, pattern):
        node = self.root    # zaczyna od korzenia
        # dla każdego znaku w patternie
        for c in pattern:
            # przechodzi do węzła-dziecka rozpatrywanego znaku
            node = node.get_child(c)
            if node is None:
                # jeśli taki węzeł-dziecko nie istnieje, to nie znaleziono patternu
                return 0
        # zlicz liście poddrzewa, czyli ilość wystąpień patternu
        return self._count_leaves_universal(node)

    # Metoda wyszukująca wzorzec w skompresowanym drzewie
    def search_compressed(self, pattern):
        node = self.root
        # inicjalizacja licznika na przesuwanie się po wzorcu i flagi odnalezienia
        i = 0
        found_flag = False
        # dopóki nie przeszliśmy całego wzorca
        while i < len(pattern):
            # dla każdego istniejącego dziecka
            for char, child in node.children:
                # Sprawdź, czy wzorzec zaczyna się od char
                if pattern[i:i + len(char)] == char:
                    # Przesuń licznik i do przodu o długość char
                    i += len(char)
                    # Przejdź do tego dziecka
                    node = child
                    found_flag = True
                    # przerwij pętlę for
                    break
                # sprawdź, czy wzorzec zawiera się w char
                elif pattern[i:i + len(char)] == char[:len(pattern) - i]:
                    # zwróć liczbę liści z tego poddrzewa dziecka
                    return self._count_leaves_universal(child)
            if not found_flag:
                return 0

        # jeśli pętla while przeszła 'cała', to zwróć liczbę liści poddrzewa aktualnego (ostatniego) węzła
        return self._count_leaves_universal(node)

    # Metoda kompresująca drzewo
    def compress_trie(self, node=None):
        # zacznij od korzenia
        if node is None:
            node = self.root
        # dla każdej pozycji w liście dzieci
        for i in range(len(node.children)):
            # rozpakuj znak i dziecko
            char, child = node.children[i]
            # dopóki to dziecko ma jedno dziecko i nie jest to koniec tekstu
            while len(child.children) == 1 and child.children[0][0] != '\0':
                # następny znak, wnuki od tego dziecka
                next_char, grandchild = child.children[0]
                # aktualizacja krawędzi i przypisanie wnuków jako dzieci
                char += next_char
                child = grandchild
            # nadpisanie dzieci tego węzła tym, co uzyskane w pątli while
            node.children[i] = (char, child)
            # powtórz wszystko dla nowego dziecka
            self.compress_trie(child)

    def print_tree(self):
        print("==============")
        for char_node in self.root.children:
            self._print_tree(char_node, 0)
        print("==============")

    def _print_tree(self, char_node, lvl):
        if char_node:
            char, node = char_node
            if len(node.children) > 1:
                self._print_tree(node.children[1], lvl + 5)
            print()
            print(" " * lvl + char)
            if len(node.children) > 0:
                self._print_tree(node.children[0], lvl + 5)


#############################################
### PONIŻEJ FUNKCJE DO TABLIC SUFFIXOWYCH ###
#############################################

# tworzenie tabicy suffiksowej
def build_suffix_array(text):
    # lista suffiksów z indeksami
    suffixes = [(text[i:], i) for i in range(len(text))]
    # lista posortowanych suffiksów
    sorted_suffixes = sorted(suffixes)
    # lista samych indeksów suffiksów
    suffix_array = [suffix[1] for suffix in sorted_suffixes]

    return suffix_array


# wyszukiwanie wzorca w tablicy suffixowej
def search_in_tab(text, suffix_array, pattern):
    # skrajny lewy i prawy indeks (indeks początku i końca)
    left = 0
    right = len(suffix_array) - 1

    while left <= right:
        # połowa z indeksów
        new_idx = (left + right) // 2
        # aktualnie rozpatrywany suffix
        suffix = text[suffix_array[new_idx]:]

        # jeśli suffix zaczyna się patternem
        if suffix.startswith(pattern):
            # zwróć wartość spod indeksu new_idx z tablicy suffikxów
            return suffix_array[new_idx]
        # w przeciwnym wypadku zaktualizuj odpowiednio indeks right lub left
        # porównanie na zasadzie alfabetycznej
        elif suffix > pattern:
            right = new_idx - 1
        else:
            left = new_idx + 1

    return -1


if __name__ == '__main__':
    # Przykład użycia z tekstem "banana"
    text = "banana"
    trie = SuffixTrie()

    trie.build_suffix_trie(text)
    trie.compress_trie()
    # Wyszukiwanie wzorca
    wz1 = "ban"
    wz2 = "ana"
    wz3 = "a"
    wz4 = "nna"
    wzorce = [wz1, wz2, wz3, wz4]
    for wz in wzorce:
        print(f"Liczba wystąpień '{wz}': {trie.search_compressed(wz)}")

    # wypisywanie drzewa
    trie.print_tree()

    # Konstrukcja tablicy sufiksowej
    text = "banana\0"
    suffix_array = build_suffix_array(text)
    print("Tablica sufiksowa dla 'banana\0':", suffix_array)

    # Wyszukiwanie wzorca
    for wz in wzorce:
        index = search_in_tab(text, suffix_array, wz)
        if index != -1:
            print(f"Wzorzec '{wz}' znaleziony na pozycji {index}.")
        else:
            print(f"Wzorzec '{wz}' nie znaleziony.")
