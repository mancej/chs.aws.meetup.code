import websocket
import json


def on_message(ws, message):
    print(json.loads(message))


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
