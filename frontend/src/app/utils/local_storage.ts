import { CheckLogin } from './check_login';
import { CheckAdmin } from './check_admin';
import { JwtHelperService } from '@auth0/angular-jwt';

const jwtHelper = new JwtHelperService();

export const setAccessToken = (accessToken: string) => {
  localStorage.setItem('access_token', accessToken);
  CheckLogin.checkLoginEmitter.emit(true);
  const decodedToken = jwtHelper.decodeToken(accessToken);
  CheckAdmin.checkAdminEmitter.emit(decodedToken.is_admin);
  return accessToken;
};

export const getAccessToken = () => {
  return localStorage.getItem('access_token');
};

export const removeAccessToken = () => {
  localStorage.removeItem('access_token');
  CheckLogin.checkLoginEmitter.emit(false);
  CheckAdmin.checkAdminEmitter.emit(false);
};

export const setBearerHeader = () => {
  const accessToken = getAccessToken();
  return { headers: { Authorization: `Bearer ${accessToken}` } };
};
