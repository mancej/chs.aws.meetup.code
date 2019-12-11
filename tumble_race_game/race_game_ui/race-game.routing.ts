import { ModuleWithProviders } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RaceGameComponent } from './race-game.component';

const routes: Routes = [
  { path: '', component: RaceGameComponent }
];

export const routing: ModuleWithProviders = RouterModule.forChild(routes);
