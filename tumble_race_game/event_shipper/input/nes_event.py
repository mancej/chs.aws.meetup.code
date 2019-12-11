from input.colored_joystick import ColoredJoystick, MockJoystick
from input.nes_button import NESButton, NESAxis
import json
import uuid


class NESEvent:
    _MESSAGE_TYPE = 'NESClick'
    _IOT_ACTION = 'submitIotEvent'
    _KINESIS_SOURCE = 'kinesis'
    _WS_SOURCE = 'websocket'

    def __init__(self, joystick: [ColoredJoystick, MockJoystick], button: [NESButton, NESAxis], axis: int = 0,
                 value: int = 0):
        self.color: str = joystick.color
        self.button: [NESButton, NESAxis] = button
        self.axis: int = axis
        self.value: int = value

    def kinesis_format(self):
        return json.dumps({
            'MessageType': self._MESSAGE_TYPE,
            'Message': {
                'color': self.color,
                'button': self.button.button,
                'axis': self.axis,
                'value': self.value,
                'source': self._KINESIS_SOURCE
            },
        })

    def websocket_format(self):
        return {
            'action': self._IOT_ACTION,
            'event': {
                'MessageType': self._MESSAGE_TYPE,
                'Message': {
                    'color': self.color,
                    'button': self.button.button,
                    'axis': self.axis,
                    'value': self.value,
                    'source': self._WS_SOURCE
                },
            }
        }

    def kinesis_record(self):
        return {
            'Data': self.kinesis_format().encode('utf-8'),
            'PartitionKey': str(uuid.uuid4())
        }

    def __str__(self):
        return f"{self.color}: {self.button.button}"
