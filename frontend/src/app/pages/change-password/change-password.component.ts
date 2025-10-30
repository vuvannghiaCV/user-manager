import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth-service.service';

@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.css'],
})
export class ChangePasswordComponent implements OnInit {
  form!: FormGroup;
  errorMessage: string | null = null;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      password: ['', [Validators.required, Validators.minLength(6)]],
      password_confirm: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  onSubmit(): void {
    if (this.form.valid) {
      if (this.form.value.password !== this.form.value.password_confirm) {
        this.errorMessage = 'Passwords do not match';
        return;
      }

      this.authService
        .changePassword(
          this.form.value.password,
          this.form.value.password_confirm
        )
        .subscribe({
          next: (response: any) => {
            if (response.success) {
              this.router.navigate(['/login']);
            } else {
              this.errorMessage = response.message || 'Password change failed';
            }
          },
          error: (error) => {
            this.errorMessage =
              error.error?.message ||
              'An error occurred while changing password';
          },
        });
    } else {
      if (this.form.get('password')?.errors?.['required']) {
        this.errorMessage = 'Password is required';
      } else if (this.form.get('password')?.errors?.['minlength']) {
        this.errorMessage = 'Password must be at least 6 characters';
      } else if (this.form.get('password_confirm')?.errors?.['required']) {
        this.errorMessage = 'Password confirmation is required';
      } else if (this.form.get('password_confirm')?.errors?.['minlength']) {
        this.errorMessage =
          'Password confirmation must be at least 6 characters';
      } else {
        this.errorMessage = 'Please check all required fields';
      }
    }
  }
}
