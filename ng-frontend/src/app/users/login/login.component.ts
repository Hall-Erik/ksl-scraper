import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, Validators } from '@angular/forms';

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
    public dialogRef: MatDialogRef<LoginComponent>,
    private fb: FormBuilder,
    private authService: AuthService) { }

    onClick(): void {
      if(this.loginForm.valid) {
        this.authService.login(
          this.username.value,
          this.password.value
        ).subscribe(() => {
          this.dialogRef.close();
        }, () => this.loginForm.setErrors({noUser: true}));
      }
    }

    onNoClick(): void { this.dialogRef.close(); }
}
