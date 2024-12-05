import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';
import { Token } from '../interfaces/token.interface';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private learningPathApiUrl = environment.LearningPathApiUrl;

  constructor(private httpClient: HttpClient) { }

  login(username: string, password: string): Observable<Token> {
    return this.httpClient.post<Token>(
      `${this.learningPathApiUrl}auth/login/`,
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
