import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

import { LoginComponent } from './users/login/login.component';
import { RegisterComponent } from './users/register/register.component';

import { AuthService } from './services/auth.service';

import { User } from './models/user';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  public user: User;

  constructor(
    public dialog: MatDialog,
    private authService: AuthService,
    private snackBar: MatSnackBar) {}

  openSnackBar(message: string) {
    this.snackBar.open(message, null, {duration: 3000});
  }

  ngOnInit() {
    this.user = this.authService.currentUserValue;
    this.authService.currentUser.subscribe((user) => {
      this.user = user;
    });
  }

  openLoginDialog(): void {
    this.dialog.open(LoginComponent, {width: '310px'});
  }

  openRegisterDialog(): void {
    this.dialog.open(RegisterComponent, {width: '310px'});
  }

  logout(): void {
    this.authService.logout().subscribe(
      () => this.openSnackBar('Logged out.')
    );
  }
}