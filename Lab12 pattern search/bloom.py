# Jakub  Głód
# 417193
import time

# P = 0.001 - zadana przez nas dokładność


# Dla n = 20:

# bq = 293     # - długość tablicy filtru blooma + liczba pierwsza
# k = 10      # 10 funkcji haszujących

# Dla n = 1:
# bq = 14 => 17
# k = 10

# hash_d_parameters = [256, 446, 354, 566, 838, 324, 432, 448, 672, 936]
hash_d_parameters = [588, 358, 295, 353, 541, 251, 991, 191, 859, 829]


# d to jest podstawa systemu
def hash(word, d, q):
    hw = 0
    dlugosc_wzorca = len(word)
    for i in range(dlugosc_wzorca):
        hw = (hw * d + ord(word[i])) % q
    return hw


def bloom(S, tablica_wzorcow: list[str], bq, k):
    # global hash_parameters
    bloom_tab = [0 for _ in range(bq)]
    dl_wzorca = len(tablica_wzorcow[0])
    dl_tekstu = len(S)
    find_indexes = []
    false_flags = 0
    hash_d_parameters_fcn = hash_d_parameters[0:k]
    # dla każdego wzorca
    for wz in tablica_wzorcow:
        # dla każdej wartości q funkcji hashującej
        for d in hash_d_parameters_fcn:
            one_idx = hash(wz, d, bq)
            # print(one_idx)
            bloom_tab[one_idx] = 1
            # print(q, one_idx, wz)
    # mam gotową tablicę blooma dla 10ciu f-kcji hashujących.

    h_lst = [1 for _ in range(len(hash_d_parameters_fcn))]
    # print(h_lst)
    # print(bq)
    for d, j in zip(hash_d_parameters_fcn, range(len(h_lst))):
        # print(d, j)
        for i in range(dl_wzorca - 1):  # N - jak wyżej - długość wzorca
            h_lst[j] = ((h_lst[j] * d) % bq)
    # print(h_lst)

    Sw_lst = []
    for m in range(dl_tekstu - dl_wzorca + 1):
        if m == 0:
            for d in hash_d_parameters_fcn:
                Sw_lst.append(hash(S[m:m+dl_wzorca], d, bq))
        else:
            for i, d, h in zip(range(len(Sw_lst)), hash_d_parameters_fcn, h_lst):
                Sw_lst[i] = ((d * (Sw_lst[i] - ord(S[m - 1]) * h)) + ord(S[m - 1 + dl_wzorca])) % bq
                if Sw_lst[i] < 0:
                    Sw_lst[i] += bq

        # Sw_lst_correct = []
        # for d in hash_d_parameters_fcn:
        #     Sw_lst_correct.append(hash(S[m:m+dl_wzorca], d, bq))

        # if Sw_lst != Sw_lst_correct:
        #     print("different\n", Sw_lst, "\n", Sw_lst_correct)

        find_flag = True
        for Sw in Sw_lst:
            if bloom_tab[Sw] != 1:
                find_flag = False
                break

        if find_flag:
            if S[m:m+dl_wzorca] in tablica_wzorcow:
                find_indexes.append(m)
            else:
                false_flags += 1

        # if m == 1:
        #     break

    return len(find_indexes), false_flags


if __name__ == '__main__':
    # wczytywanie pliku, definiowanie wzorców
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text).lower()
    to_find = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred', 'hobbits', 'however',
               'popular', 'nothing', 'enjoyed', 'stuffed', 'relaxed', 'himself', 'present', 'deliver', 'welcome',
               'baggins', 'further']
    to_find_one = ['gandalf']
    ############################################
    start_t1 = time.time()
    find1, false_flags_1 = bloom(S, to_find_one, 17, 2)
    stop_t1 = time.time()
    print("Wyszukiwanie jednego wzorca:", stop_t1 - start_t1)
    print("Odnaleziono:", find1, "\nFałszywe wykrycia:", false_flags_1)

    start_t2 = time.time()
    find20, false_flags_20 = bloom(S, to_find, 293, 10)
    stop_t2 = time.time()
    print("Wyszukiwanie 20stu wzorców:", stop_t2 - start_t2)
    print("Odnaleziono:", find20, "\nFałszywe wykrycia:", false_flags_20)
