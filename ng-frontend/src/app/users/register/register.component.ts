import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, Validators } from '@angular/forms';

export interface RegisterData {
  username: string;
  email: string;
  password1: string;
  password2: string;
}

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  public registerForm = this.fb.group({
    username: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    password1: ['', Validators.required],
    password2: ['', Validators.required]
  });

  get username() { return this.registerForm.get('username'); }
  get email() { return this.registerForm.get('email'); }
  get password1() { return this.registerForm.get('password1'); }
  get password2() { return this.registerForm.get('password2'); }

  constructor(
    public dialogRef: MatDialogRef<RegisterComponent>,
    private fb: FormBuilder) { }

    onClick(): void {
      if(this.registerForm.valid) {
        console.log('registerd.');
      }
      this.dialogRef.close();
    }

    onNoClick(): void {
      console.log('cancelled.');
      this.dialogRef.close();
    }
}
