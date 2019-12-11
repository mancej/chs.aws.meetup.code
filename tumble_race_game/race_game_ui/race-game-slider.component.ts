import {Component, Input} from '@angular/core';
import { Options } from 'ng5-slider';
import {ColorState} from "./race-game.model";

@Component({
  selector: 'race-game-slider',
  templateUrl: './race-game-slider.component.html',
  styleUrls: ['./race-game-slider.component.scss']
})

export class RaceGameSliderComponent {
  @Input() value: number = 0;
  @Input() options: Options = {
    floor: 0,
    ceil: 100,
    step: 10,
    showTicks: true,
    showSelectionBar: true,
    getSelectionBarColor: (value: number): string => {
      if (value <= 3) {
          return 'red';
      }
      if (value <= 6) {
          return 'orange';
      }
      if (value <= 9) {
          return 'yellow';
      }
      return '#2AE02A';
    }
  };

  constructor() {}

  change_image(color: string, image_url: string) {
    document.getElementById(`${color}-slider`).style.setProperty('--cropped-image-url', `url(${image_url})`);
  }

  set_rotation(color: string, amount: number) {
    document.getElementById(`${color}-slider`).style.setProperty('--rotate-percent', `${amount}deg`);
  }

  change_image_kinesis(color: string, image_url: string) {
        document.getElementById(`kinesis-${color}-slider`).style.setProperty('--cropped-image-url', `url(${image_url})`);
  }

  set_rotation_kinesis(color: string, amount: number) {
    document.getElementById(`kinesis-${color}-slider`).style.setProperty('--rotate-percent', `${amount}deg`);
  }

  set_all(image_url: string, set_kinesis=false) {
    ColorState.COLORS.forEach((color) => {
          this.change_image(color, image_url);
    });

    if (set_kinesis) {
      ColorState.COLORS.forEach((color) => {
            this.change_image_kinesis(color, image_url);
      });
    }
  }

  rotate_all(amount: number, set_kinesis=false) {
    ColorState.COLORS.forEach((color) => {
          this.set_rotation(color, amount);
    });

    if (set_kinesis) {
      ColorState.COLORS.forEach((color) => {
          this.set_rotation_kinesis(color, amount);
      });
    }
  }
}

