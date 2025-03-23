# Jakub Głód 417193


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


class Edge:

    def __init__(self, capacity, res_flag=False):
        if res_flag:
            self.capacity = 0  # właściwie można pominąć
            self.flow = 0  # te dwa pola ???????????
            self.residual = 0
            self.isResidual = res_flag
        else:
            self.capacity = capacity
            self.flow = 0
            self.residual = capacity
            self.isResidual = res_flag

    def __repr__(self):
        rep = str(self.capacity) + " " + str(self.flow) + " "
        rep += str(self.residual) + " " + str(self.isResidual)
        return rep

    def __str__(self):
        rep = str(self.capacity) + " " + str(self.flow) + " "
        rep += str(self.residual) + " " + str(self.isResidual)
        return rep


class AdjList:

    def __init__(self):
        self.adj_list = {}

    def is_empty(self):
        return self.adj_list == {}

    def insert_vertex(self, vertex):
        # jeśli nie ma wierzchołka, dodaje go do kluczy i przypisuje mu puste sąsiedztwo
        if vertex not in self.adj_list:
            self.adj_list[vertex] = {}

    def insert_edge(self, vertex1, vertex2, edge_data: Edge):
        # jeśli nie istnieją takie wierzchołki, dodaje je
        if vertex1 not in self.adj_list:
            self.insert_vertex(vertex1)
        if vertex2 not in self.adj_list:
            self.insert_vertex(vertex2)
        # dodaje wagę krawędzi jako daną charakterystyczną dla dwóch wierzchołków w określonej kolejności
        self.adj_list[vertex1][vertex2] = edge_data

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
        if vertex1 in self.adj_list and vertex2 in self.adj_list[vertex1]:
            del self.adj_list[vertex1][vertex2]

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
            print(n, w, end="; ")
        print()
    print("-------------------")


def bfs_ff(graph: AdjList(), start_vertex=Vertex('s')):
    # wybór wierzchołka startowego
    if start_vertex is None:
        start_vertex = list(graph.vertices())[0]
    elif isinstance(start_vertex, str):
        start_vertex = Vertex(start_vertex)

    visited = []
    parent = {}
    queue = [start_vertex]
    # parent[start_vertex] = None
    while queue:
        current_vertex = queue.pop(0)
        current_neighbours = graph.neighbours(current_vertex)
        # print(current_vertex)
        # print(current_neighbours)
        for n_vertex, n_edge in current_neighbours:
            if n_vertex not in visited:
                if n_edge.residual > 0:
                    visited.append(n_vertex)
                    parent[n_vertex] = current_vertex
                    queue.append(n_vertex)
    return parent


def find_bottleneck(graph: AdjList(), parent: dict):
    current_vertex = Vertex('t')
    bottleneck = float('inf')
    if not current_vertex in parent.keys():
        return 0
    if not parent[current_vertex]:
        return 0

    while current_vertex != Vertex('s'):
        current_parent = parent[current_vertex]
        # parent neighbour oraz parent neighbour's edge
        for p_n, p_n_e in graph.neighbours(current_parent):
            if p_n == current_vertex:
                if p_n_e.residual < bottleneck:
                    bottleneck = p_n_e.residual
        current_vertex = current_parent

    return bottleneck


def path_aug(graph: AdjList(), parent: dict, limit: (int, float)):
    current_vertex = Vertex('t')

    if not parent[current_vertex]:
        return

    while current_vertex != Vertex('s'):
        current_parent = parent[current_vertex]
        parent_edge = Edge(0)
        vertex_edge = Edge(0)
        # parent neighbour oraz parent neighbour's edge
        for p_n, p_n_e in graph.neighbours(current_parent):
            if p_n == current_vertex:
                parent_edge = p_n_e
        for c_n, c_n_e in graph.neighbours(current_parent):
            if c_n == current_parent:
                vertex_edge = c_n_e

        if not parent_edge.isResidual:
            parent_edge.flow += limit
            parent_edge.residual -= limit
            vertex_edge.residual += limit
        else:
            parent_edge.residual -= limit
            vertex_edge.flow -= limit
            vertex_edge.residual += limit

        current_vertex = current_parent


def edmonds_karp(graph):
    bfs_parent = bfs_ff(graph)
    minimal_flow = find_bottleneck(graph, bfs_parent)
    # print(f"Min_Flow = {minimal_flow}, bfs_parent = {bfs_parent}")
    # counter = 1
    while minimal_flow > 0:
        path_aug(graph, bfs_parent, minimal_flow)
        bfs_parent = bfs_ff(graph)
        if bfs_parent == {}:
            break
        # # monitoring
        # print(f"Counter = {counter}")
        # print(f"Min_Flow = {minimal_flow}, bfs_parent = {bfs_parent}")
        # counter += 1

        minimal_flow = find_bottleneck(graph, bfs_parent)


    # Poniżej niezgodność z opisem algorytmu - miały być sumowane krawędzie
    # wchodzące do ujścia, ja natomiast zdecydowałem się na prostsze sumowanie
    # krawędzie WYchodzących ze źródła
    flow = 0
    for neighb in graph.neighbours(Vertex('s')):
        flow += neighb[1].flow

    print(f"Flow = {flow}")


if __name__ == "__main__":
    # test klasy Edge
    # test_edge_residual = Edge(0, True)
    # test_edge_normal = Edge(55)
    # print(test_edge_residual)
    # print(test_edge_normal)

    # tworzenie grafów
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]
    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9), ('b', 't', 20),
              ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
    graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6),
              ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    adj_graph0 = AdjList()
    adj_graph1 = AdjList()
    adj_graph2 = AdjList()
    for v1, v2, weight in graf_0:
        adj_graph0.insert_edge(Vertex(v1), Vertex(v2), Edge(weight))
        adj_graph0.insert_edge(Vertex(v2), Vertex(v1), Edge(0, True))
    for v1, v2, weight in graf_1:
        adj_graph1.insert_edge(Vertex(v1), Vertex(v2), Edge(weight))
        adj_graph1.insert_edge(Vertex(v2), Vertex(v1), Edge(0, True))
    for v1, v2, weight in graf_2:
        adj_graph2.insert_edge(Vertex(v1), Vertex(v2), Edge(weight))
        adj_graph2.insert_edge(Vertex(v2), Vertex(v1), Edge(0, True))

    print("Graf 0: ", end='')
    edmonds_karp(adj_graph0)
    printGraph(adj_graph0)
    print("Graf 1: ", end='')
    edmonds_karp(adj_graph1)
    printGraph(adj_graph1)
    print("Graf 2: ", end='')
    edmonds_karp(adj_graph2)
    printGraph(adj_graph2)
