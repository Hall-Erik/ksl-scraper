import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, Validators } from '@angular/forms';

export interface LoginData {
  username: string;
  password: string;
}

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

  constructor(
    public dialogRef: MatDialogRef<LoginComponent>,
    private fb: FormBuilder) { }

    onClick(): void {
      this.dialogRef.close();
      if(this.loginForm.valid) {
        console.log('logged in.');
      }
    }

    onNoClick(): void {
      console.log('cancelled.');
      this.dialogRef.close();
    }
}
