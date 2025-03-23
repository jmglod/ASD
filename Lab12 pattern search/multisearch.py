# Jakub Głód 417193
# wersja opisana pseudokodem - 23.05


def hash_pseudocode(word, dlugosc_wzorca, d=256, q=101):
    hw = 0
    for i in range(dlugosc_wzorca):
        hw = (hw * d + ord(word[i])) % q
    return hw


def RabinKarpSet_pseudocode(string, subs, N):
    M = len(string)
    start_idxs = []
    comparisons = 0
    collisions = 0
    hsubs = {hash_pseudocode(sub, N) for sub in subs}

    d = 256
    q = 101
    h = 1
    for i in range(N - 1):
        h = (h * d) % q

    for m in range(M - N + 1):
        if m == 0:
            Sw = hash_pseudocode(string[0:0 + N], N)
        else:
            Sw = ((d * (Sw - ord(string[m - 1]) * h)) + ord(string[m - 1 + N])) % q
            if Sw < 0:
                Sw += q

        comparisons += 1
        if Sw in hsubs:
            comparisons += 1
            if string[m:m + N] in subs:
                start_idxs.append(m)
            else:
                collisions += 1

    return start_idxs, comparisons, collisions


if __name__ == '__main__':
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()

    S = ' '.join(text).lower()

    to_find = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred', 'hobbits', 'however',
               'popular', 'nothing', 'enjoyed', 'stuffed', 'relaxed', 'himself', 'present', 'deliver', 'welcome',
               'baggins', 'further']

    to_find_len = len(to_find[0])

    a, b, c = RabinKarpSet_pseudocode(S, to_find, to_find_len)

    print(f"wykrycia: {len(a)}; porównania {b}; kolizje {c}")
