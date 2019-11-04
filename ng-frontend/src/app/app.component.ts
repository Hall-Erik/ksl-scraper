import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

import { LoginComponent } from './users/login/login.component';
import { RegisterComponent } from './users/register/register.component';

import { JobService } from './services/job.service';
import { UserService } from './services/user.service';

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
    private userService: UserService,
    private snackBar: MatSnackBar) {}

  openSnackBar(message: string) {
    this.snackBar.open(message, null, {
      duration: 3000
    });
  }

  ngOnInit() {    
    this.userService.user.subscribe(user => this.user = user);
    this.userService.get_user().subscribe(() => {
      this.jobService.get_jobs().subscribe(jobs => this.jobs = jobs);
    }, () => {
      this.jobService.get_all_jobs().subscribe(jobs => this.jobs = jobs);
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
    const dialogRef = this.dialog.open(LoginComponent, {
      width: '300px',
      data: {}
    });

    dialogRef.afterClosed().subscribe(() => {
      this.userService.get_user().subscribe(() => {
        this.jobService.get_jobs().subscribe(jobs => this.jobs = jobs);
        this.openSnackBar('Log in successful.');
      });
    });
  }

  openRegisterDialog(): void {
    const dialogRef = this.dialog.open(RegisterComponent, {
      width: '300px',
      data: {}
    });

    dialogRef.afterClosed().subscribe(result => {
      this.openSnackBar('Account created.');
    });
  }

  logout(): void {
    this.userService.logout().subscribe(
      () => {
        this.userService.user.next(null);
        this.jobService.get_all_jobs().subscribe(jobs => this.jobs = jobs);
        this.openSnackBar('Logged out.');
      });
  }
}