'''A figure that counts the seconds for inhalation, holding the breath, and exhalation'''

# Import modules
from abc import ABC, abstractmethod
import math
import tkinter as tk


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


class Star(Figure):
    def to_draw(self, size):
        self.delete()
        points = 10 # 5-pointed star
        coordinates = [] # This is were we store x, y coordinates

        for i in range(points):
            if i % 2 == 0:  # If it’s an even number, it’s a point
                # The distance is the line segment from the centre point to the tip of the star 
                distance = size
            else:  # If it’s an odd number, it’s a valley
                #Distance is the line from the centre point to the valley point
                distance = size * 0.4

            angle = i * (2 * math.pi / points)
            x = self.center_x + distance * math.cos(angle)
            y = self.center_y + distance * math.sin(angle)

            coordinates.append(x)
            coordinates.append(y)

        self.drawing = self.table.create_polygon(
            coordinates, fill=self.colour, outline=""
        )


# Setting the table
window = tk.Tk()
window.title("Figure test")
canvas = tk.Canvas(window, width=400, height=400, bg="white")
canvas.pack()

# Creation of the figure
figure = Star(canvas, 200, 200)
figure.to_draw(80)

window.mainloop()