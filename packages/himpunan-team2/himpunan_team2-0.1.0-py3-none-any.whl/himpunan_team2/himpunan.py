class Himpunan:
    def __init__(self, elements=None):
        self.elements = []
        if elements:
            for item in elements:
                if item not in self.elements:
                    self.elements.append(item)

    def __str__(self):
        return "{" + ", ".join(map(str, self.elements)) + "}"

    # Representasi yang lebih terbaca untuk objek
    def __repr__(self):
        return self.__str__()

    # Menambah anggota ke dalam himpunan
    def add(self, item):
        if item not in self.elements:
            self.elements.append(item)

    # Mengurangi anggota dari himpunan
    def remove(self, item):
        if item in self.elements:
            self.elements.remove(item)

    # Mengembalikan jumlah elemen dalam himpunan
    def __len__(self):
        return len(self.elements)

    # Mengecek apakah suatu elemen ada dalam himpunan
    def __contains__(self, item):
        return item in self.elements

    # Mengecek apakah dua himpunan sama
    def __eq__(self, other):
        return len(self) == len(other) and all(elem in other.elements for elem in self.elements)

    # Mengecek apakah himpunan merupakan subset
    def __le__(self, other):
        return all(elem in other.elements for elem in self.elements)

    # Mengecek apakah himpunan merupakan proper subset
    def __lt__(self, other):
        return self <= other and len(self) < len(other)

    # Mengecek apakah himpunan merupakan superset
    def __ge__(self, other):
        return all(elem in self.elements for elem in other.elements)

    # Mengecek apakah himpunan ekuivalen
    def __floordiv__(self, other):
        return self.__eq__(other)

    # Irisan (Intersect)
    def __truediv__(self, other):
        intersect_elements = [elem for elem in self.elements if elem in other.elements]
        return Himpunan(intersect_elements)

    # Gabungan (Union)
    def __add__(self, other):
        union_elements = self.elements[:]
        for elem in other.elements:
            if elem not in union_elements:
                union_elements.append(elem)
        return Himpunan(union_elements)

    # Selisih (Difference)
    def __sub__(self, other):
        diff_elements = [elem for elem in self.elements if elem not in other.elements]
        return Himpunan(diff_elements)

    # Komplement
    def komplement(self, universal):
        comp_elements = [elem for elem in universal.elements if elem not in self.elements]
        return Himpunan(comp_elements)

    # Selisih Simetris (Symmetric Difference)
    def __mul__(self, other):
        sym_diff_elements = [elem for elem in self.elements if elem not in other.elements] + \
                            [elem for elem in other.elements if elem not in self.elements]
        return Himpunan(sym_diff_elements)

    # Cartesian Product
    def __pow__(self, other):
        cartesian_product = [(a, b) for a in self.elements for b in other.elements]
        return Himpunan(cartesian_product)

    # Himpunan Kuasa
    def __abs__(self):
        power_set = self.generate_power_set(self.elements)
        return [Himpunan(subset) for subset in power_set]

    # Anggota Himpunan Kuasa
    def ListKuasa(self):
        power_set_list = self.generate_power_set(self.elements)
        return [Himpunan(subset) for subset in power_set_list]

    # Fungsi untuk menghasilkan himpunan kuasa tanpa itertools
    def generate_power_set(self, s):
        power_set = [[]]
        for elem in s:
            new_subsets = [subset + [elem] for subset in power_set]
            power_set.extend(new_subsets)
        return power_set

# Contoh penggunaan kelas Himpunan
A = Himpunan([1, 2, 3])
B = Himpunan([3, 4, 5])
U = Himpunan([1, 2, 3, 4, 5, 6])

print("A:", A)
print("B:", B)
print("A ∪ B (Union):", A + B)
print("A ∩ B (Intersection):", A / B)
print("A - B (Difference):", A - B)
print("A * B (Symmetric Difference):", A * B)
print("Complement of A in U:", A.komplement(U))
print("A ⨯ B (Cartesian Product):", A ** B)
print("Power Set of A (as list of Himpunan):", abs(A))
print("Power Set of A (as list of Himpunan via ListKuasa):", A.ListKuasa())
