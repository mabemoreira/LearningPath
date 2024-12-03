import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';

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

  createAccount(username: string, password: string): Observable<{id: number; username: string}> {
    return this.httpClient.post<{id: number; username: string}>(
      `${this.learningPathApiUrl}user/`,
      {username, password}
    );
  }

  logout(): Observable<void> {
    return this.httpClient.post<void>(
      `${this.learningPathApiUrl}auth/logout/`,
      {}
    );
  }
}
