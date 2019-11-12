import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-auth-dialog',
  templateUrl: './auth-dialog.component.html',
  styleUrls: ['./auth-dialog.component.css']
})
export class AuthDialogComponent {
  forgot: boolean = false;
  sent: boolean = false;

  constructor(
    public dialogRef: MatDialogRef<AuthDialogComponent>
  ) { }

  forgot_pwd() { this.forgot = true; }
  remembered_pwd() { this.forgot = false; }

  email_sent() { this.sent = true; }

  close() { this.dialogRef.close(); }
}
