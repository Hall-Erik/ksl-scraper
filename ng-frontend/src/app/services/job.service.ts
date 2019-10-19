import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Job } from '../models/job';
import { Search } from '../models/search';

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

  public hide_job(job_id: string): Observable<any> {
    return this.http.post(`/api/jobs/${job_id}/hide/`, {});
  }

  public mark_all_seen(): Observable<any> {
    return this.http.post('/api/jobs/mark_seen/', {});
  }

  public get_searches(): Observable<Search[]> {
    return this.http.get<Search[]>('/api/search/');
  }

  public add_search(pattern: string): Observable<any> {
    return this.http.post('/api/search/', {pattern: pattern});
  }
}
