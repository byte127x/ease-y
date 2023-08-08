from typing import Union
from tkinter import Tk, Canvas
import easing_functions, time
import numpy as np

class ShapeException(Exception):
    def __str__(self, *args):
        return "Shape has not been added to a canvas"

class Shape:
    # A class used for storing Tk Canvas shapes permentantly. Supports Motion
    def __init__(self, x:int=0, y:int=0, width:int=100, height:int=100, fill:Union[str, list, tuple]='black', outline:Union[str, list, tuple]='black', stroke_width:Union[int, float]=1, rotation:int=0, scale:int=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill = fill
        self.outline = outline
        self.stroke_width = stroke_width
        
        self.rotation = rotation
        self.scale = scale
        self.tween = None
        
        self.tk_id = None
        self.tk_canvas = None
        
    def create_tween(self, tween_style:str='linear', new_x:int=10, new_y:int=10, new_rotation:int=90, new_scale:int=0.5) -> list:
        self.tween = {
            'x': easing_functions.CubicEaseInOut(start=self.x, end=new_x),
            'y': easing_functions.CubicEaseInOut(start=self.y, end=new_y),
            'rotation': easing_functions.CubicEaseInOut(start=self.rotation, end=new_rotation),
            'scale': easing_functions.CubicEaseInOut(start=self.scale, end=new_scale),
        }
        
    def get_tween_frames(self, fps=30):
        if self.tween is not None:
            resolution = np.arange(0, 1, 1/fps)
            frames = {}
            for key, tween in self.tween.items():
                frames[key] = list(map(tween, resolution))
            return frames

    def fps_counter(self, last_tick):
        self.tick = time.time()*30
        self.delta = self.tick-last_tick
        if self.delta == 0:
            self.delta = 1
        self.actual_fps = round(30/self.delta)
        print(self.actual_fps)
                
    def play_tween(self, fps=30, seconds=1):
        self.tick = 0
        self.delta = 1
        self.actual_fps = 1
        self.start_time = time.time()
        frames = self.get_tween_frames(fps)
        self.fps_counter(self.tick)
        self.tk_canvas.after(1000//fps, lambda: self.show_frame(1, frames, fps))
        
    def show_frame(self, frame, frame_list, fps=30):
        if frame == len(frame_list['x']):
            print(time.time()-self.start_time)
            return
        self.fps_counter(self.tick)
        self.remove_from_tk()
        self._shape_drawer(frame_list['x'][frame], frame_list['y'][frame], self.fill, self.outline, self.stroke_width)
        self.tk_canvas.after(1000//self.actual_fps, lambda: self.show_frame(frame+1, frame_list, fps))
    
    def draw_to_tk(self, canvas: Union[Canvas, type(None)]=None):
        if canvas is None:
            return
        self.tk_canvas = canvas
        self._shape_drawer(self.x, self.y, self.fill, self.outline, self.stroke_width)
        
    def remove_from_tk(self):
        if self.tk_id is None or self.tk_canvas is None:
            raise ShapeException()
            return
        self.tk_canvas.delete(self.tk_id)
            
class Rectangle(Shape):
    # Persistent Data Rectangle
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _shape_drawer(self, x, y, fill, outline, stroke_width):
        width, height = (self.width, self.height)
        self.tk_id = self.tk_canvas.create_rectangle(
            x-(width/2),
            y-(height/2),
            x+(width/2),
            y+(height/2),
            fill=fill,
            outline=outline,
            width=stroke_width,
        )
        
class Circle(Shape):
    # Persistent Data Circle
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _shape_drawer(self, x, y, fill, outline, stroke_width):
        width, height = (self.width, self.height)
        self.tk_id = self.tk_canvas.create_oval(
            x-(width/2),
            y-(height/2),
            x+(width/2),
            y+(height/2),
            fill=fill,
            outline=outline,
            width=stroke_width,
        )
    
# Viewing Test
if __name__ == '__main__':
    s = Rectangle(237, 369, 50, 50)

    root = Tk()
    #root.attributes('-zoomed', True)
    c = Canvas(root)
    c.pack(fill='both', expand=1)
    s.draw_to_tk(c)
    s.create_tween(new_scale=1)
    root.after(1500, s.play_tween)

    root.mainloop()