import websocket
import json
from sty import fg

fg_bl = fg(33)
fg_gr = fg(2)
fg_rd = fg(160)
rs = fg.rs


def on_message(ws, message):
    message = json.loads(message)
    payload = json.loads(message.get('payload'))
    source = payload.get('source')

    if source == 'kinesis':
        print(f"{fg_bl}KINESIS:{rs} {payload.get('button')}")
    if source == 'websocket':
        print(f"{fg_gr}WEBSOCKET:{rs} {payload.get('button')}")


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("Socket opened...subscribing")
    subscribe(ws)


def subscribe(ws):
    subscription_msg = \
        {
            "action": "subscribe",
            "subscriptions":
                [
                    {
                        "event_type": "DashClick",
                        "filter_field": "event",
                        "filter_expr": "*"
                    },
                    {
                        "event_type": "NESClick",
                        "filter_field": "color",
                        "filter_expr": "*"
                    },
                    {
                        "event_type": "PhotoUpload",
                        "filter_field": "key",
                        "filter_expr": "*"
                    },
                    {
                        "event_type": "PhotoCropped",
                        "filter_field": "key",
                        "filter_expr": "*"
                    },
                    {
                        "event_type": "TranscribeEvent",
                        "filter_field": "key",
                        "filter_expr": "*"
                    },

                ]
        }

    for subscription in subscription_msg['subscriptions']:
        print(f"Subscribing to: {subscription.get('event_type')}")

    ws.send(
        json.dumps(subscription_msg)
    )
    print("\n\n")


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("WS_URL",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

"""

{
    "action": "subscribe",
    "subscriptions": [
        {
            "event_type": "ApplicationCompletedFact",
            "filter_field": "postal_code",
            "filter_expr": "*",
            "desired_fields": ["postal_code", "city", "org_id"]
        },
        {
            "event_type": "signals.find.ApplicationIntentClickedV2",
            "filter_field": "posting_id",
            "filter_expr": "*"
        }
    ]
}

"""
