import numpy as np
from PIL import Image, ImageDraw


class Animator:

    def __init__(self, fps, img_size, font) -> None:
        self.fps = fps
        self.img_size = img_size
        self.font = font

    # ============================
    # Fade in and Fade Out of text
    # ============================

    def _dynamic_fade(self, slide, fade_function, target, duration):
        
        frames = int(duration * self.fps)

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

    def fade_in(self, slide, duration):
        return self._dynamic_fade(slide, self.ascending_quad_fun, 1, duration)
    def fade_out(self, slide, duration):
        return self._dynamic_fade(slide, self.descending_quad_fun, -1, duration)

    # ================
    # Movement of text
    # ================


    def _dynamic_move(self, slide, move_function, inverse, duration):

        fps = int(duration * self.fps)

        new_is = 1 if not inverse else -1

        new_diff = [diff[0] for diff in slide.diff if (diff[0] in [0,new_is])]
        old_diff = [diff[0] for diff in slide.diff if (diff[0] in [0,-new_is])]
        original = [img for (img, diff) in zip(self.new_frame(slide, [0,-1], True), old_diff) if (diff==0)]

        before_pos = np.array([pos[0] for pos in zip(slide.frags_to_coords([0,-1]), old_diff) if pos[1] == 0])
        after_pos = np.array([pos[0] for pos in zip(slide.frags_to_coords([0,1]), new_diff) if pos[1] == 0])

        #steps = np.array([(after-bef)/fps for (bef, after) in zip(before_pos, after_pos)])
        distance = (after_pos - before_pos)
        
        frames = []
        for frame in range(fps):
                step = move_function(frame, fps, distance)

                output_array = [tuple(map(int, sub_array)) for sub_array in step]
                frames.append(self.blend_imgs(original, output_array))
        return frames

    def make_space(self, slide, duration):
        return self._dynamic_move(slide, self.distance_weighted_quadratic, False, duration)

    def move_back(self, slide, duration):
        return self._dynamic_move(slide, self.distance_weighted_quadratic, True, duration)

    # ================
    # Static sequences
    # ================

    def _static_sequence(self, slide, target, duration):
        """
        Renders a static video of a slide.
        slide:Slide -> the slide to be rendered
        duration:int -> time in seconds of the clip
        fps:int -> fps should 
        """
        
        frames_to_render = int(duration*self.fps)
        frame = self.new_frame(slide, [0, target])
        frames = [frame for _ in range(frames_to_render)]
        return frames

    def show(self, slide, duration=5):
        return self._static_sequence(slide, -1, duration)

    def show_after(self, slide, duration=5):
        return self._static_sequence(slide, 1, duration)

    # ==================
    # Default Animations
    # ==================

    def default(self, slide, duration):
        frames = []
        frames += self.show(slide, duration/2)
        frames += self.fade_out(slide, duration/8)
        frames += self.make_space(slide, duration/4)
        frames += self.fade_in(slide, duration/8)
        return frames

    
    # =================
    # Functions
    # =================

    @staticmethod
    def ascending_quad_fun(n, max_n, power=2): 
        return pow((n/max_n), power)
    @staticmethod
    def descending_quad_fun(n, max_n, power=2): 
        return pow(((max_n-n)/max_n), power)
    @staticmethod
    def distance_weighted_quadratic(n, max_n, distance):
        return distance / pow((max_n - 1), 2) * pow(n, 2)

    # =================
    # Utility Functions
    # =================


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


