class Himpunan:
    # Konstruktor: Inisialisasi elemen himpunan, elemen duplikat dihapus otomatis
    def __init__(self, *elemen):
        self.elemen = list(set(elemen))  # Hindarin elemen duplikat

    # Magic method untuk menghitung jumlah elemen dalam himpunan
    def __len__(self):
        return len(self.elemen)

    # Magic method untuk mengecek apakah suatu item ada dalam himpunan
    def __contains__(self, item):
        return item in self.elemen

    # Magic method untuk membandingkan apakah dua himpunan sama
    def __eq__(self, other):
        return sorted(self.elemen) == sorted(other.elemen)

    # Magic method untuk mengecek apakah himpunan ini adalah subset dari himpunan lain
    def __le__(self, other):
        return all(item in other.elemen for item in self.elemen)

    # Magic method untuk mengecek proper subset
    def __lt__(self, other):
        return self <= other and self != other

    # Magic method untuk mengecek apakah himpunan ini adalah superset dari himpunan lain
    def __ge__(self, other):
        return other <= self

    # Magic method untuk mengecek apakah dua himpunan ekuivalen (mengandung elemen yang sama)
    def __floordiv__(self, other):
        return set(self.elemen) == set(other.elemen)
    
    # Method untuk menghitung komplemen himpunan terhadap semesta
    def Komplemen(self, semesta):
        return semesta - self
    
    # Nama alias untuk method Komplemen (tidak dipakai di sini)
    def komplement(self, semesta):
        self.Komplemen(semesta)

    # Magic method untuk operasi union (gabungan), mendukung + dengan himpunan lain atau elemen tunggal
    def __add__(self, other):
        if isinstance(other, Himpunan):
            return Himpunan(*(self.elemen + other.elemen))
        else:
            return Himpunan(*(self.elemen + [other]))

    # Magic method untuk operasi difference (selisih)
    def __sub__(self, other):
        return Himpunan(*(item for item in self.elemen if item not in other.elemen))

    # Magic method untuk operasi intersection (irisan)
    def __truediv__(self, other):
        return Himpunan(*(item for item in self.elemen if item in other.elemen))

    # Magic method untuk operasi symmetric difference (selisih simetris)
    def __mul__(self, other):
        return Himpunan(*((set(self.elemen) ^ set(other.elemen))))

    # Magic method untuk menghitung Cartesian product (perkalian Kartesius)
    def __pow__(self, other):
        return Himpunan(*[(x, y) for x in self.elemen for y in other.elemen])
    
    # Method untuk menghitung himpunan kuasa (power set) sebagai list objek Himpunan
    def ListKuasa(self):
        from itertools import chain, combinations
        power_set = list(chain.from_iterable(combinations(self.elemen, r) for r in range(len(self.elemen) + 1)))
        return [Himpunan(*subset) for subset in power_set]

    # Magic method untuk menghitung jumlah elemen dalam himpunan kuasa (absolute)
    def __abs__(self):
        return len(self.ListKuasa())

    # Magic method untuk merepresentasikan himpunan sebagai string
    def __repr__(self):
        return f"{{{', '.join(map(str, sorted(self.elemen)))}}}"
