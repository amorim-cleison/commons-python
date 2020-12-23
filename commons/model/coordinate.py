import numpy as np


class Coordinate:

    __AXES = (__X, __Y, __Z) = (0, 1, 2)

    def __init__(self, x, y, z, score=None, name="unnamed"):
        self._coords = np.array([np.nan] * len(self.__AXES))
        self._coords[self.__X] = x
        self._coords[self.__Y] = y
        self._coords[self.__Z] = z
        self._score = score
        self._name = name

    @property
    def x(self):
        return self._coords[self.__X]

    @property
    def y(self):
        return self._coords[self.__Y]

    @property
    def z(self):
        return self._coords[self.__Z]

    @property
    def score(self):
        return self._score

    @property
    def name(self):
        return self._name

    def is_zero(self):
        return np.count_nonzero(self._coords) == 0

    def cross_product(self, other):
        """
        Cross product between this coordinate and the `other` informed.
        """
        res = np.cross(self.__val(self), self.__val(other))
        return self.__from_array(res)

    def dist_to(self, other):
        """
        Calculate the distance from this coordinate to the `other`.
        """
        return np.linalg.norm(self.__val(self) - self.__val(other))

    def to_tuple(self):
        return tuple(self.__val(self))

    def __from_array(self, arr):
        return Coordinate(arr[self.__X], arr[self.__Y], arr[self.__Z])

    def __val(self, obj):
        if isinstance(obj, Coordinate):
            return obj._coords
        else:
            return obj

    def __add__(self, other):
        # Operators overloading:
        # https://www.programiz.com/python-programming/operator-overloading
        res = np.add(self.__val(self), self.__val(other))
        return self.__from_array(res)

    def __sub__(self, other):
        res = np.subtract(self.__val(self), self.__val(other))
        return self.__from_array(res)

    def __truediv__(self, other):
        res = np.divide(self.__val(self), self.__val(other))
        return self.__from_array(res)

    def __floordiv__(self, other):
        res = np.floor_divide(self.__val(self), self.__val(other))
        return self.__from_array(res)

    def __mul__(self, other):
        res = np.multiply(self.__val(self), self.__val(other))
        return self.__from_array(res)

    def __pow__(self, exponent):
        res = np.power(self.__val(self), self.__val(exponent))
        return self.__from_array(res)

    def __str__(self):
        score = f"?" if self.score is None else f"{self.score:.3%}"
        return f"{self.name}@({self.x}, {self.y}, {self.z}) ~ {score}"

    def __repr__(self):
        return str(self)
