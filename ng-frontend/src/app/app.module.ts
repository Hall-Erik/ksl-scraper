import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FlexLayoutModule } from '@angular/flex-layout';

import { MaterialModule } from './material/material.module';

import { ApiInterceptor } from './services/api.interceptor';

import { JobService } from './services/job.service';
import { AuthService } from './services/auth.service';

import { AppComponent } from './app.component';
import { LoginComponent } from './users/login/login.component';
import { RegisterComponent } from './users/register/register.component';
import { JobCardComponent } from './jobs/job-card/job-card.component';
import { AuthDialogComponent } from './users/auth-dialog/auth-dialog.component';
import { ResetRequestComponent } from './users/reset-request/reset-request.component';
import { HomeComponent } from './home/home.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    JobCardComponent,
    AuthDialogComponent,
    ResetRequestComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken'
    })
  ],
  providers: [
    JobService,
    AuthService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ApiInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent],
  entryComponents: [
    AuthDialogComponent,
    LoginComponent,
    RegisterComponent
  ]
})
export class AppModule { }
