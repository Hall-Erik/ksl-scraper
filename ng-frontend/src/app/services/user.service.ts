import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { map } from 'rxjs/operators';

import { User } from '../models/user';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  public user: BehaviorSubject<User> = new BehaviorSubject<User>(null);

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
    return this.http.get<User>('/api/auth/user/').pipe(
      map((user: User) => {
        this.user.next(user);
        return user;
      }, () => {
        this.user.next(null);
        return null;
      })
    );
  }

  public logout(): Observable<any> {
    return this.http.post('/api/auth/logout/', {});
  }
}
