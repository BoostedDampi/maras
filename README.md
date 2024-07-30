# 🎥 maras 🎥

Maras is a Python tool designed for creating dynamic, **animated presentations of code changes**. It uses a slide-based approach, where each slide represents a state of the code, and transitions between slides are animated to highlight differences and changes. Ideal for tutorials, lectures, and presentations, Maras helps you visually demonstrate the evolution of code in an engaging way.

This is a **personal project** to learn a bit of Object Oriented Programming, it is very chaotic and absolutly not optimized, but it works.
If you now how to improve my code please tell me.

### Features

- Slide-based Presentation: Create multiple slides, each representing a state of the code.
- Animated Transitions: Automatically generate fade-in, fade-out, and move animations to highlight changes between slides.
- Customizable Fonts and Sizes: Specify font type and size for your code presentation.
- High-Quality Rendering: Uses moviepy and PIL to generate high-quality video output.

### To-Do

- [ ] More transitions and movement styles.
- [ ] Colors (i need an ast and i'm scared).
- [ ] Better usage and more customizability.
- [ ] Nice code seperation and OOP patterns

## Installation

To use maras, clone the repository and install the required dependencies:

```bash

git clone https://github.com/boosteddampi/maras.git
cd maras
pip install -r requirements.txt
```

## Usage

_This explanation is **deprecated**, look in the "main.py" file for a up to date example_

Here's a basic example of how to use maras:

    Initialize the Engine: Create an instance of CodeEngine with your desired font, size, and image dimensions.

```python

from maras import CodeEngine

engine = CodeEngine(font_name="Arial.ttf", font_size=24)
```
Add Slides: Add slides by specifying the code content for each slide.

```python

engine.new_slide("print('Hello, World!')")
engine.new_slide("print('Hello, CodeEngine!')")
```
Render the Presentation: Generate the final video output with engine.render().

```python
engine.render()
```
### Example

```python

from codeengine import CodeEngine

# Initialize CodeEngine with font settings
engine = CodeEngine(font_name="Arial.ttf", font_size=24)

# Add slides
engine.new_slide("def hello_world():\n    print('Hello, World!')")
engine.new_slide("def hello_codeengine():\n    print('Hello, CodeEngine!')")

# Render the presentation
engine.render()
```
This will create a video showcasing the transition from the first function definition to the second, with animations highlighting the changes.
