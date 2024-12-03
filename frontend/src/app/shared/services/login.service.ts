import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private learningPathApiUrl = environment.LearningPathApiUrl;

  constructor(private httpClient: HttpClient) { }

  login(username: string, password: string): Observable<{token: string}> {
    return this.httpClient.post<{token: string}>(
      `${this.learningPathApiUrl}auth/login/`,
      {username, password}
    );
  }

  createAccount(username: string, password: string): Observable<any> {
    return this.httpClient.post<any>(
      `${this.learningPathApiUrl}user/`,
      {username, password}
    );
  }
}
