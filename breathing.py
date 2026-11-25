'''A figure that counts the seconds for inhalation, holding the breath, and exhalation'''

# Import modules
from abc import ABC, abstractmethod
import math
import tkinter as tk
import time
from PIL import Image, ImageTk


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


# --- Variables ---
initial_size = 20
final_size = 100
growth = final_size - initial_size
delay = 20 # Milliseconds between each step of the animation
backgrounds = {
    "sea":    {"image": "images/mar.jpg",       "colour": "#F2C88A"},
    "marble": {"image": "images/marmol.jpg",    "colour": "#F4A77A"},
    "nebula": {"image": "images/nebulosa.jpg",  "colour": "#B8EDDF"},
    "clouds": {"image": "images/nubes.jpg",     "colour": "#4A5288"},
}

# --- Functions ---
def seconds_to_ms(seconds):
    '''Convert seconds to milliseconds.'''
    milliseconds = seconds * 1000
    return milliseconds

def minutes_to_seconds(minutes):
    '''Convert minutes to seconds.'''
    seconds = minutes * 60
    return seconds

def seconds_to_steps(seconds):
    '''Convert seconds to animation steps.'''
    step_per_seconds = 1000 / delay # the number of steps that fit into one second, calculated based on the delay
    steps = int(seconds * step_per_seconds)
    return steps

def ask_number(question):
    '''Ask for a number, repeating until the input is valid; returns it as an integer.'''
    while True:
        number = input(question)
        if number.isdigit():
            return int(number)
        else:
            print("Please, enter a valid option.")

def ask_colour(question, palette):
    '''Find the selected color in the palette'''
    while True:
        choice = input(question).lower()
        if choice in palette:
            return palette[choice]
        else:
            print("Please, enter a valid option.")

# --- Inspiration ---
def to_inhale(step, inhalation_steps, retention_ms, exhalation_steps):
    '''Increase the size of the geometric shape.'''
    size = initial_size + (growth / inhalation_steps) * step
    figure.to_draw(size)
    if step < inhalation_steps:
        # I program the next step until the final size is reached
        window.after(delay, lambda: to_inhale(step + 1, inhalation_steps, retention_ms, exhalation_steps))
    else:
        window.after(delay, lambda: to_hold(retention_ms, inhalation_steps, exhalation_steps))


# --- Exhalation ---
def to_exhale(step, exhalation_steps, inhalation_steps, retention_ms):
    '''Reduce the size of the geometric shape.'''
    size = final_size - (growth / exhalation_steps) * step
    figure.to_draw(size)
    if step < exhalation_steps:
        window.after(delay, lambda: to_exhale(step + 1, exhalation_steps, inhalation_steps, retention_ms))
    else:
        elapsed_time = time.time() - start_time
        if elapsed_time < session_seconds:
            window.after(bottom_hold_ms, lambda: to_inhale(0, inhalation_steps, retention_ms, exhalation_steps))
        else:
            pass


# --- Retention ---
def to_hold(retention_ms, inhalation_steps, exhalation_steps):
    '''Holding: waiting without changing position.'''
    window.after(retention_ms, lambda: to_exhale(0, exhalation_steps, inhalation_steps, retention_ms))

# --- Questions ---

inhalation = ask_number("How many seconds should you inhale for?: ")
inhalation_steps = seconds_to_steps(inhalation)
retention = ask_number("How many seconds should you hold your breath for?: ")
retention_ms = seconds_to_ms(retention)
exhalation = ask_number("How many seconds should you exhale for?: ")
exhalation_steps = seconds_to_steps(exhalation)
while True:
    breathing_type = input("Choose breathing type (3 = 3-phase, 4 = 4-phase): ")
    if breathing_type == "3":
        bottom_hold_ms = delay # No bottom hold: continue almost immediately.
        break
    elif breathing_type == "4":
        bottom_hold = ask_number("How many seconds should you hold your breath after exhale?:")
        bottom_hold_ms = seconds_to_ms(bottom_hold)
        break
    else:
        print("Please, enter a valid option.")
session = ask_number("How many minutes should the session last?: ")
session_seconds = minutes_to_seconds(session)
# Session context(start_time, session_seconds) stays global on purpose:
# It's not phase data passed through the cycle, so we don't thread it as arguments.
chosen = ask_colour("Choose a background (sea, marble, nebula, clouds): ", backgrounds)
background_image = chosen["image"]
figure_colour = chosen["colour"]

## --- Choose figure ---
while True:
    figure_choice = input("Choose a geometric shape (circle, triangle or star): ").lower()
    if figure_choice == "circle":
        break
    elif figure_choice == "triangle":
        break
    elif figure_choice == "star":
        break
    else:
        print("Please, enter a valid option.")

# --- Setting the table ---
window = tk.Tk()
window.title("Breathing")
canvas = tk.Canvas(window, width=400, height=400)
canvas.pack()

# --- Load and display the image ---
bg_image = Image.open(background_image).resize((400, 400))
bg_photo = ImageTk.PhotoImage(bg_image)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# --- Creation of the figure ---
if figure_choice == "circle":
    figure = Circle(canvas, 200, 200, figure_colour)
elif figure_choice == "triangle":
    figure = Triangle(canvas, 200, 200, figure_colour)
elif figure_choice == "star":
    figure = Star(canvas, 200, 200, figure_colour)

start_time = time.time() # The moment the session begins
to_inhale(0, inhalation_steps, retention_ms, exhalation_steps)
window.mainloop()