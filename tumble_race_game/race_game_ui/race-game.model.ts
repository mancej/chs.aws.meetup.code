import {Options} from "ng5-slider";
import {RaceGameComponent} from "./race-game.component";
import {throwError} from "rxjs";

export class ColorState {
    static DEFAULT_IMG = "https://SOME_BUCKET.s3.amazonaws.com/photo-uploads/MysteryPerson.png";
    static DEFAULT_ACTION_IMG = "https://SOME_BUCKET.s3.amazonaws.com/photo-uploads/EmptyImage.png";
    static RESET_UNAVAILABLE = "assets/images/NoReset.png";
    static RESET_AVAILABLE = "assets/images/ResetAvailable.png";
    static UP = "UP";
    static DOWN = "DOWN";
    static LEFT = "LEFT";
    static RIGHT = "RIGHT";
    static A = "A";
    static B = "B";
    static SELECT = "SELECT";
    static START = "START";
    static RED = "red";
    static BLUE = "blue";
    static GREEN = "green";
    static YELLOW = "yellow";
    static COLORS = [ColorState.RED, ColorState.BLUE, ColorState.GREEN, ColorState.YELLOW];
    static BASE_REQUEST_COUNT = [0,0,0,0,0];
    static BOOST_AMOUNT = 5;
    static POWER_UP_BAR_COLORS = ["#cfa6ff","#b87aff","#a557ff","#9233ff", "#8214ff"];
    static EMOTION_MAP = {
        'Happy': 'Joyous',
        'Sad': 'Sad',
        'Angry': 'Furious',
        'Confused': 'Confused',
        'Disgusted': 'Disgusted',
        'Surprised': 'Surprised',
        'Unknown': 'Vulcan',
        'Fear': 'Terrified'
    };

    IMAGE_MAP = new Map();
    static GAUGE_UPDATE_MS = 200;

    constructor(private color: string, private MAX_CLICKS: number, private MAX_POWER_UP_CLICKS: number) {
        this.IMAGE_MAP.set(ColorState.UP, "assets/images/Up.png");
        this.IMAGE_MAP.set(ColorState.DOWN, "assets/images/Down.png");
        this.IMAGE_MAP.set(ColorState.LEFT, "assets/images/Left.png");
        this.IMAGE_MAP.set(ColorState.RIGHT, "assets/images/Right.png");
        this.IMAGE_MAP.set(ColorState.A, "assets/images/A.png");
        this.IMAGE_MAP.set(ColorState.B, "assets/images/B.png");
        this.IMAGE_MAP.set(ColorState.SELECT, "assets/images/EmptyImage.png");
        this.IMAGE_MAP.set(ColorState.START, "assets/images/EmptyImage.png");
        if (color == ColorState.RED) {
            this.bar_color = RaceGameComponent.RED;
        } else if (color == ColorState.BLUE) {
            this.bar_color = RaceGameComponent.BLUE;
        } else if (color == ColorState.GREEN) {
            this.bar_color = RaceGameComponent.GREEN;
        } else if (color == ColorState.YELLOW) {
            this.bar_color = RaceGameComponent.YELLOW;
        }
    };

    options: Options = {
        floor: 0,
        ceil: this.MAX_CLICKS,
        showSelectionBar: true,
        getSelectionBarColor: (value: number): string => {
            return this.bar_color;
        }
    };

    kinesis_bar_options: Options = {
        floor: 0,
        ceil: this.MAX_POWER_UP_CLICKS,
        showSelectionBar: true,
        getSelectionBarColor: (value: number): string => {
            value = (value < 1) ? 1 : value;
            return ColorState.POWER_UP_BAR_COLORS[Math.floor(
                value / this.MAX_POWER_UP_CLICKS * ColorState.POWER_UP_BAR_COLORS.length)];
        }
    };

    bar_color: string;
    val: number = 0;
    rotation: number = 90;
    hist = [];
    img = ColorState.DEFAULT_IMG;
    avatar: string = ColorState.DEFAULT_IMG;
    action_img = ColorState.DEFAULT_ACTION_IMG;
    reset_available = true;
    reset_img = ColorState.RESET_AVAILABLE;

    emotions = ["Manic", "Inquisitive", "Confused", "Contemplative", "Interested", "Furious", "Bored", "Curious"];
    names = ["Steve", "Jessica", "Jamie", "Elise", "Carl", "Miriah", "Brad", "Trevor", "Jamal", "Clayton",
        "Katie", "Andrew", "Fran", "Amy", "Nia", "Cadence", "Hanna", "Ayah", "Dalia", "Jamir", "Amari", "Jabari"];
    emotion = this.emotions[Math.floor(Math.random() * this.emotions.length)];
    emotion_confidence = 0;
    name = this.names[Math.floor(Math.random() * this.names.length)];

    kinesis_val = 0;
    kinesis_hist = [];
    kinesis_rotation = 90;

    request_count = ColorState.BASE_REQUEST_COUNT.slice(0);
    gauge_name = "Finger Speed";
    gauge_bottom = "req/s";
    gauge_val = 0;
    gauge_options= {
        hasNeedle: true,
        outerNeedle: true,
        needleUpdateSpeed: 0,
        arcColors: ['rgb(61,204,91)', RaceGameComponent.YELLOW, RaceGameComponent.RED],
        arcDelimiters: [33,66],
        rangeLabel: ['0', '100']
    };

    add_val(num: number) {
        if ((this.val > 0 && this.val < this.MAX_CLICKS) || this.val == 0 && num > 0) {
            this.val = this.val + num;
        }
    }

    gauge_val_str(){
        return `${this.gauge_val}`;
    }

    add_kinesis_val(num: number) {
        this.kinesis_val = this.kinesis_val + num;

        if (this.kinesis_val > this.MAX_POWER_UP_CLICKS) {
            this.val = this.val + ColorState.BOOST_AMOUNT;
            this.kinesis_val = 0;
        }
    }

    set_kinesis_val(val: number) {
        this.kinesis_val = val;
    }

    update_gauge() {
        const total = this.request_count.reduce( (a, b) => a + b, 0);
        const length = this.request_count.length;

        this.gauge_val = total * (1000 / ColorState.GAUGE_UPDATE_MS) / length;
        this.request_count.shift();
        this.request_count.push(0);
    }

    rotate(num: number) {
        this.rotation = this.rotation + num;
    }

    rotate_kinesis(num: number) {
        this.kinesis_rotation = this.kinesis_rotation + num;
    }

    increment_req_count() {
        this.request_count[this.request_count.length - 1 ] = this.request_count[this.request_count.length -1] + 1;
    }

    set_name(name: string) {
        this.name = name
    }

    set_emotion(emotion: string, confidence: number) {
        console.log(`Setting emotion: ${emotion}`);
        if (emotion in ColorState.EMOTION_MAP) {
            this.emotion = ColorState.EMOTION_MAP[emotion];
        } else {
            this.emotion = emotion;
        }
        this.emotion_confidence = Math.round(confidence * 10) / 10;
    }

    consume_target_code_reset() {
        this.reset_available = false;
        this.reset_img = ColorState.RESET_UNAVAILABLE
    }

    is_target_code_reset_available() {
        return this.reset_available;
    }

    push_click(button: string) {
        let hist_item = this.hist;
        this.set_action_image(button);
        this.push_history(hist_item, button);
        return hist_item;
    }

    push_kinesis_click(button: string) {
        let hist_item = this.kinesis_hist;
        this.push_history(hist_item, button);
        return hist_item;
    }

    set_val(val: number) {
        this.val = val
    }

    set_avatar(img: string) {
        this.avatar = img
    }

    set_user_image(img: string) {
        this.img = img;
    }

    set_action_image(button: string) {
        this.action_img = this.IMAGE_MAP.get(button)
    }

    set_hist(history: []) {
        this.hist = history
    }

    push_history(hist_list, button) {
        if (hist_list.length < 4) {
            hist_list.push(button);
        } else {
            hist_list.push(button);
            hist_list.shift();
        }
    }

    reset_history() {
        this.hist = []
    }

    reset_kinesis_history() {
        this.kinesis_hist = []
    }

    reset() {
        this.reset_history();
        this.reset_kinesis_history();
        this.val = 0;
        this.kinesis_val = 0;
        this.request_count = ColorState.BASE_REQUEST_COUNT;
        this.reset_available = true;
        this.reset_img = ColorState.RESET_AVAILABLE;
    }
}

export class RaceGameModel {

    COLOR_STATE_MAP = new Map<string, ColorState>();
    PHOTO_UPLOAD_CODE = [ColorState.SELECT, ColorState.START, ColorState.SELECT, ColorState.START];
    ROTATION_INCREMENT = 25;


    constructor(private MAX_CLICKS: number, private MAX_POWER_UP_CLICKS: number) {
        this.COLOR_STATE_MAP.set(ColorState.RED, new ColorState(ColorState.RED, this.MAX_CLICKS, this.MAX_POWER_UP_CLICKS));
        this.COLOR_STATE_MAP.set(ColorState.BLUE, new ColorState(ColorState.BLUE, this.MAX_CLICKS, this.MAX_POWER_UP_CLICKS));
        this.COLOR_STATE_MAP.set(ColorState.GREEN, new ColorState(ColorState.GREEN, this.MAX_CLICKS, this.MAX_POWER_UP_CLICKS));
        this.COLOR_STATE_MAP.set(ColorState.YELLOW, new ColorState(ColorState.YELLOW, this.MAX_CLICKS, this.MAX_POWER_UP_CLICKS));
    };


    get_state(color: string) {
        return this.COLOR_STATE_MAP.get(color)
    }

    update_click_img(button: string, color: string) {
        this.get_state(color).set_action_image(button);
    }

    reset_history(color: string) {
        this.get_state(color).reset_history()
    }

    shift_color(color: string, positive = true) {
        const increment: number = positive ? 1 : -1;
        this.get_state(color).add_val(increment);
    }

    shift_kinesis_color(color: string, positive = true) {
        if (positive) {
            this.get_state(color).add_kinesis_val(1);
        } else {
            this.get_state(color).set_kinesis_val(0);
        }
    }

    reset_kinesis_history(color: string) {
        this.get_state(color).reset_kinesis_history()
    }

    push_click(button: string, color: string, source: string) {
        if (source == RaceGameComponent.WEBSOCKET_SOURCE) {
            return this.get_state(color).push_click(button);
        } else if (source == RaceGameComponent.KINESIS_SOURCE) {
            return this.get_state(color).push_kinesis_click(button)
        } else {
            throw(`Click button: ${button} color: ${color} source: ${source} is not of a valid source type.`)
        }
    }

    set_name(name: string, upload_color: string) {
        if (ColorState.COLORS.includes(upload_color)) {
            this.get_state(upload_color).set_name(name);
        }
    }

    set_emotion(color: string, emotion: string, confidence: number) {
        this.get_state(color).set_emotion(emotion, confidence)
    }

    update_user_image(image_url: string, emotion: string, confidence: number, upload_color: string) {
        console.log(`Updating image url: to ${image_url}`);
        if (ColorState.COLORS.includes(upload_color)) {
            this.get_state(upload_color).set_user_image(image_url);
            this.get_state(upload_color).set_emotion(emotion, confidence);
        }
    }

    update_avatar(image_url: string, upload_color: string) {
        console.log(`Updating avatar url: to ${image_url} for color ${upload_color}`);
        if (ColorState.COLORS.includes(upload_color)) {
            this.get_state(upload_color).set_avatar(image_url);
        }
    }

    update_gauge() {
        ColorState.COLORS.forEach((color) => {
            this.get_state(color).update_gauge();
        })
    }

    increment_request_count(color: string) {
        this.get_state(color).increment_req_count();
    }

    is_winner(color: string) {
        return this.get_state(color).val >= this.MAX_CLICKS
    }


    rotate(color, positive = true) {
        this.get_state(color).rotate(this.ROTATION_INCREMENT * (positive ? 1 : -1))
    }

    rotate_kinesis(color, positive = true) {
        this.get_state(color).rotate_kinesis(this.ROTATION_INCREMENT * (positive ? 1 : -1))
    }

    consume_target_code_reset(color: string) {
        this.get_state(color).consume_target_code_reset()
    }

    is_target_code_reset_available(color: string) {
        return this.get_state(color).is_target_code_reset_available();
    }

    reset_all_hist() {
        this.get_state(ColorState.BLUE).reset_history();
        this.get_state(ColorState.GREEN).reset_history();
        this.get_state(ColorState.RED).reset_history();
        this.get_state(ColorState.YELLOW).reset_history();
    }

    static compare(a, b) {
        if (a.length != b.length)
            return false;
        else {
            for (var i = 0; i < a.length; i++)
                if (a[i] != b[i])
                    return false;
            return true;
        }
    }
}


