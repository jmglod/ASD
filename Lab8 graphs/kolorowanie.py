import polska
# Jakub Głód 417193
# skonczone 30.04
# Najważniejsze, co chciałem dodać to to, że największe komplikacje wyniknęły z tego, że klasa macierzowa
# posługuje się indeksami wierzchołków, natomiast klasa listy sąsiedztwa posługuje się samymi wierzchołkami
# jako identyfikatorami. Udało się jednak napisać uniwersalny kod działający dla obu, co prezentuję w rozwiązaniu.


class Vertex:

    def __init__(self, key):
        self.key = key

    def __hash__(self):
        return hash(self.key)

    def __repr__(self):
        return f"{self.key}"

    def __str__(self):
        return f"{self.key}"

    def __eq__(self, other):
        return self.key == other.key


class AdjList:

    def __init__(self):
        self.adj_list = {}

    def is_empty(self):
        return self.adj_list == {}

    def insert_vertex(self, vertex):
        # jeśli nie ma wierzchołka, dodaje go do kluczy i przypisuje mu puste sąsiedztwo
        if vertex not in self.adj_list:
            self.adj_list[vertex] = {}

    def insert_edge(self, vertex1, vertex2, edge=1):
        # jeśli nie istnieją takie wierzchołki, dodaje je
        if vertex1 not in self.adj_list:
            self.insert_vertex(vertex1)
        if vertex2 not in self.adj_list:
            self.insert_vertex(vertex2)
        # dodaje wagę krawędzi jako daną charakterystyczną dla dwóch wierzchołków w określonej kolejności
        self.adj_list[vertex1][vertex2] = edge
        self.adj_list[vertex2][vertex1] = edge  # we dwie strony, bo graf nieskierowany

    def delete_vertex(self, vertex):
        # Jeśli wierzchołek znajduje się w liście sąsiedztwa
        if vertex in self.adj_list:
            # Iteruj po wszystkich sąsiadach wierzchołka do usunięcia
            for adj_vertex in self.adj_list[vertex].keys():
                # usuń wierzchołek z list tych sąsiadów
                del self.adj_list[adj_vertex][vertex]
            # Usuń wierzchołek i przypisanych mu sąsiadów
            del self.adj_list[vertex]

    def delete_edge(self, vertex1, vertex2):
        # Usuń krawędź między dwoma wierzchołkami
        # obsługuje graf NIEskierowany, czyli od razu usuwa krawędź w jedną oraz drugą stornę
        if vertex1 in self.adj_list and vertex2 in self.adj_list[vertex1]:
            del self.adj_list[vertex1][vertex2]
        if vertex2 in self.adj_list and vertex1 in self.adj_list[vertex2]:
            del self.adj_list[vertex2][vertex1]

    def neighbours(self, vertex_id):
        # zwraca całą zawartość listy sąsiedztwa dla danego wierzchołka
        return list(self.adj_list[vertex_id].items())

    def vertices(self):
        # zwraca listę węzłów grafu
        return list(self.adj_list.keys())

    @staticmethod  # metoda statyczna (trafna sugestia Pycharm)
    def get_vertex(vertex_id):
        # Zwróć identyfikator węzła, co jest tożsame z węzłem w tej implementacji
        return vertex_id


class AdjMat:

    def __init__(self):
        self.matrix = []  # tutaj przechowywana będzie macierz (lista list)
        self.vertices_list = []  # to będzie lista wierzchołków w grafie
        self.init_weight = 0  # to jest domyślna waga, dla której krawędź NIE istnieje

    def is_empty(self):
        return self.matrix == []

    def insert_vertex(self, vertex):
        if vertex not in self.vertices_list:  # jeśli nie ma wierzchoła w grafie
            self.vertices_list.append(vertex)  # dodaj do listy wierzchołków
            for row in self.matrix:  # dodaj kolumnę
                row.append(self.init_weight)
            self.matrix.append([self.init_weight] * len(self.vertices_list))  # dodaj wiersz

    def insert_edge(self, vertex1, vertex2, edge=1):
        # jeśli wierzchołków nie ma, dodaje je
        if vertex1 not in self.vertices_list:
            self.insert_vertex(vertex1)
        if vertex2 not in self.vertices_list:
            self.insert_vertex(vertex2)
        # lista jest uporządkowana tak jak wiersze i kolumny macierzy, więc jej indeksami się odwołujemy
        index1 = self.vertices_list.index(vertex1)
        index2 = self.vertices_list.index(vertex2)
        self.matrix[index1][index2] = edge
        self.matrix[index2][index1] = edge

    def delete_vertex(self, vertex):
        if vertex in self.vertices_list:
            # uzyskujemy indeks tego wierzchołka
            index = self.vertices_list.index(vertex)
            # usunięcie wiersza
            del self.matrix[index]
            # usunięcie kolumny
            for row in self.matrix:
                del row[index]
            # usuwamy go z listy
            self.vertices_list.remove(vertex)
            # warto dodać, że z poprzednimi wierzchołkami w liście nic się nie dzieje,
            # natomiast te kolejne uzyskują mniejsze indeksy i tak samo macierz się pomniejsza.

    def delete_edge(self, vertex1, vertex2):
        # jeśli istnieją wierzchołki, które krawędź łączy
        if vertex1 in self.vertices_list and vertex2 in self.vertices_list:
            # uzyskaj indeksy i wpisz podstawową (zerową) krawędź
            index1 = self.vertices_list.index(vertex1)
            index2 = self.vertices_list.index(vertex2)
            self.matrix[index1][index2] = self.init_weight
            self.matrix[index2][index1] = self.init_weight

    def neighbours(self, vertex_id):
        neighbs = []
        for neighb_id, weight in zip(self.vertices(), self.matrix[vertex_id]):
            if weight != self.init_weight:
                neighbs.append((neighb_id, weight))
        return neighbs

    def vertices(self):
        # równie dobrze mogłyby być liczby od 0 do len(vertices_list)
        return [self.vertices_list.index(v) for v in self.vertices_list]

    def get_vertex(self, vertex_id):
        return self.vertices_list[vertex_id]

############## WŁAŚCIWA CZĘŚĆ ZADANIA DODATKOWEGO PONIŻEJ ##############


def dfs(graph, start_vertex=None):  # algorytm ITERACYJNY
    # wybór wierzchołka startowego
    if start_vertex is None:
        start_vertex = list(graph.vertices())[0]
    # lista odwiedzionych wierzchołków (w kolejności)
    visited = []
    # stos, potrzebny do algorytmu DFS
    stack = [start_vertex]

    while stack:
        start_vertex = stack.pop(-1)    # argument "-1" jest niepotrzebny, dodaję dla czytelności
        if start_vertex not in visited:
            visited.append(start_vertex)    # odwiedź dany wierzchołek
            neigh_lst = graph.neighbours(start_vertex)  # pozyskaj jego sąsiadów
            for element in neigh_lst:
                # if element[0] not in visited: - możnaby dodać taki warunek, może on wpłynąć na zł. czasową, ale działanie jest to samo
                stack.append(element[0])    # umieść sąsiadów na stosie (potem zaczyna od ostatniego 'sąsiada'

    return visited


def bfs(graph, start_vertex=None):
    # wybór wierzchołka startowego
    if start_vertex is None:
        start_vertex = list(graph.vertices())[0]

    visited = []
    queue = [start_vertex]

    while queue:
        start_vertex = queue.pop(0)
        if start_vertex not in visited:
            visited.append(start_vertex)
            # użycie list comprehension
            queue.extend(element[0] for element in graph.neighbours(start_vertex))

    return visited


def color_graph(graph, parameter='bfs'):
    """
    Funkcja kolorująca graf
    :param graph: graf
    :param parameter: typ przeszukania grafu
    :return: Lista krotek postaci (wierzchołek, kolor-numer)
    """
    # korzysta z pomocniczych funkcji bfs() oraz dfs()
    if parameter == 'bfs':
        vertex_lst = bfs(graph)
    elif parameter == 'dfs':
        vertex_lst = dfs(graph)
    else:
        print("Entry error")
        return

    colour_dct = {}
    # dla każdego wierzchołka w liście wierzchołków
    for current_vertex in vertex_lst:
        neigh_lst = [element[0] for element in graph.neighbours(current_vertex)]
        neigh_colors = set()
        for neigh in neigh_lst:
            if neigh in colour_dct:
                neigh_colors.add(colour_dct[neigh])
        try_color = 0
        while try_color in neigh_colors:
            try_color += 1
        colour_dct[current_vertex] = try_color

    # mała komplikacja typów, bo funkcja draw_map nie przyjmuje
    # w krotkach obiektów vertex, ale stringi bez problemu
    keyval = list(colour_dct.items())
    if isinstance(keyval[0][0], int):
        keyval = [(str(graph.vertices_list[idx]), color) for idx, color in keyval]
    else:
        keyval = [(element[0].key, element[1]) for element in list(colour_dct.items())]
    return keyval


if __name__ == "__main__":

    mat_graph = AdjMat()
    for i in polska.polska:
        mat_graph.insert_vertex(Vertex(i[2]))
    for i in polska.graf:
        mat_graph.insert_edge(Vertex(i[0]), Vertex(i[1]), 1)

    list_graph = AdjList()
    for i in polska.polska:
        list_graph.insert_vertex(Vertex(i[2]))
    for i in polska.graf:
        list_graph.insert_edge(Vertex(i[0]), Vertex(i[1]), 1)

    # jak widać przeszukania BFS i DFS różnią się od siebie w zależności od tego,
    # czy wykonano je na podstawie listy sąsiedztwa, czy macierzy sąsiedztwa
    # natomiast co do zasady są to pełnoprawne ideowo algorytmy bfs oraz dfs
    color_mat_bfs = color_graph(mat_graph)      # bds to domyślny typ przeszukania
    color_mat_dfs = color_graph(mat_graph, 'dfs')
    color_lst_bfs = color_graph(list_graph)
    color_lst_dfs = color_graph(list_graph, 'dfs')
    # print(f"{color_mat_bfs}\n{color_lst_bfs}\n{color_mat_dfs}\n{color_lst_dfs}\n")
    # celowo używam macierzowego grafu i listy kolorów uzyskanej z grafu listy sąsiedztwa,
    # aby pokazać uniwersalność i wzajemną kompatybilność
    polska.draw_map(mat_graph, color_lst_dfs)
