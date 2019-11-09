import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';

import { AuthService } from '../../services/auth.service';
import { JobService } from '../../services/job.service';
import { User } from '../../models/user';
import { Job } from '../../models/job';

@Component({
  selector: 'app-job-card',
  templateUrl: './job-card.component.html',
  styleUrls: ['./job-card.component.css']
})
export class JobCardComponent implements OnInit {
  @Input() job: Job;
  @Output() hideJob: EventEmitter<number> = new EventEmitter();
  user: User;

  constructor(private jobService: JobService,
              private authService: AuthService) { }

  ngOnInit() {
    this.user = this.authService.currentUserValue;
    this.authService.currentUser.subscribe(user => this.user = user);
  }

  onHide() { this.hideJob.emit(this.job.id); }

  onVisit() {
    this.jobService.mark_job_seen(this.job.id.toString())
    .subscribe(() => this.job.seen = true);
  }
}
