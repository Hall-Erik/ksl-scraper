import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Job } from '../models/job';

@Injectable({
  providedIn: 'root'
})
export class JobService {

  constructor(private http: HttpClient) { }

  public get_jobs(): Observable<Job[]> {
    return this.http.get<Job[]>('/api/jobs/');
  }

  public get_all_jobs(): Observable<Job[]> {
    return this.http.get<Job[]>('/api/jobs/all/');
  }
}
