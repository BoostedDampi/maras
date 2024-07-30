import moviepy.editor as mpy
from PIL import ImageFont
import numpy as np
from .slide import Slide
from .animator import Animator
from os import path

# I could make code engine a singleton pattern but i'm not sure if it is usefull
class AnimationEngine:

    def __init__(self, font_name, font_size, img_size=(1000,1000), fps=30, output_name = "new_animation"):

        #somme error handling
        if not isinstance(font_name, str):
            raise ValueError("The path to the font must be set")
        if not isinstance(font_size, int) or font_size <= 0:
            raise ValueError("The size of the font must be set")
        if not isinstance(img_size, tuple) or len(img_size) != 2 or not all(isinstance(i, int) and i > 0 for i in img_size):
            raise ValueError("Image size has to be a tuple with elements greater then zero")
        if not isinstance(fps, int) or fps <= 0:
            raise ValueError("FPS has to be bigger then zero")


        self.slides = []
        self.font = ImageFont.truetype(f"fonts/{font_name}", font_size) if font_name else ImageFont.load_default()
        self.font_size = font_size
        self.img_size = img_size
        self.fps = fps
        self.file_name = output_name

        self.animator = Animator(fps, img_size, self.font)

    def __str__(self) -> str:
        return f"== Animation Engine ==\nCurrently {len(self.slides)} slides are created.\nFont used: {self.font.getname()} with size {self.font_size}.\nThe image size is {self.img_size}.\n"


    def new_slide(self, text):
        """
        Creates a new slide diffing the one before with this one, then it overwrites fragments for the elements by type (mantein, remove, add).
        text:str -> the code that should be displayed in this slide
        """

        if not isinstance(text, str) or len(text) == 0:
            raise ValueError("text has to be a non empty string")


        slide = Slide(text)
        slide.generate_frags(self.font)

        if len(self.slides) > 0:
            self.slides[-1].diff_with(slide)
            self.slides[-1].generate_frags(self.font)

        self.slides.append(slide)
        return slide
   
    
    # =========================================================
    # Creation of Image arrays and rendering
    # =========================================================

    def render(self):

        print("\nPreparing slides...")

        if len(self.slides) < 2:
            raise Exception("At least one slide is neccesary...")

        frames = []

        for counter, slide in enumerate(self.slides):
            print(f"Slide {counter} is beeing proccessed...")
            for (animation, duration) in slide.animations:
                frames += animation(slide, duration=duration)
        print("Finished preparing slides")
        print("Start rendering")
        clip = mpy.ImageSequenceClip([np.array(frame) for frame in frames], fps=self.fps)

        clip.write_videofile("output/"+self.file_name+".mp4", fps=self.fps)


    
