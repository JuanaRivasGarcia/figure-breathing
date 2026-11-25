# Geometric Shape for Breathing
A terminal app that draws a geometric shape. The shape moves in sync with your breathing: it grows larger as you inhale, pauses as you hold your breath, and shrinks as you exhale.

## Features
- Choose from three shapes: a circle, a triangle, and a star.
- Set the duration of each phase of breathing (inhalation, breath hold, and exhalation).
- Set the total session length.
- Always ends on an exhalation.
- Choose between 3-phase or 4-phase breathing.
- Validates input, so invalid answers don’t crash the program.
- Choose from several image backgrounds, each with a matching shape colour.

## Requirements
- Python 3.x
- Tkinter, usually included with Python; on Debian/Ubuntu Linux, install it with `sudo apt install python3-tk`.
- Pillow, for loading the background images. Install the dependencies with `pip install -r requirements.txt`

## Usage 
```bash
python3 breathing.py
```
The program asks for the durations of each phase of breathing (in seconds), the length of the session (in minutes), the type of geometric shape and the background. Finally, a window opens showing the shape breathing.

## Design notes
- **Liskov:** This project is designed to practice the SOLID principles. There is an abstract class `Figure` and three child classes: `Circle`, `Triangle`, and `Star`, each of which can be substituted for the others without causing the program to fail. 

- **Open/Closed Principle:** In the future, other child classes (such as Hexagon) could be added without modifying the existing code.

- **Single Responsibility:** Shapes are only responsible for drawing themselves; the breathing logic lives separately, in its own functions.

- **Dependency Inversion:** The functions responsible for breathing work directly with the abstract class `Figure` without needing to know the specific figure: `Circle`, `Triangle` or `Star`.

- **Dependency injection:** The functions responsible for breathing receive what they need via arguments; they do not require global variables. This allows them to be self-contained and easy to follow. The variables `start_time` and `session_seconds` are global because they are not phase data.

- **Interface Segregation:** The figures aren't required to know anything about the phases of breathing; they simply draw themselves.

- **Animation:** This is achieved using `after`. If we used a loop, the window would freeze. With `Tkinter`'s `after`, the program proceeds step by step and chains the calls together; this way, the figure grows smoothly and the window remains responsive.


## Future improvements

- Add soft, blurred edges to the shapes.
- Configure a graphical interface to select the type of figure and session durations.
- Package it as an app.

## Credits
- Background images from [Pexels](https://www.pexels.com).