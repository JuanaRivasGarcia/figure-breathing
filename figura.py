'''A figure that counts the seconds for inhalation, holding the breath, and exhalation'''

# Import modules
from abc import ABC, abstractmethod

class Figure(ABC):
    def __init__(self, table, center_x, center_y, colour="skyblue"):
        self.table = table
        self.center_x = center_x
        self.center_y = center_y
        self.colour = colour
        self.drawing = None # We keep our paintings here

    @abstractmethod
    def to_draw(self, size):
        '''The shape is drawn centered, using its size as the radius'''
        ...

    def delete(self):
        '''Delete the shape'''
        if self.drawing is not None:
            self.table.delete(self.drawing)
            self.drawing = None


class Circle(Figure):
    def to_draw(self, size):
        self.delete() #Clear the previus figure
        x0 = self.center_x - size
        y0 = self.center_y - size
        x1 = self.center_x + size
        y1 = self.center_y + size
        self.drawing = self.table.create_oval(x0, y0, x1, y1, fill=self.colour, outline="")
        # Draw me an oval inside that box
        # Fill it with our color(fill) and remove the outline(outline=“”)


class Triangle(Figure):
    def to_draw(self, size):
        self.delete()
        self.drawing = self.table.create_polygon(
            self.center_x, self.center_y - size, # Top vertex
            self.center_x - size, self.center_y + size, # Bottom-left
            self.center_x + size, self.center_y + size, # Bottom-right
            fill=self.colour, outline=""
        )