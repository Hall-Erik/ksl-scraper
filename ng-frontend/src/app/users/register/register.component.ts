import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';

import { AuthService } from '../../services/auth.service';

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

  public usernameErrors: string[];
  public emailErrors: string[];
  public password1Errors: string[];
  public password2Errors: string[];

  constructor(
    public dialogRef: MatDialogRef<RegisterComponent>,
    private fb: FormBuilder,
    private authService: AuthService,
    private snackBar: MatSnackBar) { }

  openSnackBar(message: string) {
    this.snackBar.open(message, null, {duration: 3000});
  }

  onClick(): void {
    if(this.registerForm.valid) {
      this.authService.register(
        this.username.value,
        this.email.value,
        this.password1.value,
        this.password2.value
      ).subscribe(() => {
        this.openSnackBar('Account created.');
        this.dialogRef.close();
      }, (err) => {
        if ('username' in err.error) {
          this.username.setErrors({apiError: true});
          this.usernameErrors = err.error.username;
        }
        if ('email' in err.error) {
          this.email.setErrors({apiError: true});
          this.emailErrors = err.error.email;
        }
        if ('password1' in err.error) {
          this.password1.setErrors({apiError: true});
          this.password1Errors = err.error.password1;
        }
        if ('password2' in err.error) {
          this.password2.setErrors({apiError: true});
          this.password2Errors = err.error.password2;
        }
        if ('non_field_errors' in err.error) {
          if (err.error.non_field_errors[0] === "The two password fields didn't match.") {
            this.password1.setErrors({matchError: true});
            this.password2.setErrors({matchError: true});
            this.registerForm.setErrors({matchError: true});
          }
        }
      });
    }
  }

  onNoClick(): void { this.dialogRef.close(); }
}
