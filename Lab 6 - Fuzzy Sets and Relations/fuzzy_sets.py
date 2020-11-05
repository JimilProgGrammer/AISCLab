import numpy as np

class FuzzySet:
    def __init__(self, iterable: any):
        self.f_set = set(iterable)
        self.f_list = list(iterable)
        self.f_len = len(iterable)
        for elem in self.f_set:
            if not isinstance(elem, tuple):
                raise TypeError("No tuples in the fuzzy set")
            if not isinstance(elem[1], float):
                raise ValueError("Probabilities not assigned to elements")

    def __or__(self, other):
        # fuzzy set union
        if len(self.f_set) != len(other.f_set):
            raise ValueError("Length of the sets is different")
        f_set = [x for x in self.f_set]
        other = [x for x in other.f_set]
        return FuzzySet([f_set[i] if f_set[i][1] > other[i][1] else other[i] for i in range(len(self))])

    def __and__(self, other):
        # fuzzy set intersection
        if len(self.f_set) != len(other.f_set):
            raise ValueError("Length of the sets is different")
        f_set = [x for x in self.f_set]
        other = [x for x in other.f_set]

        return FuzzySet([f_set[i] if f_set[i][1] < other[i][1] else other[i] for i in range(len(self))])

    def __invert__(self):
        f_set = [x for x in self.f_set]
        for indx, elem in enumerate(f_set):
            f_set[indx] = (elem[0], float(round(1 - elem[1], 2)))
        return FuzzySet(f_set)
    
    def __sub__(self, other):
        if len(self) != len(other):
            raise ValueError("Length of the sets is different")
        return self & ~other

    def __mod__(self, other):
        # cartesian product
        print(f'The size of the relation will be: {len(self)}x{len(other)} ')
        mx = self
        mi = other
        tmp = [[] for i in range(len(mx))]
        i = 0
        for x in mx:
            for y in mi:
                tmp[i].append(min(x[1], y[1]))
            i += 1
        return np.array(tmp)

    @staticmethod
    def max_min(x: np.ndarray, y: np.ndarray):
        z = []
        for x1 in x:
            for y1 in y.T:
                z.append(max(np.minimum(x1,y1)))
        return np.array(z).reshape((x.shape[0], y.shape[1]))
    
    @staticmethod
    def max_product(x: np.ndarray, y: np.ndarray):
        z = []
        for x1 in x:
            for y1 in y.T:
                z.append(max(np.multiply(x1, y1)))
        return np.array(z).reshape((x.shape[0], y.shape[1]))

    def __len__(self):
        self.f_len = sum([1 for i in self.f_set])
        return self.f_len

    def __str__(self):
        return f'{[x for x in self.f_set]}'

    def __getitem__(self, item):
        return self.f_list[item]

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

a = FuzzySet({('x1', 0.15/50), ('x2', 0.25/100), ('x3', 0.5/150), ('x4', 0.7/200)})
b = FuzzySet({('x1', 0.2/50), ('x2', 0.3/100), ('x3', 0.6/150), ('x4', 0.65/200)})
print(f'a -> {a}')
print(f'b -> {b}')
print(f'Fuzzy union: \n{a | b}')
print(f'Fuzzy inversion of b: \n{~b}')
print(f"Fuzzy inversion of a: \n {~a}")
print(f'Fuzzy intersection: \n{a & b}')
print(f'Fuzzy Subtraction: \n{a - b}')

r = np.array([[1,0.3,0.1,0],[0.2,1,0.3,0.1],[0,0.7,1,0.2],[0,0.1,0.4,1]])
s = np.array([[1,0.4],[0.5,1],[0.3,1],[0,0]])

print(f"Max Min: of \n{r} \nand \n{s}\n:\n\n")
print(FuzzySet.max_min(r, s))

print(f"Max Product: of \n{r} \nand \n{s}\n:\n\n")
print(FuzzySet.max_product(r, s))
