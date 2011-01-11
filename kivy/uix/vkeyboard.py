__all__ = ('VKeyboard', )

from kivy.uix.scatter import Scatter
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty

class KeyboardLayout(object):
    '''Base for all Keyboard Layout'''
    ID              = 'nolayout'
    TITLE           = 'nolayout'
    DESCRIPTION     = 'nodescription'
    FONT_FILENAME   = None
    NORMAL_1 = []
    NORMAL_2 = []
    NORMAL_3 = []
    NORMAL_4 = []
    NORMAL_5 = []
    SHIFT_1 = []
    SHIFT_2 = []
    SHIFT_3 = []
    SHIFT_4 = []
    SHIFT_5 = []
    # Actual letters. No numbers or special chars or keys. Upper & lower.
    LETTERS = []

class KeyboardLayoutQWERTY(KeyboardLayout):
    '''Implementation of QWERTY Layout'''
    ID              = 'qwerty'
    TITLE           = 'Qwerty'
    DESCRIPTION     = 'A classical US Keyboard'
    SIZE            = (15, 5)
    NORMAL_1 = [
        ('`', '`', None, 1),    ('1', '1', None, 1),    ('2', '2', None, 1),
        ('3', '3', None, 1),    ('4', '4', None, 1),    ('5', '5', None, 1),
        ('6', '6', None, 1),    ('7', '7', None, 1),    ('8', '8', None, 1),
        ('9', '9', None, 1),    ('0', '0', None, 1),    ('+', '+', None, 1),
        ('=', '=', None, 1),    (u'\u232b', None, 'backspace', 2),
    ]
    NORMAL_2 = [
        (u'\u21B9', chr(0x09), None, 1.5),  ('q', 'q', None, 1),    ('w', 'w', None, 1),
        ('e', 'e', None, 1),    ('r', 'r', None, 1),    ('t', 't', None, 1),
        ('y', 'y', None, 1),    ('u', 'u', None, 1),    ('i', 'i', None, 1),
        ('o', 'o', None, 1),    ('p', 'p', None, 1),    ('{', '{', None, 1),
        ('}', '}', None, 1),    ('|', '|', None, 1.5)
    ]
    NORMAL_3 = [
        (u'\u21ea', None, 'capslock', 1.8),  ('a', 'a', None, 1),    ('s', 's', None, 1),
        ('d', 'd', None, 1),    ('f', 'f', None, 1),    ('g', 'g', None, 1),
        ('h', 'h', None, 1),    ('j', 'j', None, 1),    ('k', 'k', None, 1),
        ('l', 'l', None, 1),    (':', ':', None, 1),    ('"', '"', None, 1),
        (u'\u23ce', None, 'enter', 2.2),
    ]
    NORMAL_4 = [
        (u'\u21e7', None, 'shift_L', 2.5),  ('z', 'z', None, 1),    ('x', 'x', None, 1),
        ('c', 'c', None, 1),    ('v', 'v', None, 1),    ('b', 'b', None, 1),
        ('n', 'n', None, 1),    ('m', 'm', None, 1),    ('<', '<', None, 1),
        ('>', '>', None, 1),    ('?', '?', None, 1),    (u'\u21e7', None, 'shift_R', 2.5),
    ]
    NORMAL_5 = [
        (' ', ' ', None, 12), (u'\u2b12', None, 'layout', 1.5), (u'\u2a2f', None, 'escape', 1.5),

    ]
    SHIFT_1 = [
        ('~', '~', None, 1),    ('!', '!', None, 1),    ('@', '@', None, 1),
        ('#', '#', None, 1),    ('$', '$', None, 1),    ('%', '%', None, 1),
        ('^', '^', None, 1),    ('&', '&', None, 1),    ('*', '*', None, 1),
        ('(', '(', None, 1),    (')', ')', None, 1),    ('_', '_', None, 1),
        ('+', '+', None, 1),    (u'\u232b', None, 'backspace', 2),
    ]
    SHIFT_2 = [
        (u'\u21B9', chr(0x09), None, 1.5),  ('Q', 'Q', None, 1),    ('W', 'W', None, 1),
        ('E', 'E', None, 1),    ('R', 'R', None, 1),    ('T', 'T', None, 1),
        ('Y', 'Y', None, 1),    ('U', 'U', None, 1),    ('I', 'I', None, 1),
        ('O', 'O', None, 1),    ('P', 'P', None, 1),    ('[', '[', None, 1),
        (']', ']', None, 1),    ('?', '?', None, 1.5)
    ]
    SHIFT_3 = [
        (u'\u21ea', None, 'capslock', 1.8),  ('A', 'A', None, 1),    ('S', 'S', None, 1),
        ('D', 'D', None, 1),    ('F', 'F', None, 1),    ('G', 'G', None, 1),
        ('H', 'H', None, 1),    ('J', 'J', None, 1),    ('K', 'K', None, 1),
        ('L', 'L', None, 1),    (':', ':', None, 1),    ('"', '"', None, 1),
        (u'\u23ce', None, 'enter', 2.2),
    ]
    SHIFT_4 = [
        (u'\u21e7', None, 'shift_L', 2.5),  ('Z', 'Z', None, 1),    ('X', 'X', None, 1),
        ('C', 'C', None, 1),    ('V', 'V', None, 1),    ('B', 'B', None, 1),
        ('N', 'N', None, 1),    ('M', 'M', None, 1),    (',', ',', None, 1),
        ('.', '.', None, 1),    ('/', '/', None, 1),    (u'\u21e7', None, 'shift_R', 2.5),
    ]
    SHIFT_5 = [
        (' ', ' ', None, 12), (u'\u2b12', None, 'layout', 1.5), (u'\u2a2f', None, 'escape', 1.5),
    ]

    LETTERS = NORMAL_2[1:11] + NORMAL_3[1:10] + NORMAL_4[1:8] + \
              SHIFT_2[1:11] + SHIFT_3[1:10] + SHIFT_4[1:8]


class KeyboardLayoutAZERTY(KeyboardLayout):
    '''Implementation of AZERTY Layout'''
    ID              = 'azerty'
    TITLE           = 'Azerty'
    DESCRIPTION     = 'A French keyboard without international keys'
    SIZE            = (15, 5)
    NORMAL_1 = [
        ('@', '@', None, 1),    ('&', '&', None, 1),    (u'\xe9', u'\xe9', None, 1),
        ('"', '"', None, 1),    ('\'', '\'', None, 1),  ('(', '(', None, 1),
        ('-', '-', None, 1),    (u'\xe8', u'\xe8', None, 1),    ('_', '_', None, 1),
        (u'\xe7', u'\xe7', None, 1),    (u'\xe0', u'\xe0', None, 1),    (')', ')', None, 1),
        ('=', '=', None, 1),    (u'\u232b', None, 'backspace', 2),
    ]
    NORMAL_2 = [
        (u'\u21B9', chr(0x09), None, 1.5),  ('a', 'a', None, 1),    ('z', 'z', None, 1),
        ('e', 'e', None, 1),    ('r', 'r', None, 1),    ('t', 't', None, 1),
        ('y', 'y', None, 1),    ('u', 'u', None, 1),    ('i', 'i', None, 1),
        ('o', 'o', None, 1),    ('p', 'p', None, 1),    ('^', '^', None, 1),
        ('$', '$', None, 1),    (u'\u23ce', None, 'enter', 1.5),
    ]
    NORMAL_3 = [
        (u'\u21ea', None, 'capslock', 1.8),  ('q', 'q', None, 1),    ('s', 's', None, 1),
        ('d', 'd', None, 1),    ('f', 'f', None, 1),    ('g', 'g', None, 1),
        ('h', 'h', None, 1),    ('j', 'j', None, 1),    ('k', 'k', None, 1),
        ('l', 'l', None, 1),    ('m', 'm', None, 1),    (u'\xf9', u'\xf9', None, 1),
        ('*', '*', None, 1),    (u'\u23ce', None, 'enter', 1.2),
    ]
    NORMAL_4 = [
        (u'\u21e7', None, 'shift_L', 1.5),  ('<', '<', None, 1),    ('w', 'w', None, 1),
        ('x', 'x', None, 1),
        ('c', 'c', None, 1),    ('v', 'v', None, 1),    ('b', 'b', None, 1),
        ('n', 'n', None, 1),    (',', ',', None, 1),    (';', ';', None, 1),
        (':', ':', None, 1),    ('!', '!', None, 1),    (u'\u21e7', None, 'shift_R', 2.5),
    ]
    NORMAL_5 = [
        (' ', ' ', None, 12), (u'\u2b12', None, 'layout', 1.5), (u'\u2a2f', None, 'escape', 1.5),
    ]
    SHIFT_1 = [
        ('|', '|', None, 1),    ('1', '1', None, 1),    ('2', '2', None, 1),
        ('3', '3', None, 1),    ('4', '4', None, 1),    ('5', '5', None, 1),
        ('6', '6', None, 1),    ('7', '7', None, 1),    ('8', '8', None, 1),
        ('9', '9', None, 1),    ('0', '0', None, 1),    ('#', '#', None, 1),
        ('+', '+', None, 1),    (u'\u232b', None, 'backspace', 2),
    ]
    SHIFT_2 = [
        (u'\u21B9', chr(0x09), None, 1.5),  ('A', 'A', None, 1),    ('Z', 'Z', None, 1),
        ('E', 'E', None, 1),    ('R', 'R', None, 1),    ('T', 'T', None, 1),
        ('Y', 'Y', None, 1),    ('U', 'U', None, 1),    ('I', 'I', None, 1),
        ('O', 'O', None, 1),    ('P', 'P', None, 1),    ('[', '[', None, 1),
        (']', ']', None, 1),    (u'\u23ce', None, 'enter', 1.5),
    ]
    SHIFT_3 = [
        (u'\u21ea', None, 'capslock', 1.8),  ('Q', 'Q', None, 1),    ('S', 'S', None, 1),
        ('D', 'D', None, 1),    ('F', 'F', None, 1),    ('G', 'G', None, 1),
        ('H', 'H', None, 1),    ('J', 'J', None, 1),    ('K', 'K', None, 1),
        ('L', 'L', None, 1),    ('M', 'M', None, 1),    ('%', '%', None, 1),
        (u'\xb5', u'\xb5', None, 1),    (u'\u23ce', None, 'enter', 1.2),
    ]
    SHIFT_4 = [
        (u'\u21e7', None, 'shift_L', 1.5),  ('>', '>', None, 1),    ('W', 'W', None, 1),
        ('X', 'X', None, 1),    ('C', 'C', None, 1),    ('V', 'V', None, 1),
        ('B', 'B', None, 1),    ('N', 'N', None, 1),    ('?', '?', None, 1),
        ('.', '.', None, 1),    ('/', '/', None, 1),    (u'\xa7', u'\xa7', None, 1),
        (u'\u21e7', None, 'shift_R', 2.5),
    ]
    SHIFT_5 = [
        (' ', ' ', None, 12), (u'\u2b12', None, 'layout', 1.5), (u'\u2a2f', None, 'escape', 1.5),
    ]

    LETTERS = NORMAL_2[1:11] + NORMAL_3[1:11] + NORMAL_4[2:8] + \
              SHIFT_2[1:11] + SHIFT_3[1:11] + SHIFT_4[2:8]


class VKeyboard(Scatter):

    layout_object = ObjectProperty(KeyboardLayoutAZERTY)

    layout = StringProperty('azerty')

    shift = BooleanProperty(False)

    def __init__(self, **kwargs):
        kwargs.setdefault('scale_min', .5)
        kwargs.setdefault('scale_max', 3)
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('size', (700, 200))
        super(VKeyboard, self).__init__(**kwargs)
        self.root = BoxLayout()
        self.root.pos = (20, 20)
        self.root.size = (self.width - 40, self.height - 40)
        self.add_widget(self.root)
        self._layouts = [None, None]
        self.build_layout()

    def on_layout(self, *largs):
        self.build_layout()
        self.update_selected_layout()

    def update_selected_layout(self):
        self.root.clear_widgets()
        layout = self._layouts[int(self.shift)]
        self.root.add_widget(layout)

    def build_layout(self, *largs):
        # build shift and non shift layout.
        self.root.clear_widgets()
        self._layouts[0] = self.build_layout_mode('NORMAL')
        self._layouts[1] = self.build_layout_mode('SHIFT')
        self.update_selected_layout()

    def build_layout_mode(self, mode):
        layout = self.layout_object
        lw, lh = layout.SIZE

        vlayout = BoxLayout(orientation='vertical')

        for index in xrange(1, lh + 1):
            line = getattr(layout, '%s_%d' % (mode, index))
            hlayout = BoxLayout(orientation='horizontal')

            for key in line:
                displayed_str, internal_str, internal_action, scale = key
                button = Button(text=displayed_str, size_hint=(scale, 1))
                hlayout.add_widget(button)

            vlayout.add_widget(hlayout)

        return vlayout


