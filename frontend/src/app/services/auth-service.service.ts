import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BaseUrl } from '../config';
import { setBearerHeader } from '../utils/local_storage';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    const url = `${BaseUrl}/auth/login?username=${username}&password=${password}`;
    return this.http.post(url, {});
  }

  getCurrentUser(): Observable<any> {
    const url = `${BaseUrl}/auth/current-user`;
    return this.http.get(url, setBearerHeader());
  }

  verifyOtp(code: string): Observable<any> {
    const url = `${BaseUrl}/auth/mfa/verify-otp`;
    return this.http.post(url, { code }, setBearerHeader());
  }

  downloadRecoveryOtp(): Observable<any> {
    const url = `${BaseUrl}/auth/mfa/download-recovery-otp`;
    return this.http.get(url, setBearerHeader());
  }

  verifyRecoveryOtp(code: string): Observable<any> {
    const url = `${BaseUrl}/auth/mfa/verify-recovery-otp?code=${code}`;
    return this.http.post(url, {}, setBearerHeader());
  }

  forgotPassword(username: string, email: string): Observable<any> {
    const url = `${BaseUrl}/auth/forgot-password?username=${username}&email=${email}`;
    return this.http.post(url, {});
  }

  changePassword(password: string, password_confirm: string): Observable<any> {
    const url = `${BaseUrl}/auth/change-password`;
    return this.http.put(
      url,
      { password, password_confirm },
      setBearerHeader()
    );
  }

  logout(): void {
    const url = `${BaseUrl}/auth/logout`;
    this.http.post(url, {}).subscribe();
  }

  registerUser(user: any): Observable<any> {
    const url = `${BaseUrl}/auth/register`;
    return this.http.post(url, user, setBearerHeader());
  }
}
