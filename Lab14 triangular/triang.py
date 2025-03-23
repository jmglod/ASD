import numpy as np
import time


class Point:
    def __init__(self, x_cor, y_cor):
        self.x = x_cor
        self.y = y_cor

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"


# odległość między dwoma punktami
def distance(p1, p2):
    return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


# obwód trójkąta (na podstawie jego 3 wierzchołków)
def obwod_trojkata(p1, p2, p3):
    return distance(p1, p2) + distance(p2, p3) + distance(p1, p3)


# Funkcja rekurencyjna do obliczania minimalnego kosztu triangulacji
def min_triangulation_rec(points, i=None, j=None):
    # przyjmuje zbiór punktów oraz indeksy początku i końca rozpatrywanego zbioru (do rekurencji)
    if i is None or j is None:
        i = 0
        j = len(points) - 1

    # jeśli indeksy się różnią o 1 (lub w ogóle wyminęły) - zwracamy dalej tylko 0
    if j <= i + 1:
        return 0

    # inicjalizacja początkowa minimum
    min_cost = float('inf')
    for k in range(i + 1, j):
        # trojkat
        tr = obwod_trojkata(points[i], points[j], points[k])
        # punkty poprzednie i następne
        part1 = min_triangulation_rec(points, i, k)
        part2 = min_triangulation_rec(points, k, j)

        cost = tr + part1 + part2

        # jeśli obliczony koszt jest lepszy, to go nadpisujemy
        min_cost = min(min_cost, cost)

    return min_cost


def min_triangulation_pd(points):
    n = len(points)
    if n < 3:
        return 0

    # macierz n x n wypełniona zerami
    D = [[0] * n for _ in range(n)]

    # przejście po możliwych długościach wielokątów (od trójkątów do największych)
    for length in range(2, n):
        # iteracja po wszystkich możliwych do zrealizowania w wielokącie podwielokątach
        for i in range(n - length):
            # i - początkowy indeks wielokąta
            # j - końcowy indeks wielokąta
            j = i + length
            # pesymistyczna inicjalizacja optymalnego kosztu
            D[i][j] = float('inf')
            # przejście po możliwych punktach pomiędzy indeksami (możliwych podziałach)
            for k in range(i + 1, j):
                # kosz triangulacji dla rozpatrywango przypadku
                cost = obwod_trojkata(points[i], points[j], points[k]) + D[i][k] + D[k][j]
                # aktualizacja, jeśli koszt jest lepszy
                D[i][j] = min(D[i][j], cost)

    return D[0][-1]


if __name__ == "__main__":
    wielokat1 = [[0, 0], [1, 0], [2, 1], [1, 2], [0, 2]]
    wielokat2 = [[0, 0], [4, 0], [5, 4], [4, 5], [2, 5], [1, 4], [0, 3], [0, 2]]
    pointlist1 = [Point(x, y) for x, y in wielokat1]
    pointlist2 = [Point(x, y) for x, y in wielokat2]

    start1 = time.time()
    result1_rec = min_triangulation_rec(pointlist1)
    stop1 = time.time()
    r1_rec_time = stop1 - start1
    start2 = time.time()
    result2_rec = min_triangulation_rec(pointlist2)
    stop2 = time.time()
    r2_rec_time = stop2 - start2
    start3 = time.time()
    result1_pd = min_triangulation_pd(pointlist1)
    stop3 = time.time()
    r1_pd_time = stop3 - start3
    start4 = time.time()
    result2_pd = min_triangulation_pd(pointlist2)
    stop4 = time.time()
    r2_pd_time = stop4 - start4

    print("Wielokąt 1:")
    print(f"Czy wynik taki sam?: {result1_rec == result1_pd}\nczas_rec: {r1_rec_time}"
          f"\nczas_pd: {r1_pd_time}\nWynik: {result1_rec}")
    print("\nWielokąt 2:")
    print(f"Czy wynik taki sam?: {result2_rec == result2_pd}\nczas_rec: {r2_rec_time}"
          f"\nczas_pd: {r2_pd_time}\nWynik: {result2_rec}")