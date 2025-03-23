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
            # mat_str = mat_str[:-2]
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


def transpose(mat: Matrix) -> Matrix:
    temp = Matrix((mat.size()[1], mat.size()[0]))

    for i in range(mat.size()[0]):
        for j in range(mat.size()[1]):
            temp[j][i] = mat[i][j]
    return temp


def main():
    mat1 = Matrix([[1, 0, 2],
                   [-1, 3, 1]])
    mat_ones = Matrix((2, 3), 1)
    mat2 = Matrix([[3, 1],
                   [2, 1],
                   [1, 0]])
    print(transpose(mat1))
    print(mat1 + mat_ones)
    print(mat1 * mat2)


main()
