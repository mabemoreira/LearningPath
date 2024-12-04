import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../api.service';
import { getStatsOptions } from '@angular-devkit/build-angular/src/tools/webpack/utils/helpers';
import { CommonModule } from '@angular/common';

// ng add @angular/material


@Component({
  selector: 'app-study-plan',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './study-plan.component.html',
  styleUrl: './study-plan.component.css'
})
export class StudyPlanComponent implements OnInit {
  studyPlan: any = {};
  title: string = 'Study Plan';
  topics: any[] = [];
  visibility: string = 'private';
  author: any = {};
  planId: number | null = null;

  constructor(private route: ActivatedRoute, private apiService: ApiService) {}

  ngOnInit(): void {
    this.planId = Number(this.route.snapshot.paramMap.get('id'));
    this.get_study_plan(this.planId);
  }

  get_study_plan(planId: number): any {
    this.apiService.getStudyPlanById(planId).subscribe(
      (data) => {
        console.log('Dados recebidos:', data);
        this.studyPlan = data; // Armazena os dados retornados
  
        // Processar os dados recebidos
        this.title = this.studyPlan.title;
        this.topics = this.studyPlan.topics;
        this.author = this.studyPlan.author;
        this.visibility = this.studyPlan.visibility?.name;
  
        console.log('Title:', this.title);
        console.log('Topics:', this.topics);
        console.log('Author:', this.author);
        console.log('Visibility:', this.visibility);
      },
      (error) => {
        console.error('Erro ao buscar study plans:', error);
      }
    );
  }
}