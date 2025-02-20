import math

# ''' FIRST TASK '''
class Canvas(list):
    def __init__(self, width: int, height: int):
        # calls the __init__ method of the parent list class -> inherits all list functionalities
        super().__init__()
        self.width = width
        self.height = height
        for _ in range(height):
            self.append(" " * width)

    def print(self):
        def create_row_headers(length: int):
            return "".join([str(i % 10) for i in range(length)])
        header = " " + create_row_headers(self.width)
        print(header)
        for idx, row in enumerate(self):
            print(idx % 10, row, idx % 10, sep="")  # sep="" no space between
        print(header)

    def replace_at_index(self, s: str, r: str, idx: int) -> str:
        return s[:idx] + r + s[idx + len(r):]

    def draw_line_segment(self, start: tuple[int, int], end: tuple[int, int], line_char: str = "*"):
        x1, y1 = start
        x2, y2 = end
        dx = abs(x2 - x1)  # horizontal distance between start and end points
        dy = abs(y2 - y1)  # vertical distance between start and end points
        sx = 1 if x1 < x2 else -1  # determines direction of movement along x and y axes
        sy = 1 if y1 < y2 else -1
        error = dx - dy
        # Bresenham's Line Algorithm Loop
        while x1 != x2 or y1 != y2:
            self[y1] = self.replace_at_index(self[y1], line_char, x1)
            # checks if current error value is enough to trigger a step in either the x or y direction
            double_error = error * 2
            if double_error > -dy:
                error -= dy
                x1 += sx
            if double_error < dx:
                error += dx
                y1 += sy
        self[y2] = self.replace_at_index(self[y2], line_char, x2)

    def draw_polygon(self, *points: tuple[int, int], closed: bool = True, line_char: str = "*"):
        start_points = points[:-1]
        end_points = points[1:]
        if closed:
            start_points += (points[-1],) # notation with comma at the end -> indicates a tuple
            end_points += (points[0],)
        for start_point, end_point in zip(start_points, end_points):
            self.draw_line_segment(start_point, end_point, line_char)

    def draw_line(self, start: tuple[int, int], end: tuple[int, int], line_char: str = "*"):
        self.draw_line_segment(start, end, line_char)

    def draw_rectangle(self, upper_left: tuple[int, int], lower_right: tuple[int, int], line_char: str = "*"):
        x1, y1 = upper_left
        x2, y2 = lower_right
        self.draw_polygon(upper_left, (x2, y1), lower_right, (x1, y2), line_char=line_char)

    def draw_n_gon(self, center: tuple[int, int], radius: int, number_of_points: int,
                   rotation: int = 0,
                   line_char: str = "*"):
        angles = range(rotation, 360 + rotation, 360 // number_of_points)

        points = []
        for angle in angles:
            # Convert the angle of the point to radians
            angle_in_radians = math.radians(angle)
            # Calculate the x and y positions of the point
            x = center[0] + radius * math.cos(angle_in_radians)
            y = center[1] + radius * math.sin(angle_in_radians)
            # Add the point to the list of points as a tuple
            points.append((round(x), round(y)))

        self.draw_polygon(*points, line_char=line_char)


# Example usage
my_canvas = Canvas(100,40)
my_canvas.draw_line((10,4), (92,19), "+")
my_canvas.draw_rectangle((10,10),(20, 20), "#")
my_canvas.draw_polygon((7, 12), (24,29), (42,15), (37, 32), (15,35))
my_canvas.draw_n_gon((72,25), 12, 20, 80, "-")
my_canvas.print()



# ''' SECOND TASK '''
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}/{self.y})"

    __repr__ = __str__

    def distance_from_origin(self) -> float:
        return math.sqrt((self.x ** 2) + (self.y **2))

p1 = Point(2.3, 43.14)
p2 = Point(5.53, 2.5)
p3 = Point(12.2, 28.7)
p4 = Point(1, 1)
p5 = Point(5, 5)
p6 = Point(10,10)


class Shape(list):
    # *points --> allows Shape to accept any numbers of Point objects
    def __init__(self, *points):
        super().__init__()
        self.points = list(points)

    def __str__(self):
        points_str = ", ".join(str(point) for point in self.points)
        return f"Shape [{points_str}]"

    def centroid(self) -> Point:
        # number of points in Shape = length of the list with the points
        n = len(self.points)
        # no points means no centroid
        if n == 0:
            return None

        sum_x = sum(point.x for point in self.points)
        sum_y = sum(point.y for point in self.points)

        return Point(sum_x / n, sum_y / n)

    def distance_from_origin(self):
        # same as in Point class but with centroid point
        centroid = self.centroid()
        return math.sqrt(centroid.x ** 2 + centroid.y ** 2)

    def __eq__(self, other):
        return self.distance_from_origin() == other.distance_from_origin()

    def __lt__(self, other):
        return self.distance_from_origin() < other.distance_from_origin()

    def __repr__(self):
        points_str = ', '.join(str(point) for point in self.points)
        return f"Shape [{points_str}]"

# Example usage change coordinates
p1 = Point(4.3, 34.12)  # Create a Point object at ()
p2 = Point(6.23, 1.2)   # Create a Point object at ()
p3 = Point(13.4, 30.5)  # Create a Point object at ()

s1 = Shape(p1, p2, p3)  # Create a Shape object with multiple points
s2 = Shape(p2)          # Create a Shape object with a single point
s3 = Shape()            # Create an empty Shape object

print(s1)  # Print the string representation of s1
print(s2)  # Print the string representation of s2
print(s3)  # Print the string representation of s3

s4 = Shape(Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0))  # Create a square Shape object
print(s4.centroid())  # Print the centroid of s4

print(p1.distance_from_origin())  # Print the distance of p1 from the origin
print(p2.distance_from_origin())  # Print the distance of p2 from the origin
print(p3.distance_from_origin())  # Print the distance of p3 from the origin

s5 = Shape(Point(0, 0.5), Point(0.5, 1), Point(1, 0.5), Point(0.5, 0))  # Create another Shape object
print(s4 == s5)  # Check if s4 and s5 have the same centroid
print(s4 < s5)   # Compare distances of centroids of s4 and s5

# Summary of all created shapes
shapes = [s1, s2, s3, s4, s5]  # Create a list of all created shapes
print("\nAll shapes created:")  # Print a header
print(shapes)  # Print the list of shapes