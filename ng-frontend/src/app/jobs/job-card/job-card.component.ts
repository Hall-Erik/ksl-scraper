import { Component, Input, Output, EventEmitter } from '@angular/core';

import { JobService } from '../../services/job.service';
import { Job } from '../../models/job';

@Component({
  selector: 'app-job-card',
  templateUrl: './job-card.component.html',
  styleUrls: ['./job-card.component.css']
})
export class JobCardComponent {
  @Input() job: Job;
  @Output() hideJob: EventEmitter<number> = new EventEmitter();

  constructor(private jobService: JobService) { }

  onHide() { this.hideJob.emit(this.job.id); }

  onVisit() {
    this.jobService.mark_job_seen(this.job.id.toString())
    .subscribe(() => this.job.seen = true);
  }
}
