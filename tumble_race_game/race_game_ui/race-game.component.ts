/* tslint:disable:no-trailing-whitespace */
import {
    Component,
    OnInit,
    ViewChild,
    OnDestroy,
    ElementRef,
    ChangeDetectionStrategy,
    ChangeDetectorRef, NgModule
} from '@angular/core';

import {map} from 'rxjs/operators';

import {EventStreamService} from './app-event-stream.service';
import {ColorState, RaceGameModel} from './race-game.model';
import {RaceGameSliderComponent} from "./race-game-slider.component";

@Component({
    selector: 'race-game',
    templateUrl: './race-game.component.html',
    styleUrls: ['./race-game.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class RaceGameComponent implements OnInit, OnDestroy {


    static RED = '#fc4c66';
    static BLUE = '#00d5ff';
    static GREEN = '#86f799';
    static YELLOW = '#edf55b';
    static SELECTION_COLOR = '#19d4d1';
    static KINESIS_SOURCE = 'kinesis';
    static WEBSOCKET_SOURCE = 'websocket';

    // Constants
    NES_CLICK = "NESClick";
    DASH_CLICK = "DashClick";
    PHOTO_UPLOAD = "PhotoUpload";
    PHOTO_CROPPED = "PhotoCropped";
    AUDIO_TRANSCRIBED = "TranscribeEvent";
    TOGGLE_KINESIS = 'toggle-kinesis';
    TOGGLE_SELECTION = 'toggle-selection';
    TOGGLE_GAME = 'toggle-game';
    MAX_CLICKS = 40;
    MAX_POWER_UP_CLICKS = 10;
    BUTTONS = ["UP", "DOWN", "LEFT", "RIGHT", "A", "B"];
    NEUTRAL = ["VERT_NEUTRAL", "HORIZONTAL_NEUTRAL"];
    TARGET_BUTTONS = ["UP", "DOWN", "A", "B"];
    SELECT_USER = ["SELECT", "START", "SELECT", "START"];
    RANDOM_RESET = ["SELECT", "START", "B", "A"];
    RECORD_AUDIO = ["START", "START", "SELECT", "SELECT"];

    // Component State
    paused = true;
    paused_text = "[[ PAUSED ]]";
    winner = false;
    kinesis_enabled = true;
    winner_text = "???";
    winner_color = "";
    model = new RaceGameModel(this.MAX_CLICKS, this.MAX_POWER_UP_CLICKS);
    selection_order = ['none', ColorState.RED, ColorState.BLUE, ColorState.GREEN, ColorState.YELLOW];
    selection_index = 1;
    last_update = Date.now();
    show_microphone = false;

    constructor(private eventStreamService: EventStreamService, private cdr: ChangeDetectorRef,
                private slider: RaceGameSliderComponent) {}

    ngOnInit() {
        this.cdr.detectChanges();
        this.slider.set_all(ColorState.DEFAULT_IMG, this.kinesis_enabled);
        this.slider.rotate_all(90, this.kinesis_enabled);

        setInterval(() => {
            this.update_gauges();
            this.cdr.detectChanges();
        }, 100);


        this.eventStreamService.messages.subscribe(event => {
            const event_type = event.message_type;
            const payload = JSON.parse(event.payload);
            const color = payload.color;
            const button = payload.button;
            const source = payload.source;

            if (event_type == this.NES_CLICK  && !this.winner) {
                this.register_nes_click(button, color, source);
                this.check_winner(color);
            } else if (event_type == this.DASH_CLICK) {
                this.register_dash_click(payload)
            } else if (event_type == this.PHOTO_UPLOAD) {
                this.update_user_image(`https://${payload.bucket}.s3.amazonaws.com/${encodeURI(payload.key)}`,
                    payload.emotion, payload.confidence)
            } else if (event_type == this.PHOTO_CROPPED) {
                const cropped_image = `https://${payload.bucket}.s3.amazonaws.com/${encodeURI(payload.key)}`;
                this.update_slider_image();
                this.update_avatar(cropped_image);
            } else if (event_type == this.AUDIO_TRANSCRIBED) {
                this.model.set_name(payload.transcribed_text, this.get_selected_color());
                this.model.reset_all_hist()
            }

            // this.update_gauges();
            this.cdr.detectChanges()
        });
    }

    register_nes_click(button: string, color: string, source: string) {
        this.model.increment_request_count(color);

        // Do not register neutrals clicks.
        if (this.NEUTRAL.includes(button)) {
            return
        }

        let hist_item = this.model.push_click(button, color, source);

        const hist_equals_select = this.compare_hists(hist_item, this.SELECT_USER);
        if (hist_equals_select && this.paused) {
            this.select_color(color);
            return;
        }

        const hist_equals_record  = this.compare_hists(hist_item, this.RECORD_AUDIO);
        if (hist_equals_record && this.paused) {
            this.toggle_microphone();
            return;
        }

        // Only shift if we've had enough clicks for color.
        if (hist_item.length >= this.TARGET_BUTTONS.length && !this.paused) {
            // If most recent clicks match the current target
            const hist_equals_target = this.compare_hists(hist_item, this.TARGET_BUTTONS);
            if (hist_equals_target) {
                this.shift_color(color, source, true);
                return;
            }

            if (this.model.is_target_code_reset_available(color)) {
                const hist_equals_random = this.compare_hists(hist_item, this.RANDOM_RESET);
                if (hist_equals_random && !this.paused) {
                    this.change_target_buttons(Math.ceil(1 + Math.random() * 3));
                    this.model.consume_target_code_reset(color);
                    let i; // Undo penalty of reset.
                    for (i = 0; i < 4; i++) {
                        this.shift_color(color, source, true);
                    }

                    return;
                }
            }

            this.shift_color(color, source, false);
        }

    }

    update_gauges() {
        if (Date.now() - this.last_update > ColorState.GAUGE_UPDATE_MS) {
            this.model.update_gauge();
            this.last_update = Date.now()
        }
    }

    toggle_microphone() {
        this.sleep(1000).then(() => {
            this.show_microphone = true;
        });


        this.sleep(5000).then(() => {
          this.show_microphone = false;
        })
    }

    shift_color(color: string, source: string, positive=true) {
        if (source == RaceGameComponent.WEBSOCKET_SOURCE) {
            this.model.shift_color(color, positive);
            this.model.rotate(color, positive);
            this.slider.set_rotation(color, this.model.get_state(color).rotation);
            if (positive) {
                this.model.reset_history(color);
            }
        } else if (source == RaceGameComponent.KINESIS_SOURCE) {
            this.model.shift_kinesis_color(color, positive);
            this.model.rotate_kinesis(color, positive);
            if (positive) {
                this.model.reset_kinesis_history(color);
            }
            if (this.kinesis_enabled) {
                this.slider.set_rotation_kinesis(color, this.model.get_state(color).kinesis_rotation);
            }
        }
    }

    compare_hists(history, target_hist) {
        return RaceGameComponent.compare(history.slice(-target_hist.length), target_hist);
    }

    check_winner(color: string) {
        if (this.model.is_winner(color)) {
            this.winner = true;
            this.winner_color = color;
            this.winner_text = `${this.model.get_state(color).emotion} ${this.model.get_state(color).name} WINS!`
        }
    }

    update_avatar(image_url: string) {
        this.model.update_avatar(image_url, this.get_selected_color());
        this.update_slider_image()
    }

    update_user_image(image_url: string, emotion: string, confidence: number) {
        this.model.update_user_image(image_url, emotion, confidence, this.get_selected_color())
    }

    register_dash_click(payload) {
        console.log(payload);
        if (payload.event == this.TOGGLE_KINESIS) {
            this.kinesis_enabled = !this.kinesis_enabled;
            this.cdr.detectChanges();

            if (this.kinesis_enabled) {
                ColorState.COLORS.forEach(color => {
                    this.slider.change_image_kinesis(color, this.model.get_state(color).avatar);
                    this.slider.set_rotation_kinesis(color, this.model.get_state(color).kinesis_rotation);
                });
            }

        } else if (payload.event == this.TOGGLE_GAME) {
            if (payload.click_type == 'DOUBLE') {
                this.reset_game()
            } else {
                this.paused = !this.paused;
                if (!this.paused) {
                    this.toggle_selection()
                }
            }
        } else if (payload.event == this.TOGGLE_SELECTION) {
            this.toggle_selection()
        }
    }

    toggle_selection() {
        document.getElementById(`${this.selection_order[this.selection_index]}-card`).style.
            setProperty('--selection-color', 'white');

        this.selection_index = 0;
    }

    select_color(color: string) {
        document.getElementById(`${this.selection_order[this.selection_index]}-card`).style.
            setProperty('--selection-color', 'white');

        this.selection_index = this.selection_order.indexOf(color);

        document.getElementById(`${this.selection_order[this.selection_index]}-card`).style.
            setProperty('--selection-color', RaceGameComponent.SELECTION_COLOR);
    }

    get_selected_color() {
        return this.selection_order[this.selection_index];
    }

    update_slider_image() {
        ColorState.COLORS.forEach(color =>
            this.slider.change_image(color, this.model.get_state(color).avatar)
        );

        if (this.kinesis_enabled) {
            ColorState.COLORS.forEach(color =>
                this.slider.change_image_kinesis(color, this.model.get_state(color).avatar)
            );
        }
    }


    change_target_buttons(length: number) {
        this.TARGET_BUTTONS = [];
        for (let i = 0; i < length; i++) {
            this.TARGET_BUTTONS.push(this.BUTTONS[Math.floor(Math.random() * this.BUTTONS.length)])
        }
    }

    static compare(a, b) {
        if (a.length != b.length)
            return false;
        else {
            for (let i = 0; i < a.length; i++)
                if (a[i] != b[i])
                    return false;
            return true;
        }
    }

    reset_game() {
        ColorState.COLORS.forEach((color) => {
            this.model.get_state(color).reset();
        });

        this.paused = true;
        this.winner_text = "";
        this.winner_color = "";
        this.winner = false;
        this.cdr.detectChanges();
        this.toggle_selection();
    }

    sleep = (milliseconds) => {
        return new Promise(resolve => setTimeout(resolve, milliseconds))
    };

    ngOnDestroy() {
    }
}
