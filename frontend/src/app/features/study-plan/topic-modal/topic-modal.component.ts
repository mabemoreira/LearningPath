import { CommonModule } from '@angular/common';
import { Component,
  ViewEncapsulation,
  OnInit
 } from '@angular/core';
import {
  MatDialogRef,
  MatDialogContent,
  MatDialogTitle,
  MatDialogActions,
} from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import {
  ReactiveFormsModule,
  FormGroup,
  FormControl,
  Validators, 
  ValidationErrors 
} from '@angular/forms';
import { ApiService } from '../../../api.service';
import { Router } from '@angular/router';
import { Topic } from '../../../shared/interfaces/topic.interface';

@Component({
  selector: 'app-topic-modal',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogContent,
    MatDialogTitle,
    MatDialogActions,
    MatButtonModule,
    ReactiveFormsModule
  ],
  templateUrl: './topic-modal.component.html',
  styleUrls: ['./topic-modal.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class TopicModalComponent implements OnInit {
  public topicForm: FormGroup = new FormGroup({
    title: new FormControl(null, [
      Validators.required,
      (control): ValidationErrors | null => {
        if (control.value && control.value.trim().length > 0) {
          return null;
        }
        return { error: 'O título é obrigatório!' };
      },
    ]),
    description: new FormControl(null, [
      Validators.required,
      (control): ValidationErrors | null => {
        if (control.value && control.value.trim().length > 0) {
          return null;
        }
        return { error: 'A descrição é obrigatória!' };
      },
    ]),
  });
  public formErrors: string | null = null;

  constructor(
    private dialogRef: MatDialogRef<TopicModalComponent>,
    private apiService: ApiService,
    private router: Router // Injeção do ActivatedRoute
  ) { }

  studyPlanId: number | null = null;

  ngOnInit() {
    const url = this.router.url; // Exemplo: "/planos/37"
    this.studyPlanId = Number(url.split('/').pop());
    console.log('ID do Plano extraído da URL:', this.studyPlanId);
  }

  createTopic() {
    if (this.topicForm.valid) {
      const payload: Topic = {
        id: 0, // Assuming 0 or any default value for the id
        title: this.topicForm.get('title')?.value,
        description: this.topicForm.get('description')?.value,
      };

      if (!this.studyPlanId) {
        console.error('ID do plano não encontrado!');
        this.formErrors = 'Erro ao criar tópico. Por favor, tente novamente.';
        return;
      }

      this.apiService.createTopic(this.studyPlanId, payload).subscribe({
        next: () => {
          this.dialogRef.close(payload); // Retorna o tópico criado ao componente pai
        },
        error: (error) => {
          console.error('Erro ao criar tópico:', error);
          this.formErrors = 'Erro ao criar tópico. Por favor, tente novamente.';
        },
      });
    }
  }


  close() {
    this.dialogRef.close(); // Fecha o modal sem retornar dados.
  }
}
