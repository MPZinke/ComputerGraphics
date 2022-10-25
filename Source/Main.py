

import re
from tkinter import BOTH, Canvas, Frame, Tk


from Point import Point
from Shape import Shape


WIDTH = 1200
HEIGHT = 900


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

		raw_points: str = re.findall(Point.XYZ_REGEX, line)
		points = [Point(float(point[0]), float(point[1]), float(point[2])) for point in raw_points]
		shapes.append(Shape(*points))

	return shapes


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
		if(shape.is_visible()):
			shape.draw(canvas, Point(-2.5, 2.5, -5))
		print(f"	Is Visible: {str(shape.is_visible())}")

	root.mainloop()


def main():
	shapes = read_shapes("../Cylinder.pnt")
	draw(shapes)



if __name__ == '__main__':
	main()
