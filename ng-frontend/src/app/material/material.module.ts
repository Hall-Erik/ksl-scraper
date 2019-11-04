import { NgModule } from '@angular/core';

import { MatSliderModule } from '@angular/material/slider';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar'; 
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card'; 
import { MatGridListModule } from '@angular/material/grid-list';
import { MatProgressSpinnerModule } from '@angular/material';
import { MatBadgeModule } from '@angular/material/badge';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBarModule } from '@angular/material/snack-bar'; 

const material = [
  MatSliderModule,
  MatButtonModule,
  MatToolbarModule,
  MatDialogModule,
  MatFormFieldModule,
  MatInputModule,
  MatCardModule,
  MatGridListModule,
  MatProgressSpinnerModule,
  MatBadgeModule,
  MatIconModule,
  MatSnackBarModule
];

@NgModule({
  imports: [material],
  exports: [material]
})
export class MaterialModule { }
