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
import { ReactiveFormsModule, FormGroup, FormControl, Validators, ValidationErrors } from '@angular/forms';

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
    visibility: new FormControl(null, [Validators.required]),
  });
  public formErrors: string | null = null;

  public visibilityOptions = [
    { value: 'private', label: 'Privado' },
    { value: 'public', label: 'Público' },
  ];
  apiService: any;

  constructor(private dialogRef: MatDialogRef<PlanModalComponent>) {}

  createPlan() {
    if (this.planForm.valid) {
      const planData = this.planForm.value;
      console.log('Plano Criado:', planData);
      this.dialogRef.close(planData); // Fecha o modal e retorna os dados.
    } else {
      this.formErrors = 'Por favor, preencha todos os campos corretamente.';
    }
  }

  createStudyPlan() {
    this.apiService.createStudyPlan(
      this.planForm.get('title')?.value,
      this.planForm.get('visibility')?.value
    ).subscribe({
      next: () => {
        console.log('Study plan criado com sucesso:', response);
        alert('Study plan criado com sucesso!');
      },
      error: (error) => {
        console.error('Erro ao criar o study plan:', error);
      }
    });
  }


  close() {
    this.dialogRef.close(); // Fecha o modal sem retornar dados.
  }
}
