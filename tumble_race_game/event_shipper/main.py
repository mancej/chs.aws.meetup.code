import pygame
import boto3
import logging
import time
import sys
from input.colored_joystick import ColoredJoystick, MockJoystick
from input.nes_event import NESEvent
from input.button_factory import ButtonFactory
from input.nes_button import NESButton, NESAxis
from svcs.event_shipper import EventShipper
from threading import Thread
from multiprocessing import Queue, Manager
from websocket import WebSocketApp
from pprint import pprint
import random
import os
from config import *

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stdout)
root_logger.addHandler(stdout_handler)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

pygame.init()

colors = ['red', 'blue', 'green', 'yellow']
joysticks = [ColoredJoystick(x, colors[x]) for x in range(pygame.joystick.get_count())]

for joystick in joysticks:
    log.info(f"Initializing: {joystick.joystick.get_name()} on color: {joystick.color} and index: {joystick.index}")

color_override = os.environ['COLOR_OVERRIDE'] if 'COLOR_OVERRIDE' in os.environ else None

if color_override:
    log.info(f"Overriding all joystick evnets for color: {color_override}")
    joysticks = [ColoredJoystick(x, color_override) for x in range(pygame.joystick.get_count())]

keep_shipping = True

mgr = Manager()
conveyor: Queue = mgr.Queue(maxsize=0)
websocket: WebSocketApp = WebSocketApp(WS_URL)
shipper: EventShipper = EventShipper(conveyor, websocket)

consumer = Thread(target=shipper.ship_events, args=())
consumer.start()

while keep_shipping:
    time.sleep(.01)
    for event in pygame.event.get():
        button = event.button if hasattr(event, 'button') else None
        axis = event.axis if hasattr(event, 'axis') else None
        value = int(event.value) if hasattr(event, 'value') else None
        joy = event.joy if hasattr(event, 'joy') else None
        event_type = event.type if hasattr(event, 'type') else None

        # Skip button depress events, and non joystick events.
        if joy is None or event_type == 11:
            continue

        mapped_joy = [j for j in joysticks if j.index == joy][0]
        button = ButtonFactory.instance(button_id=button, button_axis=axis, button_value=value)
        nes_event = NESEvent(mapped_joy, button, axis, value)

        log.info(nes_event)
        conveyor.put_nowait(nes_event)


"""
Used for testing without hooking up all the joysticks
"""

# while not done:
#     colors = ['red', 'blue', 'green', 'yellow']
#     time.sleep(.25)
#     color = random.choice(colors)
#     joy = MockJoystick(colors.index(color), color)
#     event1 = NESEvent(joy, NESButton(random.choice([0, 1])))
#     event2 = NESEvent(joy, NESAxis(random.choice([0, 1]), random.choice([1, -1])))
#     event_choice = random.choice([event1, event2])
#     conveyor.put_nowait(event_choice)
#     log.info(f"Event sent: {event_choice}")


# while keep_shipping:
#     colors = ['red', 'blue', 'green', 'yellow']
#     time.sleep(.25)
#     color = random.choice(colors)
#     joy = MockJoystick(colors.index(color), color)
#     event1 = NESEvent(joy, NESButton(6))
#     event2 = NESEvent(joy, NESButton(7))
#     event3 = NESEvent(joy, NESButton(6))
#     event4 = NESEvent(joy, NESButton(7))
#     event5 = NESEvent(joy, NESButton(0))
#     event6 = NESEvent(joy, NESButton(1))
#     event7 = NESEvent(joy, NESButton(0))
#     event8 = NESEvent(joy, NESButton(1))
#     # event_choice = random.choice([event1, event2])
#     conveyor.put_nowait(event1)
#     conveyor.put_nowait(event2)
#     conveyor.put_nowait(event3)
#     conveyor.put_nowait(event4)
#     conveyor.put_nowait(event5)
#     conveyor.put_nowait(event6)
#     conveyor.put_nowait(event7)
#     conveyor.put_nowait(event8)
#     print("Code sent, sleeping...")
#     time.sleep(1)
