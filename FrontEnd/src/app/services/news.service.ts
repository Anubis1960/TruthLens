import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

const BASE_URL = 'http://localhost:5000'
@Injectable({
  providedIn: 'root'
})
export class NewsService {

  constructor(private http: HttpClient) { }

  fetchNews(): Observable<any> 
  {
    return this.http.get<any>(`${BASE_URL}/api/sites/`)
  }
}
