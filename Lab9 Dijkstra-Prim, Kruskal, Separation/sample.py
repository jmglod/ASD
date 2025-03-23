# Jakub Głód 417193
# skonczone 04.05.2024


# import cv2
import numpy as np
import matplotlib.pyplot as plt
from math import inf


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
        self.adj_list[vertex2][vertex1] = weight

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

    def get_vertex(self, vertex_id):
        v_list = self.vertices()
        idx = v_list.index(Vertex(vertex_id))
        return v_list[idx]

    def edges(self):
        edges_lst = []
        visited = set()

        for vertex in self.adj_list:
            for neighbour, weight in self.adj_list[vertex].items():
                if (neighbour, vertex) not in visited:
                    edges_lst.append((vertex, neighbour, weight))
                    visited.add((vertex, neighbour))

        return edges_lst


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
    sum_of_edges = 0

    intree = {x: 0 for x in vertices_list}
    distance = {x: inf for x in vertices_list}
    parent = {x: None for x in vertices_list}

    if start_vertex is None:
        start_vertex = vertices_list.pop(0)

    v = start_vertex
    mst = AdjList()
    mst.insert_vertex(v)

    while v is not None and intree[v] == 0:
        intree[v] = 1

        for k, w in graph.neighbours(v):
            if w < distance[k] and intree[k] == 0:
                distance[k] = w
                parent[k] = v

        minimal = inf
        minimal_vertex = None

        for vertex in vertices_list:

            if distance[vertex] < minimal:
                minimal = distance[vertex]
                minimal_vertex = vertex

        if minimal_vertex is None:
            break

        mst.insert_edge(parent[minimal_vertex], minimal_vertex, distance[minimal_vertex])

        sum_of_edges += distance[minimal_vertex]

        v = minimal_vertex
        vertices_list.pop(vertices_list.index(v))

    return mst, sum_of_edges


# pierwsza lepsza funkcja do przeszukiwania grafu, padło na bfs
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


if __name__ == "__main__":
    # pusty graf, wczytanie obrazka, pozyskanie jego rozmiaru
    graph = AdjList()
    # I = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)
    I = plt.imread('sample.png')
    I = np.dot(I[..., :3], [0.2989, 0.5870, 0.1140])
    rows, cols = I.shape

    # for v1, v2, weight in graf_mst.graf:
    #     graph.insert_edge(Vertex(v1), Vertex(v2), weight)

    # verts = graph.vertices()
    # print(verts)
    # print(type(verts[0]))
    # vert_dct = {str(x): x for x in verts}
    # print(vert_dct)
    # print(type(vert_dct['A']))


    # # jeden sposób na stworzenie grafu (korzysta z pola vertex.color)
    # for i in range(rows):
    #     for j in range(cols):
    #         graph.insert_vertex(Vertex(cols*j + i, I[i][j]))
    #
    # vertices_list = graph.vertices()
    # vert_dct = {str(x): x for x in vertices_list}
    #
    # for i in range(1, rows - 1):
    #     for j in range(1, cols - 1):
    #         for k in range(i - 1, i + 2):
    #             for l in range(j - 1, j + 2):
    #                 v1 = vert_dct[str(cols*j + i)]
    #                 v2 = vert_dct[str(cols*l + k)]
    #                 weight = abs(v1.color - v2.color)
    #                 graph.insert_edge(v1, v2, weight)

    # drugi sposób tworzenia grafu:
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            graph.insert_edge(Vertex(cols*j + i), Vertex(cols*(j-1) + i), abs(I[i][j] - I[i][j-1]))
            graph.insert_edge(Vertex(cols*j + i), Vertex(cols*(j+1) + i), abs(I[i][j] - I[i][j+1]))
            graph.insert_edge(Vertex(cols*j + i), Vertex(cols*j + i+1), abs(I[i][j] - I[i+1][j]))
            graph.insert_edge(Vertex(cols*j + i), Vertex(cols*j + i-1), abs(I[i][j] - I[i-1][j]))
            graph.insert_edge(Vertex(cols*j + i), Vertex(cols*(j-1) + i+1), abs(I[i][j] - I[i+1][j-1]))
            graph.insert_edge(Vertex(cols*j + i), Vertex(cols*(j+1) + i+1), abs(I[i][j] - I[i+1][j+1]))
            graph.insert_edge(Vertex(cols*j + i), Vertex(cols*(j-1) + i-1), abs(I[i][j] - I[i-1][j-1]))
            graph.insert_edge(Vertex(cols*j + i), Vertex(cols*(j+1) + i-1), abs(I[i][j] - I[i-1][j+1]))

    # graf jest utworzony dobrze
    # uzyskanie drzewa MST
    mst, _ = prim_alg(graph)
    # usunięcie z MST największej krawędzi (metody edges używam, bo stworzyłem taką
    # na potrzeby algorytmu Kruskala)
    mst_edges = mst.edges()
    mst_edges.sort(key=lambda key: key[2])
    biggest_edge = mst_edges[-1]
    mst.delete_edge(biggest_edge[0], biggest_edge[1])

    # trawersuję rozdzielone mst w celu uzyskania dwóch poddrzew
    vertices_subtree1 = bfs(mst, biggest_edge[0])
    vertices_subtree2 = bfs(mst, biggest_edge[1])

    IS = np.zeros((rows, cols), dtype='uint8')

    for vertex in vertices_subtree1:
        y = vertex.key // cols
        x = vertex.key % cols
        IS[x][y] = 60

    for vertex in vertices_subtree2:
        y = vertex.key // cols
        x = vertex.key % cols
        IS[x][y] = 210

    # wyświetlenie obrazka
    plt.imshow(IS, 'gray', vmin=0, vmax=255)
    plt.show()
