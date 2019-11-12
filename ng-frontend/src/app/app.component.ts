import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

import { AuthDialogComponent } from './users/auth-dialog/auth-dialog.component';
import { LoginComponent } from './users/login/login.component';
import { RegisterComponent } from './users/register/register.component';

import { JobService } from './services/job.service';
import { AuthService } from './services/auth.service';

import { Job } from './models/job';
import { User } from './models/user';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  public jobs: Job[];
  public user: User;

  constructor(
    public dialog: MatDialog,
    private jobService: JobService,
    private authService: AuthService,
    private snackBar: MatSnackBar) {}

  openSnackBar(message: string) {
    this.snackBar.open(message, null, {duration: 3000});
  }

  ngOnInit() {
    this.user = this.authService.currentUserValue;
    this.authService.currentUser.subscribe((user) => {
      this.user = user;
      if (user != null) {
        this.jobService.get_jobs().subscribe(jobs => this.jobs = jobs);
      } else {
        this.jobService.get_all_jobs().subscribe(jobs => this.jobs = jobs);
      }
    });
  }

  hideJob(job_id: number) {
    this.jobService.hide_job(job_id.toString())
    .subscribe(() => {
      this.jobs = this.jobs.filter(j => j.id != job_id);
      this.openSnackBar('Job hidden.');
    });
  }

  openLoginDialog(): void {
    // this.dialog.open(LoginComponent, {width: '310px'});
    this.dialog.open(AuthDialogComponent, {width: '310px'});
  }

  openRegisterDialog(): void {
    var registerDialog = this.dialog.open(RegisterComponent, {width: '310px'});

    registerDialog.afterClosed().subscribe((val) => {
      if (val) { this.openLoginDialog(); }
    });
  }

  logout(): void {
    this.authService.logout().subscribe(
      () => this.openSnackBar('Logged out.')
    );
  }
}