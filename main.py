
from maraslib.codeengine import CodeEngine

print("Code Animation")


engine = CodeEngine("RobotoMono.ttf", 30)
slide = engine.new_slide("""
if what == lol:
print(fuck you)

else {}""")
slide1 = engine.new_slide("""
if what == tette:
print(fuck youuu)

else {
testiamo questo
}""")

#engine.render()
print(slide.diff)
print(slide1.diff)

#engine.static_render(slide)



frames = engine.static_sequence(slide, duration=2) + engine.dynamic_remove(slide, duration=2) + engine.dynamic_move(slide, duration=2) + engine.dynamic_blendin(slide, duration=2)

#frames = engine.dynamic_move(slide, duration=3)

engine.list_render(frames)


