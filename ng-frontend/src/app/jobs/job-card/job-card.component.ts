import { Component, Input, Output, EventEmitter } from '@angular/core';

import { Job } from '../../models/job';

@Component({
  selector: 'app-job-card',
  templateUrl: './job-card.component.html',
  styleUrls: ['./job-card.component.css']
})
export class JobCardComponent {
  @Input() job: Job;
  @Output() hideJob: EventEmitter<number> = new EventEmitter();

  constructor() { }

  onHide() { this.hideJob.emit(this.job.id); }
}
