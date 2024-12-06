class Himpunan:
    """
    Kelas untuk merepresentasikan himpunan dengan berbagai operasi matematika diskrit.
    """
    
    def __init__(self, *elements):
        # Inisialisasi himpunan, menghilangkan elemen duplikat.
        self.elements = []
        for element in elements:
            if element not in self.elements:
                self.elements.append(element)
    
    def __str__(self):
        # Mengembalikan representasi string dari himpunan.
        return "{" + ", ".join(map(str, self.elements)) + "}"
    
    def __len__(self):
        # Mengembalikan jumlah elemen dalam himpunan.
        return len(self.elements)
    
    def __contains__(self, item):
        # Mengecek apakah elemen tertentu ada di dalam himpunan.
        return item in self.elements
    
    def __eq__(self, other):
        # Mengecek apakah dua himpunan memiliki elemen yang sama.
        if not isinstance(other, Himpunan):
            return False
        return sorted(self.elements) == sorted(other.elements)
    
    def __le__(self, other):
        # Mengecek apakah himpunan ini merupakan subset dari himpunan lain.
        if not isinstance(other, Himpunan):
            return False
        return all(x in other.elements for x in self.elements)
    
    def __lt__(self, other):
        # Mengecek apakah himpunan ini merupakan proper subset dari himpunan lain.
        return self <= other and len(self) < len(other)
    
    def __ge__(self, other):
        # Mengecek apakah himpunan ini merupakan superset dari himpunan lain.
        if not isinstance(other, Himpunan):
            return False
        return all(x in self.elements for x in other.elements)
    
    def __floordiv__(self, other):
        # Mengecek apakah dua himpunan ekuivalen (sama persis).
        return self == other
    
    def __truediv__(self, other):
        # Mengembalikan irisan dua himpunan.
        if not isinstance(other, Himpunan):
            raise TypeError("Operand harus berupa Himpunan")
        return Himpunan(*[x for x in self.elements if x in other.elements])
    
    def __add__(self, other):
        # Mengembalikan gabungan dua himpunan atau menambahkan elemen baru.
        if isinstance(other, Himpunan):
            return Himpunan(*(self.elements + [x for x in other.elements if x not in self.elements]))
        return Himpunan(*(self.elements + [other] if other not in self.elements else self.elements))
    
    def __sub__(self, other):
        # Mengembalikan selisih dua himpunan.
        if not isinstance(other, Himpunan):
            raise TypeError("Operand harus berupa Himpunan")
        return Himpunan(*[x for x in self.elements if x not in other.elements])
    
    def komplement(self, semesta):
        # Mengembalikan komplemen dari himpunan terhadap semesta.
        if not isinstance(semesta, Himpunan):
            raise TypeError("Semesta harus berupa Himpunan")
        return Himpunan(*[x for x in semesta.elements if x not in self.elements])
    
    def __mul__(self, other):
        # Mengembalikan selisih simetris antara dua himpunan.
        if not isinstance(other, Himpunan):
            raise TypeError("Operand harus berupa Himpunan")
        result = (self - other) + (other - self)
        return result
    
    def __pow__(self, other):
        # Mengembalikan hasil cartesian product antara dua himpunan.
        if not isinstance(other, Himpunan):
            raise TypeError("Operand harus berupa Himpunan")
        return Himpunan(*[(x, y) for x in self.elements for y in other.elements])
    
    def __abs__(self):
        # Mengembalikan jumlah anggota dalam himpunan kuasa.
        return 2 ** len(self)
    
    def ListKuasa(self):
        # Mengembalikan daftar semua subset (himpunan kuasa).
        def powerset(items):
            result = [[]]
            for item in items:
                result.extend([subset + [item] for subset in result])
            return result
        
        power_set = powerset(self.elements)
        return [Himpunan(*subset) for subset in power_set]

# Contoh penggunaan
S = Himpunan(1, 2, 3, 4, 5, 6, 7, 8, 9)  # Himpunan semesta
h1 = Himpunan(1, 2, 3)
h2 = Himpunan(3, 4, 5)

# Pengujian method-method dasar
print(len(h1))  # Output: 3
print(3 in h1)  # Output: True
print(h1 == h2)  # Output: False

# Menambah elemen
h1 += 4
print(h1)  # Output: {1, 2, 3, 4}

# Operasi himpunan
h3 = h1 / h2  # Irisan
print(h3)  # Output: {3, 4}

h4 = h1 + h2  # Gabungan
print(h4)  # Output: {1, 2, 3, 4, 5}

h5 = h1 - h2  # Selisih
print(h5)  # Output: {1, 2}

h6 = h1.komplement(S)  # Komplemen
print(h6)  # Output: {5, 6, 7, 8, 9}

# Himpunan kuasa
print(abs(h1))  # Output: 16 (2^4 karena h1 memiliki 4 elemen)
