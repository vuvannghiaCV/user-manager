import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthService } from 'src/app/services/auth-service.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css'],
})
export class ForgotPasswordComponent implements OnInit {
  form!: FormGroup;
  errorMessage: string | null = null;

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    this.form = new FormGroup({
      username: new FormControl('', [
        Validators.required,
        Validators.minLength(2),
      ]),
      email: new FormControl('', [Validators.required, Validators.email]),
    });
  }

  onSubmit() {
    if (this.form.valid) {
      this.authService
        .forgotPassword(this.form.value.username, this.form.value.email)
        .subscribe({
          next: (response: any) => {
            if (response.success) {
              this.router.navigate(['/login']);
            } else {
              this.errorMessage =
                response.message || 'Password reset request failed';
            }
          },
          error: (error) => {
            this.errorMessage =
              error.error?.message ||
              'An error occurred while requesting password reset';
          },
        });
    } else {
      if (this.form.get('username')?.errors?.['required']) {
        this.errorMessage = 'Username is required';
      } else if (this.form.get('username')?.errors?.['minlength']) {
        this.errorMessage = 'Username must be at least 2 characters';
      } else if (this.form.get('email')?.errors?.['required']) {
        this.errorMessage = 'Email is required';
      } else if (this.form.get('email')?.errors?.['email']) {
        this.errorMessage = 'Please enter a valid email address';
      } else {
        this.errorMessage = 'Please check all required fields';
      }
    }
  }
}
