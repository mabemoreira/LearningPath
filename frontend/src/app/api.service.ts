import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = 'http://127.0.0.1:8000'; // Substitua pela URL do seu backend
  private token: string | null = null; // Armazena o token

  constructor(private http: HttpClient) { }

  // Adicionando o método no ApiService
  createStudyPlan(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/study_plan/`, data);
  }

  createTopic(plan_id: number, data: any): Observable<any> {
    console.log('Criando tópico para o plano:', plan_id, 'com dados:', data);
    return this.http.post(`${this.baseUrl}/study_plan/${plan_id}/topic/`, data);
  }

  getAllStudyPlans(): Observable<any> {
    return this.http.get(`${this.baseUrl}/study_plan/get_all/`);
  }
  
  getStudyPlanById(id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/study_plan/${id}/`);
  }

  getCurrentUser(): any {
    return this.http.get(`${this.baseUrl}/user/0/`);
  }

}
