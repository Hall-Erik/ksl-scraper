import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from "@angular/router";
import { MatSnackBar } from '@angular/material/snack-bar';

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-reset-request',
  templateUrl: './reset-request.component.html',
  styleUrls: ['./reset-request.component.css']
})
export class ResetRequestComponent {
  public resetForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]]
  });

  get email() { return this.resetForm.get('email'); }

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private snackBar: MatSnackBar,
    private router: Router
  ) { }

  openSnackBar(message: string) {
    this.snackBar.open(message, null, {duration: 3000});
  }

  onClick(): void {
    if(this.resetForm.valid) {
      this.authService.request_reset(this.email.value)
      .subscribe(() => {
        this.openSnackBar('Request sent. Check your email for instructions.');
        this.router.navigate(['/']);
      });
    }
  }
}
