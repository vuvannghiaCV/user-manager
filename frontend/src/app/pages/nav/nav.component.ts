import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { JwtHelperService } from '@auth0/angular-jwt';
import { AuthService } from 'src/app/services/auth-service.service';
import { CheckAdmin } from 'src/app/utils/check_admin';
import { CheckLogin } from 'src/app/utils/check_login';
import { getAccessToken, removeAccessToken } from 'src/app/utils/local_storage';
@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css'],
})
export class NavComponent implements OnInit {
  isLoggedIn: boolean = false;
  isAdmin: boolean = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private jwtHelper: JwtHelperService
  ) {}

  ngOnInit(): void {
    const token = getAccessToken();
    if (token) {
      this.isLoggedIn = true;
      const decodedToken = this.jwtHelper.decodeToken(token);
      CheckLogin.checkLoginEmitter.emit(true);
      this.isAdmin = decodedToken.is_admin;
      CheckAdmin.checkAdminEmitter.emit(this.isAdmin);
    } else {
      this.isLoggedIn = false;
    }

    CheckLogin.checkLoginEmitter.subscribe((isLoggedIn: boolean) => {
      this.isLoggedIn = isLoggedIn;
    });
  }

  logout() {
    this.authService.logout();
    removeAccessToken();
    CheckLogin.checkLoginEmitter.emit(false);
    CheckAdmin.checkAdminEmitter.emit(false);
    this.router.navigate(['/login']);
  }
}
