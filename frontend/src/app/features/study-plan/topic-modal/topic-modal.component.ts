import { CommonModule } from '@angular/common';
import { Component, ViewEncapsulation } from '@angular/core';
import {
  MatDialogRef,
  MatDialogContent,
  MatDialogTitle,
  MatDialogActions,
} from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { ReactiveFormsModule, FormGroup, FormControl, Validators, ValidationErrors } from '@angular/forms';

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
export class TopicModalComponent {
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

  constructor(private dialogRef: MatDialogRef<TopicModalComponent>) {}

  createTopic() {
    if (this.topicForm.valid) {
      const topicData = this.topicForm.value;
      console.log('Tópico Criado:', topicData);
      this.dialogRef.close(topicData); // Fecha o modal e retorna os dados.
    } else {
      this.formErrors = 'Por favor, preencha todos os campos corretamente.';
    }
  }

  close() {
    this.dialogRef.close(); // Fecha o modal sem retornar dados.
  }
}
