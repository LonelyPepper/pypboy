import time

import pygame
import game
import pypboy.ui
import settings
from math import atan2, pi, degrees

from pypboy.modules import data
from pypboy.modules import items
from pypboy.modules import stats
from pypboy.modules import boot
from pypboy.modules import map
from pypboy.modules import radio
from pypboy.modules import passcode

if settings.GPIO_AVAILABLE:
    import RPi.GPIO as GPIO


class Pypboy(game.core.Engine):
    currentModule = 0
    prev_fps_time = 0

    def __init__(self, *args, **kwargs):
        # Support rescaling
        # if hasattr(settings, 'OUTPUT_WIDTH') and hasattr(settings, 'OUTPUT_HEIGHT'):
        #     self.rescale = False

        # Initialize modules
        super(Pypboy, self).__init__(*args, **kwargs)
        self.init_persitant()
        self.init_modules()

        self.gpio_actions = {}
        # if settings.GPIO_AVAILABLE:
        # self.init_gpio_controls()

        self.prev_fps_time = 0

    def init_persitant(self):
        # self.background = pygame.image.load('images/background.png')
        overlay = pypboy.ui.Overlay()
        self.root_persitant.add(overlay)
        scanlines = pypboy.ui.Scanlines()
        self.root_persitant.add(scanlines)
        pass

    def init_modules(self):
        self.modules = {
            "radio": radio.Module(self),
            "map": map.Module(self),
            "data": data.Module(self),
            "items": items.Module(self),
            "stats": stats.Module(self),
            "boot": boot.Module(self),
            "passcode": passcode.Module(self)
        }
        self.switch_module(settings.STARTER_MODULE)  # Set the start screen

    def init_gpio_controls(self):
        for pin in settings.gpio_actions.keys():
            print("Initialing pin %s as action '%s'" % (pin, settings.gpio_actions[pin]))
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.gpio_actions[pin] = settings.gpio_actions[pin]

    def check_gpio_input(self):
        for pin in self.gpio_actions.keys():
            if GPIO.input(pin) == False:
                self.handle_action(self.gpio_actions[pin])

    # def render(self):
    #     super(Pypboy, self).render()
    #     if hasattr(self, 'active'):
    #         self.active.render()

    def switch_module(self, module):
        # if not settings.hide_top_menu:
        if module in self.modules:
            if hasattr(self, 'active'):
                self.active.handle_action("pause")
                self.remove(self.active)
            self.active = self.modules[module]
            self.active.parent = self
            self.active.handle_action("resume")
            self.add(self.active)
        else:
            print("Module '%s' not implemented." % module)

    def handle_action(self, action):
        if action.startswith('module_'):
            self.switch_module(action[7:])
        else:
            if hasattr(self, 'active'):
                self.active.handle_action(action)

    def handle_event(self, event):
        pygame.mouse.set_visible(True) # set mouse visible for measurement, hacked into position @TODO: REMOVE
        if event.type == pygame.KEYDOWN:  # Some key has been pressed
            # Persistent Events:
            if event.key == pygame.K_ESCAPE:  # ESC
                self.running = False

            elif event.key == pygame.K_PAGEUP:  # Volume up
                settings.radio.handle_radio_event(event)
            elif event.key == pygame.K_PAGEDOWN:  # Volume down
                settings.radio.handle_radio_event(event)
            elif event.key == pygame.K_END:  # Next Song
                settings.radio.handle_radio_event(event)
            elif event.key == pygame.K_HOME:  # Prev Song
                settings.radio.handle_radio_event(event)
            elif event.key == pygame.K_DELETE:
                settings.radio.handle_radio_event(event)
            elif event.key == pygame.K_INSERT:
                settings.radio.handle_radio_event(event)
            else:
                if event.key in settings.ACTIONS:  # Check action based on key in settings
                    self.handle_action(settings.ACTIONS[event.key])

        elif event.type == pygame.MOUSEBUTTONDOWN: # making the touch code synced with mouse for PC testing
            pos = pygame.mouse.get_pos()
            #print("coords of click: ", pos[0], ", ", pos[1])
            if 48 <= pos[1] <= 88: # check if click is in bar row
                if 100 <= pos[0] <= 170: # stat
                    self.handle_action("module_stats")
                elif 200 <= pos[0] <= 260: # inv
                    self.handle_action("module_items")
                elif 285 <= pos[0] <= 390: # data
                    self.handle_action("module_data")
                elif 410 <= pos[0] <= 475: # map
                    self.handle_action("module_map")
                elif 515 <= pos[0] <= 610: # radio
                    self.handle_action("module_radio")
                else:
                    pass
                print("\n\n", type(self.active), "\n\n") #testing module codes
            elif 95 <= pos[1] <= 125: #click is a submodule, @TODO: make this a member function
                if self.active == self.modules['stats']:
                    if 95 <= pos[0] <= 195:
                        self.handle_action("knob_1")
                    elif 205 <= pos[0] <= 310:
                        self.handle_action("knob_2")
                    elif 325 <= pos[0] <= 410:
                        self.handle_action("knob_3")
                elif self.active == self.modules['items']:
                    if 95 <= pos[0] <= 225:
                        self.handle_action("knob_1")
                    elif 235 <= pos[0] <= 350:
                        self.handle_action("knob_2")
                    elif 365 <= pos[0] <= 405:
                        self.handle_action("knob_3")
                    elif 410 <= pos[0] <= 485:
                        self.handle_action("knob_4")
                    elif 495 <= pos[0] <= 580:
                        self.handle_action("knob_5")

                elif self.active == self.modules['data']:
                    if 95 <= pos[0] <= 245:
                        self.handle_action("knob_1")
                    elif 255 <= pos[0] <= 360:
                        self.handle_action("knob_2")
                    elif 370 <= pos[0] <= 440:
                        self.handle_action("knob_3")
                elif self.active == self.modules['map']:
                    if 95 <= pos[0] <= 250:
                        self.handle_action("knob_1")
                    elif 260 <= pos[0] <= 410:
                        self.handle_action("knob_2")
                else:
                    print("module has no subclick implementation")

            print("horizontal click position: ", pos[0])

        elif event.type == pygame.FINGERDOWN: # handling touchscreen inputs
            pos = pygame.finger.get_pos();
            if 48 <= pos[1] <= 88: # check if tap is in bar row
                if 100 <= pos[0] <= 170: # stat
                    self.handle_action("module_stats")
                elif 200 <= pos[0] <= 260: # inv
                    self.handle_action("module_items")
                elif 285 <= pos[0] <= 390: # data
                    self.handle_action("module_data")
                elif 410 <= pos[0] <= 475: # map
                    self.handle_action("module_map")
                elif 515 <= pos[0] <= 610: # radio
                    self.handle_action("module_radio")
                else:
                    pass

        elif event.type == pygame.QUIT:
            self.running = False

        elif event.type == settings.EVENTS['SONG_END']:
            if settings.SOUND_ENABLED:
                if hasattr(settings, 'radio'):
                    settings.radio.handle_radio_event(event)
        elif event.type == settings.EVENTS['PLAYPAUSE']:
            if settings.SOUND_ENABLED:
                if hasattr(settings, 'radio'):
                    settings.radio.handle_radio_event(event)
        else:
            if hasattr(self, 'active'):
                self.active.handle_event(event)

    def inRange(self, angle, init, end):
        return (angle >= init) and (angle < end)

    def run(self):
        self.running = True
        while self.running:
            self.check_gpio_input()
            for event in pygame.event.get():
                self.handle_event(event)
                if hasattr(self, 'active'):
                    self.active.handle_event(event)

            # slow code debugger
            # debug_time = time.time()

            self.render()
            #
            # time_past = time.time() - debug_time
            # if time_past:
            #     max_fps = int(1 / time_past)
            #     print("self.render took:", time_past, "max fps:", max_fps)

        try:
            pygame.mixer.quit()
        except Exception as e:
            print(e)
