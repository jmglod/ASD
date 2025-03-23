# Jakub Głód 417193
# skonczone na zajęciach 04.06

def string_compare(P, T, i=None, j=None):
    if i is None:
        i = len(P) - 1
    if j is None:
        j = len(T) - 1

    if i == 0:
        return j
    if j == 0:
        return i

    zamian = string_compare(P, T, i - 1, j - 1) + (P[i] != T[j])
    wstawien = string_compare(P, T, i, j - 1) + 1
    usuniec = string_compare(P, T, i - 1, j) + 1

    return min(zamian, wstawien, usuniec)


def string_compare_pd(P, T):
    len_P = len(P)
    len_T = len(T)

    D = [[0 for _ in range(len_T)] for _ in range(len_P)]
    for i in range(len(D)):
        D[i][0] = i
    for i in range(len(D[0])):
        D[0][i] = i

    parents = [['X' for _ in range(len_T)] for _ in range(len_P)]
    for i in range(1, len(parents)):
        parents[i][0] = 'D'
    for i in range(1, len(parents[0])):
        parents[0][i] = 'I'

    for i in range(1, len_P):
        for j in range(1, len_T):

            zamian = D[i - 1][j - 1] + (P[i] != T[j])
            wstawien = D[i][j - 1] + 1
            usuniec = D[i - 1][j] + 1

            possibilities = [zamian, wstawien, usuniec]
            min_dst = min(possibilities)
            idx = possibilities.index(min_dst)
            D[i][j] = min_dst
            if idx == 0:
                # if T[j] == P[i]: - wyszłoby chyba na to samo
                if zamian == D[i - 1][j - 1]:
                    parents[i][j] = 'M'
                else:
                    parents[i][j] = 'S'
            elif idx == 1:
                parents[i][j] = 'I'
            else:
                parents[i][j] = 'D'

    path = solve_path(parents)

    return D[-1][-1], path


def solve_path(parents):

    i = len(parents) - 1
    j = len(parents[0]) - 1
    path = []
    while parents[i][j] != 'X':
        path.append(parents[i][j])

        if parents[i][j] == 'M' or parents[i][j] == 'S':
            i -= 1
            j -= 1
        elif parents[i][j] == 'I':
            j -= 1
        elif parents[i][j] == 'D':
            i -= 1

    path.reverse()
    path = ''.join(path)
    return path


def string_compare_pd_dop_podc(P, T):
    len_P = len(P)
    len_T = len(T)

    D = [[0 for _ in range(len_T)] for _ in range(len_P)]
    for i in range(len(D)):
        D[i][0] = i

    parents = [['X' for _ in range(len_T)] for _ in range(len_P)]
    for i in range(1, len(parents)):
        parents[i][0] = 'D'

    for i in range(1, len_P):
        for j in range(1, len_T):

            zamian = D[i - 1][j - 1] + (P[i] != T[j])
            wstawien = D[i][j - 1] + 1
            usuniec = D[i - 1][j] + 1

            possibilities = [zamian, wstawien, usuniec]
            min_dst = min(possibilities)
            idx = possibilities.index(min_dst)
            D[i][j] = min_dst
            if idx == 0:
                # dodatkowe, może niezbyt efektywne sprawdzanie rodzaju M/S
                if zamian == D[i - 1][j - 1]:
                    parents[i][j] = 'M'
                else:
                    parents[i][j] = 'S'
            elif idx == 1:
                parents[i][j] = 'I'
            else:
                parents[i][j] = 'D'
    minimum = float('inf')
    min_idx = None
    for i in range(len(D[0])):
        if D[-1][i] < minimum:
            minimum = D[-1][i]
            min_idx = i

    return min_idx


def string_compare_pd_najd_wsp_sekw(P, T):
    len_P = len(P)
    len_T = len(T)

    D = [[0 for _ in range(len_T)] for _ in range(len_P)]
    for i in range(len(D)):
        D[i][0] = i
    for i in range(len(D[0])):
        D[0][i] = i

    parents = [['X' for _ in range(len_T)] for _ in range(len_P)]
    for i in range(1, len(parents)):
        parents[i][0] = 'D'
    for i in range(1, len(parents[0])):
        parents[0][i] = 'I'

    for i in range(1, len_P):
        for j in range(1, len_T):

            penalty = 0
            if P[i] != T[j]:
                penalty = 99999
            zamian = D[i - 1][j - 1] + penalty

            wstawien = D[i][j - 1] + 1
            usuniec = D[i - 1][j] + 1

            possibilities = [zamian, wstawien, usuniec]
            min_dst = min(possibilities)
            idx = possibilities.index(min_dst)
            D[i][j] = min_dst
            if idx == 0:
                if zamian == D[i - 1][j - 1]:
                    parents[i][j] = 'M'
                else:
                    parents[i][j] = 'S'
            elif idx == 1:
                parents[i][j] = 'I'
            else:
                parents[i][j] = 'D'

    # szukam ścieżki jak poprzednio, ale dodaję literkę tylko w przypadku gdy litery są zgodne
    st = []
    i = len(parents) - 1
    j = len(parents[0]) - 1

    while parents[i][j] != "X":
        if parents[i][j] == "M":
            st.append(P[i])
            i -= 1
            j -= 1
        # ten wartunek teoretycznie niepotrzebny, nigdy nie powinien się
        # pojawić - bo koszt tego 'rozwiązania' jest za duży
        elif parents[i][j] == "S":
            i -= 1
            j -= 1
        elif parents[i][j] == "I":
            j -= 1
        else:
            i -= 1

    st.reverse()
    st = ''.join(st)
    return st


if __name__ == '__main__':
    # a)
    P1 = ' kot'
    T1 = ' pies'
    print(string_compare(P1, T1))
    # b)
    P2 = ' biały autobus'
    T2 = ' czarny autokar'
    print(string_compare_pd(P2, T2)[0])
    #  c)
    P3 = ' thou shalt not'
    T3 = ' you should not'
    print(string_compare_pd(P3, T3)[1])
    # d)
    P4 = ' bin'
    T4 = ' mokeyssbanana'
    print(string_compare_pd_dop_podc(P4, T4))
    # e)
    P5 = ' democrat'
    T5 = ' republican'
    print(string_compare_pd_najd_wsp_sekw(P5, T5))
    # f)
    T6 = ' 243517698'
    P6_lst = []
    for i in range(1, len(T6)):
        P6_lst.append(T6[i])
    P6_lst.sort()
    P6 = ' ' + ''.join(P6_lst)
    print(string_compare_pd_najd_wsp_sekw(P6, T6))


