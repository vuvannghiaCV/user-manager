import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../services/auth-service.service';
import { setAccessToken } from '../../utils/local_storage';
@Component({
  selector: 'app-otp',
  templateUrl: './otp.component.html',
  styleUrls: ['./otp.component.css'],
})
export class OtpComponent implements OnInit {
  otp_qr_code_base64: string = '';
  form!: FormGroup;
  errorMessage: string | null = null;

  constructor(
    private authService: AuthService,
    private route: ActivatedRoute,
    private formBuilder: FormBuilder,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.otp_qr_code_base64 =
      this.route.snapshot.queryParams['otp_qr_code_base64'];
    this.form = this.formBuilder.group({
      otp: ['', Validators.required],
    });
  }

  verifyOtp() {
    if (this.form.invalid) {
      this.errorMessage = 'Please enter a valid OTP code';
      return;
    }

    this.authService.verifyOtp(this.form.value.otp).subscribe({
      next: (response: any) => {
        if (response.success) {
          setAccessToken(response.access_token);
          this.router.navigate(['/']);
          this.errorMessage = null;
        } else {
          this.errorMessage = response.message || 'Invalid OTP code';
        }
      },
      error: (error) => {
        this.errorMessage =
          error.error?.message || 'An error occurred while verifying OTP';
      },
    });
  }
}
