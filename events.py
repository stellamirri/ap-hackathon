import pyxel

_handlers = []

def register(event, handler):
    _handlers.append([event, handler])

def handle():
    for event, handler in _handlers:
        if pyxel.btnp(event):
            handler()
            