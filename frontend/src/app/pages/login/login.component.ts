import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth-service.service';
import { removeAccessToken, setAccessToken } from 'src/app/utils/local_storage';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  form!: FormGroup;
  errorMessage: string | null = null;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    removeAccessToken();

    this.form = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  onSubmit(): void {
    if (this.form.valid) {
      this.authService
        .login(this.form.value.username, this.form.value.password)
        .subscribe({
          next: (response: any) => {
            if (response.success) {
              setAccessToken(response.access_token);
              if (response.otp_qr_code_base64) {
                this.router.navigate(['/otp'], {
                  queryParams: {
                    otp_qr_code_base64: response.otp_qr_code_base64,
                  },
                });
              } else {
                this.router.navigate(['/otp']);
              }
            } else {
              this.errorMessage =
                response.message || 'Invalid username or password';
            }
          },
          error: (error) => {
            this.errorMessage =
              error.error?.message || 'An error occurred during login';
          },
        });
    } else {
      this.errorMessage = 'Please fill in all required fields';
    }
  }
}
