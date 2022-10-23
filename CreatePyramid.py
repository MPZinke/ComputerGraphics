

z_distance = 500


def create_pyramid(width: int, height: int) -> list[list[list[int]]]:
	base1 = [[width/2, -height/2, 500+width], [width/2, -height/2, 500], [-width/2, -height/2, 500]]
	base2 = [[-width/2, -height/2, 500], [-width/2, -height/2, 500+width], [width/2, -height/2, 500+width]]

	# top point, back right, back left
	back = [[0, height/2, 500+(width/2)], [width/2, -height/2, 500+width], [-width/2, -height/2, 500+width]]
	# top point, front right, front left
	front = [[0, height/2, 500+(width/2)], [width/2, -height/2, 500], [-width/2, -height/2, 500]]
	# top point, back left, front left
	left = [[0, height/2, 500+(width/2)], [-width/2, -height/2, 500+width], [-width/2, -height/2, 500]]
	# top point, front right, back right
	right = [[0, height/2, 500+(width/2)], [width/2, -height/2, 500], [width/2, -height/2, 500+width]]

	shapes = [
		base1,
		base2,
		back,
	 	front,
		left,
		right
	]
	shapes = [[[int(coordinate) for coordinate in point] for point in shape] for shape in shapes]

	return shapes



def write_points(shapes: list[list[list[int]]]):
	for shape in shapes:
		for point in shape:
			print(f"{point[0]:5} {point[1]:5} {point[2]:5}", end="\t\t")
		print()


def main():
	shapes = create_pyramid(1200, 900)
	write_points(shapes)


if __name__ == '__main__':
	main()
