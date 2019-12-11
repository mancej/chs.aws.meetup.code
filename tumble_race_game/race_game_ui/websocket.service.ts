import {Injectable} from '@angular/core';
import {Subject, Observable, Observer} from 'rxjs';

@Injectable()
export class WebsocketService {
    constructor() {
    }

    private subject: Subject<MessageEvent>;
    public socket_open = false;
    public subscription;
    private socket: WebSocket;

    public connect(url): Subject<MessageEvent> {
        if (!this.subject) {
            this.subject = this.create(url);
        }
        return this.subject;
    }

    public subscribe(subscription) {
        this.socket.send(JSON.stringify(subscription));
    }

    private setOpen(val) {
        this.socket_open = val;
    }

    public isOpen = () => this.socket_open;

    private create(url): Subject<MessageEvent> {
        // const WS = new WebSocket(url);
        this.socket = new WebSocket(url);

        const OBSERVABLE = Observable.create((obs: Observer<MessageEvent>) => {
            this.socket.onopen = () => {
                this.setOpen(true);
                this.subscribe(this.subscription);
            };
            this.socket.onmessage = obs.next.bind(obs);
            this.socket.onerror = obs.error.bind(obs);
            this.socket.onclose = obs.complete.bind(obs);
            return this.socket.close.bind(this.socket);
        });
        const observer = {
            next: (data: Object) => {
                if (this.socket.readyState === WebSocket.OPEN) {
                    this.socket.send(JSON.stringify(data));
                }
            }
        };
        return Subject.create(observer, OBSERVABLE);
    }
}
