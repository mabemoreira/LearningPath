import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../layout/header/header.component';
import { FooterComponent } from '../layout/footer/footer.component';
import { ApiService } from '../../../api.service';

@Component({
  selector: 'app-plan-page',
  standalone: true,
  imports: [HeaderComponent, FooterComponent, CommonModule],
  templateUrl: './plan-page.component.html',
  styleUrl: './plan-page.component.css'
})
export class PlanPageComponent {
  studyPlans: any[] = []; // Variável para armazenar os dados retornados
  
  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.fetchStudyPlans();
  }

  // Dados fictícios para criação do study plan
  studyPlanData = {
    name: 'New Study Plan',
    description: 'Description of the new study plan'
  };

  fetchStudyPlans() {
    this.studyPlans = [];
    this.apiService.getAllStudyPlans().subscribe(
      (data) => {
        console.log('Dados recebidos:', data);
        this.studyPlans = data; // Armazena os dados retornados
      },
      (error) => {
        console.error('Erro ao buscar study plans:', error);
      }
    );
  }

  createStudyPlan() {
    this.apiService.createStudyPlan(this.studyPlanData).subscribe(
      (response) => {
        console.log('Study plan criado com sucesso:', response);
        alert('Study plan criado com sucesso!');
      },
      (error) => {
        console.error('Erro ao criar o study plan:', error);
      }
    );
  }

  openStudyPlan(id: number) {
    this.apiService.getStudyPlanById(id).subscribe(
      (response) => {
        console.log('Study plan com ID:', id, response);
      },
      (error) => {
        console.error('Erro ao abrir o study plan com ID:', id, error);
      }
    );
    console.log('Abrir o study plan com ID:', id);
  }

}
