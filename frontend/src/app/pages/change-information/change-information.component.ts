import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { UsersService } from 'src/app/services/users-service.service';

@Component({
  selector: 'app-change-information',
  templateUrl: './change-information.component.html',
  styleUrls: ['./change-information.component.css'],
})
export class ChangeInformationComponent implements OnInit {
  form!: FormGroup;
  errorMessage: string | null = null;

  constructor(
    private formBuilder: FormBuilder,
    private usersService: UsersService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      age: ['', [Validators.required, Validators.min(1), Validators.max(150)]],
      email: ['', [Validators.required, Validators.email]],
    });
  }

  onSubmit(): void {
    if (this.form.valid) {
      const data_update: any = {};
      for (const key in this.form.value) {
        if (this.form.value[key] !== '') {
          data_update[key] = this.form.value[key];
        }
      }

      this.usersService.updateUser(data_update).subscribe({
        next: (response: any) => {
          if (response.success) {
            this.router.navigate(['/']);
          } else {
            this.errorMessage = response.message || 'Update failed';
          }
        },
        error: (error) => {
          this.errorMessage =
            error.error?.message ||
            'An error occurred while updating information';
        },
      });
    } else {
      if (this.form.get('name')?.errors?.['required']) {
        this.errorMessage = 'Name is required';
      } else if (this.form.get('name')?.errors?.['minlength']) {
        this.errorMessage = 'Name must be at least 2 characters';
      } else if (this.form.get('age')?.errors?.['required']) {
        this.errorMessage = 'Age is required';
      } else if (
        this.form.get('age')?.errors?.['min'] ||
        this.form.get('age')?.errors?.['max']
      ) {
        this.errorMessage = 'Age must be between 1 and 150';
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
