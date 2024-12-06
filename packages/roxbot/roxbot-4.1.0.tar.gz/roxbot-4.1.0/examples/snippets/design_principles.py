from abc import ABC, abstractmethod
import math


# Shape (Abstract Base Class) - Demonstrating Liskov Substitution Principle (LSP)
# Any subclass of Shape can be substituted for Shape.
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


# Rectangle class - adhering to Single Responsibility Principle (SRP)
# Its only responsibility is to handle rectangle-specific logic.
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


# Circle class - adhering to SRP
# Its only responsibility is to handle circle-specific logic.
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius**2


# ShapeRenderer class - Demonstrating Dependency Inversion Principle (DIP)
# It depends on the abstract Shape class, not on concrete implementations.
class ShapeRenderer:
    def render(self, shape: Shape):
        # Here we depend on the abstraction (Shape) rather than concrete implementations.
        print(f"Rendering a shape with area: {shape.area()}")


# Adding a new shape type, like Triangle, would not require modifying the ShapeRenderer class.
# This demonstrates the Open/Closed Principle (OCP).
class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height


# Client code
rectangle = Rectangle(5, 3)
circle = Circle(2)
triangle = Triangle(3, 4)

renderer = ShapeRenderer()
renderer.render(rectangle)  # Works for Rectangle
renderer.render(circle)  # Works for Circle
renderer.render(triangle)  # Also works for Triangle without modifying the renderer
