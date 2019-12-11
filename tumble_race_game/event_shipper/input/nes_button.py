class NESButton:
    _BUTTON_MAP = {
        0: 'A',
        1: 'B',
        6: 'SELECT',
        7: 'START'
    }

    def __init__(self, button_id: int):
        assert button_id in self._BUTTON_MAP.keys()

        self.button = self._BUTTON_MAP[button_id]


class NESAxis:
    _BUTTON_MAP = {
        (1, -1): "UP",
        (1, 1): "DOWN",
        (0, -1): "LEFT",
        (0, 1): "RIGHT",
        (1, 0): "VERT_NEUTRAL",
        (0, 0): "HORIZONTAL_NEUTRAL"
    }

    def __init__(self, button_axis: int, button_value: int):
        assert (button_axis, button_value) in self._BUTTON_MAP.keys()

        self.button = self._BUTTON_MAP[(button_axis, button_value)]
