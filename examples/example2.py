from maraslib.engine import AnimationEngine

engine = AnimationEngine("RobotoMono.ttf", 30, img_size=(1000, 700))

slide0 = engine.new_slide("""
def Hello():
    Some code
""")

slide1 = engine.new_slide("""
def Hello():
    
    data = going to put "Hello" inside a list here :)
    print(" World")

    Some other code 
""")


slide2 = engine.new_slide("""
def Hello():
    
    data = ["H", "e", "l", "l", "o"]
    for letter in data:
        word += letter

    print(data + " World")

    print("Maras can animate code but also other text")

    ===== Output =====
    > hello.py
    Hello World
    > 
""")


slide0.add_animation(engine.animator.default, 4)

slide1.add_animation(engine.animator.show, 3)
slide1.add_animation(engine.animator.fade_out, 0.5)
slide1.add_animation(engine.animator.make_space, 1)
slide1.add_animation(engine.animator.fade_in, 0.5)

slide2.add_animation(engine.animator.show, 3)

print(engine)

engine.render()

