import moviepy.editor as mpy
from PIL import ImageFont
import numpy as np
from .slide import Slide
from .animator import Animator

# I could make code engine a singleton pattern but i'm not sure if it is usefull
class AnimationEngine:

    def __init__(self, font_name, font_size, img_size=(1000,1000), fps=30):
        self.slides = []
        self.font = ImageFont.truetype(f"fonts/{font_name}", font_size) if font_name else ImageFont.load_default()
        self.font_size = font_size
        self.img_size = img_size
        self.fps = fps

        self.animator = Animator(fps, img_size, self.font)


    def new_slide(self, text):
        """
        Creates a new slide diffing the one before with this one, then it overwrites fragments for the elements by type (mantein, remove, add).
        text:str -> the code that should be displayed in this slide
        """
        slide = Slide(text)
        slide.generate_frags(self.font)

        if len(self.slides) > 0:
            print(f"Diffing slide {len(self.slides)} with slide {len(self.slides)-1}")
            self.slides[-1].diff_with(slide)
            self.slides[-1].generate_frags(self.font)

        self.slides.append(slide)
        return slide
   
    
    # =========================================================
    # Rendering of image arrays outputed by the other functions
    # =========================================================

    def render(self):

        if len(self.slides) < 2:
            raise Exception("At least one slide is neccesary...")

        frames = []

        for slide in self.slides:
            for (animation, duration) in slide.animations:
                frames += animation(slide, duration=duration)

        self.list_render(frames)


    def list_render(self, frames, name="new_list_render.mp4"):
        clip = mpy.ImageSequenceClip([np.array(frame) for frame in frames], fps=self.fps)
        # Write the video clip to a file
        clip.write_videofile("output/"+name, fps=self.fps)


    
