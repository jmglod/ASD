#!/usr/bin/python
# -*- coding: utf-8 -*-
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
            mat_str += "| "
            for number in row:
                mat_str += str(number) + " "
            mat_str += "|\n"
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


def chio(mat: Matrix, number: float = 1.0) -> float:
    if mat.size() == (2, 2):
        return (mat[0][0] * mat[1][1] - mat[1][0] * mat[0][1]) * number

    else:
        if mat[0][0] == 0:
            for i in range(1, mat.size()[0]):
                if mat[i][0] != 0:
                    mat[0], mat[i] = mat[i], mat[0]
                    number *= -1
                    break
    temp = Matrix((mat.size()[0] - 1, mat.size()[1] - 1))

    for i in range(temp.size()[0]):
        for j in range(temp.size()[1]):
            temp[i][j] = mat[0][0] * mat[i + 1][j + 1] - mat[i + 1][0] * mat[0][j + 1]
    print(temp)
    return chio(temp, number / (mat[0][0] ** (mat.size()[0] - 2)))


def main():
    matrix1 = Matrix([
                    [5, 1, 1, 2, 3],
                    [4, 2, 1, 7, 3],
                    [2, 1, 2, 4, 7],
                    [9, 1, 0, 7, 0],
                    [1, 4, 7, 2, 2]
                    ])
    matrix2 = Matrix([
                    [0, 1, 1, 2, 3],
                    [4, 2, 1, 7, 3],
                    [2, 1, 2, 4, 7],
                    [9, 1, 0, 7, 0],
                    [1, 4, 7, 2, 2]
                    ])
    print(chio(matrix1))
    print(chio(matrix2))


main()
