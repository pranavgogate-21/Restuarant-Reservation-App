import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  
  public constructor(private http: HttpClient){
  }

  loginUser (data:any): Observable<any>{
      return this.http.post(environment.loginURL, data);
  }
}
