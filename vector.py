"""
A simple 3D Cartesian vector class.
Not particularly efficient. Not particularly thoroughly tested.

Author: David Mayo <dcmayo@gmail.com>

License: MIT
"""

import dataclasses
import functools
import math
import random
from typing import Generator, Union


epsilon = 1e-9
"""Floating point fudge factor"""


@dataclasses.dataclass(frozen=True, slots=True)
class Vector:
    """
    A simple 3D Cartesian vector class.
    Not particularly efficient. Not particularly thoroughly tested.
    """
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __neg__(self) -> "Vector":
        return Vector(
            x = -self.x,
            y = -self.y,
            z = -self.z,
        )

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(
            x = self.x + other.x,
            y = self.y + other.y,
            z = self.z + other.z,
        )
    
    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(
            x = self.x - other.x,
            y = self.y - other.y,
            z = self.z - other.z,
        )
    
    def __mul__(self, other: float) -> "Vector":
        return Vector(
            x = self.x * other,
            y = self.y * other,
            z = self.z * other,
        )
    
    def __rmul__(self, other: float) -> "Vector":
        return self * other
    
    def __truediv__(self, other: float) -> "Vector":
        return self * (1.0 / other)
    
    def __eq__(self, other: "Vector") -> bool:
        return (
            abs(self.x - other.x) < epsilon
            and abs(self.y - other.y) < epsilon
            and abs(self.z - other.z) < epsilon
        )
    
    def __ne__(self, other: "Vector") -> bool:
        return (
            self.x != other.x
            or self.y != other.y
            or self.z != other.z
        )
    
    # For casting to tuple, list, etc.
    def __iter__(self) -> Generator[float, None, None]:
        yield self.x
        yield self.y
        yield self.z

    # for vector[0], vector[-2:], etc.
    def __getitem__(self, index: Union[int, slice]) -> float:
        return tuple(self)[index]
    

    @functools.cache
    def dot(self, other: "Vector") -> float:
        return (
            self.x * other.x
            + self.y * other.y
            + self.z * other.z
        )
    
    def cross(self, other: "Vector") -> "Vector":
        """Cross product (assumes right-handed coordinate system)"""
        # Formula: https://math.libretexts.org/Bookshelves/Calculus/Calculus_(OpenStax)/12%3A_Vectors_in_Space/12.04%3A_The_Cross_Product
        x = self.y * other.z - self.z * other.y
        y = -(self.x * other.z - self.z * other.x)
        z = self.x * other.y - self.y * other.x
        return Vector(x=x, y=y, z=z)
    
    @functools.cache
    def magnitude(self) -> float:
        return math.sqrt(
            self.x ** 2
            + self.y ** 2
            + self.z ** 2
        )
    
    def distance(self, other: "Vector") -> float:
        return (other - self).magnitude()
    
    def angle(self, other: "Vector") -> float:
        """Angle in radians, 0.0 <= angle <= pi"""
        denominator = self.magnitude() * other.magnitude()
        if denominator < epsilon:
            raise ZeroDivisionError(f"One or both magnitudes too close to zero: {self!r}, {other!r}")
        cosine = self.dot(other) / denominator
        # Clamp this to [-1.0, 1.0] because of floating point problems yielding 1.000000000003 etc.
        if cosine < -1.0:
            cosine = -1.0
        if cosine > 1.0:
            cosine = 1.0
        return math.acos(cosine)
    
    def angle_degrees(self, other: "Vector") -> float:
        return math.degrees(self.angle(other))

    def rotate_towards(self, other: "Vector", angle: float) -> "Vector":
        """_summary_

        Args:
            other (Vector): _description_
            angle (float): angle IN RADIANS

        Returns:
            Vector: _description_
        """
        # Method from https://stackoverflow.com/a/22101541/11700208
        rotation_axis = self.cross(other).cross(self).normalized
        return math.cos(angle) * self + math.sin(angle) * rotation_axis
    
    def rotate_towards_degrees(self, other: "Vector", angle: float) -> "Vector":
        """_summary_

        Args:
            other (Vector): _description_
            angle (float): angle IN DEGREES

        Returns:
            Vector: _description_
        """
        return self.rotate_towards(
            other=other,
            angle=math.radians(angle)
        )

    @property
    @functools.cache
    def normalized(self) -> "Vector":
        return self / self.magnitude()
    
    def __str__(self) -> str:
        return f"<{self.x:.4f},{self.y:.4f},{self.z:.4f}>"
    
    @classmethod
    @property
    def zero(cls) -> "Vector":
        """<0, 0, 0>"""
        return Vector(0.0, 0.0, 0.0)
    
    @classmethod
    @property
    def plus_x(cls) -> "Vector":
        """<1, 0, 0>"""
        return Vector(1.0, 0.0, 0.0)
    
    @classmethod
    @property
    def zero(cls) -> "Vector":
        return Vector(0.0, 0.0, 0.0)


    @classmethod
    def random_direction(cls) -> "Vector":
        """Get a random normalized vector, from a spherically uniform distribution"""
        # Technique from https://mathworld.wolfram.com/SpherePointPicking.html
        x = random.gauss()
        y = random.gauss()
        z = random.gauss()
        return Vector(x=x, y=y, z=z).normalized
    

if __name__ == "__main__":
    vec1 = Vector(1,2,2)
    vec2 = Vector(3,4,0)

    print(f"{vec1 = }  {vec2 = }")
    print(f"{vec1.magnitude() = }  {vec2.magnitude() = }")
    print(f"{vec1.distance(vec2) = }  {vec2.distance(vec1) = }")
    print(f"{vec1 + vec2 = }")
    print(f"{vec2 + vec1 = }")
    print(f"{vec1 - vec2 = }")
    print(f"{vec2 - vec1 = }")
    print(f"{vec1 * 3.0 = }")
    print(f"{3.0 * vec1 = }")
    print(f"{vec1 / 3.0 = }")
    print(f"{vec1.normalized = }  {vec2.normalized = }")
    print(f"{vec1.dot(vec2) = }  {vec2.dot(vec1) = }")
    print(f"{tuple(vec1) = }  {tuple(vec1)}")
    print(f"{vec2[0] = }  {vec2[1] = }  {vec2[2] = }")
    print(f"{vec2[0:2] = }  {vec2[-2:] = }  {vec2[:] = }")
    print(f"{vec2 == vec1 = }  {vec2 == vec2 = }  {vec1 == vec1 = }")
    print(f"{vec1.cross(vec2) = }  {vec2.cross(vec1) = }")
    print(f"{vec1.cross(vec2) == -vec2.cross(vec1) = }")
    print(f"{vec1.angle(vec2) = }  {vec2.angle(vec1) = }")
    print(f"{vec1.angle_degrees(vec2) = }  {vec2.angle_degrees(vec1) = }")
    print(f"{vec1.angle_degrees(vec1) = }  {vec1.angle_degrees(-vec1) = }")
    for _ in range(10):
        print(f"{Vector.random_direction() = }")
    print(f"{Vector.zero = }")
    print(f"{Vector.plus_x = }")
    
    print(f"==============")
    vec1 = Vector(10,0,0)
    vec2 = Vector(0,1,0)
    print(f"{vec1.rotate_towards(vec2, math.radians(30)) = }")
    print(f"{vec1.rotate_towards_degrees(vec2, 30) = }")

    for angle in range(0, 375, 15):
        print(f"{angle}: {vec1.rotate_towards_degrees(vec2, angle)}")