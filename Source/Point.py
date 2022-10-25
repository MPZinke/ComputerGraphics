#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.10.25                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import json
import math


Point = type("Point", (), {})


class Point:
	NUMBER_REGEX = r"-?\d+(?:\.\d+)?"
	XYZ_REGEX = rf"\s*({NUMBER_REGEX})\s+({NUMBER_REGEX})\s+({NUMBER_REGEX})\s*"

	def __init__(self, *coordinates: list[int]):
		self.coordinates: list[int] = [coordinate for coordinate in coordinates]


	def __iter__(self) -> list:
		yield from self.coordinates


	def __str__(self) -> str:
		return json.dumps(list(self))


	def __len__(self) -> int:
		return len(self.coordinates)


	def __getitem__(self, index: int) -> int:
		return self.coordinates[index]


	def __abs__(self) -> Point:
		return Point(*[abs(a) for a in self])


	def __add__(left: Point, right: Point) -> Point:
		return Point(*[a + b for a, b in zip(left, right)])


	def __truediv__(left: Point, right: float) -> Point:
		return Point(*[a / right if(right) else 0 for a in left])


	def __mul__(left: Point, right: int|float|Point) -> int:
		if(isinstance(right, (int, float))):
			return Point(*[point * right for point in left])

		# Dot product
		if(isinstance(right, Point)):
			return sum([a * b for a, b in zip(left, right)])


	def __rmul__(right, left) -> int:
		return right * left


	def __pow__(left, right: float) -> Point:
		return Point(*[a ** right for a in left])


	def __sub__(left, right) -> Point:
		return Point(*[a - b for a, b in zip(left, right)])


	def magnitude(self) -> int:
		return math.sqrt(sum(value ** 2 for value in self))


	def project_onto_plane(self, plane_depth: int) -> Point:
		# (self.x / self.z) = (x / plane_depth) ~ x = (self.x * plane_depth / self.z)
		# FROM https://www.scratchapixel.com/lessons/3d-basic-rendering/computing-pixel-coordinates-of-3d-point/mathematics-computing-2d-coordinates-of-3d-points
		return Point(*[self[axis] * plane_depth / self[-1] if(self[-1]) else 0 for axis in range(len(self)-1)])


	def translate(self, *translations: list[int]) -> None:
		for i in range(len(translations)):
			self.coordinates[i] = self.coordinates[i] + translations[i]
