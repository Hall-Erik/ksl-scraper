import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, Validators } from '@angular/forms';

import { UserService } from '../../services/user.service';

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
    private userService: UserService) { }

    onClick(): void {
      if(this.loginForm.valid) {
        this.userService.login(
          this.username.value,
          this.password.value
        ).subscribe(() => {
          this.dialogRef.close();
        }, (err) => {
          console.log(err);
        });
      }
    }

    onNoClick(): void { this.dialogRef.close(); }
}
