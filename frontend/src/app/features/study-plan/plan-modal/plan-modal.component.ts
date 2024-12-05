import { CommonModule } from '@angular/common';
import {
  Component,
  ViewEncapsulation,
  Inject, 
  OnInit } from '@angular/core';
import {
  MatDialogRef,
  MAT_DIALOG_DATA,
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
import { ApiService } from '../../../api.service'; 
import {
  ResponseError
} from '../../../shared/interfaces/response-error.interface';
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
export class PlanModalComponent implements OnInit {
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

  public isEditMode = false;

  constructor(
    private dialogRef: MatDialogRef<PlanModalComponent>,
    private apiService: ApiService,
    @Inject(MAT_DIALOG_DATA) public data:
    { isEditMode: boolean; planData: StudyPlan } // Dados do modal
  ) {}
  
  ngOnInit() {
    this.isEditMode = this.data.isEditMode; // Recebe o estado de edição
    if (this.data.planData) {
      this.planForm.patchValue({
        title: this.data.planData.title,
        visibility: this.data.planData.visibility,
      });
    }
  }

  private loadPlan(planId: number): void {
    this.apiService.getStudyPlanById(planId).subscribe({
      next: (plan: StudyPlan) => {
        this.planForm.patchValue({
          title: plan.title,
          visibility: plan.visibility,
        });
      },
      error: (error: ResponseError) => {
        console.error('Erro ao carregar plano:', error);
        this.formErrors = 'Erro ao carregar os dados do plano.';
      },
    });
  }

  savePlan() {
    if (this.planForm.valid) {
      const payload: StudyPlan = {
        title: this.planForm.get('title')?.value,
        visibility: this.planForm.get('visibility')?.value,
      };
      console.log('informações do modal:', payload, 'isEditMode:', this.isEditMode);

      if (this.isEditMode && this.data.planData.id) {
        this.apiService.editStudyPlan(this.data.planData.id, payload).subscribe({
          next: (response: StudyPlan) => {
            console.log('Plano Editado:', response);
            this.dialogRef.close(response);
          },
          error: (error: ResponseError) => {
            console.error('Erro ao editar plano:', error);
            this.formErrors = 'Erro ao editar plano. Por favor, tente novamente.';
          },
        });
      } else {
        this.apiService.createStudyPlan(payload).subscribe({
          next: (response: StudyPlan) => {
            console.log('Plano Criado:', response);
            this.dialogRef.close(response);
          },
          error: (error: ResponseError) => {
            console.error('Erro ao criar plano:', error);
            this.formErrors = 'Erro ao criar plano. Por favor, tente novamente.';
          },
        });
      }
    }
  }

  save() {
    if (this.planForm.valid) {
      this.dialogRef.close(this.planForm.value);
    }
  }

  close() {
    this.dialogRef.close();
  }
}
