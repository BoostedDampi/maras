import diff_match_patch as dmp_module
class Frag:
    
    def __init__(self, text, frag_type, font):
        self.frag_type = frag_type #-1 to remove, 0 to sta, 1 to add
        self.content = text
        self.length = self.get_length(text, font)
        self.height = self.get_height(font)


    def get_length(self, text, font):
        left, top, length, bottom = font.getbbox(text)
        return length

    def get_height(self, font):
        ascent, descent = font.getmetrics()
        return ascent+descent

class Slide:
    
    def __init__(self, text, fade_out=None, fade_in=None, move=None):

        self.content = text
        self.diff = self.diff_newline_split([(0, self.content)]) #In case this is the first slide no diff will be use
        self.dynamic_frags = [] 

        self.fade_out = lambda frame, frames: pow(1-(frame/frames), 2) if fade_out is None else fade_out
        self.fade_in = lambda frame, frames: pow(frame/frames,2) if fade_in is None else fade_in
        self.move = lambda frame, fps, distance: (distance / (fps - 1) ** 2) * frame ** 2


    def diff_with(self, other_slide):
        dmp = dmp_module.diff_match_patch()
        diff = dmp.diff_main(self.content, other_slide.content)
        dmp.diff_cleanupSemantic(diff)
        self.diff = self.diff_newline_split(diff)

    def diff_newline_split(self, diff):
        adjusted_diff = []
        for elem in diff:
            if '\n' in elem[1]:
                splitted = elem[1].splitlines(True) 
                for slice in splitted:
                    adjusted_diff.append((elem[0], slice))
            else:
                adjusted_diff.append(elem)
        return adjusted_diff

    def generate_frags(self, font):
        self.dynamic_frags = []
        for elem in self.diff:
            self.dynamic_frags.append(Frag(elem[1], elem[0], font))

    def frags_to_coords(self, frag_type):
        pos = []
        cursor = (0,0)
        for frag in [frag for frag in self.dynamic_frags if (frag.frag_type in frag_type)]:
            pos.append(cursor)

            if '\n' in frag.content:
                y_mod = cursor[1] + frag.height
                x_mod = 0
            else:
                y_mod = cursor[1]
                x_mod = cursor[0] + frag.length
       
            cursor = (x_mod, y_mod)

        return pos
