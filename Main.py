

import json
import math
import re
from tkinter import BOTH, Canvas, Frame, Tk
from typing import Union


WIDTH = 1200
HEIGHT = 900
Point = object


def to_hex(value: int) -> str:
	if(value > 255):
		return "FF"
	if(value <= 0):
		return "00"

	return f"{str(hex(value // 16))[2:]}{str(hex(value % 16))[2:]}"


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


	def __mul__(left: Point, right: Union[int, float, Point]) -> int:
		if(isinstance(right, (int, float))):
			return Point(*[point * right for point in left])

		# Dot product
		if(isinstance(right, Point)):
			return sum([a * b for a, b in zip(left, right)])


	def __rmul__(right, left) -> int:
		return right * left


	def __sub__(left, right) -> Point:
		return Point(*[a - b for a, b in zip(left, right)])


	def magnitude(self) -> int:
		return math.sqrt(sum(value ** 2 for value in self))


	def project_onto_plane(self, plane_depth: int) -> Point:
		# (self.x / self.z) = (x / plane_depth) ~ x = (self.x * plane_depth / self.z)
		# FROM https://www.scratchapixel.com/lessons/3d-basic-rendering/computing-pixel-coordinates-of-3d-point/mathematics-computing-2d-coordinates-of-3d-points

		# x = self.x * plane_depth / self.z
		# y = self.y * plane_depth / self.z
		# return Point(x, y)
		return Point(*[self[axis] * plane_depth / self[-1] if(self[-1]) else 0 for axis in range(len(self)-1)])


	def translate(self, *translations: list[int]) -> None:
		for i in range(len(translations)):
			self.coordinates[i] = self.coordinates[i] + translations[i]


class Shape:
	def __init__(self, point1, point2, *points: list, dimensions: int=2):
		self.dimensions: int = dimensions
		self.name: str = {2: "Line", 3: "Triangle", 4: "Rectangle", 5: "Pentagon"}.get(len(points), "Polygon")
		self.points: list[Point] = [point1, point2, *[point for point in points]]


	def __iter__(self) -> list:
		yield from [list(point) for point in self.points]


	def __str__(self) -> str:
		return json.dumps(list(self))


	def __len__(self) -> int:
		return len(self.points)


	def draw(self, canvas: Canvas) -> None:
		coordinates = [coordinate for point in self.project_onto_plane(300) for coordinate in point]
		inverted_points = [coordinate * (-1 if(x & 1) else 1) for x, coordinate in enumerate(coordinates)]
		centered_points = [coordinate + (HEIGHT if(x & 1) else WIDTH)/2 for x, coordinate in enumerate(inverted_points)]

		print(centered_points)

		if(len(centered_points) > 2):
			canvas.create_polygon(centered_points, fill=self.lighting(Point(-5, 5, -5), diffuse=.5), width=2)
			# canvas.create_polygon(centered_points, outline='gray', fill='', width=2)
		else:
			canvas.create_line(*centered_points, fill="white", width=2)

		canvas.pack(fill=BOTH, expand=1)


	def is_visible(self) -> bool:
		return -1 * self.normal() * self.points[0] >= 0


	def lighting(self, lighting_angle: Point=None, *, brightness: float=1, ambient=32, diffuse: float=1.0,
	  specular: float=1.0) -> str:
		if(lighting_angle is None):
			lighting_angle = Point(0, 0, -1)
		normalized_lighting_angle = lighting_angle / lighting_angle.magnitude()

		normal = self.normal()
		normalized_normal = normal / normal.magnitude()

		# FROM: http://www.csc.villanova.edu/~mdamian/Past/graphicsfa10/notes/LightingShading.pdf
		# Id = kd * I(Normal•Light)
		diffuse_intensity = diffuse * brightness * normalized_lighting_angle * normalized_normal
		# Is = ks * I(Reflection•View)^shininess
		#FROM: https://math.stackexchange.com/a/13263
		reflection = normalized_lighting_angle - 2 * (normalized_lighting_angle * normalized_normal) * normalized_normal
		# specular_intensity = specular * brightness * (reflection * Point(0,0,-1)) ** 

		hex_value: str = to_hex(int(255 * diffuse_intensity) + ambient)
		return f"#{hex_value}{hex_value}{hex_value}"


	# ———————————————————————————————————————————————— LINEAR ALGEBRA ———————————————————————————————————————————————— #

	def normal(self) -> Point:
		if(len(self) < 3):
			raise Exception("Cannot normalize a shape that is less than 3 points")

		a1, a2, a3 = list(self.points[1] - self.points[0])
		b1, b2, b3 = list(self.points[2] - self.points[1])
		# print(f"	a.x {a1}, a.y {a2}, a.z {a3}")
		# print(f"	b.x {b1}, b.y {b2}, b.z {b3}")
		# print(f"	Normal: {list(((a2 *  b3 - a3 * b2), (a3 * b1 - a1 * b3), (a1 * b2 - a2 * b1)))}")
		return Point((a2 *  b3 - a3 * b2), (a3 * b1 - a1 * b3), (a1 * b2 - a2 * b1))


	def project_onto_plane(self, plane_depth: int) -> list[Point]:
		return Shape(*[point.project_onto_plane(plane_depth) for point in self.points], dimensions=2)


	def rotate(self) -> list[Point]:
		pass


	def scale(self) -> list[Point]:
		pass


	def translate(self, *translations: list[int]):
		[point.translate(*translations) for point in self.points]


# Read Points
def read_shapes(filename: str):
	with open(filename, "r") as file:
		lines = file.readlines()

	shapes = []
	for line in lines:
		match = re.search(r"([^;]*)", line)
		line = line[:match.span()[1] if(match) else len(line)].strip()
		if(not line):
			continue

		points = [Point(int(point[0]), int(point[1]), int(point[2])) for point in re.findall(Point.XYZ_REGEX, line)]
		shapes.append(Shape(*points))

	return shapes


# Project points on to screen


def create_canvas():
	root = Tk()
	root.geometry(f"{WIDTH}x{HEIGHT}")

	frame = Frame(root)
	frame.master.title("Image")
	frame.pack(fill=BOTH, expand=1)
	canvas = Canvas(frame)

	return root, canvas


# Draw Points
def draw(shapes: list[Shape]):
	root, canvas = create_canvas()

	for shape in shapes:
		shape.translate(0, -300)
		print(list(shape))
		if(shape.is_visible()):
			shape.draw(canvas)
		print(f"	Is Visible: {str(shape.is_visible())}")

	root.mainloop()


def main():
	shapes = read_shapes("Cylinder.pnt")
	# for shape in shapes:
	# 	print(str(shape.name))
	# 	print(f"\tShape: {str(shape)}")
	# 	print(f"\tProjection: {str(shape.project_onto_plane(200))}")

	draw(shapes)



if __name__ == '__main__':
	main()
