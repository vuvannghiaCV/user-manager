import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BaseUrl } from '../config';
import { setBearerHeader } from '../utils/local_storage';

@Injectable({
  providedIn: 'root',
})
export class UsersService {
  constructor(private http: HttpClient) {}

  getAllUsers(): Observable<any> {
    const url = `${BaseUrl}/users`;
    return this.http.get(url, setBearerHeader());
  }

  getOneUser(id: number): Observable<any> {
    const url = `${BaseUrl}/users/${id}`;
    return this.http.get(url, setBearerHeader());
  }

  updateUser(user: {
    name?: string;
    age?: number;
    email?: string;
  }): Observable<any> {
    const url = `${BaseUrl}/users`;
    return this.http.put(url, user, setBearerHeader());
  }

  deleteUser(id: number): Observable<any> {
    const url = `${BaseUrl}/users/${id}`;
    return this.http.delete(url, setBearerHeader());
  }
}
