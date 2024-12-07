from Himpunan import Himpunan
def resetHimpunan():
    return [
            Himpunan(1, 2, 3, 4, 5, 6, 7, 8, 9),
            Himpunan(1, 2, 3),
            Himpunan(3, 4, 5)
        ]


# Tes
S, h1, h2 = resetHimpunan()

print(len(h1))  # Output: 3
print(3 in h1)  # Output: True
print(h1 == h2)  # Output: False

h1 += 4  # Menambah elemen 4 ke h1
print(h1)  # Output: {1, 2, 3, 4}
S, h1, h2 = resetHimpunan()

h3 = h1 / h2  # Irisan
print(h3)  # Output: {3, 4}

h4 = h1 + h2  # Gabungan
print(h4)  # Output: {1, 2, 3, 4, 5}

h5 = h1 - h2  # Selisih
print(h5)  # Output: {1, 2]}

h6 = h1.Komplemen(S)  # Komplemen
print(h6)  # Output: {4,5,6,7,8,9}

print(abs(h1))  # 8
