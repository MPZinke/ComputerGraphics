

import json
import re
from tkinter import BOTH, Canvas, Frame, Tk


WIDTH = 1200
HEIGHT = 900


class Point2D:
	def __init__(self, x: int, y: int):
		self.x: int = x
		self.y: int = y


	def __iter__(self) -> list:
		yield from [self.x, self.y]


	def __str__(self) -> str:
		return json.dumps(list(self))


class Point3D:
	NUMBER_REGEX = r"-?\d+(?:\.\d+)?"
	REGEX = rf"\s*({NUMBER_REGEX})\s+({NUMBER_REGEX})\s+({NUMBER_REGEX})\s*"

	def __init__(self, x: int, y: int, z: int):
		self.x: int = x
		self.y: int = y
		self.z: int = z


	def __iter__(self) -> list:
		yield from [self.x, self.y, self.z]


	def __str__(self) -> str:
		return json.dumps(list(self))


	def project_onto_plane(self, plane_depth: int) -> Point2D:
		# (self.x / self.z) = (x / plane_depth) ~ x = (self.x * plane_depth / self.z)
		# FROM https://www.scratchapixel.com/lessons/3d-basic-rendering/computing-pixel-coordinates-of-3d-point/mathematics-computing-2d-coordinates-of-3d-points
		x = self.x * plane_depth / self.z
		y = self.y * plane_depth / self.z
		return Point2D(x, y)



class Shape:
	def __init__(self, *points: list, dimensions: int=3):
		self.dimensions: int = dimensions
		self.name: str = {2: "Line", 3: "Triangle", 4: "Rectangle", 5: "Pentagon"}.get(len(points), "Polygon")
		self.points: list[Point3D] = [point for point in points]


	def __iter__(self) -> list:
		yield from [list(point) for point in self.points]


	def __str__(self) -> str:
		return json.dumps(list(self))


	def project_onto_plane(self, plane_depth: int) -> list[Point2D]:
		return Shape(*[point.project_onto_plane(plane_depth) for point in self.points], dimensions=2)


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

		points = [Point3D(int(point[0]), int(point[1]), int(point[2])) for point in re.findall(Point3D.REGEX, line)]
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
		coordinates = [coordinate for point in shape.project_onto_plane(10) for coordinate in point]
		coordinates = [coordinate + (HEIGHT if(x & 1) else WIDTH)/2 for x, coordinate in enumerate(coordinates)]
		canvas.create_line(*coordinates, fill="white", width=2)
	canvas.pack(fill=BOTH, expand=1)

	root.mainloop()


def main():
	shapes = read_shapes("Shapes.pnt")
	for shape in shapes:
		print(str(shape.name))
		print(f"\tShape{str(shape)}")
		print(f"\tProjection {str(shape.project_onto_plane(200))}")

	draw(shapes)



if __name__ == '__main__':
	main()
