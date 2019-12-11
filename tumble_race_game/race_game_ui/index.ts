import {ChangeDetectorRef,  NgModule} from '@angular/core';
import { CommonModule } from '@angular/common';
import {RaceGameComponent} from './race-game.component';
import { routing } from './race-game.routing';
import { MaterialModule } from '../material/material.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HighchartsChartModule } from 'highcharts-angular';
import { WebsocketService } from './websocket.service';
import { EventStreamService } from './app-event-stream.service';
import {Ng5SliderModule} from "ng5-slider";
// import { NgxGaugeModule } from 'ngx-gauge';
import { RaceGameModel} from './race-game.model';
import { RaceGameSliderComponent } from './race-game-slider.component'
import { GaugeChartModule } from 'angular-gauge-chart'

@NgModule({
  declarations: [
    RaceGameComponent,
    RaceGameSliderComponent
  ],
  imports: [
    CommonModule,
    MaterialModule,
    FormsModule,
    ReactiveFormsModule,
    HighchartsChartModule,
    routing,
    Ng5SliderModule,
    GaugeChartModule
    // NgxGaugeModule
  ],
  providers: [
    WebsocketService,
    EventStreamService,
    RaceGameSliderComponent
  ]
})
export class RaceGameModule { }
