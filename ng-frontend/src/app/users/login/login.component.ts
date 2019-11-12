import { Component, Output, EventEmitter } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  @Output() close: EventEmitter<any> = new EventEmitter();

  public loginForm = this.fb.group({
    username: ['', Validators.required],
    password: ['', Validators.required]
  });

  get username() { return this.loginForm.get('username'); }
  get password() { return this.loginForm.get('password'); }

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private snackBar: MatSnackBar
  ) { }

  openSnackBar(message: string) {
    this.snackBar.open(message, null, {duration: 3000});
  }

  onClick(): void {
    if(this.loginForm.valid) {
      this.authService.login(
        this.username.value,
        this.password.value
      ).subscribe(() => {
        this.openSnackBar('Log in successful.');
        this.close.emit(null);
      }, () => this.loginForm.setErrors({noUser: true}));
    }
  }

  onNoClick(): void { this.close.emit(null); }
}
