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
from tkinter import BOTH, Canvas, Frame, Tk


from Point import Point
from Util import to_hex


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


	def draw(self, canvas: Canvas, lighting: Point, diffuse: float=.5) -> None:
		from Main import HEIGHT, WIDTH

		coordinates = [coordinate for point in self.project_onto_plane(300) for coordinate in point]
		inverted_points = [coordinate * (-1 if(x & 1) else 1) for x, coordinate in enumerate(coordinates)]
		centered_points = [coordinate + (HEIGHT if(x & 1) else WIDTH)/2 for x, coordinate in enumerate(inverted_points)]

		if(len(centered_points) > 2):
			lighting: str = self.lighting(lighting, diffuse=diffuse)
			canvas.create_polygon(centered_points, fill=lighting, width=2)

		else:
			canvas.create_line(*centered_points, fill="white", width=2)

		canvas.pack(fill=BOTH, expand=1)


	def is_visible(self) -> bool:
		return -1 * self.normal() * self.points[0] >= 0


	def lighting(self, lighting_angle: Point=None, *, brightness: float=1.0, ambience=32, diffuse: float=1.0,
	  shininess: int=1, specular: float=.50) -> str:
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
		# r = d - 2(d•n)n
		reflection = normalized_lighting_angle - 2 * (normalized_lighting_angle * normalized_normal) * normalized_normal
		if(Point(0, 0, 1) * reflection > 0 and normalized_normal * normalized_lighting_angle > 0):
			specular_intensity = specular * brightness * (Point(0, 0, 1) * reflection) ** shininess
		else:
			specular_intensity = 0

		hex_value: str = to_hex(ambience + int(255 * (diffuse_intensity + specular_intensity)))
		# hex_value: str = to_hex(int(255 * diffuse_intensity + shininess + ambience))
		return f"#{hex_value}{hex_value}{hex_value}"


	# ———————————————————————————————————————————————— LINEAR ALGEBRA ———————————————————————————————————————————————— #

	def normal(self) -> Point:
		if(len(self) < 3):
			raise Exception("Cannot normalize a shape that is less than 3 points")

		a1, a2, a3 = list(self.points[1] - self.points[0])
		b1, b2, b3 = list(self.points[2] - self.points[1])
		return Point((a2 *  b3 - a3 * b2), (a3 * b1 - a1 * b3), (a1 * b2 - a2 * b1))


	def project_onto_plane(self, plane_depth: int) -> list[Point]:
		return Shape(*[point.project_onto_plane(plane_depth) for point in self.points], dimensions=2)


	def rotate(self) -> list[Point]:
		pass


	def scale(self) -> list[Point]:
		pass


	def translate(self, *translations: list[int]):
		[point.translate(*translations) for point in self.points]
