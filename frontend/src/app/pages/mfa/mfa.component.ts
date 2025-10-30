import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth-service.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-mfa',
  templateUrl: './mfa.component.html',
  styleUrls: ['./mfa.component.css'],
})
export class MfaComponent implements OnInit {
  recoveryCodes: string[] = [];
  errorMessage: string | null = null;

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    this.downloadRecoveryOtp();
  }

  downloadRecoveryOtp() {
    this.authService.downloadRecoveryOtp().subscribe({
      next: (response: any) => {
        if (response.success) {
          this.recoveryCodes = response.list_otp_recovery;
          this.errorMessage = null;
        } else {
          this.errorMessage =
            response.message || 'Failed to get recovery codes';
        }
      },
      error: (error) => {
        this.errorMessage =
          error.error?.message ||
          'An error occurred while getting recovery codes';
      },
    });
  }

  verifyRecoveryOtp(code: string) {
    if (!code) {
      this.errorMessage = 'Please enter a recovery code';
      return;
    }

    this.authService.verifyRecoveryOtp(code).subscribe({
      next: (response: any) => {
        if (response.success) {
          this.router.navigate(['/home']);
          this.errorMessage = null;
        } else {
          this.errorMessage = response.message || 'Invalid recovery code';
        }
      },
      error: (error) => {
        this.errorMessage =
          error.error?.message || 'An error occurred while verifying code';
      },
    });
  }
}
