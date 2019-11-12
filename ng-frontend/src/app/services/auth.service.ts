import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { map } from 'rxjs/operators';

import { User } from '../models/user';

@Injectable({providedIn: 'root'})
export class AuthService {
  private currentUserSubj: BehaviorSubject<User>;
  public currentUser: Observable<User>;

  constructor(private http: HttpClient) {
    this.currentUserSubj = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('currentUser')));
    this.currentUser = this.currentUserSubj.asObservable();
  }

  public get currentUserValue(): User {
    return this.currentUserSubj.value;
  }

  public get_user(): Observable<User> {
    return this.http.get<User>('/api/auth/user/').pipe(
      map((user: User) => {
        localStorage.setItem('currentUser', JSON.stringify(user));
        this.currentUserSubj.next(user);
        return user;
      }, () => {
        localStorage.removeItem('currentUser');
        this.currentUserSubj.next(null);
        return null;
      })
    );
  }

  public register(
    username: string,
    email: string,
    password1: string,
    password2: string
  ): Observable<User> {
    return this.http.post<User>('/api/auth/register/', {
      username: username,
      email: email,
      password1: password1,
      password2: password2
    }).pipe(map(user => {
      this.get_user().subscribe();
      return user;
    }));;
  }

  public login(username: string, password: string): Observable<User> {
    return this.http.post<User>('/api/auth/login/', {
      username: username,
      password: password
    }).pipe(map(user => {
      this.get_user().subscribe();
      return user;
    }));
  }

  public logout(): Observable<any> {
    localStorage.removeItem('currentUser');
    this.currentUserSubj.next(null);
    return this.http.post('/api/auth/logout/', {});
  }

  public request_reset(email: string): Observable<any> {
    return this.http.post('/api/auth/password/reset/', {email: email});
  }

  public reset_password(token: string, password: string): Observable<any> {
    return this.http.post('/api/auth/password/reset/confirm/', {
      token: token,
      password: password
    });
  }
}
