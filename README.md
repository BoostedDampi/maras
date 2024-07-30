# 🎥 maras 🎥

Maras is a Python library/tool designed for creating **dynamic, animated presentations of code changes**. It uses a slide-based approach, where each slide represents a state of the code, and transitions between slides are animated to highlight differences and changes. Ideal for tutorials, lectures, and presentations, Maras helps you visually demonstrate the evolution of code in an engaging way.

This is a **personal project** inspired by [this youtube video](https://www.youtube.com/watch?v=OXk6Eabu7uM&t=184s) to learn a bit of Object Oriented Programming, it is very chaotic and absolutly not optimized, but it works.
If you now how to improve my code please tell me.

### Features

- Slide-based Presentation: Create multiple slides, each representing a state of the code.
- Animated Transitions: Automatically generate fade-in, fade-out, and move animations to highlight changes between slides.
- Customizable Fonts and Sizes: Specify font type and size for your code presentation.
- High-Quality Rendering: Uses moviepy and PIL to generate high-quality video output.

### To-Do

- [ ] More transitions and movement styles.
- [ ] Colors (A ast is needed for color schemes, seems difficult).
- [ ] Better end user customizability.
- [x] Better code positioning and use of OOP patterns
- [x] Better Error Handling

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

slide1 = engine.new_slide("print('Hello, World!')")
slide2 = engine.new_slide("print('Hello, Maras!')")
slide3 = engine.new_slide("print('Hello, Mum!')")
```
Add Animations: Add the default animation or some specific animations.

```python
slide1.add_animation(engine.animator.default, 10)

# Animations included in the default, slide1 and slide2 have the same animations
slide2.add_animation(engine.animator.show_before, 2)
slide2.add_animation(engine.animator.fade_out, 0.5)
slide2.add_animation(engine.animator.make_space, 1)
slide2.add_animation(engine.animator.fade_in, 0.5)

# The last slide cant change into another slide so only default or show_before is usefull.
slide3.add_animation(engine.animator.show_before, 2)
```
Render the Presentation: Generate the final video output with engine.render().

```python
engine.render()
```
### Example

```python

from maraslib.engine import AnimationEngine

# Initialize AnimationENgine with font settings
engine = CodeEngine(font_name="Arial.ttf", font_size=24)

# Add slides
slide1 = engine.new_slide("def hello_world():\n    print('Hello, World!')")
slide2 = engine.new_slide("def hello_codeengine():\n    print('Hello, CodeEngine!')")
slide3 = engine.new_slide("def goodbye_codeengine():\n    exit()")

# Add animations
slide1.add_animation(engine.animator.default, 3)
slide2.add_animation(engine.animator.default, 3)
slide3.add_animation(engine.animator.default, 3)

# Render the presentation
engine.render()
```
This will create a video showcasing the transition from the first function definition to the second, with animations highlighting the changes.
