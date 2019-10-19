import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { User } from '../models/user';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http: HttpClient) { }

  public register(
    username: string,
    email: string,
    password1: string,
    password2: string
  ): Observable<any> {
    return this.http.post('/api/auth/register/', {
      username: username,
      email: email,
      password1: password1,
      password2: password2
    });
  }

  public login(username: string, password: string): Observable<any> {
    return this.http.post('/api/auth/login/', {
      username: username,
      password: password
    });
  }

  public get_user(): Observable<User> {
    return this.http.get<User>('/api/auth/user/');
  }

  public logout(): Observable<any> {
    return this.http.post('/api/auth/logout/', {});
  }
}
