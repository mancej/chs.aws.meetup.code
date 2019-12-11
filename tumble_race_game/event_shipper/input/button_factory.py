from input.nes_button import NESButton, NESAxis
import logging


class ButtonFactory:

    @staticmethod
    def instance(button_id=None, button_axis=None, button_value=None):
        if button_id is not None:
            return NESButton(button_id)
        elif button_axis is not None and button_value is not None:
            return NESAxis(button_axis, button_value)
        else:
            raise ValueError("Invalid button press detected.")
