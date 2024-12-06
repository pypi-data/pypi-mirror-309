from itertools import chain, product

class Himpunan:
    def __init__(self, elements=None):
        if elements is None:
            elements = []
        self.elements = []
        for elem in elements:
            if elem not in self.elements:  # Memastikan tidak ada perulangan dalam elemen yang ditambahkan
                self.elements.append(elem)

    # Returns the number of elements in the set (set size).
    def __len__(self):
        return len(self.elements)  # Mengembalikan jumlah elemen dalam himpunan

    # Returns True if an element is in the set, and False if it is not.
    def __contains__(self, item):
        return item in self.elements  # Mengecek apakah elemen ada dalam himpunan

    # Checks whether two sets are equal. Return Boolean
    def __eq__(self, other):
        return set(self.elements) == set(other.elements)  # Membandingkan apakah dua himpunan memiliki elemen yang sama

    # Checks whether a set is a subset of another set. Return Boolean
    def __le__(self, other):
        return all(elem in other.elements for elem in self.elements)  # Mengecek apakah himpunan ini adalah subset dari himpunan lain

    # Checks whether a set is a proper subset of another set. Return Boolean
    def __lt__(self, other):
        return self <= other and len(self) < len(other)  # Mengecek apakah himpunan ini adalah subset yang benar dari himpunan lain

    # Checks whether a set is a superset of another set. Return Boolean
    def __ge__(self, other):
        return all(elem in self.elements for elem in other.elements)  # Mengecek apakah himpunan ini adalah superset dari himpunan lain

    # Checks whether two sets are equivalent (have the same elements, even if they are in a different order). Returns Boolean
    def __floordiv__(self, other):
        return set(self.elements) == set(other.elements)  # Mengecek apakah dua himpunan memiliki elemen yang sama meskipun urutannya berbeda
    
    # Adding two sets (+)
    def __add__(self, other):
        if isinstance(other, Himpunan):
            # Menggabungkan elemen dari kedua himpunan tanpa duplikasi
            return Himpunan(self.elements + [elem for elem in other.elements if elem not in self.elements])
        else:
            raise TypeError(f"Unsupported operand type(s) for +: 'Himpunan' and '{type(other).__name__}'")  # Menggabungkan dua himpunan, menghasilkan himpunan baru tanpa duplikasi
        
    # Subtracting two sets (-)
    def __sub__(self, other):
        return Himpunan([elem for elem in self.elements if elem not in other.elements])  # Mengambil elemen yang ada di himpunan ini tetapi tidak ada di himpunan lain

    # Intersection of two sets (/)
    def __truediv__(self, other):
        return Himpunan([elem for elem in self.elements if elem in other.elements])  # Menghasilkan himpunan irisan antara dua himpunan

    # Symmetric difference between two sets (*)
    def __mul__(self, other):
        return Himpunan([elem for elem in self.elements if elem not in other.elements] +
                        [elem for elem in other.elements if elem not in self.elements])  # Menghasilkan himpunan selisih simetris antara dua himpunan

    # Cartesian product of two sets (^)
    def __pow__(self, other):
        return Himpunan([(x, y) for x in self.elements for y in other.elements])  # Menghasilkan produk kartesius antara dua himpunan

    # Complement of a set with respect to the universal set
    def complement(self, universe):
        return Himpunan([elem for elem in universe.elements if elem not in self.elements])  # Menghasilkan komplemen himpunan ini terhadap himpunan semesta

    # Returns the power set of the current set
    def PowerSet(self):
        power_set = list(chain.from_iterable(product(self.elements, repeat=r) for r in range(len(self.elements)+1)))  # Menghasilkan himpunan kuasa dari himpunan ini
        unique_power_set = []
        for subset in power_set:
            subset_set = set(subset)
            if subset_set not in unique_power_set:
                unique_power_set.append(subset_set)  # Menghindari duplikasi subset
        return [Himpunan(list(s)) for s in unique_power_set]  # Mengembalikan himpunan kuasa sebagai daftar himpunan

    # Returns the number of subsets in the power set (size of the power set)
    def __abs__(self):
        powerSet = self.PowerSet()
        return len(powerSet)

    # Adds an element to the set
    def add(self, item):
        if item not in self.elements:
            self.elements.append(item)

    # Removes an element from the set
    def remove(self, item):
        if item in self.elements:
            self.elements.remove(item)

    # String representation of the set
    def __str__(self):
        return "{" + ",".join(map(str, self.elements)) + "}"

    # In-place addition of elements to the set (+=)
    def __iadd__(self, item):
        if isinstance(item, (list, set, tuple)):
            for elem in item:
                if elem not in self.elements:
                    self.elements.append(elem)
        else:
            if item not in self.elements:
                self.elements.append(item)
        return self
