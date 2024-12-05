import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../../api.service';
import { CommonModule } from '@angular/common';
import { MatDialog } from '@angular/material/dialog';
import { TopicModalComponent } from '../topic-modal/topic-modal.component';
import { User } from '../../../shared/interfaces/user.interface';
import { ResponseError } from '../../../shared/interfaces/response-error.interface';
import { StudyPlan } from '../../../shared/interfaces/study-plan.interface';
import { Topic } from '../../../shared/interfaces/topic.interface';
import { PlanModalComponent } from '../plan-modal/plan-modal.component';

// ng add @angular/material


@Component({
  selector: 'app-study-plan',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './study-plan.component.html',
  styleUrl: './study-plan.component.css'
})
export class StudyPlanComponent implements OnInit {
  studyPlan: StudyPlan | undefined;
  title = 'Study Plan';
  topics: Topic[] = [];
  visibility = 'private';
  author: User | undefined;
  planId: number | undefined;
  isAuthor = false;
  currentUser: User | undefined;

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private dialog: MatDialog,
    private router: Router
  ) { }

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


  openStudyPlanModal(studyPlan?: StudyPlan) {
    const dialogRef = this.dialog.open(PlanModalComponent, {
      data: {
        isEditMode: true,
        planData: studyPlan || null,
      },
    });
  
    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        if (studyPlan) {
          // Atualize o plano editado
          if (this.studyPlan) {
            Object.assign(this.studyPlan, result);
            this.title = this.studyPlan.title;
            this.visibility = this.studyPlan.visibility?.name;
          }
        } 
      }
    });
  }
  

  deleteTopic(topic_id: number) {
    console.log('Tópicos antes:', this.topics);
    console.log('Deletando tópico:', topic_id);
    this.apiService.deleteTopic(topic_id).subscribe(
      () => {
        console.log('Tópico deletado com sucesso:');
        this.topics = this.topics.filter((topic) => topic.id !== topic_id);
      },
      (error: ResponseError) => {
        console.error('Erro ao deletar tópico:', error);
      }
    );
  }

  
  checkIsAuthor(): void {
    // Assuming you have a method to get the current user
    this.apiService.getCurrentUser().subscribe(
      (data: User) => {
        this.currentUser = data; // Armazena os dados retornados
        this.isAuthor = this.currentUser.id === this.author?.id;
      },
      (error: ResponseError) => {
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
        this.title = this.studyPlan?.title;
        this.topics = this.studyPlan?.topics || [];
        this.author = this.studyPlan?.author;
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

  followStudyPlan(): void {
    if (!this.planId) {
      console.error('ID do plano de estudo não encontrado');
      return;
    }
    this.apiService.followStudyPlan(this.planId).subscribe(
      (data) => {
        console.log('Plano de estudo seguido com sucesso:', data);
        this.router.navigate([`/planos/${this.planId}/executar`]);
      },
      (error) => {
        console.error('Erro ao seguir plano de estudo:', error);
      }
    );
  }

  cloneStudyPlan(): void {
    if (!this.planId) {
      console.error('ID do plano de estudo não encontrado');
      return;
    }
    this.apiService.cloneStudyPlan(this.planId).subscribe(
      (data) => {
        console.log('Plano de estudo clonado com sucesso:', data);
        this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
          this.router.navigate([`/planos/${data.id}`]);
        });
      },
      (error) => {
        console.error('Erro ao clonar plano de estudo:', error);
      }
    );
  }

  unfollowStudyPlan(): void {
    if (!this.planId) {
      console.error('ID do plano de estudo não encontrado');
      return;
    }
    this.apiService.unfollowStudyPlan(this.planId).subscribe(
      (data) => {
        console.log('Plano de estudo deixado com sucesso:', data);
      },
      (error) => {
        console.error('Erro ao deixar plano de estudo:', error);
      }
    );
  }

  deleteStudyPlan(): void {
    if (!this.planId) {
      console.error('ID do plano de estudo não encontrado');
      return;
    }
    this.apiService.deleteStudyPlan(this.planId).subscribe(
      (data) => {
        console.log('Plano de estudo deletado com sucesso:', data);
        this.router.navigate(['/planos']);
      },
      (error) => {
        console.error('Erro ao deletar plano de estudo:', error);
      }
    );
  }

  openEditModal(): void {
    if (!this.planId) {
      console.error('ID do plano de estudo não encontrado');
      return;
    }
    const dialogRef = this.dialog.open(PlanModalComponent, {
      data: this.studyPlan
    });

    dialogRef.afterClosed().subscribe((editedPlan) => {
      if (editedPlan) {
        if (! this.planId) {
          console.error('ID do plano de estudo não encontrado');
          return;
        }
        this.apiService.editStudyPlan(this.planId, editedPlan).subscribe(
          (data) => {
            console.log('Plano de estudo editado com sucesso:', data);
            this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
              this.router.navigate([`/planos/${this.planId}`]);
            });
          },
          (error) => {
            console.error('Erro ao editar plano de estudo:', error);
          }
        );
      }
    });
  }

}