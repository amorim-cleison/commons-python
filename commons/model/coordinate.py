import numpy as np


class Coordinate:

    __AXES = (__X, __Y, __Z) = (0, 1, 2)

    def __init__(self, x, y, z, score=None, name=None):
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
        res = np.cross(self.__ext_coords(self), self.__ext_coords(other))
        return self.__from_array(res, self, other)

    def dist_to(self, other):
        """
        Calculate the distance from this coordinate to the `other`.
        """
        return np.linalg.norm(
            self.__ext_coords(self) - self.__ext_coords(other))

    def to_tuple(self):
        """
        Converts this coordinate to a tuple, in the format `(x, y, z)`.
        """
        return tuple(self.__ext_coords(self))

    def to_normalized(self):
        """
        Calculate the normalized coordinate (or vector).
        https://www.informit.com/articles/article.aspx?p=2854376&seqNum=4#:~:text=To%20normalize%20a%20vector%2C%20you,%2B%2016%20%2B%200%20%3D%2025.
        """
        from math import sqrt
        magnitude = sqrt(sum((self**2).to_tuple()))
        return (self / magnitude)

    def __from_array(self, arr, *coords):
        new_score = self.__calc_score(*coords)
        return Coordinate(arr[self.__X], arr[self.__Y], arr[self.__Z],
                          new_score)

    def __calc_score(self, *coords):
        from statistics import mean
        all_scores = [c.score for c in coords if isinstance(c, Coordinate)]
        return mean(all_scores) if all_scores else 0

    def __ext_coords(self, obj):
        if isinstance(obj, Coordinate):
            return obj._coords
        else:
            return obj

    def __add__(self, other):
        # Operators overloading:
        # https://www.programiz.com/python-programming/operator-overloading
        res = np.add(self.__ext_coords(self), self.__ext_coords(other))
        return self.__from_array(res, self, other)

    def __sub__(self, other):
        res = np.subtract(self.__ext_coords(self), self.__ext_coords(other))
        return self.__from_array(res, self, other)

    def __truediv__(self, other):
        res = np.divide(self.__ext_coords(self), self.__ext_coords(other))
        return self.__from_array(res, self, other)

    def __floordiv__(self, other):
        res = np.floor_divide(self.__ext_coords(self),
                              self.__ext_coords(other))
        return self.__from_array(res, self, other)

    def __mul__(self, other):
        res = np.multiply(self.__ext_coords(self), self.__ext_coords(other))
        return self.__from_array(res, self, other)

    def __pow__(self, exponent):
        res = np.power(self.__ext_coords(self), self.__ext_coords(exponent))
        return self.__from_array(res, self)

    def __str__(self):
        score = f"?" if self.score is None else f"{self.score:.3%}"
        name = f"unnamed" if self.name is None else self.name
        return f"{name}@({self.x}, {self.y}, {self.z}) ~ {score}"

    def __repr__(self):
        return str(self)
