import { Component, OnInit } from '@angular/core';
import { FormGroup, Validators } from '@angular/forms';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth-service.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
})
export class RegisterComponent implements OnInit {
  form!: FormGroup;
  errorMessage: string | null = null;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.form = this.formBuilder.group(
      {
        username: ['', [Validators.required, Validators.minLength(3)]],
        password: ['', [Validators.required, Validators.minLength(6)]],
        password_confirm: ['', [Validators.required]],
        email: ['', [Validators.required, Validators.email]],
        name: ['', [Validators.required, Validators.minLength(2)]],
        age: [
          '',
          [Validators.required, Validators.min(1), Validators.max(150)],
        ],
        is_admin: [false, Validators.required],
      },
      {
        validator: this.passwordMatchValidator,
      }
    );
  }

  passwordMatchValidator(g: FormGroup) {
    return g.get('password')?.value === g.get('password_confirm')?.value
      ? null
      : { mismatch: true };
  }

  getErrorMessage(field: string): string {
    const control = this.form.get(field);
    if (control?.errors) {
      if (control.errors['required']) {
        return `${field.charAt(0).toUpperCase() + field.slice(1)} is required`;
      }
      if (control.errors['email']) {
        return 'Please enter a valid email address';
      }
      if (control.errors['minlength']) {
        return `${
          field.charAt(0).toUpperCase() + field.slice(1)
        } must be at least ${
          control.errors['minlength'].requiredLength
        } characters`;
      }
      if (control.errors['min']) {
        return `${
          field.charAt(0).toUpperCase() + field.slice(1)
        } must be at least ${control.errors['min'].min}`;
      }
      if (control.errors['max']) {
        return `${
          field.charAt(0).toUpperCase() + field.slice(1)
        } must be at most ${control.errors['max'].max}`;
      }
    }
    return '';
  }

  onSubmit(): void {
    if (this.form.invalid) {
      Object.keys(this.form.controls).forEach((key) => {
        const control = this.form.get(key);
        if (control?.invalid) {
          control.markAsTouched();
        }
      });
      return;
    }

    if (
      this.form.get('password')?.value !==
      this.form.get('password_confirm')?.value
    ) {
      this.errorMessage = 'Passwords do not match';
      return;
    }

    this.authService.registerUser(this.form.value).subscribe({
      next: (response) => {
        this.router.navigate(['/users']);
      },
      error: (error) => {
        this.errorMessage =
          error.error?.message || 'An error occurred during registration';
      },
    });
  }
}
