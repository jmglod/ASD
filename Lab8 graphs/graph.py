import polska


# klasa reprezentująca wierzchołek
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


if __name__ == "__main__":

    list_graph = AdjList()
    for i in polska.polska:
        list_graph.insert_vertex(Vertex(i[2]))
    for i in polska.graf:
        vertex_1 = Vertex(i[0])
        vertex_2 = Vertex(i[1])
        list_graph.insert_edge(vertex_1, vertex_2)
    list_graph.delete_edge(Vertex("E"), Vertex("W"))
    list_graph.delete_vertex(Vertex("K"))

    polska.draw_map(list_graph)
    #
    # mat_graph = AdjMat()
    # for i in polska.polska:
    #     mat_graph.insert_vertex(Vertex(i[2]))
    # for i in polska.graf:
    #     vertex_1 = Vertex(str(i[0]))
    #     vertex_2 = Vertex(str(i[1]))
    #     mat_graph.insert_edge(vertex_1, vertex_2)
    # mat_graph.delete_edge(Vertex("E"), Vertex("W"))
    # mat_graph.delete_vertex(Vertex("K"))
    #
    # polska.draw_map(mat_graph)
