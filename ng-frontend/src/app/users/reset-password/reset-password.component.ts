import { Component, OnInit } from '@angular/core';
import { FormBuilder, AbstractControl, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.css']
})
export class ResetPasswordComponent implements OnInit {
  public loading: boolean = true;
  public valid: boolean = false;
  public notFound: boolean = false;
  public expired: boolean = false;

  public passwordErrors: string[];

  public resetForm = this.fb.group({
    token: '',
    password1: ['', Validators.required],
    password2: ['', Validators.required]
  }, {validator: this.passwords_match});
  
  get token() { return this.resetForm.get('token'); }
  get password1() { return this.resetForm.get('password1'); }
  get password2() { return this.resetForm.get('password2'); }

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private authService: AuthService,
    private snackBar: MatSnackBar
  ) { }

  openSnackBar(message: string) {
    this.snackBar.open(message, null, {duration: 3000});
  }

  ngOnInit() {
    let token = this.route.snapshot.paramMap.get('token');
    this.token.setValue(token);
    this.authService.validate_token(token)
    .subscribe(() => {
      this.loading = false;
      this.valid = true;
    }, (err) => {
      this.loading = false;
      if (err.error.status === "notfound") { this.notFound = true; }
      if (err.error.status === "expired") { this.expired = true; }
    });
  }

  passwords_match(c: AbstractControl) {
    if (c.get('password1').value !== c.get('password2').value) {
      return {invalid: true};
    }
  }
  
  reset_password() {
    this.authService.reset_password(
      this.token.value, this.password1.value)
      .subscribe(() => {
        this.router.navigate(['login']);
        this.openSnackBar('Password updated. You can now log in.');
      }, (err) => {
        if ('password' in err.error) {
          this.password1.setErrors({apiError: true});
          this.passwordErrors = err.error.password;
        }
      });
  }
}
