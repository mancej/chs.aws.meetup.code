/* tslint:disable:no-trailing-whitespace */
import { Injectable } from '@angular/core';
import { Subject, Observable, Observer } from 'rxjs';
import { WebsocketService } from './websocket.service';
import { map } from 'rxjs/operators';

const SOCKET_URL = 'SOCKET_URL_HERE';

@Injectable()
export class EventStreamService {
  public messages: Subject<any>;

  constructor() {
    const sub_data = {
      'action': 'subscribe',
      'subscriptions':
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
    };

    const wsService = new WebsocketService();

    wsService.subscription = sub_data;

    this.messages = <Subject<any>>wsService.connect(SOCKET_URL).pipe(map(
      (response: MessageEvent): any => {
        return JSON.parse(response.data);
      }
    ));
  }
}
