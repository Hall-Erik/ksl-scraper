import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, Validators } from '@angular/forms';

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
    private fb: FormBuilder) { }

    onClick(): void {
      if(this.loginForm.valid) {
        console.log('logged in.');
        this.dialogRef.close();
      }
    }

    onNoClick(): void {
      console.log('cancelled.');
      this.dialogRef.close();
    }
}
