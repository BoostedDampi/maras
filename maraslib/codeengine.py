import moviepy.editor as mpy
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from .slide import Slide
class CodeEngine:

    def __init__(self, font_name, font_size, img_size=(1000,1000), fps=30):
        self.slides = []
        self.font = ImageFont.truetype(f"fonts/{font_name}", font_size) if font_name else ImageFont.load_default()
        self.font_size = font_size
        self.img_size = img_size
        self.fps = fps

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
   
    # ============================
    # Fade in and Fade Out of text
    # ============================

    def dynamic_fade(self, slide, fade_function, target, duration=2):
        
        frames = duration * self.fps
        diff = [diff[0] for diff in slide.diff if (diff[0] in [0,target])]
        original = self.new_frame(slide, [0,target], True)

        #Combining images to remove and images to mantain to make blend simpler
        combined_to_remove = self.blend_imgs([zipped[1] for zipped in zip(diff, original) if zipped[0]==target])
        combined_to_maintain = self.blend_imgs([zipped[1] for zipped in zip(diff, original) if zipped[0]==0])

        #generating evenly spaced numbers for every frame
        buffer = []
        for frame in range(0, frames):
            #the factor to multiply with the alpha
            factor = fade_function(frame, frames)

            current_image = np.array(combined_to_remove)
            current_alpha= current_image[..., 3]
            new_alpha = (current_alpha * factor).astype(np.uint8)
            current_image[..., 3] = new_alpha
            edited_image = Image.fromarray(current_image, "RGBA")
            
            base = combined_to_maintain.copy()
            base.paste(edited_image, (0,0), edited_image)

            buffer.append(base)

        return buffer

    def fade_in(self, slide, duration=2):
        return self.dynamic_fade(slide, slide.fade_in, 1, duration)
    def fade_out(self, slide, duration=2):
        return self.dynamic_fade(slide, slide.fade_out, -1, duration)

    # ================
    # Movement of text
    # ================


    def dynamic_move(self, slide, duration=2):

        fps = duration * self.fps

        new_diff = [diff[0] for diff in slide.diff if (diff[0] in [0,1])]
        old_diff = [diff[0] for diff in slide.diff if (diff[0] in [0,-1])]
        original = [img for (img, diff) in zip(self.new_frame(slide, [0,-1], True), old_diff) if (diff==0)]

        before_pos = np.array([pos[0] for pos in zip(slide.frags_to_coords([0,-1]), old_diff) if pos[1] == 0])
        after_pos = np.array([pos[0] for pos in zip(slide.frags_to_coords([0,1]), new_diff) if pos[1] == 0])

        #steps = np.array([(after-bef)/fps for (bef, after) in zip(before_pos, after_pos)])
        distance = (after_pos - before_pos)
        
        movement_function = slide.move 
        frames = []
        for frame in range(fps):
                step = movement_function(frame, fps, distance)

                output_array = [tuple(map(int, sub_array)) for sub_array in step]
                frames.append(self.blend_imgs(original, output_array))
        return frames

    # ================
    # Static sequences
    # ================

    def static_sequence(self, slide, target, duration=5):
        """
        Renders a static video of a slide.
        slide:Slide -> the slide to be rendered
        duration:int -> time in seconds of the clip
        fps:int -> fps should 
        """
        
        frames_to_render = duration*self.fps
        frame = self.new_frame(slide, [0, target])
        frames = [frame for _ in range(frames_to_render)]
        return frames

    # =========================================================
    # Rendering of image arrays outputed by the other functions
    # =========================================================

    def render(self):

        if len(self.slides) < 2:
            raise Exception("At least one slide is neccesary...")

        frames = []

        for slide_n in range(len(self.slides)-1):

            frames += self.static_sequence(self.slides[slide_n], target=-1, duration=1)
            frames += self.fade_out(self.slides[slide_n], duration=1)
            frames += self.dynamic_move(self.slides[slide_n], duration=1)
            frames += self.fade_in(self.slides[slide_n], duration=1)
            frames += self.static_sequence(self.slides[slide_n+1], target=-1, duration=1)

        self.list_render(frames)


    def list_render(self, frames, name="new_list_render.mp4"):
        clip = mpy.ImageSequenceClip([np.array(frame) for frame in frames], fps=self.fps)
        # Write the video clip to a file
        clip.write_videofile("output/"+name, fps=self.fps)


    def create_text_image(self, text, position=(0, 0), color="white"):
        """
        Takes a string and returns a PIL.Image
        test:String -> the string to add to the image
        position:(int,int) -> the position in the image.
        color:String|(int,int,int,int) -> the color of the text
        """
        img = Image.new('RGBA', self.img_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text(position, text, font=self.font, fill=color)
        return img

    
    def blend_imgs(self, images, pos=[]):
        """
        Blends a list of images into one.
        images:[Image] -> the list of images to be blended
        pos:[(int,int)] -> the position of the (0,0) point in the final image. if empty (0,0)
        """
        new_image = Image.new('RGBA', self.img_size, (0, 0, 0, 0))
        # Paste images onto the new image
        if len(pos):
            for image, pos in zip(images, pos):
                new_image.paste(image, pos, image)
        else:
            for image in images:
                new_image.paste(image, (0,0), image)
        return new_image
        
    def new_frame(self, slide, frag_type=[0,-1], as_list=False):

        txt_imgs = []
        positions = slide.frags_to_coords(frag_type)
        frags = [frag for frag in slide.dynamic_frags if (frag.frag_type in frag_type)]
        
        for pos, frag in zip(positions, frags):
            txt_imgs.append(self.create_text_image(frag.content, position=pos))

        self.blend_imgs(txt_imgs)

        return txt_imgs if as_list else self.blend_imgs(txt_imgs)

