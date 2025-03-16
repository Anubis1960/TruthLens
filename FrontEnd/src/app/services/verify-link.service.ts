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
    console.log(link);
    return this.http.post<any>(`${BASE_URL}/api/sites/article-link`, {link});
  }

  verifyImage(link:string){
    console.log(link);
    return this.http.post<any>(`${BASE_URL}/api/sites/image-url`, {link});
  }

  verifyVideo(link:string){
    console.log(link);
    return this.http.post<any>(`${BASE_URL}/api/video-url`, {link});
  }

  uploadFile(formData: FormData): Observable<any> {
    return this.http.post<any>(`${BASE_URL}/api/upload/image`, formData);
  }


}
