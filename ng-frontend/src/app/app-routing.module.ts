import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from './home/home.component';
import { ResetPasswordComponent } from './users/reset-password/reset-password.component';
import { ResetRequestComponent } from './users/reset-request/reset-request.component';

const routes: Routes = [
  {path: 'jobs', component: HomeComponent},
  {path: 'reset', component: ResetRequestComponent},
  {path: 'reset/:token', component: ResetPasswordComponent},
  {path: '', pathMatch: 'full', redirectTo: '/jobs'},
  {path: '**', pathMatch: 'full', redirectTo: '/jobs'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
