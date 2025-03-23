# Jakub Głód 417193
# skonczone na zajęciach 30.04

import graf_mst


class Vertex:

    def __init__(self, key, color=None):
        self.key = key
        self.color = color

    def __hash__(self):
        return hash(self.key)

    def __repr__(self):
        return f"{self.key}"

    def __str__(self):
        return f"{self.key}"

    def __eq__(self, other):
        return self.key == other.key

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color


class AdjList:

    def __init__(self):
        self.adj_list = {}

    def is_empty(self):
        return self.adj_list == {}

    def insert_vertex(self, vertex):
        # jeśli nie ma wierzchołka, dodaje go do kluczy i przypisuje mu puste sąsiedztwo
        if vertex not in self.adj_list:
            self.adj_list[vertex] = {}

    def insert_edge(self, vertex1, vertex2, weight=1):
        # jeśli nie istnieją takie wierzchołki, dodaje je
        if vertex1 not in self.adj_list:
            self.insert_vertex(vertex1)
        if vertex2 not in self.adj_list:
            self.insert_vertex(vertex2)
        # dodaje wagę krawędzi jako daną charakterystyczną dla dwóch wierzchołków w określonej kolejności
        self.adj_list[vertex1][vertex2] = weight
        self.adj_list[vertex2][vertex1] = weight  # we dwie strony, bo graf nieskierowany

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
        return list((self.adj_list.keys()))

    @staticmethod  # metoda statyczna (trafna sugestia Pycharm)
    def get_vertex(vertex_id):
        # Zwróć identyfikator węzła, co jest tożsame z węzłem w tej implementacji
        return vertex_id


def printGraph(g):
    print("------GRAPH------")
    for v in g.vertices():
        print(v, end=" -> ")
        for (n, w) in g.neighbours(v):
            print(n, w, end=";")
        print()
    print("-------------------")


def prim_alg(graph, start_vertex=None):
    if not graph:
        return None
    vertices_list = graph.vertices()
    if start_vertex == None:
        start_vertex = vertices_list[0]

    sum_of_edges = 0

    intree = {x[0]: 0 for x in vertices_list}
    distance = {x[0]: float('inf') for x in vertices_list}
    parent = {x[0]: None for x in vertices_list}
    v = start_vertex
    mst = AdjList()
    mst.insert_vertex(v)

    while v != None and intree[v] == 0:
        intree[v] = 1

        for k, w in graph.neighbours(v):
            if w < distance[k] and intree[k] == 0:
                distance[k] = w
                parent[k] = v

        minimal = float('inf')
        minimal_vertex = None

        for vertex in [x for x in graph.vertices() if x not in mst.vertices()]:
            if distance[vertex] < minimal:
                minimal = distance[vertex]
                minimal_vertex = vertex

        if minimal_vertex == None:
            break

        mst.insert_edge(parent[minimal_vertex], minimal_vertex, distance[minimal_vertex])

        sum_of_edges += distance[minimal_vertex]

        v = minimal_vertex

    return mst, sum_of_edges


if __name__ == "__main__":

    graph = AdjList()

    for v1, v2, weight in graf_mst.graf:
        graph.insert_edge(v1, v2, weight)

    mst, mst_sum = prim_alg(graph)
    printGraph(mst)
    print("Waga krawędzi MST:", mst_sum)
