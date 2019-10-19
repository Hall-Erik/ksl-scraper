import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, Validators } from '@angular/forms';

import { UserService } from '../../services/user.service';

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
    private fb: FormBuilder,
    private userService: UserService) { }

    onClick(): void {
      if(this.registerForm.valid) {
        this.userService.register(
          this.username.value,
          this.email.value,
          this.password1.value,
          this.password2.value).subscribe(() => {
            this.dialogRef.close();
          });
      }
    }

    onNoClick(): void { this.dialogRef.close(); }
}
