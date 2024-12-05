import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { User } from '../interfaces/user.interface';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private learningPathApiUrl = environment.LearningPathApiUrl;

  constructor(private httpClient: HttpClient) { }

  createUser(username: string, password: string): Observable<User> {
    return this.httpClient.post<User>(
      `${this.learningPathApiUrl}user/`,
      {username, password}
    );
  }
}
