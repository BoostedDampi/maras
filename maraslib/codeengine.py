import moviepy.editor as mpy
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from .slide import Slide
class CodeEngine:

    def __init__(self, font_name, font_size, img_size=(800,800), fps=24):
        self.slides = []
        self.font = ImageFont.truetype(f"fonts/{font_name}", font_size) if font_name else ImageFont.load_default()
        self.font_size = font_size
        self.img_size = img_size
        self.fps = fps

    def new_slide(self, text):
        """
        Creates a new slide.
        text:str -> the code that should be displayed in this slide
        """
        slide = Slide(text)

        if len(self.slides) > 0:
            print(f"Diffing slide {len(self.slides)} with slide {len(self.slides)-1}")
            self.slides[-1].diff_with(slide)
            self.slides[-1].generate_frags(self.font)

        self.slides.append(slide)
        return slide
    
    def dynamic_remove(self, slide, duration=2):
        
        frames = duration * self.fps
        diff = [diff[0] for diff in slide.diff if (diff[0] in [0,-1])]
        original = self.static_frames(slide, [0,-1])

        #Combining images to remove and images to mantain to make blend simpler
        combined_to_remove = self.blend_imgs([zipped[1] for zipped in zip(diff, original) if zipped[0]==-1])
        combined_to_mantain = self.blend_imgs([zipped[1] for zipped in zip(diff, original) if zipped[0]==0])

        #generating evenly spaced numbers for every frame
        scaling_function = slide.fade_out 
        buffer = []
        for frame in range(1, frames):
            #the factor to multiply with the alpha
            factor = scaling_function(frame, frames)

            edited = np.array(combined_to_remove)
            edited[...,3] = (edited[..., 3] * factor).astype(np.uint8)
            edited = Image.fromarray(edited)
            buffer.append(self.blend_imgs([edited, combined_to_mantain]))

        return buffer

    def dynamic_blendin(self, slide, duration=5):
            
            frames = duration * self.fps
            diff = [diff[0] for diff in slide.diff if (diff[0] in [0,1])]
            original = self.static_frames(slide, [0,1])

            #Combining images to remove and images to mantain to make blend simpler
            combined_to_blendin = self.blend_imgs([zipped[1] for zipped in zip(diff, original) if zipped[0]==1])
            combined_to_mantain = self.blend_imgs([zipped[1] for zipped in zip(diff, original) if zipped[0]==0])

            #generating evenly spaced numbers for every frame
            scaling_function = slide.fade_in 

            buffer = []
            for t in range(0, frames):
                #the factor to multiply with the alpha
                factor = scaling_function(t, frames)

                edited = np.array(combined_to_blendin)
                edited[...,3] = (edited[..., 3] * factor).astype(np.uint8)
                edited = Image.fromarray(edited)
                buffer.append(self.blend_imgs([edited, combined_to_mantain]))

            return buffer

    def dynamic_move(self, slide, duration=2):

        fps = duration * self.fps

        new_diff = [diff[0] for diff in slide.diff if (diff[0] in [0,1])]
        old_diff = [diff[0] for diff in slide.diff if (diff[0] in [0,-1])]
        original = [img for (img, diff) in zip(self.static_frames(slide, [0,-1]), old_diff) if (diff==0)]

        before_pos = np.array([pos[0] for pos in zip(slide.frags_to_coords([0,-1]), old_diff) if pos[1] == 0])
        after_pos = np.array([pos[0] for pos in zip(slide.frags_to_coords([0,1]), new_diff) if pos[1] == 0])

        steps = np.array([(after-bef)/fps for (bef, after) in zip(before_pos, after_pos)])

        print("---------- Dynamic Move -----------")
        for b, a, s in zip(before_pos, after_pos, steps):
            # Format the positions and steps to fixed-width strings
            b_str = f"[{b[0]:3d} {b[1]:3d}]"
            a_str = f"[{a[0]:3d} {a[1]:3d}]"
            s_str = f"[{s[0]:5.2f} {s[1]:5.2f}]"
            # Print the formatted strings with the arrow in the same column
            print(f"{b_str} -> {a_str} in {s_str} steps")

        frames = []
        for frame in range(fps):
                step = steps * frame

                output_array = [tuple(map(int, sub_array)) for sub_array in step]
                frames.append(self.blend_imgs(original, output_array))
        return frames


    def static_sequence(self, slide, duration=5):
        """
        Renders a static video of a slide.
        slide:Slide -> the slide to be rendered
        duration:int -> time in seconds of the clip
        fps:int -> fps should 
        """
        if len(self.slides) < 2:
            raise Exception("At least one slide is neccesary...")

        frames_to_render = duration*self.fps
        frame = self.blend_imgs(self.static_frames(slide))
        frames = [frame for _ in range(frames_to_render)]
        return frames

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
                new_image.paste(image, (0, 0), image)
        return new_image
        
    def static_frames(self, slide, frag_type=[0,-1]):
        txt_imgs = []
        positions = slide.frags_to_coords(frag_type)
        for pos_n, frag in enumerate([frag for frag in slide.dynamic_frags if (frag.frag_type in frag_type)]):
            txt_imgs.append(self.create_text_image(frag.content, position=positions[pos_n]))
        return txt_imgs

