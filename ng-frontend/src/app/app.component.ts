import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';

import { LoginComponent } from './users/login/login.component';
import { RegisterComponent } from './users/register/register.component';

import { JobService } from './services/job.service';
import { Job } from './models/job';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  public jobs: Job[];

  constructor(
    public dialog: MatDialog,
    private jobService: JobService) {}

  ngOnInit() {
    this.jobService.get_all_jobs().subscribe(jobs => {
      this.jobs = jobs;
    });
  }

  openLoginDialog(): void {
    const dialogRef = this.dialog.open(LoginComponent, {
      width: '300px',
      data: {}
    });

    dialogRef.afterClosed().subscribe(result => {
      
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
}