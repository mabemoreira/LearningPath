import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../../api.service';
import { getStatsOptions } from '@angular-devkit/build-angular/src/tools/webpack/utils/helpers';
import { CommonModule } from '@angular/common';
import { MatDialog } from '@angular/material/dialog';
import { TopicModalComponent } from '../topic-modal/topic-modal.component';

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
  topics: { title: string; description: string }[] = [];
  visibility: string = 'private';
  author: any = {};
  planId: number | null = null;
  isAuthor: boolean = false;
  currentUser: any = null;

  constructor(private route: ActivatedRoute, private apiService: ApiService, private dialog: MatDialog) { }

  ngOnInit(): void {
    this.planId = Number(this.route.snapshot.paramMap.get('id'));

    this.get_study_plan(this.planId);
  }

  openTopicModal() {
    const dialogRef = this.dialog.open(TopicModalComponent);

    dialogRef.afterClosed().subscribe((newTopic) => {
      if (newTopic) {
        this.topics.push(newTopic); // Adicione o novo tópico à lista
      }
    });
  }

  checkIsAuthor(): void {
    // Assuming you have a method to get the current user
    this.apiService.getCurrentUser().subscribe(
      (data: any) => {
        console.log('Dados recebidos:', data);
        this.currentUser = data; // Armazena os dados retornados
        console.log('Current user:', this.currentUser);
        console.log('Comparando:', this.currentUser.id, this.author.id);
        this.isAuthor = this.currentUser.id === this.author.id;
        console.log('Is author:', this.isAuthor);
      },
      (error: any) => {
        console.error('Erro ao buscar usuário atual:', error);
      }
    );
  }

  get_study_plan(planId: number): void {
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

        // Check if the current user is the author
        this.checkIsAuthor();
        console.log('Is author:', this.isAuthor);
      },
      (error) => {
        console.error('Erro ao buscar study plans:', error);
      }
    );
  }
}