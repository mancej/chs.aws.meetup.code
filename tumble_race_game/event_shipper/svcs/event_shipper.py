import boto3
import logging
import time
import uuid
import json
import websocket
from typing import Dict
from joystick_config import *
from typing import List
from input.nes_event import NESEvent
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from websocket import WebSocketApp
from svcs.sound_processor import SoundProcessor

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class EventShipper:

    def __init__(self, conveyor: Queue, websocket: WebSocketApp):
        self._kinesis = boto3.client('kinesis')
        self._conveyor = conveyor
        self._ws = websocket
        self._sound_processor = SoundProcessor()
        self._recent_events = []
        self._MIC_RECORD_CODE = ["START", "START", "SELECT", "SELECT"]

    def send_events(self, events: List[NESEvent]):

        records = [event.kinesis_record() for event in events]
        ws_events = [event.websocket_format() for event in events]

        with ThreadPoolExecutor(max_workers=2) as pool:
            pool.submit(self._kinesis.put_records,
                        StreamName=IOT_EVENT_STREAM_NAME,
                        Records=records)

            for event in ws_events:
                try:
                    self._ws.send(json.dumps(event))
                except websocket.WebSocketConnectionClosedException as e:
                    log.info("Websocket connection was lost, but it should auto-reconnect.")
                    log.info(e)

    def ship_events(self):
        keep_running = True

        socket_conn = Thread(target=self.run_forever, args=())
        socket_conn.start()
        log.info("Socket running..")

        while keep_running:
            events: List[NESEvent] = []
            while not self._conveyor.empty():
                event = self._conveyor.get_nowait()
                events.append(event)
                self._recent_events.append(event.button.button)

                if len(self._recent_events) > 3:
                    if self._recent_events == self._MIC_RECORD_CODE:
                        self._recent_events = []
                        consumer = Thread(target=self._sound_processor.record, args=(5, 'last_recording'))
                        consumer.start()
                    else:
                        self._recent_events.pop(0)
                else:
                    log.info(f"{self._recent_events} != {self._MIC_RECORD_CODE}")

            if events:
                self.send_events(events)
            else:
                time.sleep(.05)

    def run_forever(self):
        try:
            self._ws.run_forever()
        except:
            pass
