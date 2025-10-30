import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavComponent } from './pages/nav/nav.component';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { HttpClientModule } from '@angular/common/http';
import { OtpComponent } from './pages/otp/otp.component';
import { ForgotPasswordComponent } from './pages/forgot-password/forgot-password.component';
import { ChangeInformationComponent } from './pages/change-information/change-information.component';
import { ChangePasswordComponent } from './pages/change-password/change-password.component';
import { MfaComponent } from './pages/mfa/mfa.component';
import { UsersComponent } from './pages/users/users.component';
import { getAccessToken } from './utils/local_storage';
import { JwtModule } from '@auth0/angular-jwt';
import { RegisterComponent } from './pages/register/register.component';

@NgModule({
  declarations: [
    AppComponent,
    NavComponent,
    HomeComponent,
    LoginComponent,
    OtpComponent,
    ForgotPasswordComponent,
    ChangeInformationComponent,
    ChangePasswordComponent,
    MfaComponent,
    UsersComponent,
    RegisterComponent,
  ],
  imports: [
    JwtModule.forRoot({
      config: {
        tokenGetter: () => getAccessToken(),
      },
    }),
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
