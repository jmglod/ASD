# Jakub Głód 417193
# skonczone 20.05.2024
from copy import deepcopy


class Matrix:

    def __init__(self, elem, param=0):
        if isinstance(elem, tuple):
            self.matrix = [[param] * elem[1] for _ in range(elem[0])]
        else:
            self.matrix = elem

    def __getitem__(self, key):
        return self.matrix[key]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def size(self):
        return len(self.matrix), (len(self.matrix[0]))

    def __str__(self):
        mat_str = ""
        for row in self.matrix:
            if row[0] >= 0:
                mat_str += "| " + str(row[0])
            else:
                mat_str += "|" + str(row[0])

            for number in row[1:]:
                if number >= 0:
                    mat_str += "   " + str(number)
                else:
                    mat_str += "  " + str(number)
            mat_str += " |\n"
        return mat_str

    def __add__(self, other):
        if self.size() == other.size():
            temp = Matrix(self.size())
            for row in range(temp.size()[0]):
                for col in range(temp.size()[1]):
                    temp[row][col] = self.matrix[row][col] + other.matrix[row][col]
            return temp

        else:
            raise Exception("Błędy wejścia")

    def __mul__(self, other):
        if self.size()[1] == other.size()[0]:
            temp = Matrix((self.size()[0], other.size()[1]))
            for i in range(temp.size()[0]):
                for j in range(temp.size()[1]):
                    for k in range(self.size()[1]):
                        temp[i][j] += self.matrix[i][k] * other[k][j]
            return temp

        else:
            raise Exception("Błędy wejścia")

    # metoda na potrzeby lab11
    def __eq__(self, other):
        if self.size() == other.size():
            for i in range(self.size()[0]):
                for j in range(self.size()[1]):
                    if self.matrix[i][j] != other.matrix[i][j]:
                        return False
            return True
        else:
            return False


def transpose(mat: Matrix) -> Matrix:
    temp = Matrix((mat.size()[1], mat.size()[0]))

    for i in range(mat.size()[0]):
        for j in range(mat.size()[1]):
            temp[j][i] = mat[i][j]

    return temp


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


class AdjMat:

    def __init__(self):
        self.matrix = []
        self.vertices_list = []
        self.init_weight = 0

    def is_empty(self):
        return self.matrix == []

    def insert_vertex(self, vertex):
        if vertex not in self.vertices_list:
            self.vertices_list.append(vertex)
            for row in self.matrix:
                row.append(self.init_weight)
            self.matrix.append([self.init_weight] * len(self.vertices_list))

    def insert_edge(self, vertex1, vertex2, edge=1):
        if vertex1 not in self.vertices_list:
            self.insert_vertex(vertex1)
        if vertex2 not in self.vertices_list:
            self.insert_vertex(vertex2)
        index1 = self.vertices_list.index(vertex1)
        index2 = self.vertices_list.index(vertex2)
        self.matrix[index1][index2] = edge
        self.matrix[index2][index1] = edge

    def delete_vertex(self, vertex):
        if vertex in self.vertices_list:
            index = self.vertices_list.index(vertex)
            del self.matrix[index]
            for row in self.matrix:
                del row[index]
            self.vertices_list.remove(vertex)

    def delete_edge(self, vertex1, vertex2):
        if vertex1 in self.vertices_list and vertex2 in self.vertices_list:
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
        return [self.vertices_list.index(v) for v in self.vertices_list]

    def get_vertex(self, vertex_id):
        return self.vertices_list[vertex_id]

    # metoda na potrzeby lab11
    def getMatrix(self):
        return self.matrix


def ullman_1(used_cols, current_row, matrix_m, mat_g, mat_p, liczba_wywolan=0, odnalezione=0):
    liczba_wywolan += 1
    rows, cols = matrix_m.size()

    if used_cols is None:
        used_cols = [False for _ in range(cols)]

    if current_row == rows:
        if mat_p == matrix_m * transpose(matrix_m * mat_g):
            odnalezione += 1
        return liczba_wywolan, odnalezione

    for col_idx in range(cols):
        if not used_cols[col_idx]:
            used_cols[col_idx] = True
            for i in range(cols):
                if i != col_idx:
                    matrix_m[current_row][i] = 0
                else:
                    matrix_m[current_row][i] = 1
            liczba_wywolan, odnalezione = ullman_1(used_cols, current_row + 1, matrix_m, mat_g, mat_p, liczba_wywolan,
                                                   odnalezione)
            used_cols[col_idx] = False

    return liczba_wywolan, odnalezione


def ullman_2(used_cols, current_row, matrix_m, mat_g, mat_p, liczba_wywolan=0, odnalezione=0):
    liczba_wywolan += 1
    rows, cols = matrix_m.size()

    if used_cols is None:
        used_cols = [False for _ in range(cols)]

    if current_row == rows:
        if mat_p == matrix_m * transpose(matrix_m * mat_g):
            odnalezione += 1
        return liczba_wywolan, odnalezione

    matrix_0 = deepcopy(matrix_m)

    for col_idx in range(cols):
        if not used_cols[col_idx]:
            if matrix_m[current_row][col_idx] == 1:
                used_cols[col_idx] = True

                for i in range(cols):
                    if i != col_idx:
                        matrix_0[current_row][i] = 0
                    else:
                        matrix_0[current_row][i] = 1
                liczba_wywolan, odnalezione = ullman_2(used_cols, current_row + 1, matrix_0, mat_g, mat_p, liczba_wywolan,
                                                       odnalezione)
                used_cols[col_idx] = False

    return liczba_wywolan, odnalezione


def ullman_3(used_cols, current_row, matrix_m, mat_g, mat_p, graf_G, graf_P, liczba_wywolan=0, odnalezione=0):
    liczba_wywolan += 1
    rows, cols = matrix_m.size()

    if used_cols is None:
        used_cols = [False for _ in range(cols)]

    if current_row == rows:
        if mat_p == matrix_m * transpose(matrix_m * mat_g):
            odnalezione += 1
        return liczba_wywolan, odnalezione

    matrix_0 = deepcopy(matrix_m)
    prune(matrix_m, graf_G, graf_P)

    for col_idx in range(cols):
        if not used_cols[col_idx]:
            if matrix_m[current_row][col_idx] == 1:
                used_cols[col_idx] = True

                for i in range(cols):
                    if i != col_idx:
                        matrix_0[current_row][i] = 0
                    else:
                        matrix_0[current_row][i] = 1
                liczba_wywolan, odnalezione = ullman_3(used_cols, current_row + 1, matrix_0, mat_g, mat_p, graf_G, graf_P,
                                                       liczba_wywolan, odnalezione)
                used_cols[col_idx] = False

    return liczba_wywolan, odnalezione


def prune(M, graph_g, graph_p):
    rows, cols = M.size()
    for i in range(rows):
        for j in range(cols):
            if M[i][j] == 1:
                neighb_i = graph_p.neighbours(i)
                neighb_j = graph_g.neighbours(j)
                for x in neighb_i:
                    if any(M[x[0]][y[0]] == 1 for y in neighb_j):
                        break
                else:
                    M[i][j] = 0


if __name__ == "__main__":
    ####################################### PRZYGOTOWANIE DANYCH #######################################################
    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]
    adj_mat_G = AdjMat()
    for v1, v2, weight in graph_G:
        adj_mat_G.insert_edge(v1, v2, weight)

    adj_mat_P = AdjMat()
    for v1, v2, weight in graph_P:
        adj_mat_P.insert_edge(v1, v2, weight)

    matrix_g = Matrix(adj_mat_G.getMatrix())
    matrix_p = Matrix(adj_mat_P.getMatrix())



    graph_G_size = len(adj_mat_G.vertices_list)
    graph_P_size = len(adj_mat_P.vertices_list)
    matrix_work = Matrix((graph_P_size, graph_G_size))

    matrix_work_23 = Matrix((graph_P_size, graph_G_size))

    for i in range(graph_P_size):
        for j in range(graph_G_size):
            stopien_p = sum(matrix_p[i])
            stopien_g = sum(matrix_g[j])
            if stopien_g >= stopien_p:
                matrix_work_23[i][j] = 1
    ####################################################################################################################

    # wywołanie pierwszej wersji algorytmu
    print(ullman_1(None, 0, matrix_work, matrix_g, matrix_p))

    # wywołanie drugiej wersji algorytmu
    print(ullman_2(None, 0, matrix_work_23, matrix_g, matrix_p))

    # wywołanie trzeciej wersji algorytmu
    print(ullman_3(None, 0, matrix_work_23, matrix_g, matrix_p, adj_mat_G, adj_mat_P))
