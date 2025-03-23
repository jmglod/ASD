# Jakub Głód 417193
#
import time


def naive_method(tekst, wzorzec):

    dlugosc_tekstu = len(tekst)
    dlugosc_wzorca = len(wzorzec)
    indeksy_poczatku_wzorca = []
    licznik_porownan = 0

    m = 0
    found = True
    # while m < dlugosc_tekstu - dlugosc_wzorca + 1:
    for m in range(dlugosc_tekstu - dlugosc_wzorca + 1):
        found = True
        for i in range(dlugosc_wzorca):
            licznik_porownan += 1
            if tekst[m + i] != wzorzec[i]:
                found = False
                break

        if found:
            # print(tekst[m:m+dlugosc_wzorca])
            # m += dlugosc_wzorca
            indeksy_poczatku_wzorca.append(m)

        # m += 1
    return indeksy_poczatku_wzorca, licznik_porownan


def hash(word, dlugosc_wzorca):
    hw = 0
    d = 256
    q = 101
    for i in range(dlugosc_wzorca):
        hw = (hw * d + ord(word[i])) % q
    return hw


def rolling_hash_method(tekst, wzorzec):
    dlugosc_tekstu = len(tekst)
    dlugosc_wzorca = len(wzorzec)
    indeksy_poczatku_wzorca = []
    licznik_porownan = 0
    kolizje = 0
    Hw = hash(wzorzec, dlugosc_wzorca)

    d = 256  # "liczba pierwsza"
    q = 101  # modulo to
    h = 1

    for i in range(dlugosc_wzorca - 1):  # N - jak wyżej - długość wzorca
        h = (h * d) % q
    print("HHHHHH:", h)
    # print(f"h dla {wzorzec}: {h}")
    # print(f"d: {d} q: {q}")
    # while m < dlugosc_tekstu - dlugosc_wzorca + 1:
    for m in range(dlugosc_tekstu - dlugosc_wzorca + 1):
        if m == 0:
            Sw = hash(tekst[0:0 + dlugosc_wzorca], dlugosc_wzorca)
        else:
            Sw = ((d * (Sw - ord(tekst[m - 1]) * h)) + ord(tekst[m - 1 + dlugosc_wzorca])) % q
            if Sw < 0:
                Sw += q

        licznik_porownan += 1
        if Sw == Hw:
            licznik_porownan += 1
            # warunek mógłby być w pętli tak jak w metodzie naiwnej,
            # wówczas byłoby więcej porównań
            if wzorzec[0: dlugosc_wzorca] == tekst[m:m + dlugosc_wzorca]:
                # print(tekst[m:m + dlugosc_wzorca])
                indeksy_poczatku_wzorca.append(m)
            else:
                kolizje += 1

        # m += 1

    return indeksy_poczatku_wzorca, licznik_porownan, kolizje


if __name__ == '__main__':

    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()

    S = ' '.join(text).lower()
    S = S
    to_find = 'time.'

    t_start = time.perf_counter()
    lista_znalezionych, liczba_porownan = naive_method(S, to_find)
    t_stop = time.perf_counter()
    print(f"{len(lista_znalezionych)}; {liczba_porownan}")
    print("Czas obliczeń - naive method:", "{:.7f}".format(t_stop - t_start), "\n")

    t_start = time.perf_counter()
    lista_znalezionych, liczba_porownan, wykryte_kolizje = rolling_hash_method(S, to_find)
    t_stop = time.perf_counter()
    print(f"{len(lista_znalezionych)}; {liczba_porownan}; {wykryte_kolizje}")
    print("Czas obliczeń - rolling hash:", "{:.7f}".format(t_stop - t_start))
