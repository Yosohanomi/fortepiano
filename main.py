from pygame import *
from settings import *
from sounds import load_sounds
from keys import draw_keys, create_key_rects
from buttons import Button

init()
screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.set_caption("Piano Game")

sounds = load_sounds(KEYS)
key_rects = create_key_rects(len(KEYS))
keys_list = list(KEYS.keys())
my_font = font.SysFont("Arial", 24)
pressed_keys = set()

screen_mode = "main"
settings_menu = None

current_volume = 1.0
for s in sounds.values():
    try:
        s.set_volume(current_volume)
    except Exception:
        pass

num_keys = len(KEYS)

def apply_settings(volume: float, key_count: int):
    global current_volume, num_keys, keys_list, key_rects, pressed_keys
    current_volume = float(max(0.0, min(1.0, volume)))
    for s in sounds.values():
        try:
            s.set_volume(current_volume)
        except Exception:
            pass

    key_count = max(1, min(len(KEYS), int(key_count)))
    if key_count != num_keys:
        num_keys = key_count
        keys_list = list(KEYS.keys())[:num_keys]
        key_rects = create_key_rects(num_keys)
        pressed_keys = {i for i in pressed_keys if i < num_keys}

def open_settings():
    global screen_mode, settings_menu
    screen_mode = 'settings'
    settings_menu = SettingsMenu(
        screen.get_rect(),
        initial_volume=current_volume,
        initial_keys=num_keys,
        min_keys=1,
        max_keys=len(KEYS),
        on_change=apply_settings,
        on_back=lambda: _back_to_main()
    )

def start_game(): pass
def open_settings(): pass
def exit_game(): quit()

buttons = [
    Button(60, 20, 120, 40, "Settings", open_settings)
]

running = True
while running:
    screen.fill(WHITE)

    for button in buttons:
        button.draw(screen, my_font)

    draw_keys(screen, key_rects, pressed_keys)

    display.flip()

    for e in event.get():
        if e.type == QUIT:
            running = False

        # кнопки
        for button in buttons:
            button.handle_event(e)

        # клавіатура
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
