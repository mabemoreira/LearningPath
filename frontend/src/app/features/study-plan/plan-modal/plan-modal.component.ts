import { CommonModule } from '@angular/common';
import { Component, ViewEncapsulation } from '@angular/core';
import {
  MatDialogRef,
  MatDialogContent,
  MatDialogTitle,
  MatDialogActions,
} from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import {
  ReactiveFormsModule,
  FormGroup,
  FormControl,
  Validators,
  ValidationErrors
} from '@angular/forms';
import { ApiService } from '../../../api.service'; // Certifique-se de que o caminho está correto.
import { ResponseError } from '../../../shared/interfaces/response-error.interface';
import { StudyPlan } from '../../../shared/interfaces/study-plan.interface';

@Component({
  selector: 'app-plan-modal',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogContent,
    MatDialogTitle,
    MatDialogActions,
    MatButtonModule,
    MatSelectModule,
    ReactiveFormsModule,
  ],
  templateUrl: './plan-modal.component.html',
  styleUrls: ['./plan-modal.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class PlanModalComponent {
  public planForm: FormGroup = new FormGroup({
    title: new FormControl(null, [
      Validators.required,
      (control): ValidationErrors | null => {
        if (control.value && control.value.trim().length > 0) {
          return null;
        }
        return { error: 'O título é obrigatório!' };
      },
    ]),
    visibility: new FormControl(null, [
      (control) => {
        if (control.value) {
          return null;
        }
        return { error: 'Selecione uma opção!' }
      }
    ]),
  });
  public formErrors: string | null = null;

  public visibilityOptions = [
    { value: 'private', label: 'Privado' },
    { value: 'public', label: 'Público' },
  ];

  constructor(
    private dialogRef: MatDialogRef<PlanModalComponent>,
    private apiService: ApiService // Injeção do ApiService
  ) {}

  createStudyPlan() {
    if (this.planForm.valid) {
      const payload: StudyPlan = {
        title: this.planForm.get('title')?.value,
        visibility: this.planForm.get('visibility')?.value,
      };      
      this.apiService
        .createStudyPlan(
          payload
        )
        .subscribe({
          next: (response: StudyPlan) => {
            console.log('Plano Criado:', response);
            this.dialogRef.close(response); // Fecha o modal e retorna os dados.
          },
          error: (error: ResponseError) => {
            console.error('Erro ao criar plano:', error);
            this.formErrors = 'Erro ao criar plano. Por favor, tente novamente.';
          },
        });
    }
  }

  close() {
    this.dialogRef.close(); // Fecha o modal sem retornar dados.
  }
}
