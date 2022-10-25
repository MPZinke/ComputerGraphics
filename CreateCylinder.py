

import math


z_distance = 500


def circle(diameter: int, *, z_offset: int=500, resolution: int=360) -> list[float]:
	points = []
	for x in range(resolution+1):
		degrees = 360 / resolution * x
		point = [diameter * math.cos(math.radians(degrees)), diameter * math.sin(math.radians(degrees)) + z_offset]
		points.append(point)

	return points


def create_cylinder(diameter, height) -> list[list[list[int]]]:
	shapes = []

	circle_xz = circle(diameter, resolution=360)
	for i in range(len(circle_xz)-1):
		# bottom half
		start_point = [circle_xz[i][0], -int(height/2), circle_xz[i][1]+diameter]
		top_point = [circle_xz[i][0], int(height/2), circle_xz[i][1]+diameter]
		end_point = [circle_xz[i+1][0], -int(height/2), circle_xz[i+1][1]+diameter]
		shapes.append([start_point, top_point, end_point])

		# top half
		start_point = [circle_xz[i][0], int(height/2), circle_xz[i][1]+diameter]
		right_point = [circle_xz[i+1][0], int(height/2), circle_xz[i+1][1]+diameter]
		end_point = [circle_xz[i+1][0], -int(height/2), circle_xz[i+1][1]+diameter]
		shapes.append([start_point, right_point, end_point])

		# top circle
		start_point = [circle_xz[i][0], int(height/2), circle_xz[i][1]+diameter]
		center_point = [0, int(height/2), diameter]
		end_point = [circle_xz[i+1][0], int(height/2), circle_xz[i+1][1]+diameter]

		shapes.append([start_point, center_point, end_point])


	return shapes



def write_points(shapes: list[list[list[int]]]):
	# shapes = [[[int(coordinate) for coordinate in point] for point in shape] for shape in shapes]
	with open("Cylinder.pnt", "w") as file:
		for shape in shapes:
			line = "\t\t".join([" ".join([f"{coordinate:5}" for coordinate in point]) for point in shape])
			file.write(line)
			file.write("\n")


def main():
	shapes = create_cylinder(500, 500)
	write_points(shapes)


if __name__ == '__main__':
	main()
