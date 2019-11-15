import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  public loginForm = this.fb.group({
    username: ['', Validators.required],
    password: ['', Validators.required]
  });

  get username() { return this.loginForm.get('username'); }
  get password() { return this.loginForm.get('password'); }

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    public dialogRef: MatDialogRef<LoginComponent>,
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
        this.dialogRef.close();
      }, () => this.loginForm.setErrors({noUser: true}));
    }
  }

  onNoClick(): void { this.dialogRef.close(); }
}
