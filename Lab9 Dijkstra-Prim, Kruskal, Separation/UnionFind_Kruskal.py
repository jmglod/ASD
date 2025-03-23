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

    # metoda do pobrania listy krawędzi grafu
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


################### PONIŻEJ ZAKRES ZADANIA DODATKOWEGO ###################
class UnionFind:

    def __init__(self, struct_size):
        self.p = [i for i in range(struct_size)]
        self.size = [1 for _ in range(struct_size)]
        self.n = struct_size

    def find(self, v):
        return v if self.p[v] == v else self.find(self.p[v])

    def union(self, s1, s2):
        root_s1 = self.find(s1)
        root_s2 = self.find(s2)

        if root_s1 == root_s2:
            pass
        else:
            if self.size[root_s1] >= self.size[root_s2]:
                self.p[root_s2] = root_s1
                self.size[root_s1] = self.size[root_s2] + self.size[root_s1]
            else:
                self.p[root_s1] = root_s2
                self.size[root_s2] = self.size[root_s2] + self.size[root_s1]

    def same_component(self, v, w):
        root_w = self.find(w)
        root_v = self.find(v)

        return root_w == root_v


def kruskal(graph):

    mst = AdjList()
    mst_sum = 0
    edges = graph.edges()
    # sortowanie listy krawędzi
    edges.sort(key=lambda elem: elem[2])
    # print(edges)
    help_struct = UnionFind(10)

    # iterowanie po krawędziach
    for edge in edges:
        # 'odkodowanie' krawędzi
        end1 = ord(str(edge[0])) - 65
        end2 = ord(str(edge[1])) - 65
        # sprawdzenie warunku i ewentualna aktualizacja mst
        if not help_struct.same_component(end1, end2):
            mst.insert_edge(edge[0], edge[1], edge[2])
            mst_sum += edge[2]
            help_struct.union(end1, end2)

    return mst, mst_sum


if __name__ == "__main__":

    # graf testowy
    graph = AdjList()

    for v1, v2, weight in graf_mst.graf:
        graph.insert_edge(Vertex(v1), Vertex(v2), weight)

    # # Prosty test:
    #
    # test_struct = UnionFind(6)
    # test_struct.union(1, 2)
    # test_struct.union(4, 5)
    # print(f"Połączenie 1-2: {test_struct.same_component(2, 1)}\npołączenie 2-3: {test_struct.same_component(3, 2)}\npołączenie 4-5: {test_struct.same_component(5, 4)}")
    # test_struct.union(3, 1)
    # print("Po połączeniu 1-3:")
    # print(f"Połączenie 1-2: {test_struct.same_component(2, 1)}\npołączenie 2-3: {test_struct.same_component(3, 2)}\npołączenie 4-5: {test_struct.same_component(5, 4)}")

    mst1, mst_sum1 = kruskal(graph)

    printGraph(mst1)
    print("Waga krawędzi MST:", mst_sum1)
