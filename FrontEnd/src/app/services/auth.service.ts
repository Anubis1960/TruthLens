import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { User } from '../models/user-model';

const BASE_URL = 'http://localhost:5000';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) { }

  login(email:string,password:string):Observable<User>{
    return this.http.post<User>(`${BASE_URL}/login`, { email, password });
  }
  register(name: string, email: string, password: string): Observable<User> {
    return this.http.post<User>(`${BASE_URL}/path/`, { name, email, password });
  }
}
