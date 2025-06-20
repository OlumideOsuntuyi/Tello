import tkinter as tk

class Rect:
    def __init__(self, canvas, parent=None, anchor=(0, 0), size=(100, 100), stretch=(0, 0)):
        self.canvas = canvas
        self.parent = parent
        self.set_parent(parent or canvas)
        self.anchor_x, self.anchor_y = anchor
        self.width_fixed, self.height_fixed = size
        self.stretch_x, self.stretch_y = stretch
        self.left = self.top = self.right = self.bottom = 0

    def set_parent(self, parent):
        self.parent = parent or self.canvas

    def _get_parent_size(self):
        if isinstance(self.parent, tk.Canvas):
            return int(self.canvas['width']), int(self.canvas['height'])
        if isinstance(self.parent, Rect):
            return self.parent.width(), self.parent.height()
        else:
            return 0, 0

    def set_position(self):
        pw, ph = self._get_parent_size()

        w = self.width_fixed + self.stretch_x * pw
        h = self.height_fixed + self.stretch_y * ph

        cx = self.anchor_x * pw
        cy = self.anchor_y * ph

        self.left = cx - w / 2
        self.top = cy - h / 2
        self.right = self.left + w
        self.bottom = self.top + h

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top

    def draw(self, **kwargs):
        return self.canvas.create_rectangle(self.left, self.top, self.right, self.bottom, **kwargs)
