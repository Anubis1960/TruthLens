import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

const BASE_URL = 'http://localhost:5000';


@Injectable({
  providedIn: 'root'
})
export class VerifyLinkService {

  constructor(private http: HttpClient) { }

  verifySite(link: string):Observable<any>{
    return this.http.post<any>(`${BASE_URL}/site`, {link});
  }
  verifyImage(link:string){
    return this.http.post<any>(`${BASE_URL}/image`, {link});
  }
  verifyVideo(link:string){
    return this.http.post<any>(`${BASE_URL}/video`, {link});
  }
  uploadFile(formData: FormData): Observable<any> {
    return this.http.post<any>(`${BASE_URL}/api/upload/image`, formData);
  }


}
