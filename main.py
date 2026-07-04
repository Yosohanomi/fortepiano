from pygame import *

from keys import create_key_rects
from settings import *
from sounds import load_sounds

init()
window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.set_caption("fortepiano")
running = True

sounds = load_sounds(KEYS)
key_rects = create_key_rects(len(KEYS))
keys_list =
pressed_keys =

while running:
    window.fill(WHITE)
    for e in event.get():
        if e.type == QUIT:
            running = False

        if e.type == KEYDOWN:
            k = key.name(e.key)
            if k in sounds:
                sounds[k].play()
                idx = keys_list.index(k)
                pressed_keys.add(idx)

        if e.type == KEYUP:
            k = key.name(e.key)
            if k in sounds:
                idx = keys_list.index(k)
                if idx in pressed_keys:
                    pressed_keys.remove(idx)

        if e.type == MOUSEBUTTONDOWN:
            pos = e.pos
            for i, rect in enumerate(key_rects):
                if rect.collidepoint(pos):
                    sounds[keys_list[i]].play()
                    pressed_keys.add(i)

        if e.type == MOUSEBUTTONUP:
            pos = e.pos
            for i, rect in enumerate(key_rects):
                if i in pressed_keys and rect.collidepoint(pos):
                    pressed_keys.remove(i)

    display.flip()
