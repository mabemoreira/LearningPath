import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { StudyPlan } from './shared/interfaces/study-plan.interface';
import { Topic } from './shared/interfaces/topic.interface';
import { User } from './shared/interfaces/user.interface';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = 'http://127.0.0.1:8000'; // Substitua pela URL do seu backend
  private token: string | null = null; // Armazena o token

  constructor(private http: HttpClient) { }

  createStudyPlan(data: StudyPlan): Observable<StudyPlan> {
    return this.http.post<StudyPlan>(`${this.baseUrl}/study_plan/`, data);
  }

  createTopic(plan_id: number, data: Topic): Observable<Topic> {
    console.log('Criando tópico para o plano:', plan_id, 'com dados:', data);
    return this.http.post<Topic>(`${this.baseUrl}/study_plan/${plan_id}/topic/`, data);
  }

  getAllStudyPlans(): Observable<StudyPlan[]> {
    return this.http.get<StudyPlan[]>(`${this.baseUrl}/study_plan/get_all/`);
  }
  
  getStudyPlanById(id: number): Observable<StudyPlan> {
    return this.http.get<StudyPlan>(`${this.baseUrl}/study_plan/${id}/`);
  }

  getExecuteStudyPlanById(id: number): Observable<StudyPlan> {
    return this.http.get<StudyPlan>(`${this.baseUrl}/study_plan/execute/${id}/`);
  }

  getCurrentUser(): Observable<User> {
    return this.http.get<User>(`${this.baseUrl}/user/0/`);
  }

  followStudyPlan(plan_id: number): Observable<StudyPlan> {
    return this.http.post<StudyPlan>(`${this.baseUrl}/study_plan/follow/${plan_id}/`, {});
  }

  unfollowStudyPlan(plan_id: number): Observable<StudyPlan> {
    return this.http.post<StudyPlan>(`${this.baseUrl}/study_plan/unfollow/${plan_id}/`, {});
  }

  cloneStudyPlan(plan_id: number): Observable<StudyPlan> {
    return this.http.post<StudyPlan>(`${this.baseUrl}/study_plan/clone/${plan_id}/`, {});
  }

  markTopicAsDoneOrUndone(topic_id: number): Observable<Topic> {
    return this.http.post<Topic>(`${this.baseUrl}/study_plan/topic/mark/${topic_id}/`, {});
  }

  deleteStudyPlan(plan_id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/study_plan/${plan_id}/`);
  }

  deleteTopic(topic_id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/study_plan/topic/${topic_id}/`);
  }

}
