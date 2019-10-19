import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';

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
    private userService: UserService) {}

  ngOnInit() {
    
    this.userService.user.subscribe(user => this.user = user);
    this.userService.get_user().subscribe(() => {
      this.jobService.get_jobs().subscribe(jobs => this.jobs = jobs);
    }, () => {
      this.jobService.get_all_jobs().subscribe(jobs => this.jobs = jobs);
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
      });
    });
  }

  openRegisterDialog(): void {
    const dialogRef = this.dialog.open(RegisterComponent, {
      width: '300px',
      data: {}
    });

    dialogRef.afterClosed().subscribe(result => {
      
    });
  }

  logout(): void {
    this.userService.logout().subscribe(
      () => {
        this.userService.user.next(null);
        this.jobService.get_all_jobs().subscribe(jobs => this.jobs = jobs);
      });
  }
}