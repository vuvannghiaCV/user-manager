import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { OtpComponent } from './pages/otp/otp.component';
import { ForgotPasswordComponent } from './pages/forgot-password/forgot-password.component';
import { ChangeInformationComponent } from './pages/change-information/change-information.component';
import { ChangePasswordComponent } from './pages/change-password/change-password.component';
import { MfaComponent } from './pages/mfa/mfa.component';
import { UsersComponent } from './pages/users/users.component';
import { RegisterComponent } from './pages/register/register.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: 'otp',
    component: OtpComponent,
  },
  {
    path: 'forgot-password',
    component: ForgotPasswordComponent,
  },
  {
    path: 'profile/change-information',
    component: ChangeInformationComponent,
  },
  {
    path: 'profile/change-password',
    component: ChangePasswordComponent,
  },
  {
    path: 'mfa',
    component: MfaComponent,
  },
  {
    path: 'users',
    component: UsersComponent,
  },
  {
    path: 'register',
    component: RegisterComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
